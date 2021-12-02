# Instance types

## What are instance types?
Instance types are an Azure Machine Learning concept that allows targeting certain types of
compute nodes for training and inference workloads.  For an Azure VM, an example for an 
instance type is `STANDARD_D2_V3`.

In Kubernetes clusters, instance types are represented by two elements: 
[nodeSelector](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector)
and [resources](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).
In short, a `nodeSelector` lets us specify which node a pod should run on.  The node must have a
corresponding label.  In the `resources` section, we can set the compute resources (CPU, memory and
Nvidia GPU) for the pod.

## Create instance types
Instance types are represented in a custom resource definition (CRD) that is installed with the
Azure Machine Learning extension.  To create a new instance type, create a new custom resource
for the instance type CRD.  For example:
```bash
kubectl apply -f my_instance_type.yaml
```

With `my_instance_type.yaml`:
```yaml
apiVersion: amlarc.azureml.com/v1alpha1
kind: InstanceType
metadata:
  name: myinstancetypename
spec:
  nodeSelector:
    mylabel: mylabelvalue
  resources:
    limits:
      cpu: "1"
      nvidia.com/gpu: 1
      memory: "2Gi"
    requests:
      cpu: "700m"
      memory: "1500Mi"
```

This creates an instance type with the following behavior:
- Pods will be scheduled only on nodes with label `mylabel: mylabelvalue`.
- Pods will be assigned resource requests of `700m` CPU and `1500Mi` memory.
- Pods will be assigned resource limits of `1` CPU, `2Gi` memory and `1` Nvidia GPU.

Note:
- Nvidia GPU resources are only specified in the `limits` section as integer values.  For more information,
  please refer to the Kubernetes [documentation](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/#using-device-plugins).
- CPU and memory resources are string values.
- CPU can be specified in millicores, for example `100m`, or in full numbers, for example `"1"` which
  is equivalent to `1000m`.
- Memory can be specified as a full number + suffix, for example `1024Mi` for 1024 MiB.

It is also possible to create multiple instance types at once:
```bash
kubectl apply -f my_instance_type_list.yaml
```

With `my_instance_type_list.yaml`:
```yaml
apiVersion: amlarc.azureml.com/v1alpha1
kind: InstanceTypeList
items:
  - metadata:
      name: cpusmall
    spec:
      resources:
        requests:
          cpu: "100m"
          memory: "100Mi"
        limits:
          cpu: "1"
          nvidia.com/gpu: 0
          memory: "1Gi"

  - metadata:
      name: defaultinstancetype
    spec:
      resources:
        limits:
          cpu: "1"
          nvidia.com/gpu: 0
          memory: "1Gi"
        requests:
          cpu: "1"
          memory: "1Gi" 
```

The above example creates two instance types: `cpusmall` and `defaultinstancetype`.  The latter
is examplained in more detail in the following section.

## Default instance types
If a training or inference workload is submitted without an instance type, it uses the default
instance type.  To specify a default instance type for a Kubernetes cluster, create an instance
type with name `defaultinstancetype`.  It will automatically be recognized as the default.

If no default instance type was defined, the following default behavior applies:
- No nodeSelector is applied, meaning the pod can get scheduled on any node.
- The workload's pods are assigned default resources:
```yaml
resources:
  limits:
    cpu: "0.6"
    memory: "1536Mi"
  requests:
    cpu: "0.6"
    memory: "1536Mi"
```
- This default instance type will not appear as an InstanceType custom resource in the cluster,
but it will appear in all clients (UI, CLI, SDK).

Note: The default instance type purposefully uses little resources.  To ensure all ML workloads
run with appropriate resources, it is highly recommended to create custom instance types.

## Select instance type to submit training job
To select an instance type for a training job using CLI (V2), specify its name as part of the
`compute` section.  For example:
```yaml
command: python -c "print('Hello world!')"
environment:
  docker:
    image: python
compute: azureml:<compute_target_name>
resources:
  instance_type: <instance_type_name>
```

In the above example, replace `<compute_target_name>` with the name of your Kubernetes compute
target and `<instance_type_name>` with the name of the instance type you wish to select.

## Select instance type to deploy model

To select an instance type for a model deployment using CLI (V2), specify its name deployment YAML.  For example:

```yaml
deployments:
  - name: blue
    app_insights_enabled: true
    model: 
      name: sklearn_mnist_model
      version: 1
      local_path: ./model/sklearn_mnist_model.pkl
    code_configuration:
      code: 
        local_path: ./script/
      scoring_script: score.py
    instance_type: <your instance type>
    environment: 
      name: sklearn-mnist-env
      version: 1
      path: .
      conda_file: file:./model/conda.yml
      docker:
        image: mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04:20210727.v1
```