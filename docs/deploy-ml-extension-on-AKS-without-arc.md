## Deploy AzureML extension to AKS cluster without connecting via Azure Arc (private preview)

For Azure Kubernetes Service (AKS), now you can deploy AzureML extension to the cluster directly, and don't need to connect it to Azure Arc beforehand.

### Prerequisites

*  Sign up [here](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR82DXV1MLKFCgun1LAU3Tz1URjJUSjZZQ0IwTUlKNkVaSFM5OUJHRzgwSC4u), and receive email reply to get confirmation that your subscription is added to the allowlist.
* Provision an AKS cluster - **the cluster must have minimum of 6 vCPU cores and 16GB memory, around 3 vCPU cores and 6GB memory would be used by system**.
* A ```kubeconfig``` file and context pointing to your AKS cluster.
* Install the [latest release of Helm 3](https://helm.sh/docs/intro/install/)
* Install or upgrade Azure CLI to version >= **2.24.0**.
* Install k8s-extension Azure CLI extension from the [whl file](../files/k8s_extension-0.6.1-py3-none-any.whl)
```
az extension remove --name k8s-extension

az extension add --source <whl filepaht> --yes
```
* Register this preview feature before you are able to deploy the extension to AKS
```azurecli
az feature register --namespace Microsoft.ContainerService -n AKS-ExtensionManager
```

### Deploy AzureML extension to AKS

Refer to the guidance in [Deploy AzureML extension to your Kubernetes cluster](deploy-extension.md#deploy-azureml-extension-for-model-training). Only need to change the  `cluster-type` from `connectedClusters` to `managedClusters`

```azurecli
   az k8s-extension create --name amlarc-compute --extension-type Microsoft.AzureML.Kubernetes --configuration-settings enableTraining=True  --cluster-type managedClusters --cluster-name <your-AKS-cluster-name> --resource-group <resource-group> --scope cluster
   ```
### Attach AKS to AzureML workspace as a compute target

Refer to the guidance in [Create a compute target - Attach Azure Arc enabled Kubernetes cluster to AML Workspace](attach-compute.md). You can use **Python SDK or ML 2.0 CLI** to attach your AKS cluster.

Note that when you do the attachment via Python SDK or 2.0 CLI, the AKS cluster resource ID is needed. The resource ID is formatted as,
```
resource_id = "/subscriptions/<sub ID>/resourceGroups/<resource group>/providers/Microsoft.ContainerService/managedclusters/<cluster name>"

```
