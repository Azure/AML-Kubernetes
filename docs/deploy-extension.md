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

For detailed list of AzureML extension system componenents, please see [AzureML extension componenets](#azureml-extension-components) section.

## Key considerations for AzureML extension deployment

AzureML extension allows you to specify config settings needed for different workload support at deployment time. Before AzureML extension deployment, **please read following carefully to avoid unnecessary extension deployment errors**:

  * Type of workload to enable for your cluster. ```enableTraining``` and ```enableInference``` config settings are your convenient choices here, they will enable training and inference workload respectively. 
  * For inference workload support, it requires ```azureml-fe``` rounter service to be deployed for routing incoming inference requests to model pod, and you would need to specify ```inferenceRouterServiceType``` config setting for ```azureml-fe```. ```azureml-fe``` can be deployed with one of following ```inferenceRouterServiceType```:
      * Type ```LoadBalancer```. Exposes ```azureml-fe``` externally using a cloud provider's load balancer. To specify this value, you have to ensure that your cluster supports load balancer provisioning. Note most on-premises Kubernetes clusters might not support external load balancer.
      * Type ```NodePort```. Exposes ```azureml-fe``` on each Node's IP at a staic port. You'll be able to contact ```azureml-fe```, from outside of cluster, by requesting ```<NodeIP>:<NodePort>```. Using ```NodePort``` also allows you to setup your own load balancing solution and SSL termination for ```azureml-fe```.
      * Type ```ClusterIP```. Exposes ```azureml-fe``` on a cluster-internal IP, and it makes ```azureml-fe``` only reachable from within the cluster. For ```azureml-fe``` to serve inference requests coming outside of cluster, it requires you to setup your own load balancing solution and SSL termination for ```azureml-fe```. 

    For more information about ```azureml-fe``` router service, please refer to documentation [here](https://docs.microsoft.com/en-us/azure/machine-learning/v1/how-to-deploy-azure-kubernetes-service?tabs=python#azure-ml-router)
   * For inference workload support, in order to ensure high availability of ```azureml-fe``` routing service, AzureML extension deployment by default creates 3 replicas of ```azureml-fe``` for clusters having 3 nodes or more. If your cluster has **less than 3 nodes**, please set ```inferenceLoadbalancerHA=False```.
   * For inference workload support, you would also want to consider using **HTTPS** to restrict access to model endpoints and secure the data that clients submit. For this purpose, you would need to specify either ```sslSecret``` config setting or combination of ```sslCertPemFile``` and ```sslCertKeyFile``` config settings. By default, AzureML extension deployment expects **HTTPS** support required and you would need to provide above config setting. For development or test purpose, **HTTP** support is conveniently supported through config setting ```allowInsecureConnections=True```.

For a quick POC using Minikube on your desktop or AKS in Azure, please try [happy path](./happy-path.md) instruction.

For a complete list of config settings available to choose at AzureML deployment time, please see [Review AzureML extension config settings](#review-azureml-deployment-configuration-settings)

## AzureML extension deployment scenarios

### Uing AKS in Azure for a quick POC, both training and inference workloads support

Please ensure you have fullfiled [prerequisites](./../README.md#prerequisites). For AzureML extension deployment on AKS, please make sure to specify ```managedClusters``` value for ```--cluster-type``` parameter. Run following simple Azure CLI command to deploy AzureML extension:
```azurecli
   az k8s-extension create --name azureml-extension --extension-type Microsoft.AzureML.Kubernetes --config enableTraining=True enableInference=True inferenceRouterServiceType=LoadBalancer allowInsecureConnections=True inferenceLoadBalancerHA=False --cluster-type managedClusters --cluster-name <your-AKS-cluster-name> --resource-group <your-RG-name> --scope cluster
```

### Using Minikube on your desktop for a quick POC, training workload support only

Please ensure you have fullfiled [prerequisites](./../README.md#prerequisites). Since this would be an Azure Arc connected cluster, you would need to specify ```connectedClusters``` value for ```--cluster-type``` parameter. Run following simple Azure CLI command to deploy AzureML extension:
```azurecli
   az k8s-extension create --name azureml-extension --extension-type Microsoft.AzureML.Kubernetes --config enableTraining=True --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <your-RG-name> --scope cluster
```

### Enable an AKS cluster in Azure for production training and inference workload

Please ensure you have fullfiled [prerequisites](./../README.md#prerequisites). Assuming your cluster has more than 3 nodes, and you will use Azure public load balancer and HTTPS for inference workload support, run following Azure CLI command to deploy AzureML extension:
```azurecli
   az k8s-extension create --name azureml-extension --extension-type Microsoft.AzureML.Kubernetes --config enableTraining=True enableInference=True inferenceRouterServiceType=LoadBalancer --config-protected sslCertPemFile=<file-path-to-cert-PEM> sslCertKeyFile=<file-path-to-cert-KEY> --cluster-type managedClusters --cluster-name <your-AKS-cluster-name> --resource-group <your-RG-name> --scope cluster
```
### Enable an Azure Arc connected cluster anywhere for production training and inference workload

Please ensure you have fullfiled [prerequisites](./../README.md#prerequisites). Assuming your cluster has more than 3 nodes, you will use NodePort service type and HTTPS for inference workload support, run following Azure CLI command to deploy AzureML extension:
```azurecli
   az k8s-extension create --name azureml-extension --extension-type Microsoft.AzureML.Kubernetes --config enableTraining=True enableInference=True inferenceRouterServiceType=NodePort --config-protected sslCertPemFile=<file-path-to-cert-PEM> sslCertKeyFile=<file-path-to-cert-KEY> --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <your-RG-name> --scope cluster
```

## Verify your AzureML extension deployment

1. Run the following CLI command to check AzureML extension details:

   ```azurecli
   az k8s-extension show --name azureml-extension --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <resource-group>
   ```

1. In the response, look for "name": "azureml-extension" and "provisioningState": "Succeeded". Note it might show "provisioningState": "Pending" for the first few minutes.

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

## AzureML extension components

Upon AzureML extension deployment completes, it will create following resources in Azure cloud:
   |Resource name  |Resource type | Description |
   |--|--|--|
   |Azure Service Bus|Azure resource|Used to sync nodes and cluster resource information to Azure Machine Learning services regularly.|
   |Azure Relay|Azure resource|Route traffic between Azure Machine Learning services and the Kubernetes cluster.|

Upon AzureML extension deployment completes, it will create following resources in Kubernetes cluster, depending on each AzureML extension deployment scenario:
   |Resource name  |Resource type |Training |Inference |Training and Inference| Description | Communication with cloud service|
   |--|--|--|--|--|--|--|
   |relayserver|Kubernetes deployment|**&check;**|**&check;**|**&check;**|The entry component to receive and sync the message with cloud.|Receive the request of job creation, model deployment from cloud service; sync the job status with cloud service.|
   |gateway|Kubernetes deployment|**&check;**|**&check;**|**&check;**|The gateway to communicate and send data back and forth.|Send nodes and cluster resource information to cloud services.|
   |aml-operator|Kubernetes deployment|**&check;**|N/A|**&check;**|Manage the lifecycle of training jobs.| Token exchange with cloud token service for authentication and authorization of Azure Container Registry used by training job.|
   |metrics-controller-manager|Kubernetes deployment|**&check;**|**&check;**|**&check;**|Manage the configuration for Prometheus|N/A|
   |{EXTENSION-NAME}-kube-state-metrics|Kubernetes deployment|**&check;**|**&check;**|**&check;**|Export the cluster-related metrics to Prometheus.|N/A|
   |{EXTENSION-NAME}-prometheus-operator|Kubernetes deployment|**&check;**|**&check;**|**&check;**| Provide Kubernetes native deployment and management of Prometheus and related monitoring components.|N/A|
   |amlarc-identity-controller|Kubernetes deployment|N/A|**&check;**|**&check;**|Request and renew Azure Blob/Azure Container Registry token through managed identity.|Token exchange with cloud token service for authentication and authorization of Azure Contianer Registry and Azure Blob used by inference/model deployment.|
   |amlarc-identity-proxy|Kubernetes deployment|N/A|**&check;**|**&check;**|Request and renew Azure Blob/Azure Container Registry token  through managed identity.|Token exchange with cloud token service for authentication and authorization of Azure Contianer Registry and Azure Blob used by inference/model deployment.|
   |[azureml-fe](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-azure-kubernetes-service?tabs=python#azure-ml-router)|Kubernetes deployment|N/A|**&check;**|**&check;**|The front-end component that routes incoming inference requests to deployed services.|azureml-fe service logs are sent to Azure Blob.|
   |inference-operator-controller-manager|Kubernetes deployment|N/A|**&check;**|**&check;**|Manage the lifecycle of inference endpoints. |N/A|
   |cluster-status-reporter|Kubernetes deployment|**&check;**|**&check;**|**&check;**|Gather the cluster information, like cpu/gpu/memory usage, cluster healthness.|N/A|
<!--    |csi-blob-controller|Kubernetes deployment|**&check;**|N/A|**&check;**|Azure Blob Storage Container Storage Interface(CSI) driver.|N/A|
   |csi-blob-node|Kubernetes daemonset|**&check;**|N/A|**&check;**|Azure Blob Storage Container Storage Interface(CSI) driver.|N/A| -->
   |fluent-bit|Kubernetes daemonset|**&check;**|**&check;**|**&check;**|Gather the components' system log.| Upload the components' system log to cloud.|
<!--    |k8s-host-device-plugin-daemonset|Kubernetes daemonset|**&check;**|**&check;**|**&check;**|Expose fuse to pods on each node.|N/A| -->
   |prometheus-prom-prometheus|Kubernetes statefulset|**&check;**|**&check;**|**&check;**|Gather and send job metrics to cloud.|Send job metrics like cpu/gpu/memory uitilization to cloud.|
   |volcano-admission|Kubernetes deployment|**&check;**|N/A|**&check;**|Volcano admission webhook.|N/A|
   |volcano-controllers|Kubernetes deployment|**&check;**|N/A|**&check;**|Manage the lifecycle of Azure Machine Learning training job pods.|N/A|
   |volcano-scheduler |Kubernetes deployment|**&check;**|N/A|**&check;**|Used to do in cluster job scheduling.|N/A|

> **<span style="color:orange">Important**:</span> 
   > * Azure ServiceBus and Azure Relay resources  are under the same resource group as the Arc cluster resource. These resources are used to communicate with the Kubernetes cluster and modifying them will break attached compute targets.
   > * By default, the deployed kubernetes deployment resourses are randomly deployed to 1 or more nodes of the cluster, and daemonset resource are deployed to ALL nodes. If you want to restrict the extension deployment to specific nodes, please use `nodeSelector` configuration setting described as below.


> **<span stype="color:orane">Notes**:</span>
   > * **{EXTENSION-NAME}:** This is the extension name specified with ```az k8s-extension create --name``` CLI command. 

## Review AzureML deployment configuration settings

Use ```k8s-extension create``` CLI command to deploy AzureML extension, review list of required and optional parameters for ```k8s-extension create``` CLI command [here](https://docs.microsoft.com/en-us/cli/azure/k8s-extension?view=azure-cli-latest#az_k8s_extension_create). For AzureML extension deployment configurations, use ```--config``` or ```--config-protected``` to specify list of ```key=value``` pairs. Following is the list of configuration settings available to be used for different AzureML extension deployment scenario ns.
   |Configuration Setting Key Name  |Description  |Training |Inference |Training and Inference
   |--|--|--|--|--|
   |```enableTraining``` |```True``` or ```False```, default ```False```. **Must** be set to ```True``` for AzureML extension deployment with Machine Learning model training support.  |  **&check;**| N/A |  **&check;** |
   | ```enableInference``` |```True``` or ```False```, default ```False```.  **Must** be set to ```True``` for AzureML extension deployment with Machine Learning inference support. |N/A| **&check;** |  **&check;** |
   | ```allowInsecureConnections``` |```True``` or ```False```, default False. This **must** be set to ```True``` for AzureML extension deployment with HTTP endpoints support for inference, when ```sslCertPemFile``` and ```sslKeyPemFile``` are not provided. |N/A| Optional |  Optional |
   | ```inferenceRouterServiceType``` |```loadBalancer```, ```nodePort``` or ```clusterIP```.  **Must** be set for ```enableInference=true```. | N/A| **&check;** |   **&check;** |
   | ```internalLoadBalancerProvider``` | This config is only applicable for Azure Kubernetes Service(AKS) cluster now. **Must** be set to ```azure``` to allow the inference router use internal load balancer.  | N/A| Optional |  Optional |
   |```sslSecret```| The Kubernetes secret name under azureml namespace to store `cert.pem` (PEM-encoded SSL cert) and `key.pem` (PEM-encoded SSL key), required for AzureML extension deployment with HTTPS endpoint support for inference, when  ``allowInsecureConnections`` is set to False. Use this config or give static cert and key file path in configuration protected settings. See sample Kubernetes secret definition YAML [file](../files/sslsecret.yaml). |N/A| Optional |  Optional |
   |```sslCname``` |A SSL CName to use if enabling SSL validation on the cluster.   |  N/A | N/A |  required when using HTTPS endpoint |
   | ```inferenceLoadBalancerHA``` |```True``` or ```False```, default ```True```. By default, AzureML extension will deploy 3 ingress controller replicas for high availability, which requires at least 3 workers in a cluster. Set this to ```False``` if you have fewer than 3 workers and want to deploy AzureML extension for development and testing only, in this case it will deploy one ingress controller replica only. | N/A| Optional |  Optional |
   |```openshift``` | ```True``` or ```False```, default ```False```. Set to ```True``` if you deploy AzureML extension on ARO or OCP cluster. The deployment process will automatically compile a policy package and load policy package on each node so AzureML services operation can function properly.  | Optional| Optional |  Optional |
   |```nodeSelector``` | Set the node selector so the extension components and the training/inference workloads will only be deployed to the nodes with all specified selectors. Usage: `nodeSelector.key=value`, support multiple selectors. Example: `nodeSelector.node-purpose=worker nodeSelector.node-region=eastus`| Optional| Optional |  Optional |
   |```installNvidiaDevicePlugin```  | ```True``` or ```False```, default ```False```. [Nvidia Device Plugin](https://github.com/NVIDIA/k8s-device-plugin#nvidia-device-plugin-for-kubernetes) is required for ML workloads on Nvidia GPU hardware. By default, AzureML extension deployment will not install Nvidia Device Plugin regardless Kubernetes cluster has GPU hardware or not. User can specify this configuration setting to ```True```, so the extension will install Nvidia Device Plugin, but make sure to have [Prerequesities](https://github.com/NVIDIA/k8s-device-plugin#prerequisites) ready beforehand. | Optional |Optional |Optional |
   |```blobCsiDriverEnabled```| ```True``` or ```False```, default ```True```.  Blob CSI driver is required for ML workloads. User can specify this configuration setting to ```False``` if it was installed already. | Optional |Optional |Optional |
   |```reuseExistingPromOp```|```True``` or ```False```, default ```False```. AzureML extension needs prometheus operator to manage prometheus. Set to ```True``` to reuse existing prometheus operator. Compatible [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/README.md) helm chart versions are from 9.3.4 to 30.0.1.| Optional| Optional |  Optional |
 |```volcanoScheduler.enable```| ```True``` or ```False```, default ```True```. AzureML extension needs volcano scheduler to schedule the job. Set to ```False``` to reuse existing volcano scheduler. Supported volcano scheduler versions are 1.4, 1.5. | Optional| N/A |  Optional |
 |```logAnalyticsWS```  |```True``` or ```False```, default ```False```. AzureML extension integrates with Azure LogAnalytics Workspace to provide log viewing and analysis capability through LogAalytics Workspace. This setting must be explicitly set to ```True``` if customer wants to use this capability. LogAnalytics Workspace cost may apply.  |N/A |Optional |Optional |
 |```installDcgmExporter```  |```True``` or ```False```, default ```False```. Dcgm-exporter is used to collect GPU metrics for GPU jobs. Specify ```installDcgmExporter``` flag to ```true``` to enable the build-in dcgm-exporter. But if you want to utilize your own dcgm-exporter, please refer to [DCGM exporter](./troubleshooting.md#dcgm) |Optional |Optional |Optional |

   |Configuration Protected Setting Key Name  |Description  |Training |Inference |Training and Inference
   |--|--|--|--|--|
   | ```sslCertPemFile```, ```sslKeyPemFile``` |Path to SSL certificate and key file (PEM-encoded), required for AzureML extension deployment with HTTPS endpoint support for inference, when  ``allowInsecureConnections`` is set to False. | N/A| Optional |  Optional |


