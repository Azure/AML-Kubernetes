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
1. Cteate PVC. In `metadata`, add label `ml.azure.com/pvc: "true"` to indicate the PVC can be mounted to the upcoming training job, and add annotation  `ml.azure.com/mountpath: <mount path>` to specify the mount path. 

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


### How AML will use the PVC

The training job in the same `namespace` with the PVC will be mounted the volume automatically. Then data scientist can access the mount path in the training job.

By default, the job will be created in  `default` namespace. IT operator can decide/update the namespace in attached compute target configuration. 


