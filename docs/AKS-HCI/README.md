# Setup and Run AzureML Training & Inferencing Workloads On Premises Using AKS on Azure Stack HCI Via Azure Arc 

This repository is intended to serve as an information hub for AKS on Azure Stack HCI customers and partners who are interested in Arc AML training using ARC Connected AKS cluster and NFS Server on Azure Stack HCI. Use this repository for onboarding and testing instructions as well as an avenue to provide feedback, issues, enhancement requests and stay up to date as the public preview progresses.

<p align="center">
            <img src="imgs/structure.png" />
</p>

## Setup Azure Arc-enabled Machine Learning on AKS on Azure Stack HCI

You can use the following documents to get started with setting up your Azure Arc-enabled Machine Learning on AKS on Azure Stack HCI:

1. [Setup Azure Arc-enabled Machine Learning Training and Inferencing on AKS on Azure Stack HCI](AML-ARC-Compute.md)
2. [Setup NFS Server on Azure Stack HCI and Use your Data and run managed Machine Learning Experiments On-Premises](Train-AzureArc.md)

## Sample Notebooks

After following the documents above, you can go through the sample notebooks linked below to get a better understanding of how the process works and the possibilities it can unlock:

* [Image Classification Using Scikit-learn](notebooks/mnist/MNIST_Training_with_ASH_Cluster_and_Storage.ipynb) (Image Classification, Aprox. 20 Minutes)

  This notebook serves as "hello world" of using Azure Stack Hub (ASH) Storage accounts and ASH clusters for training with 
  Azure Machine Learning workspaces. Estimated run time for the notebook is 20 minutes.
  
* [Distributed Image Classification with PyTorch](notebooks/distributed-cifar10/distributed-pytorch-cifar10.ipynb) (Image Classification, Aprox. 30 Minutes/Epoch)
  
  Image classification with PyTorch. The estimated run time for the notebook is 30 minutes for one epoch of training.
  
* [Distributed Image Classification with Tensorflow](notebooks/distributed-cifar10/distributed-tf2-cifar10.ipynb) (Image Classification, Aprox. 30 Minutes/Epoch)
  
  Image classification with TensorFlow, Estimated run time for the notebook is 30 minutes for one epoch of training.
  
* [Object Segmentation with Transfer Learning](notebooks/object-segmentation-on-azure-stack/object_segmentation-ash.ipynb) (Object Segmentation, Aprox. 45 Minutes/Epoch)
  
  Object segmentation using pre-trained Mask R-CNN model on PyTorch. AML pipeline steps are used for data preprocessing. The model was trained using ASH clusters and storage account. The estimated run time for the notebook is 45 minutes for one epoch of training.
  
* [AML Pipelines with NYC-TAXI-DATA](notebooks/pipeline/nyc-taxi-data-regression-model-building.ipynb) (Structured Text Data Prediction)


Note: Above run time estimated assume a vm size comparable to [Standard_DS3_v2](https://docs.microsoft.com/en-us/azure/virtual-machines/sizes-general)

## Troubleshooting

If you face issues during setup or experimenting, please check out [Limitations and known issues](../limitations-and-known-issues.md) and [Support](../../README.md#support) pages.
