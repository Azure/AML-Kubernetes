# Assign Managed Identity to the compute target (preview)

A common challenge for developers is the management of secrets and credentials used to secure communication between different components making up a solution. [Managed Identity](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview) eliminate the need for developers to manage credentials.

To access Azure Container Registry (ACR) for Docker image, and Storage Account for trainig data, attach AMLArc compute with system-assigned or user-assigned managed identity enabled.

## Assign Managed Identity using Python SDK

You can assign Managed Identity duing compute attachment.

1. Install or upgrade AzureML Python SDK `azureml-core` to version >= **v1.34.0**, and very the SDK version.

   ```pip install --upgrade azureml-core```
   ```pip show azureml-core```
1. Attach the compute to AML workspace with Managed Identity enabled
```python

from azureml.core.compute import KubernetesCompute
from azureml.core.compute import ComputeTarget
from azureml.core.workspace import Workspace
import os

ws = Workspace.from_config()

# choose a name for your Azure Arc-enabled Kubernetes compute
amlarc_compute_name = "<COMPUTE_CLUSTER_NAME>"

# resource ID for your Azure Arc-enabled Kubernetes cluster and user-managed identity
resource_id = "/subscriptions/<sub ID>/resourceGroups/<RG>/providers/Microsoft.Kubernetes/connectedClusters/<cluster name>"
user_assigned_identity_resouce_id = ['subscriptions/<sub ID>/resourceGroups/<RG>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<identity name>']
    
if amlarc_compute_name in ws.compute_targets:
    amlarc_compute = ws.compute_targets[amlarc_compute_name]
    if amlarc_compute and type(amlarc_compute) is KubernetesCompute:
        print("found compute target: " + amlarc_compute_name)
else:
   print("creating new compute target...")
   ns = "default" 
   instance_types = {
      "gpu_instance": {
         "resources": {
            "requests": {
               "cpu": "1",
               "memory": "4Gi",
               "nvidia.com/gpu": "1"
            },
            "limits": {
               "cpu": "1",
               "memory": "4Gi",
               "nvidia.com/gpu": "1"
            }
        }
      },
      "big_cpu_sku": {
         "resources": {
            "requests": {
               "cpu": "0.5",
               "memory": "1Gi",
               "nvidia.com/gpu": "0"
            },
            "limits": {
               "cpu": "0.5",
               "memory": "1Gi",
               "nvidia.com/gpu": "0"
            }         
         }
      }
   }

# assign user-assigned managed identity
amlarc_attach_configuration = KubernetesCompute.attach_configuration(resource_id = resource_id, namespace = ns, default_instance_type="big_cpu_sku", instance_types = instance_types, identity_type ='UserAssigned',identity_ids = user_assigned_identity_resouce_id) 

# assign system-assigned managed identity
# amlarc_attach_configuration = KubernetesCompute.attach_configuration(resource_id = resource_id, namespace = ns, default_instance_type="gpu_instance", instance_types = instance_types, identity_type ='SystemAssigned') 

amlarc_compute = ComputeTarget.attach(ws, amlarc_compute_name, amlarc_attach_configuration)
amlarc_compute.wait_for_completion(show_output=True)

# get detailed compute description containing managed identity principle ID, used for permission access. 
print(amlarc_compute.get_status().serialize())
```

**Parameters**

`identity_type` [string](https://docs.python.org/3/library/string.html#module-string)

default value: None

Possible values are:

- SystemAssigned - System assigned identity

- UserAssigned - User assigned identity. Requires identity_ids to be set.

`identity_ids` [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/string.html#module-string)]

default value: None

List of resource ids for the user assigned identity. e.g. ['subscriptions/\<sub ID>/resourceGroups/\<RG>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/\<identity name>']