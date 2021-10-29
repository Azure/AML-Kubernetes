# Setup Azure Arc-enabled Machine Learning Training and Inferencing on AKS on Azure Stack HCI

In this article, you will:

*	Connect your AKS on Azure Stack HCI Cluster to Azure Via Azure Arc
*	Install AzureML training and inferencing extentions on your AKS on Azure Stack HCI 
*	Attach your Azure Arc-enabled AKS on Azure Stack HCI's cluster to your Azure Machine Learning workspace as a compute target

## Prerequisites

Before you begin, please make sure that you have the following items available:

* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/en-us/free/) before you begin.
* An AKS on Azure Stack HCI cluster with **at least one Linux worker node** that is up and running. **Your Linux nodes must have a minimum of 4 vCPU cores and 8GB memory, around 2 vCPU cores and 3GB memory would be used by Arc and AzureML extension components** that we will be installing as part of this tutorial. If you don't have an AKS on Azure Stack HCI cluster, you can follow [the official documentation here](https://docs.microsoft.com/en-us/azure-stack/aks-hci/kubernetes-walkthrough-powershell) to create one on your Azure Stack HCI hardware. Alternatively, you can follow [AKS on Azure Stack HCI Evaluation guide](https://github.com/Azure/aks-hci/tree/main/eval) to create a cluster on an Azure VM with only a couple of commands (This should only be used for proof of concept, please use [the official documentation](https://docs.microsoft.com/en-us/azure-stack/aks-hci/kubernetes-walkthrough-powershell) and hardware for production workloads).
* An Azure Machine Learning (AML) Workspace deployed as part of your subscription. You can [create an AML workspace](https://docs.microsoft.com/azure/machine-learning/how-to-manage-workspace?tabs=python) if you don't already have one. If you are using the AML Python SDK to create your workspace, please make sure it has a version>= **1.30**. We strongly recommend learning more about [the innerworkings and concepts in Azure Machine Learning](https://docs.microsoft.com/en-us/azure/machine-learning/concept-azure-machine-learning-architecture) before continuing with the rest of this article (optional).

## Connect your AKS on Azure Stack HCI Cluster to Azure Via Azure Arc

We start the process of connecting our newly created Kubernetes cluster to Azure by installing the most recent Arc enabled Kubernetes CLI extensions (private preview). Follow the instructions below to install the required extensions and connect your newly created cluster to Azure az an Azure Arc Cluster:

*	Make sure the system that you are using to install CLI extensions has access to your cluster, cluster-admin role and, Azure. For more information please read [Before you Begin](https://docs.microsoft.com/en-in/azure/azure-arc/kubernetes/connect-cluster#before-you-begin). 
*   Follow the instructions given in the Pre-requisites section of [this repository](https://github.com/Azure/azure-arc-kubernetes-preview/blob/master/docs/k8s-extensions.md#pre-requisites) to install preview extensions and connect your cluster to Azure via Azure ARC.

## Install AzureML training and inferencing extentions on your AKS on Azure Stack HCI 

## Attach your Azure Arc-enabled AKS on Azure Stack HCI's cluster to your Azure Machine Learning workspace as a compute target

If you do not already have an Azure Machine learning workspace in your desired Azure resource group, please [create your Machine learning workspace](https://docs.microsoft.com/en-us/azure/machine-learning/concept-workspace#-create-a-workspace). You can then attach Azure Arc’s Kubernetes cluster to your workspace through Azure Machine Learning’s Python SDK:

### Python SDK:

1. Install the latest version of the AzureML SDK by running following command:

    ```pip install --upgrade azureml-sdk```

2. Make sure your Azure Machine Learning workspace is defined/loaded in your python environment. If not, you can load your workspace using Workspace class:
    
    ```python 
    from azureml.core import Workspace 
    
    ws = Workspace.from_config(path = "<PATH TO CONFIG FILE>")
    ws.get_details()
    ```
    ‘from_config’ method reads JSON configuration file that tells SDK how to communicate with your Azure Machine Learning workspace. If needed, [create a workspace JSON configuration file](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-configure-environment#workspace) before running the snippet above.

3. Attach/Register Azure Arc’s Kubernetes cluster as Azure Machine Learning compute target by running the following python code snippet:
    
    ```python
    from azureml.core.compute import KubernetesCompute

    k8s_config = {
    }

    attach_config = KubernetesCompute.attach_configuration(
      resource_id="<Arc_Cluster_ResourceID>",
      aml_k8s_config=k8s_config
    )
    
    compute_target = KubernetesCompute.attach(ws, "arccompute", attach_config)
    compute_target.wait_for_completion(show_output=True)
    ```

4. If the attachment is successful, “SucceededProvisioning operation finished, operation "Succeeded"” message will be printed as a result. This means that we have successfully attached the Arc Cluster as a compute target named “arccompute” in your Azure Machine Learning workspace. 


## Next Steps

Learn how to [Setup NFS Server on Azure Stack HCI and Use your Data and run managed Machine Learning Experiments On-Premises](Train-AzureArc.md).
