# Azure Arc-enabled Machine Learning - Training Public Preview

As part of Azure Machine Learning (AML) service capabilities, Azure Arc-enabled Machine Learning enables customer to run Machine Learning workload on Kubernetes anywhere, in cloud or on-premises, with seamless AML experience. Training public preview feature enables data scientist to train models on customer-managed Kubernetes anywhere with seamless [AML model training experience on Azure compute cluster](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-set-up-training-targets). To deploy a trained model using Azure Arc-enabled Machine Learning, please sign up [Inference Private Preview](https://github.com/Azure/amlarc-preview).

This repository is intended to serve as an information hub for customers and partners who are interested in Azure Arc-enabled AML training public preview. Use this repository for onboarding and testing instructions as well as an avenue to provide feedback, issues, enhancement requests and stay up to date as the preview progresses. Please note that preview release is subject to the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/en-us/support/legal/preview-supplemental-terms/)

## Prerequisites

1. An Azure subscription. If you don't have an Azure subscription, [create a free account](https://aka.ms/AMLFree) before you begin.
1. You have a Kubernetes cluster up and running, and learn about [Azure Arc enabled Kubernetes](https://docs.microsoft.com/en-us/azure/azure-arc/kubernetes/overview) and [cluster extension](https://docs.microsoft.com/en-us/azure/azure-arc/kubernetes/conceptual-extensions)
1. Your Kubernetes cluster is [connected to Azure Arc](https://docs.microsoft.com/en-us/azure/azure-arc/kubernetes/quickstart-connect-cluster). Please note down the region to be used in step 5.
1. You've met the pre-requisites listed under the [generic cluster extensions documentation](https://docs.microsoft.com/en-us/azure/azure-arc/kubernetes/extensions#prerequisites).
1. [Create an AML workspace](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-manage-workspace?tabs=python) in **the same region** as where your Kubernetes cluster is connected to Azure Arc.

## Getting started

Getting started with Training Public Preview is easy with following steps:

* [Deploy AzureML extension to your Azure Arc enabled Kubernetes cluster](./docs/deploy-extension.md)
* [Attach your Azure Arc enabled Kubernetes cluster to AML Workspace](./docs/attach-compute.md)
* [Train an image classification model](./docs/simple-train.md)






## Disclaimer
#### The lifecycle management (health, kubernetes version upgrades, security updates to nodes, scaling, etc.) of the AKS or Arc Kubernetes cluster is the responsibility of the customer.
For AKS, read what is managed and what is shared responsibility [here](https://docs.microsoft.com/en-us/azure/aks/support-policies)

#### All preview features are available on a self-service, opt-in basis and are subject to breaking design and API changes. Previews are provided "as is" and "as available," and they're excluded from the service-level agreements and limited warranty. As such, these features aren't meant for production use.


#### AMLK8s supports targeting ML training on both [Azure Kubernetes Service (AKS)](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough) clusters or any cluster that is registered in Azure using [Arc](https://docs.microsoft.com/en-us/azure/azure-arc/kubernetes/overview).


### Kubernetes version support
1.18.x or below

Known [issue](https://github.com/Azure/AML-Kubernetes/issues/40) with 1.19.x we are working on a fix

### Kubernetes version support is in accordance with what AKS supports. See [here](https://docs.microsoft.com/en-us/azure/aks/supported-kubernetes-versions) for details

## Getting Started

To use AMLK8s compute in private preview, follow these steps:

#### Install the Azure Machine Learning Python SDK
```
pip install --upgrade azureml-sdk
```

#### Install the latest Azure ML Python SDK
```
pip install --upgrade azureml-sdk
```

#### Register Microsoft.Relay resource provider

Please follow the [instructions for registering resource providers](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider) and enable `Microsoft.Relay`.

```
az provider register --namespace Microsoft.Relay
```

Check registration status
```
az provider show --namespace Microsoft.Relay -o table
```
### Concepts 

1. [How does this work?](/docs/how-does-this-work.md)

### Tutorials

#### IT Operator steps to set up Kubernetes cluster
1. Create/provision a Kubernetes cluster to attach to an AML workspace
    * [Create AKS cluster](/docs/create-provision-AKS-cluster.md)
    * [Connect Azure Arc Kubernetes cluster](/docs/enable-arc-kubernetes-cluster.md)
      * [GKE setup](/docs/gke-setup.md) 
      * [Bare metal setup](/docs/onprem-baremetal-blobfuse-setup.md)

1. Attaching Kubernetes cluster to AML workspace
    * [Using AML Studio](/docs/attach-kubernetes-portal.md)
    * [Using Python SDK](/docs/attach-kubernetes-sdk.md)

<!-- 1. [Manually install AMLK8S operator on ARC kubernetes clusters](/docs/manual-installation-amlk8s-operator.md). Not needed on AKS - currently installed automatically during attach step. -->

#### Data Scientist steps to submit trainig jobs
Submit AML training jobs to AMLK8s compute
1. [TensorFlow training](/docs/sample-notebooks/001-Tensorflow)
1. [Scikit image classification](/docs/sample-notebooks/002-SciKitLearn)
1. [Distributed TensorFlow with parameter server](/docs/sample-notebooks/003-Distributed%20TensorFlow%20with%20parameter%20server)


[Limitations and Known Issues](/docs/limitations-and-knownIssues.md)

[Troubleshooting](/docs/troubleshooting.md)

## FAQ
#### Recommended AKS cluster resources
We recommend you use a at least 3 nodes cluster, each node having at least 2C 4G. And if you want to running GPU jobs, you need some GPU nodes.
#### AML add-on version upgrade
We will install the latest AML add-on services automatically when you first attach AKS cluster to AML workspace. You can check add-on components version using ```helm list``` and update according to [Manage AML Add-on](https://github.com/Azure/CMK8s-Samples/blob/master/docs/5.%20Manage%20AML%20add-on.markdown).
#### Why the nodes run ocupied in a run is more than node count in run list?
The node count in the number of worker, for distribute training job, such as ps-worker or MPI/horovod they may need extra launcher node or ps node, they may also ocuppy one node. We will optimise this in following version.
#### What Azure storage does AMLK8s support?
AML K8s compute only suport Azure blob container, if your data is in other Azure storage, please move it to Azure blob first. We will support other Azure storage in following iteration.
#### How do I use AMLK8s compute in China Region?
Firstly, make sure you have switched the active cloud to AzureChinaCloud with [az cloud set](https://docs.microsoft.com/en-us/cli/azure/manage-clouds-azure-cli?view=azure-cli-latest) command. Then you can use the SDK and CLI sample in this repo.


# Contributing

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
