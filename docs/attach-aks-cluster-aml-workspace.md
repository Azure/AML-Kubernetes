
## Attach kubernetes compute from UI

1. Goto AML studio [portal](https://ml.azure.com), Compute > Attached compute, click "+New" button, and select "Kubernetes service (Preview)"

![addKubernetesCompute](/media/addKubernetesCompute.png)

2. Enter a compute name and check 'Azure Kubernetes service' radio button. In the dropdown below, you should see all your AKS clusters in that subscription

![listAKS](/media/listAKS.png)

3. Select an AKS cluster

![selectAksCluster](/media/2.3akscluster.png)

4. (Optional) Attach a profile config file
A profile config is a YAML file that defines a namespace and/or node selctors to which the data scientist is set up to deploy training jobs
If you skip this section, all jobs/pods will be deployed to the default namespace
Profile config schema is captured [here](/profile-config/profile-schema-v1.0.yaml)
Profile config sample can be found [here](/profile-config/profile-v1.0-sample-1)
It is expected that the IT operator sets up the kubernetes namespaces/node selectors, otherwise the jobs/pods will be deployed in the default namespace

![profileConfig]()


After attach a CMAKS compute you can [Submit AML training jobs to CMAKS compute](https://github.com/Azure/CMK8s-Samples/blob/master/docs/3.%20Submit%20AML%20training%20jobs%20to%20CMASK%20compute.markdown)

### Detach compute from UI
Go to compute list and then Compute Details, click on Detach and confirm.
![detach](/media)


# Pending edit

## Attach CMAKS compute using SDK
To attach CMAKS compute you need install private branch SDK
### Install private branch SDK
```
pip install --disable-pip-version-check --extra-index-url https://azuremlsdktestpypi.azureedge.net/CmAks-Compute-Test/D58E86006C65 azureml-pipeline-steps azureml-contrib-pipeline-steps azureml-contrib-k8s --upgrade
```
### Attach CMAKS compute via SDK

```python
from azureml.contrib.core.compute.cmakscompute import CmAksCompute
from azureml.core import Workspace
from azureml.core.compute import ComputeTarget
attach_config = CmAksCompute.attach_configuration(cluster_name =<cluster_name>
                                                    , resource_group =<resource group>
                                                    , node_pool=<node pool>
                                                 )

cmaks_target = ComputeTarget.attach(ws, <compute name>, attach_config)
```
### Detach CMAKS compute via SDK
```
cmaks_target.detach()
```



<!--
## Attach/Detach compute from CLI
### Install azure-cli-extension private branch
- Firstly, use  ```az extension remove -n azure-cli-ml ``` command to remove the previous extension. 
- Secondly, use the following command to install extension
```
az extension add --source https://azuremlsdktestpypi.blob.core.windows.net/wheels/AzureML-ITP-CLI/24196246/azure_cli_ml_private_preview-0.1.0.24196246-py3-none-any.whl --pip-extra-index-urls https://azuremlsdktestpypi.azureedge.net/AzureML-ITP-CLI/24196246 --yes --debug
```

### Attach CMAKS compute via CLI
Parameters are not same as [az ml computetarget attach](https://docs.microsoft.com/en-us/cli/azure/ext/azure-cli-ml/ml/computetarget/attach?view=azure-cli-latest#ext-azure-cli-ml-az-ml-computetarget-attach-aks), we also need to specify the cluster nood pool name.
```
az ml computetarget attach akscompute --compute-target-name mycmaks --aks-cluster-name myakscluster --aks-resource-group myresourcegroup --node-pool-name agentpool --workspace-name myworkspace --workspace-resource-group myresourcegroup --subscription-id mysubscriptionid -v
```

### Detach CMAKS compute via CLI
```
az ml computetarget detach akscompute --name mycmaks --workspace-name myworkspace --resource-group myresourcegroup --subscription-id mysubscriptionid -v
```
-->
