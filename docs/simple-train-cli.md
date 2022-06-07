
# Train an image classification model with AML 2.0 CLI

1. Remove any previous AML CLI extension installations

   ```azurecli
   az extension remove -n ml
   az extension remove -n azure-cli-ml
   ```

1. Install the latest AML 2.0 CLI, which is in public preview, and then verify installation

   ```azurecli
   az extension add -n ml
   az ml -h
   ```

1. Let's set some defaults for all subsequent "az ml" CLI commands

   ```azurecli
   az account set --subscription <subcription id>
   az configure --defaults workspace=<azureml workspace name> group=<resource group>
   ```

1. For this simple training job with AML 2.0 CLI, we have following project directory structure:

   ``` code
   simple-train-cli
   |-- src
   |   |-- train.py
   |   |-- utils.py
   |-- job.yml
   ```

   As you can see from above, the project simply contains a job YAML file and some Python training scripts. In general, this a very typical project setup for Azure Arc-enabled ML training. Let's take a look at job YAML file: 

   ```yaml
   experiment_name: Tutorial-sklearn-mnist
   code: ./src
   command: python train.py --data-folder ./mnist-data --regularization 0.5
   environment: azureml:AzureML-sklearn-0.24-ubuntu18.04-py37-cpu:7
   compute: azureml:<your compute target name>
   resources:
     instance_type: <your instance type>
   ```
   
   **Note**: **Instance type** is optional parameter. If it's not given, like the YAML file below, the compute default instance type will be used. 
   
   ```yaml
   experiment_name: Tutorial-sklearn-mnist
   code: ./src
   command: python train.py --data-folder ./mnist-data --regularization 0.5
   environment: azureml:AzureML-sklearn-0.24-ubuntu18.04-py37-cpu:7
   compute: azureml:<your compute target name>
   ```
   
   Refer to [here](./instance-type.md) to learn how to create different instance types.

1. Git clone preview Github repo and switch to simple-train-cli directory

   ```console
   git clone https://github.com/Azure/AML-Kubernetes.git
   cd AML-Kubernetes/examples/training/simple-train-cli
   ```

1. Modify job YAML file to specify your own compute target name

1. Run the image classification training job

   ```azurecli
   az ml job create -f job.yml --web
   ```

   Creating this job uploads any specified local assets, like the source code directory, validates the YAML file, and submits the run. If needed, the environment is built, then the compute is scaled up and configured for running the job.

1. Once the job is compute, you can download the outputs:

   ```azurecli
   az ml job download -n $run_id --outputs
   ```

That is it! You have successfully trained an image classification model and download outputs to local directory.

## Additional resources

* [Train models (create jobs) with the 2.0 CLI (preview)](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-train-cli)
* [Additional examples](https://github.com/Azure/azureml-examples/tree/main/cli/jobs)
