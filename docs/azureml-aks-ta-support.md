# AzureML access to AKS clusters with special configurations

Built-upon AKS Trusted Access (preview) feature, AzureML now supports access to AKS clusters with following special configurations:
- AKS cluster with local account disabled
- AKS cluster with authorized IP range

To preview this feature in AzureML, please ensure to fulfill following prerequisites:
- Sign up preview [here](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR9S7K-kdeMpBoc3jEmzkKMVUREwxSjhQTVNaM1I4RlVENklYQ1hRTFFSTC4u)
- You have an AKS cluster with one of above special configurations
- You have installed AzureML extension according to [documentation](https://aka.ms/amlarc/doc)

Once you get confirmation of preview feature access from Microsoft, you can enable AzureML access to your AKS cluster with following steps:
- Create AzureML role binding in AKS cluster with following AzureML CLI commmand. **Note**: AzureML role binding is per workspace, if your AKS cluster is shared among multiple workspace, you must create AzureML role binding for each workspace.

```shell
    az aks trustedaccess rolebinding create –resource group <resource-group> --cluster-name <cluster-name> --name <rolebinding-name> --source-resource-id /subscriptions/<subscriptions-id>/resourceGroups/<resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<workspaces-name> --roles Microsoft.MachineLearningServices/workspaces/mlworkload

``` 
- Verify that ```Microsoft.MachineLearningServices/workspaces/mlworkload``` role binding is created in AKS cluster:
```shell
    az aks trustedaccess rolebinding list --resource-group <resource-group> --cluster-name <cluster-name>
```
- Follow [documentation](https://aka.ms/amlarc/doc) to attach AKS cluster to workspace and create a new compute target. This new compute target will leverage AKS Trusted Access feature and access AKS cluster with above special configurations.

> [!NOTE]
  > If you have any existing compute targets created before AzureML role binding was created, those compute targets will not work with AKS cluster with above special configurations. Please detach those existing compute targets to avoid any issues.

