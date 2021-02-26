# Sample Notebooks

After following the documents above, you can go through the sample notebooks linked below to get a better understanding of how the process works and the possibilities it can unlock:

## Notebooks

* [MNIST Classification with Scikit-learn](mnist/MNIST_Training_with_ASH_Cluster_and_Storage.ipynb) (Image Classification, Aprox. 20 Minutes)

  This notebook serves as "hello world" of using Azure Stack Hub (ASH) Storage accounts and ASH clusters for training with 
  Azure Machine Learning workspaces. Estimated run time for the notebook is 20 minutes.
  
* [Distributed PyTorch Training with DistributedDataParallel](distributed-cifar10/distributed-pytorch-cifar10.ipynb) (Image Classification, Aprox. 30 Minutes/Epoch)
  
  Image classification with PyTorch. The estimated run time for the notebook is 30 minutes for one epoch of training.
  
* [Distributed Tensorflow 2 with MultiWorkerMirroredStrategy](distributed-cifar10/distributed-tf2-cifar10.ipynb) (Image Classification, Aprox. 30 Minutes/Epoch)
  
  Image classification with TensorFlow, Estimated run time for the notebook is 30 minutes for one epoch of training.
  
* [Object Segmentation with Transfer Learning](object-segmentation-on-azure-stack/object_segmentation-ash.ipynb) (Object Segmentation, Aprox. 45 Minutes/Epoch)
  
  Object segmentation using pre-trained Mask R-CNN model on PyTorch. AML pipeline steps are used for data preprocessing. The model was trained using ASH clusters and storage account. The estimated run time for the notebook is 45 minutes for one epoch of training.
  
* [AML Pipelines with NYC-TAXI-DATA](pipeline/nyc-taxi-data-regression-model-building.ipynb) (Structured Text Data Prediction)

* [Model Download and Upload](AML-model-download-upload.ipynb)

Note: Above run time estimated assume a vm size comparable to [Standard_DS3_v2](https://docs.microsoft.com/en-us/azure/virtual-machines/sizes-general)
