# ARC AMLK8s Azure Stack Hub Samples

This repository is intended to serve as an information hub for Azure Stack customers and partners who are interested in AML training using ARC Connected Kubernetes cluster and Blob Storage. Use this repository for onboarding and testing instructions as well as an avenue to provide feedback, issues, enhancement requests and stay up to date as the private preview progresses.


## Training on Azure Stack Hub

You can use the following documents to get started with setting up your training workloads on ASH:

1. [Deploy Azure Stack Hub’s Kubernetes Cluster as a Compute Cluster in Azure Machine Learning through Azure Arc (Private Preview)](AML-ARC-Compute.md)
2. [Run Azure Machine Learning training workloads utilizing Azure Stack Hub’s Kubernetes cluster and Blob storage (Private Preview)](Train-AzureArc.md)

### InnerEye SDK

If you are interested in running training using the InnerEye SDK on Azure Stack Hub, please use the following document to make some small modifications in the InnerEye SDK so that it can work with this private preview (after following [document 1 above](AML-ARC-Compute.md)):

* [Run InnerEye Deep Learning training workloads utilizing Azure Stack Hub’s Kubernetes cluster as Azure Machine Learning Compute Cluster (Private Preview)](innereye-AzureArc.md)

## Inference with Stand alone KFServing

After trained and registered your model in azure machine learning workspace, you can download then upload model files to azure blobs as in 
this notebook [AML model download and upload to Azure Blobs](notebooks/AML-model-download-upload.ipynb)

Then following these documents to deploy an inference service with KFServing:

1. [Stand alone KFServing setup](KFServing-setup.md)
2. [KFServing with model in Azure Storage blobs](KFServing-with-model-in-Azure-Storage.md)

## Sample Notebooks

After following the documents above, you can go through the sample notebooks below to get a better understanding of how the process works and the possibilities it can unlock:

* [Distributed PyTorch Training with DistributedDataParallel](notebooks/distributed-pytorch-cifar10)
* [Distributed Tensorflow 2 with MultiWorkerMirroredStrategy](notebooks/distributed-tf2-cifar10)
