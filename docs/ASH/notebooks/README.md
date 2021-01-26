# Distributed Training with Azure Stack Hub Kubernetes Clusters

These samples demonstrate how to perform distributed training using Kubernetes clusters deployed through Azure Stack Hub. 
Both Pytorch and Tensorflow are covered. The training jobs are submitted through Azure Machine Learning Workspace. 
The AML workspace attaches an Azure Stack Hub's Kubernetes cluster as a compute target. The training data is stored
in the Azure Stack Storage account. These training data is then configured as a dataset in the AML workspaces data store.

   
## Notebooks

* [Distributed PyTorch Training with DistributedDataParallel](distributed-pytorch-cifar10/distributed-pytorch-cifar10.ipynb)
* [Distributed Tensorflow 2 with MultiWorkerMirroredStrategy](distributed-tf2-cifar10/distributed-tf2-cifar10.ipynb)
* [AML Pipelines with NYC-TAXI-DATA](pipeline/nyc-taxi-data-regression-model-building.ipynb)
* [Model Download and Upload](AML-model-download-upload.ipynb)