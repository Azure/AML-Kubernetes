The required blobfuse plugin isn't installed attaching the cluster to AML.

A manual solution on Ubuntu 20.04 LTS:
- Install blobfuse (on all nodes)
```
https://github.com/Azure/kubernetes-volume-drivers/blob/master/flexvolume/blobfuse/README.md`
wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt-get update
sudo apt-get install -y blobfuse fuse
```
- Install jq (if there isn't on all nodes)
```
sudo apt-get -y jq
```
- Install blobfuse-flexvol-installer daemonset on the master node
```
kubectl apply -f https://raw.githubusercontent.com/Azure/kubernetes-volume-drivers/master/flexvolume/blobfuse/deployment/blobfuse-flexvol-installer-1.9.yaml
```
