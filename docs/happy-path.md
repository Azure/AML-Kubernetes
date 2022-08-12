# Installation Instructions
AzureML extension can be easily installed with a single ```az k8s-extension create``` command. But according to your needs and deployment scenarios, different parameters and pre-checkings should be paid attention to, like K8s distro, cluster resources, networking, security, storage and AML features. 

For a quick try scenario, please try the following two happy paths with [Minikube](#install-with-minikube) and [AKS](#install-with-aks) clusters respectively. For special production needs, please refer to [doc](./deploy-extension.md). For any errors or failures, please refer to [TroubleShooting](./troubleshooting.md).

* [Install with Minikube](#install-with-minikube)
* [Install with AKS](#install-with-aks)
* [TroubleShooting](./troubleshooting.md)

## Install with Minikube
Assuming that you have a local K8s cluster created by [Minikube](https://minikube.sigs.k8s.io/docs/start/) and have [kubectl](https://kubernetes.io/docs/tasks/tools/) , [helm](https://helm.sh/docs/intro/install/) and [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) tools installed. **<span style="color:orange">Check and make sure your cluster have at least 4 vCPU cores and 8GB memory**</span> by running ```kubectl describe node```, because ARC agents and AzureML extension agents needs around 2 vCPU cores and 3GB memory to run. **<span style="color:orange">This example mainly shows how to install AzureML extension with limited resources for test purpose**</span>.

### 1. Connect your cluster to Azure by Arc
On-prem cluster needs to be connected to Azure before it can use AzureML service. Run the command below to connect your cluster. For detailed usage and troubleshooting of ARC, please refer to [Azure Arc-enabled Kubernetes](https://docs.microsoft.com/en-us/azure/azure-arc/kubernetes/overview)

```azurecli
az connectedk8s connect --subscription <subscription-id> --resource-group <resource-group> --location <location> --name <arc-cluster-name>
```

After the connection, a ```Kubernetes - Azure Arc``` will be created under your resource group. Click the Arc cluster and makr sure its status is healthy from Azure portal. You can also confirm Arc agents status from your cluster by running ```kubectl get pod -n azure-arc``` and all pods should be in ```Running``` status.
### 2. Install AzureML extension
Run ```az extension add -n k8s-extension``` to add ```k8s-extension``` in Azure CLI, then run the following command to install AzureML extension on the Arc cluster created in previous step.

```azurecli
az k8s-extension create --subscription <subscription-id> --resource-group <resource-group> --cluster-type connectedClusters --cluster-name <arc-cluster-name> --extension-type Microsoft.AzureML.Kubernetes --name arcml-extension --scope cluster --config enableTraining=True enableInference=True allowInsecureConnections=True inferenceRouterHA=False inferenceRouterServiceType=clusterIP
```
* ```--cluster-name``` : Name of Arc-connected cluster. Azure can't directly perceive and operate your on-prem cluster and it can only operate your cluster through Arc, so cluster name is your Arc-connected cluster name.
* ```--cluster-type``` : "connectedClusters" means it's a Arc-connected cluster.
* ```--extension-type``` : Arc enables many types of extension. For AzureML extension, the extension type is ```Microsoft.AzureML.Kubernetes```.
* ```--name``` : Name of AzureML extension instance. From the extension option in the Arc cluster portal, you can find your extension instance. You can also confirm extension instance by running ```helm list -Aa``` in your local cluster.
* ```--scope``` : cluster
* ```--config or --configuration-settings``` : Used to set parameters for extension. Here we set 5 flags.
  * ```enableTraining``` : Enable training feature.
  * ```enableInference``` : Enable inference feature.
  * ```allowInsecureConnections``` : For inference feature, the http endpoints of model deployment are exposed for scoring. Explicitly setting this flag to true allows insecure connection to those http endpoints. Otherwise, ```sslCertPemFile``` and ```sslKeyPemFile``` must be provided for secure connections.
  * ```inferenceRouterHA``` : <span style="color:red">THIS FLAG IS VERY IMPORTANT!</span> To ensure the availability of inference scoring services, HA feature is enabled by default. But it requires at least 3 nodes to do so. Disable HA can make you successfully install AzureML extension.
  * ```inferenceRouterServiceType``` : <span style="color:red">THIS FLAG IS VERY IMPORTANT!</span> By default, inference will use public loadbalancer to expose scoring services. But loadbalancer is not supported by most non-cloud provided K8s. Setting this flag to clusterIP makes scoring services exposed as a ```clusterIP``` service.

### 3. Check extension status and debug
After the installation, you can check the extension status from Arc cluster portal. In the left navigation sidebar of Arc cluster portal, there is a Extensions option. You can also directly check extension instance by running ```helm list -Aa``` or ```kubectl get pod -n azureml``` in your local cluster.

## Install with AKS
Assuming you already have a AKS with **<span style="color:orange">at least 3 nodes**</span> and have the AKS kubeconfig prepared. If you have less than 3 nodes, please follow [Install with Minikube](#install-with-minikube) to continue your installation.**<span style="color:orange">This example mainly shows how to install AzureML extension with formal functionality for POC purpose**</span>.

AKS is an Azure resources and managed by Azure. And we have two ways to install AzureML extension in AKS: "directly install" or "connect first then install".

* Directly install in AKS
  * Run the follow command
      ```azurecli
      az k8s-extension create --subscription <subscription-id> --resource-group <resource-group> --cluster-type managedClusters --cluster-name <AKS-cluster-name> --extension-type Microsoft.AzureML.Kubernetes --name arcml-extension --scope cluster --config enableTraining=True enableInference=True allowInsecureConnections=True inferenceRouterServiceType=loadBalancer
      ```
    * ```--cluster-name```: Name of your **<span style="color:orange">AKS cluster**</span>.
    * ```--cluster-type```: Extension is installed in AKS directly, so the cluster type is **<span style="color:orange">managedClusters**</span>, not **<span style="color:orange">connectedClusters**</span>.
    * ```--config```: Enable both training and inference features and allow insecure connections.
* Install through Arc. **This way treats AKS as an on-prem cluster and is very similar to the Minikube way, except that you don't have extra parameters to handle resource limitation**.
  1. Connect AKS with command below
      ```azurecli
      az connectedk8s connect --subscription <subscription-id> --resource-group <resource-group> --location <location> --name <arc-cluster-name>
      ```
  2. Then install extension
      ```azurecli
      az k8s-extension create --subscription <subscription-id> --resource-group <resource-group> --cluster-type connectedClusters  --cluster-name <arc-cluster-name> --extension-type Microsoft.AzureML.Kubernetes  --name arcml-extension --scope cluster --config enableTraining=True enableInference=True allowInsecureConnections=True inferenceRouterServiceType=loadBalancer
      ```
     * ```--cluster-name```: Name of your **<span style="color:orange">Arc cluster**</span>.
     * ```--cluster-type```: Extension is installed through Arc cluster, so the cluster type is **<span style="color:orange">connectedClusters**</span>.
     * ```--config```: Enable both training and inference features and allow insecure connections.

   > Note: Don't confuse these two ways, and **don't try both ways on the same cluster**. For example, you first install extension directly in a AKS, and then uninstall the extension. After that, you want to connect the same AKS to Arc and install extension. There is a high probability that your operation will fail.