# Object Segmentation: Pipeline Training Run on AKS-HCI cluster and on-premise NFS server

Using Object Segmentation as an example, this sample notebook demonstrates how to run [Azure Machine Learning Pipelines](https://aka.ms/aml-pipelines) using AKS-HCI cluster and on-premise NFS server

## Notebooks

* [Object Segmentation with Transfer Learning](object_segmentation-akshci.ipynb) (Object Segmentation)
  
  Object segmentation using pre-trained Mask R-CNN model on PyTorch. AML pipeline steps are used for data preprocessing. **Training data are stored in on-premise NFS server, and the intermediate data are stored in default datastore associated with the ML workspace.** The whole flow includes,
  * Use AML pipelines to read training data from on-premise NFS server, do data preprocessing and generate intermediate data to default datastore
  * Use AML pipelines to trigger train step on AKS-HCI cluster
  * Register model
  * Inference with the registered model on AKS-HCI cluster
  * Test model 


* [Object Segmentation with Transfer Learning with all data on NFS server](object_segmentation-akshci-nfs.ipynb) (Object Segmentation)

  Object segmentation using pre-trained Mask R-CNN model on PyTorch. AML pipeline steps are used for data preprocessing. **Both the training and intermediate data are stored in on-prem NFS server.** The whole flow includes,
  * Use AML pipelines to read training data from on-premise NFS server, do data preprocessing and generate intermediate data to NFS server.
  * Use AML pipelines to trigger train step on AKS-HCI cluster
  * Register model
  * Inference with the registered model on AKS-HCI cluster
  * Test model 

   
