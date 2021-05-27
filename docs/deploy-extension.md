# Deploy AzureML extension to your Kubernetes cluster

You will use Azure CLI to deploy the extension on top of your Azure Arc-enabled Kubernetes cluster. 

## Review AzureML extension deployment configuration settings

Following is the list of available configuration settings to be specified when you deploy AzureML extension. Configuration settings can be specified by appending key/value pairs to ```--configuration-settings``` parameter in "az k8s-extension create" CLI command.

   |Configuration Setting Key Name  |Description  |
   |--|--|
   | ```enableTraining``` |```True``` or ```False```, default ```False```. **Must** be set to ```True``` for AzureML extension deployment with Machine Learning model training support.  |
   |```relayConnectionString```  |Connection string for Azure Relay resource. Azure Relay resource is required for Kubernetes communication with AML services in cloud. By default, AzureML extension will create Azure Relay resource under the same resource group as Azure Arc connected cluster, and user does not need to set this configuration setting. AzureML extension will use the provided Azure Relay resource if this configuration setting is set. |
   |```serviceBusConnectionString```  |Connection string for Azure Service Bus resource. Azure Service Bus resource is required for Kubernetes communication with AML services in cloud. By default, AzureML extension will create Azure Service Bus resource under the same resource group as Azure Arc connected cluster, and user does not need to set this configuration setting. AzureML extension will use the provided Azure Service Bus resource if this configuration setting is set. |
   |```logAnalyticsWS```  |```True``` or ```False```, default ```False```. AzureML extension integrates with Azure LogAnalytics Workspace to provide log viewing and analysis capability through LogAalytics Workspace. This setting must be explicitly set to ```True``` if customer wants to leverage this capability. LogAnalytics Workspace cost may apply.  |
   |```installNvidiaDevicePlugin```  | ```True``` or ```False```, default ```True```. Nvidia Device Plugin is required for ML inference on Nvidia GPU hardware. By default, AzureML extension deployment will install Nvidia Device Plugin regardless Kubernete cluster has GPU hardware or not. User can specify this configuration setting to False if Nvidia Device Plugin installation is not required (either it is installed already or there is no plan to use GPU for inference).```  |
   |```installBlobfuseSysctl```  |```True``` or ```False```, default ```True``` if ```enableTraining=True```. Blobfuse 1.3.7 is required for ML training, and by default AzureML will install Blobfuse when extension extension instance is created. User can set this configuration setting to ```False``` if Blobfuse 1.3.7 is already installed on Kubernetes cluster.   |
   |```installBlobfuseFlexvol```  |```True``` or ```False```, default ```True``` if ```enableTraining=True```. Blobfuse Flexvolume is required for ML training, and by default AzureML will install Blobfuse Flexvolume to default path. User can set this configuration setting to ```False``` if Blobfuse Flexvolume is already installed.```   |
   |```volumePluginDir```  |Hostpath for Blobfuse Flexvolume to be installed, applicable only for ```enableTraining=True```. By default, AzureML will install Blobfuse Flexvolume under default path ```/etc/kubernetes/volumeplugins```. User can specify custom installation location by specifying this configuration setting.   |   

## Login to Azure

   ```azurecli
   az login
   az account set --subscription <your-subscription-id>
   ```

## Deploy AzureML extension for model training

   ```azurecli
   az k8s-extension create --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <resource-group> --name microsoft.azureml.kubernetes --extension-type Microsoft.AzureML.Kubernetes --scope cluster --configuration-settings enableTraining=True 
   ```

## Verify your AzureML extension deployment

1. Run the following command on Azure CLI:

   ```azurecli
   az k8s-extension show --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <resource-group> --name microsoft.azureml.kubernetes
   ```

1. In the response, look for "extensionType": "microsoft.azureml.kubernetes" and "installState": "Installed". Note it might show "installState": "Pending" for the first few minutes.

1. If the state shows Installed, run the following command on your machine with the kubeconfig file pointed to your cluster to check that all pods under "azureml" namespace are in 'Running' state:

   ```bash
    kubectl get pods -n azureml
   ```
