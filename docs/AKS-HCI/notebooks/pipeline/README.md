# Pipeline Run with  Azure Stack Hub Kubernetes Clusters

These samples demonstrate how to run [Azure Machine Learning Pipelines](https://aka.ms/aml-pipelines) with Arc compute. 
Data are stored in AML datastore backed by azure storage blobs. Azure Stack Hub storage account is not used because 
it doesn't support tabular datasets. However, data are processed by Arc computes. Training step is done by
Arc compute as well.

## Notebooks

* [AML Pipelines with NYC-TAXI-DATA](nyc-taxi-data-regression-model-building.ipynb)





   