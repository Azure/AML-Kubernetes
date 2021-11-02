# Setup Azure Arc-enabled Machine Learning Training and Inferencing on AKS on Azure Stack HCI

In this article, you will:

*	Connect your AKS on Azure Stack HCI cluster to Azure Via Azure Arc
*	Install AzureML Arc extension on your AKS on Azure Stack HCI (AKS-HCI) cluster
*	Attach your Azure Arc-enabled AKS on Azure Stack HCI's cluster to your Azure Machine Learning Workspace as a Compute Target

## Prerequisites

Before you begin, please make sure that you have the following items available:

* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/en-us/free/) before you begin.
* An AKS on Azure Stack HCI cluster with **only Linux worker nodes (no Windows worker nodes)**. **Your nodes must have a minimum of 4 vCPU cores and 8GB memory, around 2 vCPU cores and 3GB memory would be used by Arc and AzureML extension components** that we will be installed as part of this tutorial. If you don't have an AKS on Azure Stack HCI cluster, you can follow [the official documentation here](https://docs.microsoft.com/en-us/azure-stack/aks-hci/kubernetes-walkthrough-powershell) to create one on your Azure Stack HCI hardware. Alternatively, you can follow [AKS on Azure Stack HCI Evaluation guide](https://github.com/Azure/aks-hci/tree/main/eval) to create a cluster on an Azure VM with only a couple of commands (This should only be used for proof of concept, please use [the official documentation](https://docs.microsoft.com/en-us/azure-stack/aks-hci/kubernetes-walkthrough-powershell) and hardware for production workloads).
* An Azure Machine Learning (AzureML or AML) Workspace deployed as part of your subscription. You can [create an AML workspace](https://docs.microsoft.com/azure/machine-learning/how-to-manage-workspace?tabs=python) if you don't already have one. If you are using the AML Python SDK to create your workspace, please make sure it has a version>= **1.30**. We strongly recommend learning more about [the inner-workings and concepts in Azure Machine Learning](https://docs.microsoft.com/en-us/azure/machine-learning/concept-azure-machine-learning-architecture) before continuing with the rest of this article (optional).

## Connect your AKS on Azure Stack HCI Cluster to Azure Via Azure Arc

Your AKS on Azure Stack HCI (AKS-HCI) cluster needs Azure Resource Manager representation to be able to take advantage of AzureML training and Inferencing Arc extensions. 
You can connect your cluster to Azure using Azure Arc. Clusters are attached to standard Azure subscriptions, are located in a resource group, and can receive tags just like any other Azure resource. Also, the Azure Arc-enabled Kubernetes representation allows for extending the following capabilities on to your Kubernetes cluster beyond AzureML capabilities being discussed as part of this document:

* Management services - Configurations (GitOps), Azure Monitor for containers, Azure Policy (Gatekeeper)
* Data Services - SQL Managed Instance, PostgreSQL Hyperscale
* Application services - App Service, Functions, Event Grid, Logic Apps, API Management

To connect a Kubernetes cluster to Azure, the cluster administrator needs to deploy a couple of Arc agents. The agents are responsible for connectivity to Azure, collecting Azure Arc logs and metrics, and enabling the above-mentioned scenarios on the cluster. These agents run in a Kubernetes namespace named azure-arc and are standard Kubernetes deployments. You can follow [Connect an Azure Kubernetes Service on Azure Stack HCI cluster to Azure Arc-enabled Kubernetes](https://docs.microsoft.com/en-us/azure-stack/aks-hci/connect-to-arc) to connect your cluster to Azure. 

## Install AzureML Arc Extension on your AKS on Azure Stack HCI cluster

Now that you have an Arc-enabled cluster, you can install Arc extensions onto your cluster and expand its capabilities using the available extensions. To learn more about available Azure Arc extensions please visit [Deploy and manage Azure Arc-enabled Kubernetes cluster extensions](https://docs.microsoft.com/en-us/azure/azure-arc/kubernetes/extensions).

To enable managed ML training and inferencing on your Arc-enabled AKS-HCI cluster, you will need to install AzureML Arc extension using Azure Arc `k8s-extension` CLI. Before installation, please make sure your Arc-enabled AKS-HCI cluster meets AzureML Arc [extension prerequisites](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-attach-arc-kubernetes#prerequisites) and [networking requirements](../network-requirements.md).


<!--- Please follow the following steps to prepare your cluster for extension installation: -->

<!--- 
2. If your AKS-HCI cluster has a mix of Windows and Linux worker nodes please [taint](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) your all of your cluster's windows worker nodes using the following `kubectl` command. Since all of AzureML's extension constructs require Linux worker nodes, this makes sure that the constructs do not get scheduled onto your Windows worker nodes and fail. Please review [Adapt apps for mixed-OS Kubernetes clusters using node selectors or taints and tolerations](https://docs.microsoft.com/en-us/azure-stack/aks-hci/adapt-apps-mixed-os-clusters) to learn more about running ways to adapt applications for AKS-HCI mixed-OS environment.

    ```
    kubectl taint nodes <name-of-your-windows-nodes> node.kubernetes.io/os=windows:NoSchedule
    ```
-->

You can use the below command to install AzureML extension onto your cluster:

```
az k8s-extension create --name <extension-name> --extension-type Microsoft.AzureML.Kubernetes --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <resource-group> --configuration-settings enableTraining=True
```

**Please note that the parameters you pass as part of `--configuration-settings` in the command above will decide what ML capabilities are enabled as part of the installation. For example, the above command enables AzureML Training on your AKS-HCI cluster. If you want to enable both training and HTTP endpoint inferencing, you can use the below command for installation:**

```
az k8s-extension create --name <extension-name> --extension-type Microsoft.AzureML.Kubernetes --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <resource-group> --scope cluster --configuration-settings enableTraining=True enableInference=True allowInsecureConnections=True
```

You can find a list of available `--configuration-settings` here: [Training Configurations](../deploy-extension.md#deploy-azureml-extension-for-model-training), [Inferencing Configurations](https://github.com/Azure/amlarc-preview/blob/main/docs/deploy-extension.md#review-azureml-extension-deployment-configuration-settings)

## Attach your Azure Arc-enabled Cluster to your Azure Machine Learning Workspace as a Compute Target

If you do not already have an Azure Machine learning workspace in your desired Azure resource group, please [create your Machine learning workspace](https://docs.microsoft.com/en-us/azure/machine-learning/concept-workspace#-create-a-workspace).

Follow the steps mentioned in [Attach Arc cluster to AzureML Workspace](../attach-compute.md) to connect your Arc-enabled AKS on Azure Stack HCI cluster to Azure Machine Learning.

## Next Steps

* Learn how to [Setup NFS Server on Azure Stack HCI and Use your Data and run managed Machine Learning Experiments On-Premises](Train-AzureArc.md).
* Experiment with ArcML on AKS on Azure Stack HCI using [Interactive Python Notebooks and AzureML CLI V2 Sample Examples](../AKS-HCI#sample-notebooks).
