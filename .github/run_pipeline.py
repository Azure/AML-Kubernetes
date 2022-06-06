import argparse
import os
from azureml.core.authentication import InteractiveLoginAuthentication, ServicePrincipalAuthentication
from msrest.authentication import BasicTokenAuthentication, BasicAuthentication
from azure.devops.connection import Connection
from azure.devops.v6_0.pipelines.models import RunPipelineParameters, RunResourcesParameters, RepositoryResourceParameters, Run
import time

def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--definition-id',
        type=int,
        required=False,
        help='branch name'
    )
    parser.add_argument(
        '--variables',
        '-v',
        type=str,
        nargs='+',
        help='variables set to the pipeline'
    )

    return parser

def init_clients():
    token = os.environ["PAT_TOKEN"]
    credentials = BasicAuthentication('', token)

    organization_url = 'https://dev.azure.com/msdata'
    
    connection = Connection(base_url=organization_url, creds=credentials)
    clients = connection.clients_v6_0
    
    return clients

def trigger_build(clients, branch, def_id, variables = {}) -> Run:
    prj = 'Vienna'
    branch = f'refs/heads/{branch}'

    repo = RepositoryResourceParameters(branch)
    res = RunResourcesParameters(repositories={'self': repo})
    params = RunPipelineParameters(resources=res)
    if variables:
        params.variables = variables

    pipeline = clients.get_pipelines_client()
    run = pipeline.run_pipeline(params, prj, def_id)
    return run

def wait_run_complete(clients, def_id, run_id, timeout_in_sec=3600) -> bool:
    pipeline = clients.get_pipelines_client()
    run = pipeline.get_run('Vienna', def_id, run_id)
    current = time.time()
    while run.state != 'completed' and time.time() - current < timeout_in_sec:
        time.sleep(10)
    if run.state != 'completed':
        return False
    if run.result == 'failed':
        return False
    return True

if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args()
    clients = init_clients()
    variables = {}
    if args.variables:
        for kv in args.variables:
            key, value = kv.split('=')
            variables[key] = value
    run = trigger_build(clients, 'master', args.definition_id, variables)
    if not run:
        exit(1)
    res = wait_run_complete(clients, args.definition_id, run.id)
    if not res:
        exit(1)
    