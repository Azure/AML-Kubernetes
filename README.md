# AMLK8s Samples
This repository is intended to serve as an information hub for customers and partners who are interested in AMLK8s (Custmer managed Kubernetes cluster). Use this repository for onboarding and testing instructions as well as an avenue to provide feedback, issues, enhancement requests and stay up to date as the preview progresses.

#### AMLK8s refers either to an Azure Kubernetes Service (AKS) cluster or any cluster that is registered in Azure using Arc. Currently, only AKS is supported.

## Overview
AMLK8s project enables customer to use their exsiting AKS cluster as compute target for AML training workload (will also support Arc k8s clusters in the near future). Data scientists will have same experience as other compute targets, they can submit different types of training jobs to AMLK8s compute target. AMLK8s Will first support SDK and CLI, and restapi will be supported later.


## Getting Started

To use CMAKS compute in private preview, you need follow these steps:

1. [Provision a GPU enabled AKS cluster](https://github.com/Azure/CMK8s-Sample/blob/master/docs/1.%20Provision%20a%20GPU%20enabled%20AKS%20cluster.md)
2. [Manage CMAKS compute](https://github.com/Azure/AML-Kubernetes/blob/master/docs/2.%20Manage%20CMAKS%20compute.markdown)
3. [Submit AML training jobs to CMAKS compute](https://github.com/Azure/CMK8s-Samples/blob/master/docs/3.%20Submit%20AML%20training%20jobs%20to%20CMASK%20compute.markdown)
4. [View metrics in Compute level and runs level](https://github.com/Azure/CMK8s-Samples/blob/master/docs/4.%20View%20metrics%20in%20Compute%20level%20and%20runs%20level.markdown)
5. [Manage AML Add-on](https://github.com/Azure/CMK8s-Samples/blob/master/docs/5.%20Manage%20AML%20add-on.markdown)
1. [Limitations and Known Issues](../docs/limitations-and-knownIssues.md)

**Note**: The compute name in Python SDK and CLI may be changed during preview.

## FAQ 
### Q1. Recommend AKS cluster resource 
We recommend you use a at least 3 nodes cluster, each node having at least 2C 4G. And if you want to running GPU jobs, you need some GPU nodes.
### Q2. AML add-on version upgrade
We will install the latest AML add-on services automatically when you first attach AKS cluster to AML workspace. You can check add-on components version using ```helm list``` and update according to [Manage AML Add-on](https://github.com/Azure/CMK8s-Samples/blob/master/docs/5.%20Manage%20AML%20add-on.markdown).
### Q3. Why the nodes run ocupied in a run is more than node count in run list?
The node count in the number of worker, for distribute training job, such as ps-worker or MPI/horovod they may need extra launcher node or ps node, they may also ocuppy one node. We will optimise this in following version.
### Q4. What Azure storage do AMLK8s support?
AML K8s compute only suport Azure blob container, if your data is in other Azure storage, please move it to Azure blob first. We will support other Azure storage in following iteration.
### Q5. What type of jobs do AMLK8s support?
AML K8s compute doesn't support all AML jobs by now. For more details, please refer to the list in [Using CMAKS Compute in AML Notebooks](https://github.com/Azure/AML-Kubernetes/blob/master/docs/6.%20Using%20CMAKS%20Compute%20in%20AML%20Notebooks.md).
### Q6. How to use AMLK8s compute in China Region?
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
