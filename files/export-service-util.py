import json
import argparse
import tempfile
from azureml.core import Workspace
from azureml.exceptions import WebserviceException
from azureml.core.compute import KubernetesCompute, ComputeTarget
from azureml._model_management._util import _get_mms_url
from azureml._model_management._util import get_paginated_results
from azureml._model_management._util import get_requests_session
from azureml._model_management._constants import AKS_WEBSERVICE_TYPE, ACI_WEBSERVICE_TYPE, UNKNOWN_WEBSERVICE_TYPE
from azureml._model_management._constants import MMS_SYNC_TIMEOUT_SECONDS
from azureml.core.webservice import Webservice
from azureml._restclient.clientbase import ClientBase

MIGRATION_WEBSERVICE_TYPES = [AKS_WEBSERVICE_TYPE, ACI_WEBSERVICE_TYPE]


def attach(ws: Workspace,
           compute_name: str,
           cluster_name: str,
           namespace: str = None):
    """
    Attach AmlArc compute to the workspace.
    :param cluster_name: AKS cluster name.
    :param namespace: Compute namespace, if not provided will be set to 'default' namespace
    :param compute_name: Compute name.
    :param ws: Target workspace.
    """
    resource_id = f"'/subscriptions/{ws.subscription_id}/resourceGroups/{ws.resource_group}/providers/" \
                  f"Microsoft.ContainerService/managedClusters/{cluster_name}"
    compute_id = None
    if compute_name in ws.compute_targets:
        amlarc_compute = ws.compute_targets[compute_name]
        if amlarc_compute and type(amlarc_compute) is KubernetesCompute:
            compute_id = amlarc_compute.id
    else:
        amlarc_attach_configuration = KubernetesCompute.attach_configuration(resource_id, namespace=namespace)
        amlarc_compute = ComputeTarget.attach(ws, compute_name, amlarc_attach_configuration)
        amlarc_compute.wait_for_completion(show_output=True)
        compute_id = amlarc_compute.id
    print(compute_id)


def export(ws: Workspace,
           compute_type: str = None,
           timeout_seconds: int = None,
           show_output: bool = True) -> (str, str):
    """
    Export all services under target workspace into template and parameters,
    valid compute_types are "AKS"/"ACI", default to export for both two types.
    :param show_output: Whether print outputs.
    :param timeout_seconds: Timeout settings for waiting export.
    :param ws: Target workspace.
    :param compute_type: Compute type to export.
    """
    base_url = _get_mms_url(ws)
    mms_endpoint = base_url + '/services'
    webservices = []
    headers = {'Content-Type': 'application/json'}
    headers.update(ws._auth_object.get_authentication_header())
    params = None
    if compute_type:
        if compute_type.upper() not in MIGRATION_WEBSERVICE_TYPES:
            raise WebserviceException('Invalid compute type "{}". Valid options are "{}"'
                                      .format(compute_type, ",".join(())))
        params = {'computeType': compute_type}
    try:
        resp = ClientBase._execute_func(get_requests_session().get, mms_endpoint, headers=headers,
                                        params=params, timeout=MMS_SYNC_TIMEOUT_SECONDS)
    except:
        raise WebserviceException(f'Cannot list WebServices ' +
                                  (f'with type: {compute_type}' if compute_type else ''))
    content = resp.content
    if isinstance(resp.content, bytes):
        content = resp.content.decode("utf-8")
    services_payload = json.loads(content)
    for service_dict in get_paginated_results(services_payload, headers):
        service_type = service_dict['computeType']
        child_class = None

        for child in Webservice._all_subclasses(Webservice):
            if service_type == child._webservice_type:
                child_class = child
                break
            elif child._webservice_type == UNKNOWN_WEBSERVICE_TYPE:
                child_class = child

        if child_class:
            service_obj = child_class.deserialize(ws, service_dict)
            webservices.append(service_obj)
    if len(webservices) == 0:
        raise WebserviceException(f'No Webservices found in workspace ' +
                                  (f'with type: {compute_type}' if compute_type else ''))
    service_entity = webservices[0]

    mms_endpoint = base_url + '/services/export'
    export_payload = {"computeType": compute_type}
    resp = ClientBase._execute_func(get_requests_session().post, mms_endpoint, params=params, headers=headers,
                                    json=export_payload)

    if resp.status_code == 202:
        service_entity.state = 'Exporting'
        operation_url = _get_mms_url(service_entity.workspace) + f'/operations/{resp.content.decode("utf-8")}'
        service_entity._operation_endpoint = operation_url
        state, _, operation = service_entity._wait_for_operation_to_complete(show_output, timeout_seconds)
        if state == "Succeeded":
            export_folder = operation.get("resourceLocation").split("/")[-1]
            storage_account = service_entity.workspace.get_details().get("storageAccount")
            if show_output:
                print(f"Services have been exported to storage account: {storage_account} \n"
                      f"Folder path: azureml/{export_folder}")
            return storage_account.split("/")[-1], export_folder
    else:
        raise WebserviceException('Received bad response from Model Management Service:\n'
                                  'Response Code: {}\n'
                                  'Headers: {}\n'
                                  'Content: {}'.format(resp.status_code, resp.headers, resp.content))


