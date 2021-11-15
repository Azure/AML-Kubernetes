# Deploy AzureML extension to your Kubernetes cluster

With a simple AzureML extension deployment an AKS cluster or any Azure Arc enabled Kuberntes cluter, you can instantly onboard data science professionals to submit ML workload to the Kubernetes clusters by using existing Azure ML tools and service capabilities. You can deploy AzureML extension and enables Kuberntes cluster for following machine learning needs:
* Deploy AzureML extension for model training and batch inference
* Deploy AzureML extension for real-time inferencing only
* Deploy AzureML extension for both model training and inferencing

Upon AzureML extension deployment completes, it will create following resources in Azure cloud and in Kubernetes cluster, depending on each AzureML extension deployment scenario:
   |Resource name  |Resource type |Training |Inference |Training and Inference|
   |--|--|--|--|--|
   |Azure ServiceBus|Azure resource|**&check;**|**&check;**|**&check;**|
   |Azure Relay|Azure resource|**&check;**|**&check;**|**&check;**|
   |{EXTENSION-NAME}|Azure resource|**&check;**|**&check;**|**&check;**|
   |aml-operator|Kubernetes deployment|**&check;**|N/A|**&check;**|
   |{EXTENSION-NAME}-kube-state-metrics|Kubernetes deployment|**&check;**|**&check;**|**&check;**|
   |{EXTENSION-NAME}-prometheus-operator|Kubernetes deployment|**&check;**|**&check;**|**&check;**|
   |amlarc-identity-controller|Kubernetes deployment|N/A|**&check;**|**&check;**|
   |amlarc-identity-proxy|Kubernetes deployment|N/A|**&check;**|**&check;**|
   |azureml-fe|Kubernetes deployment|N/A|**&check;**|**&check;**|
   |inference-operator-controller-manager|Kubernetes deployment|N/A|**&check;**|**&check;**|
   |metrics-controller-manager|Kubernetes deployment|**&check;**|**&check;**|**&check;**|
   |relayserver|Kubernetes deployment|**&check;**|**&check;**|**&check;**|
   |cluster-status-reporter|Kubernetes deployment|**&check;**|**&check;**|**&check;**|
   |nfd-master|Kubernetes deployment|**&check;**|N/A|**&check;**|
   |gateway|Kubernetes deployment|**&check;**|**&check;**|**&check;**|
   |csi-blob-controller|Kubernetes deployment|**&check;**|N/A|**&check;**|
   |csi-blob-node|Kubernetes daemonset|**&check;**|N/A|**&check;**|
   |fluent-bit|Kubernetes daemonset|**&check;**|**&check;**|**&check;**|
   |k8s-host-device-plugin-daemonset|Kubernetes daemonset|**&check;**|**&check;**|**&check;**|
   |nfd-worker|Kubernetes daemonset|**&check;**|N/A|**&check;**|
   |prometheus-prom-prometheus|Kubernetes statefulset|**&check;**|**&check;**|**&check;**|
   |frameworkcontroller|Kubernetes statefulset|**&check;**|N/A|**&check;**|

> **<span style="color:orange">Important**:</span> 
   > * Azure ServiceBus and Azure Relay resources  are under the same resource group as the Arc cluster resource. These resources are used to communicate with the Kubernetes cluster and modifying them will break attached compute targets.


> **<span stype="color:orane">Notes**:</span>
   > * **{EXTENSION-NAME}:** This is the extension name specified with ```az k8s-extension create --name``` CLI command. 

## Review AzureML deployment configuration settings

