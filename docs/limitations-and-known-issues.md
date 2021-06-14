# Limitations and known issues

## Create a compute target via compute attach

For initial public preview release, you can create compute target via [AML Studio UI](compute-attach.md#create-a-compute-target-via-aml-stuido-ui) or [AML Python SDK](compute-attach.md#create-a-compute-target-via-aml-python-sdk). We are working hard to support compute attach via AML 2.0 CLI, please stay tuned for an update soon.

## Multiple AML workspaces share the same Arc cluster

Azure Arc-enabled Machine Learning now supports multiple AML workspaces share the same Azure Acr-enabled Kubernetes cluster. However these multiple workspaces must be in the same region as the first attached AML workspace region.

## Failed to find any PEM data in certificate for gateway and cluster-status-reporter

If you see this error during AzureML extension deployment, it means the cluster lacks ```--cluster-signing-cert-file``` and ```--cluster-signing-key-file``` parameters in its controller manager setting. You can set ```enable_https``` to false and it will use http for in-cluster components communication. For morning please refer to [Kubernetes documentation](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/#a-note-to-cluster-administrators).

## Custom IP interface for MPI job

For MPI job on Azure Arc-enabled on-premise Kubernetes cluster, AzureML provides a good default value if eth0 is not available. However this good default value might not be correct and MPI job will fail. To ensure that MPI job gets correct IP interface, you can st custome IP interface at AzureML extension deployment time by appending ```amloperator.custom_ip_interface_enabled=True``` and ```amloperator.custom_ip_interface=<your-ip-interface-name>``` to ```--configuration-settings``` parameter.  

## Length of Experiment Name

The length of experiment name need to less than 15 character now. Otherwise the run will can not be scheduled.

## Compute attach permissions

To attach an AKS cluster, you must be subscription owner or have permission to access AKS cluster resources under the subscription. Otherwise, the cluster list on "attach new compute" page will be blank.

## AKS spot node pools

Cannot use spot node pools as the spot pool nodes are tainted by default with _kubernetes.azure.com/scalesetpriority=spot:NoSchedule_
Tolerations in profile config is not supported yet that will allow you to target jobs/pods to the spot node pool
