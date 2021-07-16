# Azure Arc-enabled Machine Learning - Training Public Preview

As part of Azure Machine Learning (AML) service capabilities, Azure Arc-enabled Machine Learning (ML) brings AML to any infrastructure across multi-cloud, on-premises, and the edge using Kubernetes on their hardware of choice. The design for Azure Arc-enabled ML helps IT operators leverage native Kubernetes concepts such as namespace, node selector, and resources requests/limits for ML compute utilization and optimization. By letting the IT operator manage ML compute setup, Azure Arc-enabled ML creates a seamless AML experience for data scientists who do not need to learn or use Kubernetes directly. 

This repository is intended to serve as an information hub for customers and partners who are interested in Azure Arc-enabled AML training public preview. Use this repository for onboarding and testing instructions as well as an avenue to provide feedback, issues, enhancement requests and stay up to date as the preview progresses. To deploy a trained model using Azure Arc-enabled Machine Learning, please sign up [Inference Preview](https://forms.office.com/r/X1HBQiBvP5). Please note that preview release is subject to the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/)

## Prerequisites

1. An Azure subscription. If you don't have an Azure subscription, [create a free account](https://aka.ms/AMLFree) before you begin.
1. You have a Kubernetes cluster up and running - **the cluster must have minimum of 4 vCPU cores and 16GB memory, around 3 vCPU cores and 6GB memory would be used by system**.
1. Your Kubernetes cluster is [connected to Azure Arc](https://docs.microsoft.com/azure/azure-arc/kubernetes/quickstart-connect-cluster).
1. You've met the pre-requisites listed under the [generic cluster extensions documentation](https://docs.microsoft.com/azure/azure-arc/kubernetes/extensions#prerequisites).
   * Azure CLI version >=**2.24.0**
   * Azure CLI extension k8s-extension version >=**0.4.3**.
1. [Create an AML workspace](https://docs.microsoft.com/azure/machine-learning/how-to-manage-workspace?tabs=python) if you don't have one already.
   * AML Python SDK version >= **1.30**.

## Getting started

Getting started with Training Public Preview is easy with following steps:

* [Deploy AzureML extension to your Azure Arc enabled Kubernetes cluster](./docs/deploy-extension.md)
* [Create a compute target - Attach Azure Arc enabled Kubernetes cluster to AML Workspace](./docs/attach-compute.md)
* [Train image classification model with AML 2.0 CLI](./docs/simple-train-cli.md)
* [Train image classification model with Python SDK](./examples/simple-train-sdk/img-classification-training.ipynb)

## Training Public Preview supported features

As another compute target in AML, Azure Arc-enabled ML preview supports the following built-in AML training features seamlessly:

* [Train models with AML 2.0 CLI](https://docs.microsoft.com/azure/machine-learning/how-to-train-cli?view=azure-devops)
  * [Basic Python training job](https://docs.microsoft.com/azure/machine-learning/how-to-train-cli?view=azure-devops#basic-python-training-job)
  * [Distributed training - PyTorch](https://docs.microsoft.com/azure/machine-learning/how-to-train-cli?view=azure-devops#pytorch)
  * [Distributed training - TensorFlow](https://docs.microsoft.com/azure/machine-learning/how-to-train-cli?view=azure-devops#tensorflow)
  * [Distributed training - MPI](https://docs.microsoft.com/azure/machine-learning/how-to-train-cli?view=azure-devops#mpi)
  * [Sweep hyperparameters](https://docs.microsoft.com/azure/machine-learning/how-to-train-cli?view=azure-devops#sweep-hyperparameters)
* Train models with AML Python SDK
  * [Configure and submit training run](https://docs.microsoft.com/azure/machine-learning/how-to-set-up-training-targets?view=azure-devops)
  * [Tune hyperparameters](https://docs.microsoft.com/azure/machine-learning/how-to-tune-hyperparameters?view=azure-devops)
  * [Scikit-learn](https://docs.microsoft.com/azure/machine-learning/how-to-train-scikit-learn?view=azure-devops)
  * [TensorFlow](https://docs.microsoft.com/azure/machine-learning/how-to-train-tensorflow?view=azure-devops)
  * [PyTorch](https://docs.microsoft.com/azure/machine-learning/how-to-train-pytorch?view=azure-devops)
* [Build and use ML pipelines including designer pipeline support](https://docs.microsoft.com/azure/machine-learning/how-to-create-machine-learning-pipelines?view=azure-devops)

In addition to above built-in AML training features, public preview also supports following on-premises training scenarios

* [Train model on-premises with outbound proxy server](https://docs.microsoft.com/azure/azure-arc/kubernetes/quickstart-connect-cluster#5-connect-using-an-outbound-proxy-server)
* [Train model on-premises with NFS datastore](./docs/setup-ephemeral-nfs-volume.md)

## Release notes 

New features are released at a biweekly cadance. 

**July 2, 2021 Release**

* New Kubernetes distributions support, OpenShift Kubernetes and GKE (Google Kubernetes Engine). 
* Autoscale support. If the user-managed Kubernetes cluster enables the autoscale, the cluster will be automatically scaled out or scaled in according to the volume of active runs and deployments.  
* Performance improvement on job laucher, which shortens the job scheduling time to a great deal.



## Region availability

Azure Arc-enabled Machine Learning is currently supported in these regions where Azure Arc is available:

* East US
* West Europe
* West Central US
* South Central US
* Southeast Asia
* UK South
* West US 2
* Australia East
* East US 2
* North Europe

## Supported Kubernetes distributions and versions

* Azure Kubernetes Services
* AKS Engine
* AKS on Azure Stack HCI
* GKE (Google Kubernetes Engine)  (coming with July 2, 2021 release)
* Canonical Kubernetes Distribution
* OpenShift Kubernetes Distribution (coming with July 2, 2021 release)
* Kubernetes 1.18.x and 1.19.x

## [Limitations and known issues](./docs/limitations-and-known-issues.md)

## [FAQ](./docs/faq.md)

## Support

We are always looking for feedback on our current experiences and what we should work on next. If there is anything you would like us to prioritize, please feel free to suggest so via our [GitHub Issue Tracker](https://github.com/Azure/AML-Kubernetes/issues). You can submit a bug report, a feature suggestion or participate in discussions.


## Activities

* [Check for known issues](https://github.com/Azure/amlk8s-preview/labels/known-issue)
* [View general feedback](https://github.com/Azure/amlk8s-preview/labels/feedback)
* [Browse roadmap items](https://github.com/Azure/amlk8s-preview/labels/roadmap)
* [Open a bug, provide feedback, or suggest an improvement](https://github.com/Azure/amlk8s-preview/issues/new/choose)

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

![Impressions](https://PixelServer20190423114238.azurewebsites.net/api/impressions/CMK8s-Samples/README.png)

## Disclaimer

The lifecycle management (health, kubernetes version upgrades, security updates to nodes, scaling, etc.) of the AKS or Arc Kubernetes cluster is the responsibility of the customer.

For AKS, read what is managed and what is shared responsibility [here](https://docs.microsoft.com/azure/aks/support-policies)

All preview features are available on a self-service, opt-in basis and are subject to breaking design and API changes. Previews are provided "as is" and "as available," and they're excluded from the service-level agreements and limited warranty. As such, these features aren't meant for production use.

Azure Arc-enabled ML supports targeting ML training on both [Azure Kubernetes Service (AKS)](https://docs.microsoft.com/azure/aks/kubernetes-walkthrough) clusters or any cluster that is registered in Azure using [Arc](https://docs.microsoft.com/azure/azure-arc/kubernetes/overview).

Kubernetes version support is in accordance with what AKS supports, see [here](https://docs.microsoft.com/azure/aks/supported-kubernetes-versions) for details.
