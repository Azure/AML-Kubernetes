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
                     [--file]
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
* `--type -t`

   The type of compute target. Allowed values: kubernetes, AKS, virtualmachine. Specify `kubernetes` to attach arc-enabled kubernetes cluster.

**Optional Parameters**

* `--file`

   Local path to the YAML file containing the compute specification. **Ignoring this param will allow the default compute configuration for simple compute attach scenario, or specify a YAML file with customized compute defination for advanced attach scenario**. 
* `--no-wait`

   Do not wait for the long-running operation to finish.

## Create a compute target via AML Studio UI

It is easy to attach Azure Arc-enabled Kubernetes cluster to AML workspace, you can do so from AML Studio UI portal. 


1. Go to AML studio portal, Compute > Attached compute, click "+New" button, and select "Kubernetes (Preview)"

   ![Create a generic compute target](./media/attach-1.png)

1. Enter a compute name, and select your Azure Arc-enabled Kubernetes cluster from Azure Arc-enabled Kubernetes cluster dropdown list.

   ![Create a generic compute target](./media/attach-2.png)

1. (Optional) Browse and upload an attach config file. **Skip this step to use the default compute configuration for simple compute attach scenario, or specify a YAML file with customized compute defination for [advanced attach scenario](attach-compute.md#Advanced-compute-attach-scenarios)**

   ![Create a generic compute target](./media/attach-3.png)

1. Click 'Attach' button. You will see the 'provisioning state' as 'Creating'. If it succeeds, you will see a 'Succeeded' state or else 'Failed' state.

   ![Create a generic compute target](./media/attach-4.png)



## Create compute target via AML Python SDK

You can also attach AKS or Arc cluster and create KubernetesCompute target easily via AML Python SDK 1.30 or above.

Following Python code snippets shows how you can easily attach an Arc cluster and create a compute target to be used for training job.

```python
from azureml.core.compute import KubernetesCompute
from azureml.core.compute import ComputeTarget
import os

ws = Workspace.from_config()

# choose a name for your Azure Arc-enabled Kubernetes compute
amlarc_compute_name = os.environ.get("AML_COMPUTE_CLUSTER_NAME", "amlarc-ml")

# resource ID for your Azure Arc-enabled Kubernetes cluster
resource_id = "/subscriptions/123/resourceGroups/rg/providers/Microsoft.Kubernetes/connectedClusters/amlarc-cluster"

if amlarc_compute_name in ws.compute_targets:
    amlarc_compute = ws.compute_targets[amlarc_compute_name]
    if amlarc_compute and type(amlarc_compute) is KubernetesCompute:
        print("found compute target: " + amlarc_compute_name)
else:
    print("creating new compute target...")

    amlarc_attach_configuration = KubernetesCompute.attach_configuration(resource_id) 
    amlarc_compute = ComputeTarget.attach(ws, amlarc_compute_name, amlarc_attach_configuration)

 
    amlarc_compute.wait_for_completion(show_output=True)
    
     # For a more detailed view of current KubernetesCompute status, use get_status()
    print(amlarc_compute.get_status().serialize())
```