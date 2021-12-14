## Deploy model with customer container for real-time inference

The normal workflow to deploy your model is,

1. Register the model to AML workspace.
2. Prepare an entry script (score.py).
1. Specify an [AML inference curated environment](https://docs.microsoft.com/en-us/azure/machine-learning/concept-prebuilt-docker-images-inference#list-of-prebuilt-docker-images-for-inference) as the base Docker image.
1. Deploy the model to the compute.

The normal workflow requires to register the model and prepare an entry script in the cloud. If user has concern on that, we also support a BYOC mode that user can build the model and entry script into the custom docker image. In this way, the model or  the entry script will not be saved in the cloud. Then using AML CLI v2 to deploy model for real-time inference.

###  Prepare the docker image
<!-- cd into directory azureml_artifacts/inference and you can see all the dependencies. -->

Create the Docker file as follows and build your own image.

```Dockerfile
# Specify a base image from AML inference curated environment
FROM <BASE IMAGE>

USER root
RUN mkdir -p $HOME/.cache
WORKDIR /
RUN if dpkg --compare-versions `conda --version | grep -oE '[^ ]+$'` lt 4.4.11; then conda install conda==4.4.11; fi
# copy the conda dependencies file to the container target path
COPY <conda_dependencies.yml FILE PATH> azureml-environment-setup/conda_dependencies.yml

# copy the score.py file to the container target path. If you don't need the score.py built into the docker image, comment out the next line.
COPY <score.py FILE PATH> /var/azureml-app/script/score.py

# copy the model folder/file to the container target path.  If you don't need the model built into the docker image, comment out the next line.
COPY <MODEL FOLDER OR FILE PATH> /var/azureml-app/azureml-models/<MODEL FOLDER/FILE>

RUN ldconfig /usr/local/cuda/lib64/stubs && conda env create -p /azureml-envs/azureml -f azureml-environment-setup/conda_dependencies.yml && rm -rf "$HOME/.cache/pip" && conda clean -aqy && CONDA_ROOT_DIR=$(conda info --root) && rm -rf "$CONDA_ROOT_DIR/pkgs" && find "$CONDA_ROOT_DIR" -type d -name __pycache__ -exec rm -rf {} + && ldconfig
ENV PATH /azureml-envs/azureml/bin:$PATH
ENV AZUREML_CONDA_ENVIRONMENT_PATH /azureml-envs/azureml
ENV LD_LIBRARY_PATH /azureml-envs/azureml/lib:$LD_LIBRARY_PATH
ENV AZUREML_ENVIRONMENT_IMAGE True
CMD ["runsvdir","/var/runit"]
```
### Prepare entry script and conda dependency yaml

Sample script:
```python
import json
import numpy as np
import os
import pickle
import joblib

def init():
    global model
    # MODEL_FILE_PATH is an environment variable specified in online-deployment yaml.
    # load the model from the docker container
    model = joblib.load(os.getenv('MODEL_FILE_PATH'))

def run(raw_data):
    data = np.array(json.loads(raw_data)['data'])
    # make prediction
    y_hat = model.predict(data)
    # you can return any data type as long as it is JSON-serializable
    return y_hat.tolist()
```
Sample conda dependency yaml. Add the necessary dependencies here to run the entry script.
```yaml
channels:
- anaconda
- conda-forge
dependencies:
- python=3.6.2
- pip:
  - azureml-defaults~=1.24.0.0
  - scikit-learn==0.22.1
name: azureml
```

### Create the online-endpoint
Create online endpoint yaml,
```yaml
name: <endpoint name>
compute: azureml:<compute target>
auth_mode: key
```
Create the endpoint by running,
```bash
az ml online-endpoint create -f endpoint.yml -n ${endpoint_name} --sub ${subscription} -g ${resource_group} -w ${workspace}
```
### Create the deployment
Create a deployment yaml file, and you need to update the `image` accordingly, specify the `environment variables` to use custom container, and keep the SAME `inference_config` as the example below.
- `AML_APP_ROOT` : the entry script folder at the docker container.
- `AZUREML_ENTRY_SCRIPT`: the entry script at the docker container.
- `MODEL_FILE_PATH`: the model path at the docker container.
```yaml
name: <deployment name>
type: kubernetes
environment_variables:
  AML_APP_ROOT: /var/azureml-app/script
  AZUREML_ENTRY_SCRIPT: score.py
  MODEL_FILE_PATH: /var/azureml-app/azureml-models/<model file/folder>
environment:
  name: <custom environment name>
  version: 1
  image: <docker image>
  #Please keep the SAME inference_config as below.
  inference_config:
    scoring_route:
      port: 5001
      path: /score
    liveness_route:
      port: 5001
      path: /
    readiness_route:
      port: 5001
      path: /
request_settings:
  request_timeout_ms: 1000
  max_concurrent_requests_per_instance: 1
  max_queue_wait_ms: 1000
resources:
  requests:
    cpu: "0.1"
    memory: "0.1Gi"
  limits:
    cpu: "0.2"
    memory: "200Mi"
liveness_probe:
  initial_delay: 5
  period: 5
  timeout: 10
  success_threshold: 1
  failure_threshold: 1
readiness_probe:
  initial_delay: 5
  period: 5
  timeout: 10
  success_threshold: 1
  failure_threshold: 1
instance_count: 1
scale_settings:
  type: default
```
### Create the online deployment
Create online deployment with all traffic,
```bash
az ml online-deployment create -f deployment.yaml -n blue --endpoint ${endpoint_name} -g --sub ${subscription} -g ${resource_group} -w ${workspace} --all-traffic
```

 Invoke the endpoint to test,
```bash
az ml online-endpoint invoke -r ${request json} -n ${endpoint_name} --sub ${subscription} -g ${resource_group} -w ${workspace}
```
