import os
import base64
import json
import hashlib
import logging
import argparse
import sys
from typing import TypeVar
from azure.cli.core import get_default_cli


class Context:
    def __init__(self, debug=False):
        self.debug = debug
        self.__output_file = os.environ['AZ_SCRIPTS_OUTPUT_PATH']
        self.__temp_logger_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'deploy.log')
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(
            level=level,
            format=log_format,
            handlers=[
                logging.FileHandler(self.__temp_logger_file),
                logging.StreamHandler()
            ]
        )
        self.rootLogger = logging.getLogger()

    def __enter__(self):
        self.__logger = self.rootLogger.getChild('Context Manager')
        self.__logger.debug('Entered the deployment context manager')
        return self

    def __exit__(self, exc_type, exc_val, exc_trace):
        exit_normally = True
        if any([exc_type, exc_trace, exc_val]):
            self.__logger.error(
                f'Internal server error. error type: {exc_type}, error value: {exc_val}, error trace: {exc_trace}')
            exit_normally = False

        self.rootLogger.handlers[0].flush()
        with open(self.__temp_logger_file) as f:
            outputs = {'outputs': f.read()}

        with open(self.__output_file, 'w+') as f:
            json.dump(outputs, f)

        self.__logger.info('Exit context')
        return exit_normally


T = TypeVar('T')


class CommandBuilder:
    pass


class BuildCommandError(Exception):
    pass


class ArgsCommandBuilder(CommandBuilder):
    """
    The implementation of CommandBuilder which generate the az k8s-extension command,
    which pass config settings with double dash args. Will implement another builder
    that passes config settings with json file, which need to modify the extension CLI
    """

    def __init__(self, context: Context) -> None:
        self._base_command = [
            'k8s-extension',
            'create',
            '--extension-type',
            'Microsoft.AzureML.Kubernetes',
            '--cluster-type',
            'connectedClusters',
            '--scope',
            'cluster',
            '--verbose'
        ]

    def build(self) -> list:
        resource_group = os.environ.get('AML_RESOURCE_GROUP')
        configs_base64 = os.environ.get('AML_CONFIGS')
        if not resource_group or not configs_base64:
            self._logger.debug(
                f'missed nessesary args. configs_base64: {configs_base64}, resourceGroup: {resource_group}')
            raise BuildCommandError()
        self._base_command.extend([
            '--resource-group',
            resource_group,
        ])
        # decode configs environment variable
        try:
            configs_raw = base64.b64decode(configs_base64).decode('utf-8')
            configs = json.loads(configs_raw)
        except Exception as e:
            self._logger.debug(
                f'Failed to extract configs environment variable, configs_base64: {configs_base64}', exc_info=True
            )
            raise BuildCommandError()
        clusterName = configs.get('clusterObject', {}).get('name')
        extensionName = configs.get('extensionName')
        if not clusterName or not extensionName:
            self._logger.debug(
                f'missed nessesary args. clusterName: {clusterName}, extensionName: {extensionName}')
            raise BuildCommandError()

        auto_upgrade = configs.get('autoUpgrade', False)

        self._base_command.extend([
            '--name',
            extensionName,
            '--cluster-name',
            clusterName,
            '--auto-upgrade',
            'true' if auto_upgrade else 'false'
        ])

        generator = self.ConfigSettingsGenerator(configs)
        config_settings = generator \
            .gen_node_selector() \
            .gen_basic_settings() \
            .generate()

        command = self._base_command + config_settings
        return command

    class ConfigSettingsGenerator:
        def __init__(self, configs: dict) -> None:
            self.__configs = configs
            self.__config_settings = ['--configuration-settings']
            self.__config_protected_settings = [
                '--configuration-protected-settings']

        def gen_node_selector(self: T) -> T:
            node_selectors = self.__configs.get('nodeSelector', [])
            for kv_pair in node_selectors:
                key = kv_pair.get('name')
                value = kv_pair.get('value')
                if not key or not value:
                    continue
                self.__config_settings.append(f'nodeSelector.{key}={value}')
            return self

        def gen_basic_settings(self: T) -> T:
            rename = {
                'installBlobCSIDriver': 'blobCsiDriverEnabled',
                'installPrometheusOperator': 'installPromOp',
                'installVolcanoScheduler': 'installVolcano',
                'internalLbProvider': 'internalLoadBalancerProvider',
                'sslSecretName': 'sslSecret',
                'inferenceLoadBalancerHA': 'inferenceRouterHA',
            }

            for setting in [
                'autoUpgrade',
                'enableTraining',
                'enableInference',
                'inferenceLoadBalancerHA',
                'inferenceRouterHA',
                'allowInsecureConnections',
                'installNvidiaDevicePlugin',
                'installBlobCSIDriver',
                'installPrometheusOperator',
                'installVolcanoScheduler',
                'installVolcano',
                'installDcgmExporter',
                'inferenceRouterServiceType',
                'internalLbProvider',
                'installPromOp',
                'sslCname',
                'sslSecretName',
            ]:
                if setting not in self.__configs:
                    continue
                val = self.__configs[setting]
                if val == '':
                    continue
                if setting in rename:
                    setting = rename[setting]
                self.__config_settings.append(f'{setting}={val}')

            return self

        def generate(self) -> str:
            if len(self.__config_protected_settings) > 1:
                self.__config_settings.extend(self.__config_protected_settings)
            return self.__config_settings


class RunCommandError(Exception):
    pass


def deploy(context: Context) -> None:
    command_builder = ArgsCommandBuilder(context)
    command = command_builder.build()
    cli = get_default_cli()
    logger = context.rootLogger.getChild('deploy')
    logger.info(f'Begin to run command: {command}')
    ret = cli.invoke(command)
    logger.info(f'command run return code: {ret}')
    logger.info(f'command run output: {cli.result.result}')
    logger.info(f'command run error: {cli.result.error}')
    if ret != 0:
        raise RunCommandError()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Install AMLArc Extension')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    with Context(args.debug) as c:
        deploy(c)
        
