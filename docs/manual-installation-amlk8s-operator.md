1. Install [Helm](https://helm.sh/docs/helm/helm_install) on your local machine
2. Connect to your Kubernetes cluster and run the following commands (*Saurya to verify*)

```cli
SET HELM_EXPERIMENTAL_OCI=1
helm chart remove vineetgamlarc.azurecr.io/azure-ml-k8s/install-job:1.0.0
helm chart pull vineetgamlarc.azurecr.io/azure-ml-k8s/install-job:1.0.0
helm chart export vineetgamlarc.azurecr.io/azure-ml-k8s/install-job:1.0.0 --destination ./install
cd install
helm show chart amlk8s-extension
helm install aml-compute ./amlk8s-extension -n azureml --set  relayConnectionString="Endpoint=sb://adramak8sworkspace963585242.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=U7S2h3/WSv2HRj/LHyMlnaaLs2D0xPheSWiaIJMmUR4=;EntityPath=connection_0"
```
