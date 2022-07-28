# Deploy AzureML extension to your Kubernetes cluster

1. [What is AzureML extension](#what-is-azureml-extension)

1. [**Must Read**: key considerations for AzureML extension deployment](#key-considerations-for-azureml-extension-deployment)

1. [AzureML extension deployment example scenarios](#azureml-extension-deployment-scenarios)

1. [Verify your AzureML extension deployment](#verify-your-azureml-extension-deployment)

1. [Update your AzureML extension deployment](#update-azure-machine-learning-extension)

1. [Delete AzureML extension](#delete-azure-machine-learning-extension)

1. [Apendix I: AzureML extension components](#azureml-extension-components)

1. [Appendix II: Review AzureML extension config settings](#review-azureml-deployment-configuration-settings)

## What is AzureML extension

AzureML extension consists a set of system componenents deployed to your Kubernetes cluster so you can enable cluster to run AzureML workload - model training jobs or mdoel endpoints. You can use simple Azure CLI command ```k8s-extension create``` to deployment AzureML extension.

For detailed list of AzureML extension system componenents, you need to disable `selinux`  on all workers in order to use AzureML dataset.

## Key considerations for AzureML extension deployment

AzureML extension allows you to specify config settings needed for different workload support at deployment time. Before AzureML extension deployment, **please read following carefully to avoid unnecessary extension deployment errors**:

  * Type of workload to enable for your cluster. ```enableTraining``` and ```enableInference``` config settings are your convenient choices here; `enableTraining` will enable training and batch scoring workload, `enableInference` will enable real-time inference workload.
  * For inference workload support, it requires ```azureml-fe``` rounter service to be deployed for routing incoming inference requests to model pod, and you would need to specify ```inferenceRouterServiceType``` config setting for ```azureml-fe```. ```azureml-fe``` can be deployed with one of following ```inferenceRouterServiceType```:
      * Type ```LoadBalancer```. Exposes ```azureml-fe``` externally using a cloud provider's load balancer. To specify this value, you have to ensure that your cluster supports load balancer provisioning. Note most on-premises Kubernetes clusters might not support external load balancer.
      * Type ```NodePort```. Exposes ```azureml-fe``` on each Node's IP at a staic port. You'll be able to contact ```azureml-fe```, from outside of cluster, by requesting ```<NodeIP>:<NodePort>```. Using ```NodePort``` also allows you to setup your own load balancing solution and SSL termination for ```azureml-fe```.
      * Type ```ClusterIP```. Exposes ```azureml-fe``` on a cluster-internal IP, and it makes ```azureml-fe``` only reachable from within the cluster. For ```azureml-fe``` to serve inference requests coming outside of cluster, it requires you to setup your own load balancing solution and SSL termination for ```azureml-fe```. 

    For more information about ```azureml-fe``` router service, please refer to documentation [here](https://docs.microsoft.com/en-us/azure/machine-learning/v1/how-to-deploy-azure-kubernetes-service?tabs=python#azure-ml-router)
   * For inference workload support, in order to ensure high availability of ```azureml-fe``` routing service, AzureML extension deployment by default creates 3 replicas of ```azureml-fe``` for clusters having 3 nodes or more. If your cluster has **less than 3 nodes**, please set ```inferenceRouterHA=False```.
   * For inference workload support, you would also want to consider using **HTTPS** to restrict access to model endpoints and secure the data that clients submit. For this purpose, you would need to specify either ```sslSecret``` config setting or combination of ```sslCertPemFile``` and ```sslKeyPemFile``` config settings. By default, AzureML extension deployment expects **HTTPS** support required and you would need to provide above config setting. For development or test purpose, **HTTP** support is conveniently supported through config setting ```allowInsecureConnections=True```.

For a quick POC using Minikube on your desktop or AKS in Azure, please try [happy path](./happy-path.md) instruction.

For a complete list of config settings available to choose at AzureML deployment time, please see [Review AzureML extension config settings](#review-azureml-deployment-configuration-settings)

## AzureML extension deployment scenarios

### Uing AKS in Azure for a quick POC, both training and inference workloads support

Please ensure you have fullfiled [prerequisites](./../README.md#prerequisites). For AzureML extension deployment on AKS, please make sure to specify ```managedClusters``` value for ```--cluster-type``` parameter. Run following simple Azure CLI command to deploy AzureML extension:
```azurecli
   az k8s-extension create --name <extension-name> --extension-type Microsoft.AzureML.Kubernetes --config enableTraining=True enableInference=True inferenceRouterServiceType=LoadBalancer allowInsecureConnections=True inferenceRouterHA=False --cluster-type managedClusters --cluster-name <your-AKS-cluster-name> --resource-group <your-RG-name> --scope cluster
```

### Using Minikube on your desktop for a quick POC, training workload support only

Please ensure you have fullfiled [prerequisites](./../README.md#prerequisites). Since this would be an Azure Arc connected cluster, you would need to specify ```connectedClusters``` value for ```--cluster-type``` parameter. Run following simple Azure CLI command to deploy AzureML extension:
```azurecli
   az k8s-extension create --name <extension-name> --extension-type Microsoft.AzureML.Kubernetes --config enableTraining=True --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <your-RG-name> --scope cluster
```

### Enable an AKS cluster in Azure for production training and inference workload

Please ensure you have fullfiled [prerequisites](./../README.md#prerequisites). For AzureML extension deployment on AKS, make sure to specify ```managedClusters``` value for ```--cluster-type``` parameter. Assuming your cluster has more than 3 nodes, and you will use Azure public load balancer and HTTPS for inference workload support, run following Azure CLI command to deploy AzureML extension:
```azurecli
   az k8s-extension create --name <extension-name> --extension-type Microsoft.AzureML.Kubernetes --config enableTraining=True enableInference=True inferenceRouterServiceType=LoadBalancer  sslCname=<ssl cname> --config-protected sslCertPemFile=<file-path-to-cert-PEM> sslCertKeyFile=<file-path-to-cert-KEY> --cluster-type managedClusters --cluster-name <your-AKS-cluster-name> --resource-group <your-RG-name> --scope cluster
```
### Enable an Azure Arc connected cluster anywhere for production training and inference workload using Nvidia GPUs

Please ensure you have fullfiled [prerequisites](./../README.md#prerequisites). For AzureML extension deployment on Azure Arc connected cluster, make sure to specify ```connectedClusters``` value for ```--cluster-type``` parameter. Assuming your cluster has more than 3 nodes, you will use NodePort service type and HTTPS for inference workload support, run following Azure CLI command to deploy AzureML extension:
```azurecli
   az k8s-extension create --name <extension-name> --extension-type Microsoft.AzureML.Kubernetes --config enableTraining=True enableInference=True inferenceRouterServiceType=NodePort sslCname=<ssl cname> installNvidiaDevicePlugin=True installDcgmExporter=True --config-protected sslCertPemFile=<file-path-to-cert-PEM> sslCertKeyFile=<file-path-to-cert-KEY> --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <your-RG-name> --scope cluster
```

## Verify your AzureML extension deployment

1. Run the following CLI command to check AzureML extension details:

   ```azurecli
   az k8s-extension show --name <extension-name> --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <resource-group>
   ```

1. In the response, look for "name" and "provisioningState": "Succeeded". Note it might show "provisioningState": "Pending" for the first few minutes.

1. If the provisioningState shows Succeeded, run the following command on your machine with the kubeconfig file pointed to your cluster to check that all pods under "azureml" namespace are in 'Running' state:

   ```bash
    kubectl get pods -n azureml
   ```

## Update Azure Machine Learning extension

Use ```k8s-extension update``` CLI command to update the mutable properties of  AzureML extension, review list of required and optional parameters for ```k8s-extension update``` CLI command [here](https://docs.microsoft.com/en-us/cli/azure/k8s-extension?view=azure-cli-latest#az_k8s_extension_update). 

1.	Azure Arc supports update of  ``--auto-upgrade-minor-version``, ``--version``,  ``--config``, ``--config-protected``.  
2.	For configurationSettings, only the settings that require update need to be provided. If the user provides all settings, they would be merged/overwritten with the provided values. 
3.	For ConfigurationProtectedSettings, ALL  settings should be provided. If some settings are omitted, those settings would be considered obsolete and deleted. 

> [!IMPORTANT]
> **Don't** update following configs if you have active training workloads or real-time inference endpoints. Otherwise, the training jobs will be impacted and endpoints unavailable.
> 
> * `enableTraining` from `True` to `False`
> * `installNvidiaDevicePlugin` from `True` to `False` when using GPU.
> * `nodeSelector`. The update operation can't remove existing nodeSelectors. It can only update existing ones or add new ones.
>
> **Don't** update following configs if you have active real-time inference endpoints, otherwise, the endpoints will be unavailable.
> * `allowInsecureConnections`
> * `inferenceRouterServiceType`
> * `internalLoadBalancerProvider`
> *  To update `logAnalyticsWS` from `True` to `False`, provide all original `configurationProtectedSettings`. Otherwise, those settings are considered obsolete and deleted.

## Delete Azure Machine Learning extension

Use [``k8s-extension delete``](https://docs.microsoft.com/en-us/cli/azure/k8s-extension?view=azure-cli-latest#az_k8s_extension_delete) CLI command to delete the existed AzureMl extension.

It takes around 10 minutes to delete all components deployed to the Kubernetes cluster. Run `kubectl get pods -n azureml` to check if all components were deleted. 

Please don't perform extension install or update action during extension deletion to avoid the exceptional errors.

## AzureML extension components

For Arc-connected cluster, AzureML extension deployment will create [Azure Relay](https://docs.microsoft.com/en-us/azure/azure-relay/relay-what-is-it) in Azure cloud, used to route traffic between Azure Machine Learning services and the Kubernetes cluster. For AKS cluster without Arc connected, Azure Relay resource will not be created.

Upon AzureML extension deployment completes, it will create following resources in Kubernetes cluster, depending on each AzureML extension deployment scenario:

   |Resource name  |Resource type |Training |Inference |Training and Inference| Description | Communication with cloud|
   |--|--|--|--|--|--|--|
   |relayserver|Kubernetes deployment|**&check;**|**&check;**|**&check;**|relayserver is only needed in arc-connected cluster, and will not be installed in AKS cluster. Relayserver works with Azure Relay to communicate with the cloud services.|Receive the request of job creation, model deployment from cloud service; sync the job status with cloud service.|
   |gateway|Kubernetes deployment|**&check;**|**&check;**|**&check;**|The gateway is used to communicate and send data back and forth.|Send nodes and cluster resource information to cloud services.|
   |aml-operator|Kubernetes deployment|**&check;**|N/A|**&check;**|Manage the lifecycle of training jobs.| Token exchange with the cloud token service for authentication and authorization of Azure Container Registry.|
   |metrics-controller-manager|Kubernetes deployment|**&check;**|**&check;**|**&check;**|Manage the configuration for Prometheus|N/A|
   |{EXTENSION-NAME}-kube-state-metrics|Kubernetes deployment|**&check;**|**&check;**|**&check;**|Export the cluster-related metrics to Prometheus.|N/A|
   |{EXTENSION-NAME}-prometheus-operator|Kubernetes deployment|Optional|Optional|Optional| Provide Kubernetes native deployment and management of Prometheus and related monitoring components.|N/A|
   |amlarc-identity-controller|Kubernetes deployment|N/A|**&check;**|**&check;**|Request and renew Azure Blob/Azure Container Registry token through managed identity.|Token exchange with the cloud token service for authentication and authorization of Azure Container Registry and Azure Blob used by inference/model deployment.|
   |amlarc-identity-proxy|Kubernetes deployment|N/A|**&check;**|**&check;**|Request and renew Azure Blob/Azure Container Registry token  through managed identity.|Token exchange with the cloud token service for authentication and authorization of Azure Container Registry and Azure Blob used by inference/model deployment.|
   |azureml-fe-v2|Kubernetes deployment|N/A|**&check;**|**&check;**|The front-end component that routes incoming inference requests to deployed services.|Send service logs to Azure Blob.|
   |inference-operator-controller-manager|Kubernetes deployment|N/A|**&check;**|**&check;**|Manage the lifecycle of inference endpoints. |N/A|
   |volcano-admission|Kubernetes deployment|Optional|N/A|Optional|Volcano admission webhook.|N/A|
   |volcano-controllers|Kubernetes deployment|Optional|N/A|Optional|Manage the lifecycle of Azure Machine Learning training job pods.|N/A|
   |volcano-scheduler |Kubernetes deployment|Optional|N/A|Optional|Used to perform in-cluster job scheduling.|N/A|
   |fluent-bit|Kubernetes daemonset|**&check;**|**&check;**|**&check;**|Gather the components' system log.| Upload the components' system log to cloud.|
   |{EXTENSION-NAME}-dcgm-exporter|Kubernetes daemonset|Optional|Optional|Optional|dcgm-exporter exposes GPU metrics for Prometheus.|N/A|
   |nvidia-device-plugin-daemonset|Kubernetes daemonset|Optional|Optional|Optional|nvidia-device-plugin-daemonset exposes GPUs on each node of your cluster| N/A|
   |prometheus-prom-prometheus|Kubernetes statefulset|**&check;**|**&check;**|**&check;**|Gather and send job metrics to cloud.|Send job metrics like cpu/gpu/memory uitilization to cloud.|



> **<span style="color:orange">Important**:</span> 
   > * Azure Relay resource  is under the same resource group as the Arc cluster resource. It is used to communicate with the Kubernetes cluster and modifying them will break attached compute targets.
   > * By default, the deployed kubernetes deployment resources are randomly deployed to 1 or more nodes of the cluster, and daemonset resource are deployed to ALL nodes. If you want to restrict the extension deployment to specific nodes, use `nodeSelector` configuration setting described as below.


> **<span stype="color:orane">Notes**:</span>
   > * **{EXTENSION-NAME}:** This is the extension name specified with ```az k8s-extension create --name``` CLI command. 

## Review AzureML deployment configuration settings

Use ```k8s-extension create``` CLI command to deploy AzureML extension, review list of required and optional parameters for ```k8s-extension create``` CLI command [here](https://docs.microsoft.com/en-us/cli/azure/k8s-extension?view=azure-cli-latest#az_k8s_extension_create). For AzureML extension deployment configurations, use ```--config``` or ```--config-protected``` to specify list of ```key=value``` pairs. Following is the list of configuration settings available to be used for different AzureML extension deployment scenarios.

|Configuration Setting Key Name  |Description  |Training |Inference |Training and Inference
   |--|--|--|--|--|
   |```enableTraining``` |```True``` or ```False```, default ```False```. **Must** be set to ```True``` for AzureML extension deployment with Machine Learning model training support.  |  **&check;**| N/A |  **&check;** |
   | ```enableInference``` |```True``` or ```False```, default ```False```.  **Must** be set to ```True``` for AzureML extension deployment with Machine Learning inference support. |N/A| **&check;** |  **&check;** |
   | ```allowInsecureConnections``` |```True``` or ```False```, default `False`. **Must** be set to ```True``` to use inference HTTP endpoints for development or test purposes. |N/A| Optional |  Optional |
   | ```inferenceRouterServiceType``` |```loadBalancer```, ```nodePort``` or ```clusterIP```.  **Required** if ```enableInference=True```. | N/A| **&check;** |   **&check;** |
   | ```internalLoadBalancerProvider``` | This config is only applicable for Azure Kubernetes Service(AKS) cluster now. Set to ```azure``` to allow the inference router using internal load balancer.  | N/A| Optional |  Optional |
   |```sslSecret```| The Kubernetes secret name under azureml namespace to store `cert.pem` (PEM-encoded SSL cert) and `key.pem` (PEM-encoded SSL key), required for inference HTTPS endpoint support, when  ``allowInsecureConnections`` is set to False. Use this config or combination of `sslCertPemFile` and `sslKeyPemFile` protected config settings. An example of SSL Kubernetes secret definition [YAML](../files/sslsecret.yaml)|N/A| Optional |  Optional |
   |```sslCname``` |An SSL CName is used by inference HTTPS endpoint. **Required** if ```allowInsecureConnections=False```  |  N/A | Optional | Optional|
   | ```inferenceRouterHA``` |```True``` or ```False```, default ```True```. By default, AzureML extension will deploy 3 ingress controller replicas for high availability, which requires at least 3 workers in a cluster. Set to ```False``` if your cluster has fewer than 3 workers, in this case only one ingress controller is deployed. | N/A| Optional |  Optional |
   |```nodeSelector``` | By default, the deployed kubernetes resourses are randomly deployed to 1 or more nodes of the cluster, and daemonset resources are deployed to ALL nodes. If you want to restrict the extension deployment to specific nodes with label `key1=value1` and `key2=value2`, use `nodeSelector.key1=value1`, `nodeSelector.key2=value2` correspondingly. | Optional| Optional |  Optional |
   |```installNvidiaDevicePlugin```  | ```True``` or ```False```, default ```False```. [Nvidia Device Plugin](https://github.com/NVIDIA/k8s-device-plugin#nvidia-device-plugin-for-kubernetes) is required for ML workloads on Nvidia GPU hardware. By default, AzureML extension deployment will not install Nvidia Device Plugin regardless Kubernetes cluster has GPU hardware or not. User can specify this setting to ```True```, to install it, but make sure to fulfill [Prerequisites](https://github.com/NVIDIA/k8s-device-plugin#prerequisites). | Optional |Optional |Optional |
   |```installPromOp```|```True``` or ```False```, default ```True```. AzureML extension needs prometheus operator to manage prometheus. Set to ```False``` to reuse existing prometheus operator. Compatible [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/README.md) helm chart versions are from 9.3.4 to 30.0.1. Refer to [Prometheus operator](./troubleshooting.md#prom-op) for more inforamtion| Optional| Optional |  Optional |
 |```installVolcano```| ```True``` or ```False```, default ```True```. AzureML extension needs volcano scheduler to schedule the job. Set to ```False``` to reuse existing volcano scheduler. Supported volcano scheduler versions are 1.4, 1.5. | Optional| N/A |  Optional |
 |```installDcgmExporter```  |```True``` or ```False```, default ```False```. Dcgm-exporter can expose GPU metrics for AzureML workloads, which can be monitored in Azure Portal. Set ```installDcgmExporter```  to ```True``` to install dcgm-exporter. But if you want to utilize your own dcgm-exporter,  refer to [DCGM exporter](./troubleshooting.md#dcgm) |Optional |Optional |Optional |


   |Configuration Protected Setting Key Name  |Description  |Training |Inference |Training and Inference
   |--|--|--|--|--|
   | ```sslCertPemFile```, ```sslKeyPemFile``` |Path to SSL certificate and key file (PEM-encoded), required for AzureML extension deployment with inference HTTPS endpoint support, when  ``allowInsecureConnections`` is set to False. | N/A| Optional |  Optional |

## Use ARM Template to Deploy Extension (Optional)
Extension on managed cluster can be deployed with ARM template. A sample template can be found from [deployextension.json](../files/deployextension.json), with a demo parameter file [deployextension.parameters.json](../files/deployextension.parameters.json)
<br/> To leverage the sample deployment template, edit the parameter file with correct value, then run the following command:
```
az deployment group create --name <ARM deployment name> --resource-group <resource group name> --template-file deployextension.json --parameters deployextension.parameters.json
```
More information about how to use ARM template can be found from [ARM template doc](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/)
## Next Step
- [Attach Kubernetes cluster to AzureML workspace and create a compute target](attach-compute.md)
   


