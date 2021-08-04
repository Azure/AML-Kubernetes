# Deploy AzureML extension on OpenShift Container Platform

Azure Arc enabled ML supports both Azure RedHat OpenShift Service (ARO) and OpenShift Container Platform (OCP).

## Prerequisites

1. An ARO or OCP Kubernetes cluster is up and running. 

   * To setup ARO Kubernetes cluster on Azure, please follow instruction [here](https://docs.microsoft.com/azure/openshift/tutorial-create-cluster)
   * to setup OCP Kubernetes clsuter, please follow instructure on [RedHat website](https://docs.openshift.com/container-platform/4.6/installing/installing_platform_agnostic/installing-platform-agnostic.html).

1. Ensure you have cluster admin privilege and you have kubeconfig access from where you run Azure CLI command.
1. Grant privileged access to AzureML service accounts, run $oc edit scc privileged, add following service accounts under users:

   * ```system:serviceaccount:azure-arc:azure-arc-kube-aad-proxy-sa```
   * ```system:serviceaccount:azureml:{extension-name}-kube-state-metrics```
   * ```system:serviceaccount:azureml:cluster-status-reporter```
   * ```system:serviceaccount:azureml:prom-admission```
   * ```system:serviceaccount:azureml:default```
   * ```system:serviceaccount:azureml:prom-operator```
   * ```system:serviceaccount:azureml:csi-blob-node-sa```
   * ```system:serviceaccount:azureml:csi-blob-controller-sa```
   * ```system:serviceaccount:azureml:load-amlarc-selinux-policy-sa```
   * ```system:serviceaccount:azureml:azureml-fe```

## Deploy AzureML extension

To Deploy AzureML extension on ARO or OCP, you would need to specify one additional config setting ```OpenShift=True``` in addition to regular configuration settings for normal AzureML extension deployment. Following command will deploy AzureML extension to ARO or OCP and enable Kubernetes cluster for training workload.

   ```azurecli
   az k8s-extension create --name amlarc-compute --extension-type Microsoft.AzureML.Kubernetes --configuration-settings enableTraining=True OpenShift=True  --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <resource-group> --scope cluster
   ```