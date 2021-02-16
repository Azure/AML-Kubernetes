# ARC AMLK8s Azure Stack Hub Samples

This repository is intended to serve as an information hub for Azure Stack customers and partners who are interested in AML training using ARC Connected Kubernetes cluster and Azure Stack Hub Blob Storage. Use this repository for onboarding and testing instructions as well as an avenue to provide feedback, issues, enhancement requests and stay up to date as the private preview progresses.

## Disclaimer

All features are available on a self-service, opt-in basis and are subject to breaking design and API changes. Previews are provided "as is" and "as available," and they're excluded from the service-level agreements and limited warranty. As such, these features aren't meant for production use.

## Training on Azure Stack Hub

You can use the following documents to get started with setting up your training workloads on ASH:

1. [Deploy Azure Stack Hub’s Kubernetes Cluster as a Compute Cluster in Azure Machine Learning through Azure Arc](AML-ARC-Compute.md)
2. [Setup Azure Stack Hub's Blob Storage as a Datastore on Azure Machine Learning Workspace and Run a Training Workload](Train-AzureArc.md)


## Sample Notebooks

After following the documents above, you can go through the sample notebooks below to get a better understanding of how the process works and the possibilities it can unlock:

* [Distributed PyTorch Training with DistributedDataParallel](notebooks/distributed-cifar10/distributed-pytorch-cifar10.ipynb)
* [Distributed Tensorflow 2 with MultiWorkerMirroredStrategy](notebooks/distributed-cifar10/distributed-tf2-cifar10.ipynb)
* [AML Pipelines with NYC-TAXI-DATA](notebooks/pipeline)
