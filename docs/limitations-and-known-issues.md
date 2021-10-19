# Limitations and known issues

## Failed to find any PEM data in certificate for gateway and cluster-status-reporter

If you see this error during AzureML extension deployment, it means the cluster lacks ```--cluster-signing-cert-file``` and ```--cluster-signing-key-file``` parameters in its controller manager setting. You can set ```enable_https``` to false and it will use http for in-cluster components communication. For morning please refer to [Kubernetes documentation](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/#a-note-to-cluster-administrators).

## Custom IP interface for MPI job

For MPI job on Azure Arc-enabled on-premise Kubernetes cluster, AzureML provides a good default value if eth0 is not available. However this good default value might not be correct and MPI job will fail. To ensure that MPI job gets correct IP interface, you can st custome IP interface at AzureML extension deployment time by appending ```amloperator.custom_ip_interface_enabled=True``` and ```amloperator.custom_ip_interface=<your-ip-interface-name>``` to ```--configuration-settings``` parameter.  

## AML Dataset support

Azure Arc-enabled Machine Learning job supports mounting/downloading an AML Dataset to a local path specified by the field "PathOnCompute". But this path can not be any of following: under root folder (e.g. /<myfolder>), priviledge folder (e.g. /data/<myfolder>), and an existing folder. 
