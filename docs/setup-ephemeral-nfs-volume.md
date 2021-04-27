### Set up NFS server

Set up on Ubuntu [Link](https://help.ubuntu.com/community/SettingUpNFSHowTo)

### Create a Configmap with nfs server properties

```mount-config.yaml
kind: ConfigMap
apiVersion: v1
metadata:
  name: mount-config
  namespace: azureml
data:
  mounts.yaml: |
    mountPoints:
    - mountPath: /nfs_share
      mountType: nfs
      name: nfs-name
      path: /path/to/shared-folder
      server: nfs-server.domain-name.com
```

### Apply the Configmap

`kubectl apply -f mount-config.yaml`

### Documentation on Specific Fields
* `mountPath`: defines the path that the NFS volume will be mounted into inside your job
* `mountType`: must be `nfs`
* `name`: arbitrary symbolic name for your mount.  If you define multiple mounts then this must be unique per mount
* `path`: path (on the server) to the folder you want to mount
* `server`: NFS server address

Multiple NFS mounts may be defined under `mountPoints`

The rest of the `mount-config.yaml` file must be exactly as above

### How AML will use the mount for jobs

All jobs will look for the 'mount-config' ConfigMap.  If this ConfigMap is missing or malformed then no mounts will be applied.


