# Sample Notebooks

These samples demonstrate how to perform various AML operations using Kubernetes clusters deployed on Azure Stack Hub.

   
## Notebooks

* [MNIST Classification with ASH Storage and Cluster](mnist/MNIST Training with ASH Cluster and Storage.ipynb)

  This notebook serves as "hello world" of using Azure Stack Hub (ASH) Storage accounts and ASH clusters for training with 
  Azure Machine Learning workspaces. Estimated run time for the notebook is 20 minutes.
* [Distributed PyTorch Training with DistributedDataParallel](distributed-cifar10/distributed-pytorch-cifar10.ipynb)
  
  Image classification with pytorch. Estimated run time for the notebook is 30 minutes with one epoch.
* [Distributed Tensorflow 2 with MultiWorkerMirroredStrategy](distributed-cifar10/distributed-tf2-cifar10.ipynb)
  
  Image classification with tensorflow, Estimated run time for the notebook is 30 minutes with one epoch.
* [AML Pipelines with NYC-TAXI-DATA](pipeline/nyc-taxi-data-regression-model-building.ipynb)
* [Model Download and Upload](AML-model-download-upload.ipynb)

Note: above estimated run time assuming vm size comparable to Standard_DS3_v2