Use ```k8s-extension create``` CLI command to deploy AzureML extension, review list of required and optional parameters for ```k8s-extension create``` CLI command [here](https://docs.microsoft.com/en-us/cli/azure/k8s-extension?view=azure-cli-latest#az_k8s_extension_create). 

For AzureML extension deployment/update configurations, use ```--config``` or ```--config-protected``` to specify list of ```key=value``` pairs. Following is the list of configuration settings available to be used for different AzureML extension deployment/update scenarions.
   |Configuration Setting Key Name  |Description  |Training |Inference |Training and Inference
   |--|--|--|--|--|
   |```enableTraining``` |```True``` or ```False```, default ```False```. **Must** be set to ```True``` for AzureML extension deployment with Machine Learning model training support.  |  **&check;**| N/A |  **&check;** |
   |```logAnalyticsWS```  |```True``` or ```False```, default ```False```. AzureML extension integrates with Azure LogAnalytics Workspace to provide log viewing and analysis capability through LogAalytics Workspace. This setting must be explicitly set to ```True``` if customer wants to leverage this capability. LogAnalytics Workspace cost may apply.  |Optional |Optional |Optional |
   |```installNvidiaDevicePlugin```  | ```True``` or ```False```, default ```True```. Nvidia Device Plugin is required for ML workloads on Nvidia GPU hardware. By default, AzureML extension deployment will install Nvidia Device Plugin regardless Kubernetes cluster has GPU hardware or not. User can specify this configuration setting to False if Nvidia Device Plugin installation is not required (either it is installed already or there is no plan to use GPU for workload). | Optional |Optional |Optional |
   | ```enableInference``` |```True``` or ```False```, default ```False```.  **Must** be set to ```True``` for AzureML extension deployment with Machine Learning inference support. |N/A| **&check;** |  **&check;** |
   | ```allowInsecureConnections``` |```True``` or ```False```, default False. This **must** be set to ```True``` for AzureML extension deployment with HTTP endpoints support for inference, when ```sslCertPemFile``` and ```sslKeyPemFile``` are not provided. |N/A| Optional |  Optional |
   | ```privateEndpointNodeport``` |```True``` or ```False```, default ```False```.  **Must** be set to ```True``` for AzureML deployment with Machine Learning inference private endpoints support using serviceType nodePort. | N/A| Optional |  Optional |
   | ```privateEndpointILB``` |```True``` or ```False```, default ```False```.  **Must** be set to ```True``` for AzureML extension deployment with Machine Learning inference private endpoints support using serviceType internal load balancer | N/A| Optional |  Optional |
   | ```inferenceLoadBalancerHA``` |```True``` or ```False```, default ```True```. By default, AzureML extension will deploy multiple ingress controller replicas for high availability. Set this to ```False``` if you have limited cluster resource and want to deploy AzureML extension for development and testing only, in this case it will deploy one ingress controller replica only. | N/A| Optional |  Optional |
   |```openshift``` | ```True``` or ```False```, default ```False```. Set to ```True``` if you deploy AzureML extension on ARO or OCP cluster.The deployment process will automatically compile a policy package and load policy package on each node so AzureML services operation can function properly.  | Optional| Optional |  Optional |
   |```nodeSelector``` | Set the node selector to match so that the extension component and the training/inference workloads will only be deployed to the nodes with those selector. Usage: `nodeSelector.key=value`, support multiple selectors. Example: `nodeSelector.node-purpose=worker`| Optional| Optional |  Optional |

   |Configuration Protected Setting Key Name  |Description  |Training |Inference |Training and Inference
   |--|--|--|--|--|
   | ```sslCertPemFile```, ```sslKeyPemFile``` |Path to SSL certificate and key file (PEM-encoded), required for AzureML extension deployment with HTTPS endpoint support for inference. | N/A| Optional |  Optional |

### Extension update

Use ```k8s-extension update``` CLI command to update the mutable properties of  AzureML extension, review list of required and optional parameters for ```k8s-extension update``` CLI command [here](https://docs.microsoft.com/en-us/cli/azure/k8s-extension?view=azure-cli-latest#az_k8s_extension_update). 

1.	Azure Arc supports update of  ``--auto-upgrade-minor-version``, ``--version``,  ``--configuration-settings``, ``--configuration-protected-settings``.  
2.	For configurationSettings, only the settings that require update need to be provided. If the user provides all settings, they would be merged/overwritten with the provided values. 
3.	For ConfigurationProtectedSettings, ALL  settings should to be provided. If some settings are omitted, those settings would be considered obsolete and deleted. 

> **<span style="color:orange">Important**:</span>
> 
> * DO NOT update following configs if you have active training workloads, otherwise, the training jobs will be crashed.
> * * `enableTraining` from `True` to `False`
> * * `installNvidiaDevicePlugin` from `True` to `False` if GPU is used.
> * * narrow down `nodeSelector`
> * DO NOT update following configs if you have active real-time inference endpoints, otherwise, the endpoints will be crashed.
> * * `enableTInference` from `True` to `False`
> * * `installNvidiaDevicePlugin` from `True` to `False` if GPU is used.
> * * narrow down `nodeSelector`
> * * `allowInsecureConnections`,`privateEndpointNodeport`,`privateEndpointILB`
> *  To update `logAnalyticsWS` from `True` to `False`, please provide all configurationProtectedSettings. Otherwise, those settings would be considered obsolete and deleted .

## Prerequesites 

-  For AzureML extension deployment on ARO or OCP cluster, please grant privileged access to AzureML service accounts, run ```oc edit scc privileged``` command, and add following service accounts under "users:":

   * ```system:serviceaccount:azure-arc:azure-arc-kube-aad-proxy-sa```
   * ```system:serviceaccount:azureml:{EXTENSION-NAME}-kube-state-metrics``` 
   * ```system:serviceaccount:azureml:cluster-status-reporter```
   * ```system:serviceaccount:azureml:prom-admission```
   * ```system:serviceaccount:azureml:default```
   * ```system:serviceaccount:azureml:prom-operator```
   * ```system:serviceaccount:azureml:csi-blob-node-sa```
   * ```system:serviceaccount:azureml:csi-blob-controller-sa```
   * ```system:serviceaccount:azureml:load-amlarc-selinux-policy-sa```
   * ```system:serviceaccount:azureml:azureml-fe```
   * ```system:serviceaccount:azureml:prom-prometheus```
   > **<span stype="color:yellow">Notes</span>**
      >* **{EXTENSION-NAME}:** is the extension name specified with ```az k8s-extension create --name``` CLI command. 

-  Login to Azure

   ```azurecli
   az login
   az account set --subscription <your-subscription-id>
   ```

## Deploy AzureML extension for model training or batch inference workload

Following CLI command will deploy AzureML extension and enable Kubernetes cluster for model training and batch inference workload:
   ```azurecli
   az k8s-extension create --name arcml-extension --extension-type Microsoft.AzureML.Kubernetes --config enableTraining=True  --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <resource-group> --scope cluster
   ```
> **<span stype="color:orane">Notes**:</span>
   > * **If you deploy AzureML extension on AKS directly without Azure Arc connection, please change ```--cluster-type``` parameter value to ```managedClusters```**

## Deploy AzureML extension for real-time inference workload only

Depending your network setup, Kubernetes distribution variant, and where your Kubernetes cluster is hosted (in cloud or on-premises), you can choose one of following options to deploy AzureML extension.

> **<span stype="color:orane">Notes**:</span>
   > * **If you deploy AzureML extension on AKS directly without Azure Arc connection, please change ```--cluster-type``` parameter value to ```managedClusters```**

   * **Public HTTPS endpoints support with public load balancer**

      ```azurecli
      az k8s-extension create --name arcml-extension --extension-type Microsoft.AzureML.Kubernetes --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --config enableInference=True --config-protected sslCertPemFile=<path-to-the-SSL-cert-PEM-ile> sslKeyPemFile=<path-to-the-SSL-key-PEM-file> --resource-group <resource-group> --scope cluster
      ```
   * **Private HTTPS endpoints support with internal load balancer**   
      ```azurecli
      az k8s-extension create --name amlarc-compute --extension-type Microsoft.AzureML.Kubernetes --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --config enableInference=True privateEndpointILB=True --config-protected sslCertPemFile=<path-to-the-SSL-cert-PEM-ile> sslKeyPemFile=<path-to-the-SSL-key-PEM-file> --resource-group <resource-group> --scope cluster
      ```
   * **Private HTTPS endppoints support with NodePort**
      ```azurecli
      az k8s-extension create --name arcml-extension --extension-type Microsoft.AzureML.Kubernetes --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <resource-group> --scope cluster --config enableInference=True privateEndpointNodeport=True --config-protected sslCertPemFile=<path-to-the-SSL-cert-PEM-ile> sslKeyPemFile=<path-to-the-SSL-key-PEM-file>
      ```  
     > **Note:**
     * Using a NodePort gives you the freedom to set up your own load balancing solution, to configure environments that are not fully supported by Kubernetes, or even to expose one or more nodes' IPs directly.
     * When you deploy with NodePort service, the scoring url (or swagger url) will be responsed with one of Node IP (e.g. ```http://<NodeIP><NodePort>/<scoring_path>```) and remain unchanged even if the Node is unavailable. But you can replace it with any other Node IP.
   * **Private HTTP endpoints support with internal load balancer**   
      ```azurecli
      az k8s-extension create --name arcml-extension --extension-type Microsoft.AzureML.Kubernetes --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --config enableInference=True privateEndpointILB=True allowInsecureConnections=True --resource-group <resource-group> --scope cluster
      ```
   * **Private HTTP endppoints support with NodePort**
      ```azurecli
      az k8s-extension create --name arcml-extension --extension-type Microsoft.AzureML.Kubernetes --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --config enableInference=True privateEndpointNodeport=True allowInsecureConnections=Ture --resource-group <resource-group> --scope cluster
      ```
   * **Public HTTP endpoints support with public load balancer - the least secure way, NOT recommended**
      ```azurecli
      az k8s-extension create --name arcml-extension --extension-type Microsoft.AzureML.Kubernetes --cluster-type connectedClusters --cluster-name <your-connected-cluster-name>  --config enableInference=True allowInsecureConnections=True --resource-group <resource-group> --scope cluster
      ```
## Deploy AzureML extension for training, batch inference, and real-time inference workload

To enable Kubernetes cluster for all kinds of ML workload, choose one of above inference deployment options and append config settings for training and batch inference. Following CLI command will enable cluster with real-time inference HTTPS endpoints support, training, and batch inference workload:
   ```azurecli
   az k8s-extension create --name arcml-extension --extension-type Microsoft.AzureML.Kubernetes --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --config enableTraining=True enableInference=True --config-protected sslCertPemFile=<path-to-the-SSL-cert-PEM-ile> sslKeyPemFile=<path-to-the-SSL-key-PEM-file> --resource-group <resource-group> --scope cluster
   ```

> **<span stype="color:orane">Notes**:</span>
   > * **If you deploy AzureML extension on AKS directly without Azure Arc connection, please change ```--cluster-type``` parameter value to ```managedClusters```**

## Verify your AzureML extension deployment

1. Run the following CLI command to check AzureML extension details:

   ```azurecli
   az k8s-extension show --name arcml-extension --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <resource-group>
   ```

1. In the response, look for "extensionType": "arcml-extension" and "provisioningState": "Succeeded". Note it might show "provisioningState": "Pending" for the first few minutes.

1. If the provisioningState shows Succeeded, run the following command on your machine with the kubeconfig file pointed to your cluster to check that all pods under "azureml" namespace are in 'Running' state:

   ```bash
    kubectl get pods -n azureml
   ```
