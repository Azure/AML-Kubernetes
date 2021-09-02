# Setting up an NFS Server on AML Arc

Before you can run any of the examples in this section you will need to setup an NFS mount on your
Arc-enabled Kubernetes cluster.

The included mount-config.yaml file can be used as a template to do this. You will need to replace `<nfs-server-ip>` with the
actual address of your server. Then run the following:

```
kubectl apply -f mount-config.yaml
```

More detailed documentation on ephemeral NFS volume usage in Arc-enabled Machine Learning 
can be found [here](../../../docs/setup-ephemeral-nfs-volume.md)
