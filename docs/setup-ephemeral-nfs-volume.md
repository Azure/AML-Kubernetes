### Set up NFS server

Set up on Ubuntu [Link](https://help.ubuntu.com/community/SettingUpNFSHowTo)

### Create and deploy a Configmap with nfs server properties

```nfs-configmap.yaml
kind: ConfigMap 
apiVersion: v1 
metadata:
  name: nfs-configmap 
nfs:
  # Configuration values can be set as key-value properties
 server: nfs-server.domain-name.com
 path: /path/to/shared-folder
 
 kubectl apply -f nfs-configmap.yaml
```

### How AML will use the mount for jobs

#### Phase 1
All jobs will look for the 'nfs-configmap' config-map

Alternatively, we can allow for any name for the configmap and then have it set up in the profile config

#### Phase 2
Per Job configmap setup

```
compute:
  # target is a Kubernetes Cluster 
  #if NOT specified , it will go to the default VC linked to the WS
  target: azureml:some_k8s_cluster OR a VC

resources:
  #0 default AML will find suitable resources in the cluster
  configmap: <name-of-configmap>
```
