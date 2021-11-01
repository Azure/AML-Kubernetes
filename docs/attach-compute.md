# Create a compute target - attach AKS or Arc cluster to AML workspace

## Create compute target via Azure ML 2.0 CLI

You can attach AKS or Arc cluster and create KubernetesCompute target easily via AzureML 2.0 CLI.

1. Refer to [Install, set up, and use the 2.0 CLI (preview)](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-configure-cli) to install ML 2.0 CLI. Compute attach support **requires ml extension >= 2.0.1a4**. 

1. Attach the  Arc-enabled Kubernetes cluster,

```azurecli
az ml compute attach --resource-group
                     --workspace-name
                     --name
                     --resource-id
                     --type					 
                     [--namespace]
                     [--identity-type]
                     [--user-assigned-identities]
                     [--no-wait]

```

**Required Parameters**

* `--resource-group -g` 

   Name of resource group. You can configure the default group using `az configure --defaults group=<name>`.
* `--workspace-name -w` 
   
   Name of the Azure ML workspace. You can configure the default group using `az configure --defaults workspace=<name>`.
* `--name -n`

   Name of the compute target.
* `--resource-id`

   The fully qualified ID of the resource, including the resource name and resource type.
   
   For Arc-enabld k8s cluster, it's like ` /subscriptions/<sub ID>/resourceGroups/<resource group>/providers/Microsoft.Kubernetes/connectedClusters/<cluster name>"`

   For AKS cluster with ML extension deployed without Arc conntected, it's like ` "/subscriptions/<sub ID>/resourceGroups/<resource group>/providers/Microsoft.ContainerService/managedclusters/<cluster name>`
* `--type -t`

   The type of compute target. Allowed values: kubernetes, AKS, virtualmachine. Specify `kubernetes` to attach arc-enabled kubernetes cluster or AKS cluster with ML extension deployed.

**Optional Parameters**

* `--namespace`

   Kubernetes namespace to host the ML workloads at this compute, default to `default`.
* `--no-wait`

   Do not wait for the long-running operation to finish.
* `--identity-type`

   The type of managed identity. Allowed values: SystemAssigned, UserAssigned.
* `--user-assigned-identities`
 
   Only needed when user assigned identity is used. A list of resource IDs separated by commas. Only the first identity in the list can be used today.

## Create a compute target via AML Studio UI

It is easy to attach Azure Arc-enabled Kubernetes cluster to AML workspace, you can do so from AML Studio UI portal. 


1. Go to AML studio portal > Compute > Attached compute, click "+New" button, and select "Kubernetes (Preview)"

   ![Create a generic compute target](./media/attach-1.png)

1. Enter a compute name, and select your AKS or Azure Arc-enabled Kubernetes cluster from Kubernetes cluster dropdown list.

   ![Create a generic compute target](./media/attach.png)


   * (Optional) Assign system-assigned or user-assigned [Managed Identity](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview).


1. Click 'Attach' button. You will see the 'provisioning state' as 'Creating'. If it succeeds, you will see a 'Succeeded' state or else 'Failed' state.

   ![Create a generic compute target](./media/attach-4.png)



## Create compute target via AML Python SDK

You can also attach AKS or Arc cluster and create KubernetesCompute target easily via AML Python SDK 1.30 or above.

Following Python code snippets shows how you can easily attach an kubernetes cluster and create a compute target with Managed Identity enabled.


```python

from azureml.core.compute import KubernetesCompute
from azureml.core.compute import ComputeTarget
from azureml.core.workspace import Workspace
import os

ws = Workspace.from_config()

# Specify a name for your Kubernetes compute
amlarc_compute_name = "<COMPUTE_CLUSTER_NAME>"

# resource ID for the Kubernetes cluster and user-managed identity
resource_id = "/subscriptions/<sub ID>/resourceGroups/<RG>/providers/Microsoft.Kubernetes/connectedClusters/<cluster name>"

user_assigned_identity_resouce_id = ['subscriptions/<sub ID>/resourceGroups/<RG>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<identity name>']

ns = "default" 

if amlarc_compute_name in ws.compute_targets:
    amlarc_compute = ws.compute_targets[amlarc_compute_name]
    if amlarc_compute and type(amlarc_compute) is KubernetesCompute:
        print("found compute target: " + amlarc_compute_name)
else:
   print("creating new compute target...")


# assign user-assigned managed identity
amlarc_attach_configuration = KubernetesCompute.attach_configuration(resource_id = resource_id, namespace = ns,  identity_type ='UserAssigned',identity_ids = user_assigned_identity_resouce_id) 

# assign system-assigned managed identity
# amlarc_attach_configuration = KubernetesCompute.attach_configuration(resource_id = resource_id, namespace = ns,  identity_type ='SystemAssigned') 

amlarc_compute = ComputeTarget.attach(ws, amlarc_compute_name, amlarc_attach_configuration)
amlarc_compute.wait_for_completion(show_output=True)

# get detailed compute description containing managed identity principle ID, used for permission access. 
print(amlarc_compute.get_status().serialize())
```

**Parameters of `KubernetesCompute.attach_configuration()`**

`resource_id`, [string](https://docs.python.org/3/library/string.html#module-string), required

  The fully qualified ID of the resource, including the resource name and resource type.

`namespace`, [string](https://docs.python.org/3/library/string.html#module-string), optional

Kubernetes namespace to host the ML workloads at this compute, default to `default`.

`identity_type`, [string](https://docs.python.org/3/library/string.html#module-string), optional

default value: None

Possible values are:

- SystemAssigned - System assigned identity

- UserAssigned - User assigned identity. Requires identity_ids to be set.

`identity_ids`, [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/string.html#module-string)], optional

default value: None

List of resource ids for the user assigned identity. e.g. ['subscriptions/\<sub ID>/resourceGroups/\<RG>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/\<identity name>']
