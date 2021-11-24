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

* [Distributed Image Classification with Tensorflow](distributed-cifar10/distributed-tf2-cifar10.ipynb) (Image Classification, not finished)
  
  This notebook demonstrates an example of Image classification with TensorFlow, including,
  * Distributed training using Tensorflow with 2 worker nodes on AKS-HCI cluster and the training data is stored in on-premise NFS Server
  * TBD

* [Object Segmentation with Transfer Learning](object-segmentation-on-azure-stack/object_segmentation-akshci.ipynb) (Object Segmentation)
  
  Object segmentation using pre-trained Mask R-CNN model on PyTorch. AML pipeline steps are used for data preprocessing. Training data are stored in on-premise NFS server, and the intermediate data are stored in default datastore associated with the ML workspace. The whole flow includes,
  * Use AML pipelines to read training data from on-premise NFS server, do data preprocessing and generate intermediate data to default datastore
  * Use AML pipelines to trigger train step on AKS-HCI cluster
  * Register model
  * Inference with the registered model on AKS-HCI cluster
  * Test model 
  
* [AML Pipelines with NYC-TAXI-DATA](pipeline/nyc-taxi-data-regression-model-building.ipynb) (Structured Text Data Prediction)

  This notebook demonstrates an example of Structured Text Data Prediction, preparing / preprocessing / training data in default datastore associated with the ML workspace. The whole flow includes,
  * Download and upload training data to default datastore
  * Use AML pipelines to preprocess and train
    * Cleanse data in parallel
    * Merge cleansed data
    * Normalize data
    * Transform data
    * Split data
    * Train model
  * Register model
  * Inference with the registered model on AKS-HCI cluster
  * Test model 

* [Model Download and Upload](download-upload-model/AML-model-download-upload.ipynb)