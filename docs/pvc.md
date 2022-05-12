### PV/PVC support in AMLArc training job

Now you can leverage Kubernetes native way to mount various data storage via [Persistent Volume (PV) and Persistent Volume Claim (PVC)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/).

1. Create PV, take NFS as example,

```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-pv 
spec:
  capacity:
    storage: 1Gi 
  accessModes:
    - ReadWriteMany 
  persistentVolumeReclaimPolicy: Retain
  storageClassName: ""
  nfs: 
    path: /share/nfs
    server: 20.98.110.84 
    readOnly: false
```
2. Cteate PVC. In `metadata`, add label `ml.azure.com/pvc: "true"` to indicate the PVC can be mounted to the upcoming training job, and add annotation  `ml.azure.com/mountpath: <mount path>` to specify the mount path. 

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nfs-pvc  
  namespace: default
  labels:
    ml.azure.com/pvc: "true"
  annotations:
    ml.azure.com/mountpath: "/mnt/nfs"
spec:
  storageClassName: ""
  accessModes:
  - ReadWriteMany      
  resources:
     requests:
       storage: 1Gi
```
<!-- ### Access control

All AML workloads will be executed as a special user with `uid` `200513`. To have proper read/write permission to the mounted file system like NFS, refer to the following guidance,

* If the shared folder has '777' permission, all ML workloads will have read and write permission. 
* if the file system has set all_squash and anonuid/anongid, all ML workloads will have read and write permission. 
* If `uid 200513` is added to the group with proper read/write access to NFS, all ML workloads will have read and write permission. In this case, use the annotation `ml.azure.com/gid: "XXX"` in PVC setting, then the uid 200513 will be added to the specified group. **Note** to remove `RPCMOUNTDOPTS="--manage-gids` at the path of `/etc/default/nfs-kernel-server ` in NFS server to respect the permission control in the client side. -->



### How AML will use the PVC

The training job in the same `namespace` with the PVC will be mounted the volume automatically. Then data scientist can access the mount path in the training job.

By default, the job will be created in  `default` namespace. IT operator can decide the namespace in attached compute attach.




