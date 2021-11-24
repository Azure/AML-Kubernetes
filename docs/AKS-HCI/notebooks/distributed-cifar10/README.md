# Distributed Training on AKS-HCI and on-premise NFS Server

These sample notebooks guide you through a distributed training workload that trains an ML model on [CIFAR10](https://www.cs.toronto.edu/~kriz/cifar.html) dataset hosted on on-premise NFS Server. We offer two notebooks taking advantage of the most popular deep learning frameworks PyTorch and Tensorflow.

## Notebooks

* [Distributed PyTorch Training with DistributedDataParallel](distributed-pytorch-cifar10.ipynb) (Image Classification)

  This notebook demonstrates an example of Image classification with PyTorch, including,
  * Distributed training using PyTorch with 2 worker nodes on AKS-HCI cluster and the training data is stored in on-premise NFS Server
  * Register model
  * Inference with the registered model on AKS-HCI cluster
  * Test model

* [Distributed Image Classification with Tensorflow](distributed-tf2-cifar10.ipynb) (Image Classification, not finished)
  
  This notebook demonstrates an example of Image classification with TensorFlow, including,
  * Distributed training using Tensorflow with 2 worker nodes on AKS-HCI cluster and the training data is stored in on-premise NFS Server
  * TBD