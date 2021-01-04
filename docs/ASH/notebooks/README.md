# Distributed Training with Azure Stack Hub Kubernetes Clusters

These samples demonstrate how to perform distributed training using Kubernetes clusters deployed through Azure Stack Hub. 
Both Pytorch and Tensorflow are covered. The training jobs are submitted through Azure Machine Learning Workspace. 
The AML workspace attaches an Azure Stack Hub's Kubernetes cluster as a compute target. The training data is stored
in the Azure Stack Storage account. These training data is then configured as a dataset in the AML workspaces data store.

   
