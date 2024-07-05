# AzureML access to AKS clusters with special configurations

Built-upon [AKS Trusted Access feature](https://learn.microsoft.com/azure/aks/trusted-access-feature), AzureML now supports access to AKS clusters with following special configurations:
- AKS cluster with local account disabled
- AKS cluster with authorized IP range
- Private AKS with public FQDN configuration

📣 This feature has been deployed in the public cloud(AzureCloud). AzureUSGovernment, AzureChinaCloud and AirGap clouds have not enabled this feature.

Once the feature is deplyed to your regions, you could (re/)attach your compute to enable it; you can verify if the feature has been enabled on your AKS cluster with following steps:
- Verify that ```Microsoft.MachineLearningServices/workspaces/mlworkload``` role binding is created in AKS cluster. **Note**: AzureML role binding is per workspace, if your AKS cluster is shared among multiple workspace, you should have AzureML role binding for each workspace.
```shell
    az aks trustedaccess rolebinding list --resource-group <resource-group> --cluster-name <cluster-name>
```
> <span style="color:orange">**Notes**:</span> 
> 
> * If you have any existing compute targets created before AzureML role binding was created, those compute targets will not work with AKS cluster with above special configurations. Please detach those existing compute targets to avoid any issues.
> * This role binding does not work with legacy AksCompute (AKS inference cluster).