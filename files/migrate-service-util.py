#!/usr/bin/python3

from azureml.core.compute import KubernetesCompute
from azureml.core.compute import AksCompute, ComputeTarget
from azureml.core.workspace import Workspace
from azureml.core.webservice import AksWebservice
import sys

def run(subscription_id, resource_group, workspace_name, aks_cluster_name, service_name, service_namespace, amlarc_compute_name, inference_compute_name):

    ws = Workspace.get(
        subscription_id = subscription_id, 
        resource_group = resource_group, 
        name = workspace_name)
    print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep = '\n')

    # resource ID for your Azure Arc-enabled Kubernetes cluster
    resource_id = "/subscriptions/" + subscription_id + "/resourceGroups/" + resource_group + "/providers/Microsoft.ContainerService/managedClusters/" + aks_cluster_name

    if amlarc_compute_name in ws.compute_targets:
        amlarc_compute = ws.compute_targets[amlarc_compute_name]
        if amlarc_compute and type(amlarc_compute) is KubernetesCompute:
            print("found compute target: " + amlarc_compute_name)
    else:
        print("creating new compute target...")

        amlarc_attach_configuration = KubernetesCompute.attach_configuration(resource_id, namespace = service_namespace) 
        amlarc_compute = ComputeTarget.attach(ws, amlarc_compute_name, amlarc_attach_configuration)

    
        amlarc_compute.wait_for_completion(show_output=True)
        
        # For a more detailed view of current KubernetesCompute status, use get_status()
        print(amlarc_compute.get_status().serialize())
    
    aks_service = AksWebservice(ws, service_name)
    aks_service.update(is_migration=True, compute_target=amlarc_compute_name)

    aks_service.wait_for_deployment(show_output=True)

    try:
        inference_compute = AksCompute(ws, inference_compute_name)
        print("detaching inference compute target: " + inference_compute_name)
        inference_compute.detach()
    except ComputeTargetException:
        print("Not found inference compute target: " + inference_compute_name)

if __name__ == "__main__":

    print(len(sys.argv))
    print(str(sys.argv))
    subscription_id = sys.argv[1]
    resource_group = sys.argv[2]
    workspace_name = sys.argv[3]
    aks_cluster_name = sys.argv[4]
    service_name = sys.argv[5]
    service_namespace = sys.argv[6]
    amlarc_compute_name = sys.argv[7]
    inference_compute_name = sys.argv[8]

    print(subscription_id)
    run(subscription_id, resource_group, workspace_name, aks_cluster_name, service_name, service_namespace, amlarc_compute_name, inference_compute_name)
