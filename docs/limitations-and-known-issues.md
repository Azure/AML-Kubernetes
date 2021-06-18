# Limitations and known issues

## Create a compute target via compute attach

For initial public preview release, you can create compute target via [AML Studio UI](attach-compute.md#create-a-compute-target-via-aml-studio-ui) or [AML Python SDK](attach-compute.md#create-a-compute-target-via-aml-python-sdk). We are working hard to support compute attach via AML 2.0 CLI, please stay tuned for an update soon.

## Multiple AML workspaces share the same Arc cluster

Azure Arc-enabled Machine Learning now supports multiple AML workspaces share the same Azure Acr-enabled Kubernetes cluster. However these multiple workspaces must be in the same region as the first attached AML workspace region.

## Failed to find any PEM data in certificate for gateway and cluster-status-reporter

If you see this error during AzureML extension deployment, it means the cluster lacks ```--cluster-signing-cert-file``` and ```--cluster-signing-key-file``` parameters in its controller manager setting. You can set ```enable_https``` to false and it will use http for in-cluster components communication. For morning please refer to [Kubernetes documentation](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/#a-note-to-cluster-administrators).

## Custom IP interface for MPI job

For MPI job on Azure Arc-enabled on-premise Kubernetes cluster, AzureML provides a good default value if eth0 is not available. However this good default value might not be correct and MPI job will fail. To ensure that MPI job gets correct IP interface, you can st custome IP interface at AzureML extension deployment time by appending ```amloperator.custom_ip_interface_enabled=True``` and ```amloperator.custom_ip_interface=<your-ip-interface-name>``` to ```--configuration-settings``` parameter.  

## Cluster autoscaling and job scheduler support

Azure Arc-enabled ML job scheduler does not work with upstream cluster autoscaler yet, manual cluster scaling is required if there are not enough resources in cluster.
