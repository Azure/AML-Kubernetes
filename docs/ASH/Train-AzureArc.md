# Run Azure Machine Learning training workloads utilizing Azure Stack Hub’s Kubernetes cluster and Blob storage (Private Preview)

In this article, you:
*	Create storage account on Azure Stack Hub
*	Configure the storage account to work with Azure Machine Learning and Azure Stack Hub’s Kubernetes Cluster
*	Connect the storage account to Azure Machine Learning as a datastore (where you hold all your training data) 
*	Run your first Azure Machine Learning training job on Azure Stack Hub using AzureML Python SDK (example notebooks)




## Prerequisites

Make sure you have access to Azure and your Azure Stack Hub is ready for use. In addition, this article assumes you have already:

1. Deployed a Kubernetes cluster in you Azure Stack Hub
2. Connected the Kubernetes cluster to Azure via Azure ARC

If you have not completed any of the two above, please do so using [instructions given here](AML-ARC Compute.md). Furthermore, please verify that you have already created an Azure Machine learning workspace. If not, please [create your Machine learning workspace](https://docs.microsoft.com/en-us/azure/machine-learning/concept-workspace#-create-a-workspace). It is also strongly recommended to learn more about the innerworkings and concepts in Azure Machine Learning before continuing with the rest of this article (optional). Lastly, make sure both Python and AzureML Python SDK are installed on the device that you will be using to communicate with Azure Machine Learning. 


## Create and Configure Azure Stack Hub’s Storage Account

We first start by creating a storage account on Azure Stack Hub’s Portal:

1. Select **Create a resource > Data + Storage**. Select **Storage account**. If you do not see the **Storage account**, contact your Azure Stack Hub cloud operator and ask for the image to be added to the Azure Stack Hub Marketplace.
