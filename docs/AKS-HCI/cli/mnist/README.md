# Image Classification Using Scikit-learn

## Prerequisites 

Follow this [doc](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-train-cli?view=azure-devops#prerequisites) to setup the prerequisites of using Azure Machine CLI v2.  

1. Let's set some defaults for all subsequent "az ml" CLI commands
```
az account set --subscription <subcription id>
az configure --defaults workspace=<azureml workspace name> group=<resource group>
```

2. For the training job with AML 2.0 CLI, we have following project directory structure:
```
mnist
|-- mnist_script
|   |-- train.py
|   |-- utils.py
|-- train_env
|   |-- conda.yml
|-- training.yml
|--...
```

As you can see from above, the project contains a training job YAML file and some Python training scripts, and an environment YAML file. In general, it is a typical project setup for Azure Arc enabled Machine Learning. 

In training YAML file - [training.yml](training.yml),
```yaml
$schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
code: 
  local_path: mnist_script
command: >-
  python train.py
  --data-folder <your nfs mounting point on training pods>/mnist
  --regularization 0.5
environment: 
  name: tutorial-env
  version: 1
  path: .
  conda_file: file:./train_env/conda.yml
  docker:
    image: mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04:20210806.v1
compute:
  target: azureml:<your compute target name>
  instance_type: <your instance type>
experiment_name: mnist-demo
description: Image Classification Using Scikit-learn
```

Note: Instance type is optional parameter. If it's not given, the compute default instance type will be used. For this example to run, you would have created following assets in AML Workspace: compute target named `<your compute name>`, and the training data are on NFS Server via `<your nfs mounting point on training pods>/mnist`. You can download and upload to NFS server in advance through [Azure Open Datasets](https://docs.microsoft.com/en-us/azure/open-datasets/dataset-mnist?tabs=azure-storage).

[conda.yml](model/conda.yml) defines all conda dependencies required for training job. Together with the base docker image: mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04:20210806.v1, training environment will be built before training job starts.

3. Run the image classification training job
```
az ml job create -f training.yml --web
```
Creating this job uploads any specified local assets, like the source code directory, validates the YAML file, and submits the run. If needed, the environment is built, then the compute is scaled up and configured for running the job.

In output, you can retrieve the run id from id property.

```json
{
  "code": "azureml:<REDACTED>:1",
  "command": "python train.py --data-folder /nfs_share/mnist --regularization 0.5",
  "compute": {
    "instance_count": 1,
    "instance_type": "<REDACTED>",
    "target": "azureml:<REDACTED>"
  },
  "creation_context": {
    "created_at": "<REDACTED>",
    "created_by": "<REDACTED>",
    "created_by_type": "User"
  },
  "description": "Image Classification Using Scikit-learn",
  "environment": "azureml:<REDACTED>:1",
  "environment_variables": {},
  "experiment_name": "mnist-demo",
  "id": "azureml:/subscriptions/<subscriptionId>/resourceGroups/<resourceGroupName>/providers/Microsoft.MachineLearningServices/workspaces/<workspaceName>/jobs/<runId>",
  "inputs": {},
  ...
  ...
  "resourceGroup": "<resourceGroupName>",
  "status": "Starting",
  "tags": {},
  "type": "command_job"
}
```

4. Once the job is compute, you can download the outputs:
```
az ml job download -n $run_id --outputs --download-path <downloadPath>
```
You can download the output, the downloaded folder will be named with the run id, such as,
```
run_id
|-- azureml-logs
|   |-- ...
|-- logs
|   |-- ...
|-- outputs
    |-- sklearn_mnist_model.pkl
```
sklearn_mnist_model.pkl is the trained model file.

5. Register model
```
az ml model create --name sklearn_mnist --version <version> --local-path <modelPath>
```

6. Deploy model using real-time endpoint

Here is the default inference project structure.
```
mnist
|-- score.py
|-- model
|   |-- conda.yml
|-- endpoint.yml
|-- deployment.yml
|-- sample-request.json
|--...
```
As you can see from above, "model" directory contains Conda environment definition, "[score.py](score.py)" is the scoring script. At top level directory, we have endpoint YAML definition, deployment YAML definition and sample request JSON file. In general, this is very typical project setup for Azure Arc enabled ML model deployment.

Replace the compute name in endpoint.yml, then trigger real-time endpoint creation.
```
az ml online-endpoint create -n <endpoint_name> -f endpoint.yml
```

Check status of endpoint

```
az ml online-endpoint show -n <endpoint_name>
```
Check if endpoint creation was successful

Replace instance type name, model name / version in deployment.yml, then create blue deployment
```
az ml online-deployment create --name blue --endpoint <endpoint_name> -f deployment.yml --all-traffic
```
Check status of blue deployment
```
az ml online-deployment show --name blue --endpoint <endpoint_name>
```
Check if deployment was successful

7. Test endpoint by scoring request

```
az ml online-endpoint invoke -n <endpoint_name> -r sample-request.json
```
You can also send a scoring request using cURL or Invoke-WebRequest

Obtain a token/keys for the scoring endpoint
```
az ml online-endpoint get-credentials --name <endpoint_name>
```
Obtain the scoring_uri of the endpoint
```
az ml online-endpoint show --name <endpoint_name>
```
Score using the token/key obtained above

In Linux Shell,
```shell
curl -v -i -X POST -H "Content-Type:application/json" -H "Authorization: Bearer <key_or_token>" -d '<sample_data>' <scoring_uri>
```
In Windows PowerShell,
```powershell
$accessToken="<key_or_token>"
$scoreUri = "<scoring_uri>"
$value = Get-Content .\sample-request.json
$headers = @{
    "Authorization" = "Bearer $accessToken"
    "Content-Type" = "application/json"
}
Invoke-WebRequest -UseBasicParsing -Uri $scoreUri -Headers $headers -Body $value -Method Post
```