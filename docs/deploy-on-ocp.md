# Deploy AzureML extension on OpenShift Container Platform

Azure Arc enabled ML supports both Azure RedHat OpenShift Service (ARO) and OpenShift Container Platform (OCP).

## Prerequisites

An ARO or OCP Kubernetes cluster is up and running. 

   * To setup ARO Kubernetes cluster on Azure, please follow instruction [here](https://docs.microsoft.com/azure/openshift/tutorial-create-cluster)
   * to setup OCP Kubernetes clsuter, please follow instructure on [RedHat website](https://docs.openshift.com/container-platform/4.6/installing/installing_platform_agnostic/installing-platform-agnostic.html).

## Deploy AzureML extension

To Deploy AzureML extension on ARO or OCP, you would need to specify one additional config setting ```openshift=True``` in addition to regular configuration settings for normal AzureML extension deployment. Following command will deploy AzureML extension to ARO or OCP and enable Kubernetes cluster for training workload.

   ```azurecli
   az k8s-extension create --name amlarc-compute --extension-type Microsoft.AzureML.Kubernetes --configuration-settings enableTraining=True openshift=True  --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <resource-group> --scope cluster
   ```
## Disable Security Enhanced Linux (SELinux) 

[AzureML dataset](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-train-with-datasets), usually used in ML training jobs, is not supported on machines with SELinux enabled. Therefore, to use AzureML dataset, please make sure `selinux` is disabled on workers running ML workloads, otherwise you may encounter `failed to start container` error. If your cluster is only used for real-time inference, SELinux will not cause a problem.

## Privileged setup for ARO and OCP

For AzureML extension deployment on ARO or OCP cluster, grant privileged access to AzureML service accounts, run ```oc edit scc privileged``` command, and add following service accounts under "users:":

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
   * ```system:serviceaccount:{KUBERNETES-COMPUTE-NAMESPACE}:default```
   * ```system:serviceaccount:azureml:azureml-ingress-nginx```
   * ```system:serviceaccount:azureml:azureml-ingress-nginx-admission```
   > **<span stype="color:yellow">Notes</span>**
      >* **{EXTENSION-NAME}:** is the extension name specified with ```az k8s-extension create --name``` CLI command. 
      >* **{KUBERNETES-COMPUTE-NAMESPACE}:** is the namespace of kubernetes compute specified with ```az ml compute attach --namespace``` CLI command. Skip configuring 'system:serviceaccount:{KUBERNETES-COMPUTE-NAMESPACE}:default' if no namespace specified with ```az ml compute attach ``` CLI command.
