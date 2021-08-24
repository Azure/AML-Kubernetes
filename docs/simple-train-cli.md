
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

   As you can see from above, the project simply contains a job YAML file and some Python training scripts. In general, this a very typical project setup for Azure Arc-enabled ML training. Let's take a look a job YAML file: 

   ```yaml
   experiment_name: Tutorial-sklearn-mnist
   code:
     local_path: ./src
   command: python train.py --data-folder {inputs.mnist} --regularization 0.5
   environment:
     name: tutorial-env
     version: 1
     path: .
     conda_file: file:./environment.yml
     docker:
       image: mcr.microsoft.com/azureml/intelmpi2018.3-ubuntu16.04:20210301.v1
   compute:
     target: azureml:<your compute target name>
     instance_type: <your instance type>
   inputs:
     mnist:
       data: azureml:mnist_opendataset:1
       mode: mount
   ```
   
   **Note**: **Instance type** is optional parameter. If it's not given, the compute default instance type will be used. For this example to run, you would have created following assets in AML Workspace: compute target named **\<your compute name>**, and file dataset named **mnist_opendataset**. 

1. Git clone preview Github repo and switch to simple-train-cli directory

   ```console
   git clone https://github.com/Azure/AML-Kubernetes.git
   cd AML-Kubernetes/examples/simple-train-cli
   ```

1. Modify job YAML file to replace **amlarc-ml** with your own compute target name, and register open dataset MNIST as file dataset and named **mnist_opendataset** in AML Workspace from public URL: https://azureopendatastorage.blob.core.windows.net/mnist/*.gz

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
* [Additional examples](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/train)