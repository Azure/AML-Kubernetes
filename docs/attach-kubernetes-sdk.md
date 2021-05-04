## Attach Kubernetes cluster using SDK
**Please note:  Your Arc cluster must have the AmlK8s extension installed before it can be attached to Azure Machine Learning!**

To attach Kubernetes compute you need install the latest version of the Azure ML SDK.

### Install private branch SDK
```
pip install --upgrade azureml-sdk
```

### Set up WS configuration
```
from azureml.core.workspace import Workspace

ws = Workspace.from_config()
print('Workspace name: ' + ws.name,
      'Azure region: ' + ws.location,
      'Subscription id: ' + ws.subscription_id,
      'Resource group: ' + ws.resource_group, sep='\n')
```      

### Attach Kubernetes compute compute via SDK
```python
from azureml.core.compute import KubernetesCompute

k8s_config = {
}

attach_config = KubernetesCompute.attach_configuration(
    resource_id="/subscriptions/5abfd9c4-ec8c-4db9-acd4-c762dce93508/resourceGroups/aks-eng-rg/providers/Microsoft.Kubernetes/connectedClusters/arcAksE",
    aml_k8s_config=k8s_config
)

compute_target = KubernetesCompute.attach(ws, "saurya-compute", attach_config)
compute_target.wait_for_completion(show_output=True)
```

### Detach Kubernetes compute via SDK
```
compute_target.detach()
```
