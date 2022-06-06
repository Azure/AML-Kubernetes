# Deploy AzureML extension on OpenShift Container Platform

Azure Arc enabled ML supports both Azure RedHat OpenShift Service (ARO) and OpenShift Container Platform (OCP).

## Prerequisites

An ARO or OCP Kubernetes cluster is up and running. 

   * To setup ARO Kubernetes cluster on Azure, please follow instruction [here](https://docs.microsoft.com/azure/openshift/tutorial-create-cluster)
   * to setup OCP Kubernetes clsuter, please follow instructure on [RedHat website](https://docs.openshift.com/container-platform/4.6/installing/installing_platform_agnostic/installing-platform-agnostic.html).

## Disable Security Enhanced Linux (SELinux) 

[AzureML dataset](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-train-with-datasets), usually used in ML training jobs, is not supported on machines with SELinux enabled. Therefore, to use AzureML dataset, please make sure `selinux` is disabled on workers for AzureML usage. 

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
