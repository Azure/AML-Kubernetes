1. Install [Helm](https://helm.sh/docs/helm/helm_install) on your local machine
1. Connect to your Kubernetes cluster 


1. Install required Helm charts from a public repo
```cli
export SET HELM_EXPERIMENTAL_OCI=1
helm chart remove vineetgamlarc.azurecr.io/azure-ml-k8s/install-job:1.0.0
helm chart pull vineetgamlarc.azurecr.io/azure-ml-k8s/install-job:1.0.0
helm chart export vineetgamlarc.azurecr.io/azure-ml-k8s/install-job:1.0.0 --destination ./install
cd install
```

4. View chart details
```
helm show chart amlk8s-extension
~/Downloads/install $ helm show chart amlk8s-extension
apiVersion: v2
appVersion: 1.16.0
description: Azure Machine Learning Arc Extension for K8s
name: amlk8s-extension
type: application
version: 1.0.0
```

5. Create azureml namespace

`kubectl create ns azureml`

6. Install amlk8s agent/operator
```
helm install aml-compute ./amlk8s-extension -n azureml --set  relayConnectionString="Endpoint=sb://adramak8sworkspace963585242.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=U7S2h3/WSv2HRj/LHyMlnaaLs2D0xPheSWiaIJMmUR4=;EntityPath=connection_0"
```
