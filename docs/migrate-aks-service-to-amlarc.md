# Migrate AKS service to AmlArc

We provide two paths for AKS service to [AmlArc](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-attach-arc-kubernetes?tabs=studio#prerequisites) migration.
Both of them are limit to migrations under the **same workspace**.

| | Direct migration| Export & deploy|
|--------| ----------- | ----------- | 
| Support service types | AKS, ACI | AKS, ACI|                     
| Migration target types| AmlArc| AmlArc, MIR|
| Migration target| Same cluster | Any cluster|
| Keep old service| No | Yes|
| Same service name| Yes| Partially support<sup>1</sup>|
| Keep scoring url| Yes | Partially support<sup>2</sup>|

> Notes: 
>1. Export & deploy does not support same name in same cluster.
>2. Deploy to a new cluster will change the ip address.

After decide your migration path, some scripts can help complete the process:
1. `migrate-aks-service.sh` Direct migration in same cluster.
2. `deploy-amlarc.sh` Help install AmlArc extension to your AKS cluster.
3. `export-service.sh` Export services to template and deploy to AmlArc compute.

## Prerequisites
Before export and migrate your service, please check the following prerequisites:
1. A healthy AKS webservice.
2. An AKS cluster, ready for AmlArc to deploy. Check [prerequisites for AmlArc](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-attach-arc-kubernetes?tabs=studio#prerequisites).
3. Python package: azureml-core >= 1.37.0.
4. Cli: azure-cli >= 2.30.0, storage-preview >= 0.7.4, k8s-extension >= 1.0.0.
5. A shell environment (bash is recommended), make sure the VNet connectivity with your cluster, if any.

## Direct migration
Make sure you have read the [docs](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-attach-arc-kubernetes?tabs=studio#deploy-azure-machine-learning-extension)
about AmlArc. Check `migrate-aks-service.sh`, fill in all the parameters, and find the right scenarios under OPTIONS. 
Then migrate your aks service by run:
```bash
./export-service-util
```
> Attention: direct migration is a irreversible process. 

## Export & deploy

### Install AmlArc extension on an AKS cluster
Make sure you have read the [docs](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-attach-arc-kubernetes?tabs=studio#deploy-azure-machine-learning-extension)
about AmlArc, and understand your using scenarios also the corresponding [network requirements](https://github.com/Azure/AML-Kubernetes/blob/master/docs/network-requirements.md).
* Scene1: Secure connection through [private link AML Workspace](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-attach-arc-kubernetes?tabs=studio#deploy-azure-machine-learning-extension).
* Scene2: Cluster is behind an [outbound proxy](https://docs.microsoft.com/en-us/azure/azure-arc/kubernetes/quickstart-connect-cluster?tabs=azure-cli#4a-connect-using-an-outbound-proxy-server).

Check `deploy-amlarc.sh`, fill in all the parameters, and find the right scenarios under step2. 
Then install AmlArc extension by run:
```bash
./deploy-amlarc.sh
```

The script will register feature provider for your sub, and install extension into your cluster.

### Export and deploy AKS service to AmlArc compute
The `export-service.sh` will run following steps:
1. Attach your AmlArc deployed AKS cluster as compute target to Workspace.
2. Export AKS/ACI services as template and upload to your storage.
3. Download template and modify parameters.
4. Deploy to AmlArc compute as online-endpoint and online-deployment service.
> Attention:
> - Old services will be kept after a successful export and deployment.
> - You can set online-endpoint name to the same with old service, but DO NOT deploy to the same cluster, a direct migration is recommended for this scenario.

Check `export-service.sh`, fill in all your parameters, then export and deploy to your cluster by run:
>./export-service.sh

If you want to export and deploy multiple services, the steps before STEP2 in the script is a one-time procedure.
After a successful deployment, you can check the online-endpoint and online-deployment through portal or [AzuremlCli](https://docs.microsoft.com/en-us/azure/machine-learning/reference-azure-machine-learning-cli).