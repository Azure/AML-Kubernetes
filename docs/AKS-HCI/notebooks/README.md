# Sample Notebooks

After following the setup documents, you can go through the sample notebooks linked below to get a better understanding of how the process works and the possibilities it can unlock:

* [Image Classification Using Scikit-learn](mnist/MNIST_Training_with_AKS-HCI_Cluster_and_NFS.ipynb) (Image Classification)

  This notebook serves as "hello world" of using for training and inference with AKS-HCI Cluster, on-premise NFS Server, and Azure Machine Learning, including
  * Training with AKS-HCI cluster and on-premise NFS Server
  * Register model
  * Inference with the registered model on AKS-HCI cluster
  * Test model

* [Distributed PyTorch Training with DistributedDataParallel](distributed-cifar10/distributed-pytorch-cifar10.ipynb) (Image Classification)

  This notebook demonstrates an example of Image classification with PyTorch, including,
  * Distributed training using PyTorch with 2 worker nodes on AKS-HCI cluster and the training data is stored in on-premise NFS Server
  * Register model
  * Inference with the registered model on AKS-HCI cluster
  * Test model

* [Distributed Image Classification with Tensorflow](distributed-cifar10/distributed-tf2-cifar10.ipynb) (Image Classification)
  
  This notebook demonstrates an example of Image classification with TensorFlow.