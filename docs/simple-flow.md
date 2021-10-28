
# Deploy an image classification model - create an endpoint with blue deployment

## Azure CLI for ML installation and project setup

1. Remove any previous Azure ML CLI extension installations

    ```azurecli
    az extension remove -n ml
    az extension remove -n azure-cli-ml
    ```

1. Install the latest Azure CLI for ML, which is in public preview, and then verify installation

    ```azurecli
    az extension add -n ml
    az ml -h
    ```

1. Let's set some defaults for all subsequent "az ml" CLI commands

    ```azurecli
    az account set --subscription <subscription id>
    az configure --defaults workspace=<azureml workspace name> group=<resource group>
    ```

1. For this simple deployment flow, we have following project directory structure:

    ``` code
    simple-flow
    |-- model
    |   |-- conda.yml
    |   |-- sklearn_mnist_model.pkl
    |-- script
    |   |-- score.py
    |-- endpoint.yml
    |-- sample_request.json
    ```

    As you can see from above, "model" directory contains model and Conda environment definition, "score.py" is under "script" directory. At top level directory, we have endpoint YAML definition and sample request JSON file. In general, this is very typical project setup for Azure Arc enabled ML model deployment.

## Simple deployment flow

Now let's see simple deployment flow in action!

1. Git clone preview Github repo and switch to simple-flow directory

    ```console
    git clone https://github.com/Azure/amlarc-preview.git
    cd amlarc-preview/examples/simple-flow
    ```

1. Modify endpoint YAML file to replace "\<your compute target name>" with your own compute target name, and replace "\<your instance type>" to the instance type defined in your compute configuration. Create an endpoint with blue deployment with following CLI command, endpoint creation and deployment might take a few minutes.

> Note that the resource requirements (CPU, memory, GPU) defined in the endpoint yaml should be no more than the resource limit of the specified instance type.

    ```azurecli
    az ml endpoint create -n sklearn-mnist -f endpoint.yml
    ```

1. Check status of deployment

    ```azurecli
    az ml endpoint show -n sklearn-mnist
    ```

1. Check if deployment was successful

    ```azurecli
    az ml endpoint get-logs -n sklearn-mnist --deployment blue
    ```

1. Test endpoint by scoring request

    ```azurecli
    az ml endpoint invoke -n sklearn-mnist -r sample-request.json
    ```

    You can also send a scoring request using cURL.

    * Obtain a token/keys for the scoring endpoint

    ```azurecli
    az ml endpoint get-credentials --name <endpoint_name> --resource-group <resource_group_name> --workspace-name <workspace_name>
    ```

    * Obtain the `scoring_uri` of the endpoint
  
    ```azurecli
    az ml endpoint show --name <endpoint_name> --resource-group <resource_group_name> --workspace-name <workspace_name>
    ```
  
    * Score using the token/key obtained above

    ```bash
    curl -v -i -X POST -H "Content-Type:application/json" -H "Authorization: Bearer <key_or_token>" -d '<sample_data>' <scoring_uri>
    ```

That is it! You have successfully deployed an image classification model and scored the mode with a request.

## Additional resources

* To learn more about Azure ML endpoint and deployment concents, please check [Managed Online Endpoints](https://docs.microsoft.com/azure/machine-learning/how-to-deploy-managed-online-endpoints).
* [Additional Examples](https://github.com/Azure/azureml-examples/tree/main/cli/endpoints/online)