def overwrite_parameters(parms: dict,
                         target_compute: str,
                         endpoint_name: str = None,
                         deployment_name: str = None):
    """
    Overwrite parameters
    :param deployment_name: v2 online-deployment name. Default will be v1 service name.
    :param endpoint_name: v2 online-endpoint name. Default will be v1 service name.
    :param target_compute: v2 compute target. For export to AmlArc, the compute should be a cluster with AmlArc extension installed cluster.
    :param parms: parameters as dict: loaded v2 parameters.
    """
    properties = parms["onlineEndpointProperties"]["value"]
    traffic = parms["onlineEndpointPropertiesTrafficUpdate"]["value"]
    if target_compute:
        properties["target"] = target_compute
        traffic["target"] = target_compute
    properties.pop("keys")
    traffic.pop("keys")
    if endpoint_name:
        parms["onlineEndpointName"]["value"] = endpoint_name

    # this is optional
    if deployment_name:
        parms["onlineDeployments"]["value"][0]["name"] = deployment_name
        traffic["traffic"][deployment_name] = traffic["traffic"].pop(list(traffic["traffic"].keys())[0])

    temp_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False)
    json.dump(online_endpoint_deployment, temp_file)
    temp_file.flush()
    print(temp_file.name)


if __name__ == "__main__":

    def parse_args():
        parser = argparse.ArgumentParser(description="Export v1 service script")

        parser.add_argument('--attach', action='store_true', help='using script for attach amlarc compute')
        parser.add_argument('--export', action='store_true', help='using script for export services')
        parser.add_argument('--overwrite-parameters', action='store_true',
                            help='using script for overwrite parameters purpose')
        parser.add_argument('-w', '--workspace', type=str, help='workspace name')
        parser.add_argument('-g', '--resource-group', type=str, help='resource group name')
        parser.add_argument('-s', '--subscription', type=str, help='subscription id')
        parser.add_argument('-c', '--compute-type', default=None, type=str,
                            help='compute type to export, available types are AKS and ACI, default to export for both '
                                 'two types')
        parser.add_argument('--cluster-name', type=str, help='AmlArc installed cluster name')
        parser.add_argument('--compute-name', default='inferencecompute', type=str, help='compute name')
        parser.add_argument('--compute-namespace', type=str, help='compute attach namespace')
        parser.add_argument('-e', '--export-json', action='store_true', dest='export_json',
                            help='show export result in json')
        parser.add_argument('-mp', '--parameters-path', type=str, help='parameters file path')
        parser.add_argument('-mc', '--migrate-compute', type=str, help='v2 compute target name for migrate.')
        parser.add_argument('-me', '--migrate-endpoint-name', type=str, default=None,
                            help='v2 online-endpoint name, default is v1 service name')
        parser.add_argument('-md', '--migrate-deployment-name', type=str, default=None,
                            help='v2 online-deployment name, default is v1 service name')
        parser.set_defaults(compute_type=None)
        return parser.parse_args()

    # parse args
    args = parse_args()

    if args.attach:
        workspace = Workspace.get(name=args.workspace, resource_group=args.resource_group, subscription_id=args.subscription)
        attach(workspace, args.compute_name, args.cluster_name, args.compute_namespace)

    if args.export:
        worskpace = Workspace.get(name=args.workspace, resource_group=args.resource_group, subscription_id=args.subscription)
        storage_account, blob_folder = export(worskpace, args.compute_type, show_output=not args.export_json)
        if args.export_json:
            print(json.dumps({"storage_account": storage_account, "blob_folder": blob_folder}))

    if args.overwrite_parameters:
        with open(args.parameters_path) as f:
            online_endpoint_deployment = json.load(f)
        overwrite_parameters(online_endpoint_deployment,
                             args.migrate_compute,
                             args.migrate_endpoint_name,
                             args.migrate_deployment_name)
