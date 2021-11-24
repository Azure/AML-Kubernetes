# Pipeline Run with AKS-HCI cluster

These samples demonstrate how to run [Azure Machine Learning Pipelines](https://aka.ms/aml-pipelines) with Arc compute.

## Notebooks

* [AML Pipelines with NYC-TAXI-DATA](nyc-taxi-data-regression-model-building.ipynb) (Structured Text Data Prediction)

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





   