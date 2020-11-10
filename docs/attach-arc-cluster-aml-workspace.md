Select Azure Arc Kubernetes cluster instead of AKS cluster and follow same steps as AKS

![arcattach](/docs/media/arcattach.png)

# For GKE 

Once the installation is complete, you need to SSH into each node in your cluster, and execute the following commands: 

[Utility tool to ssh into kubernetes nodes](https://github.com/kvaps/kubectl-node-shell)

```bash
sudo ln -s /etc/kubernetes/volumeplugins/azure~blobfuse /home/kubernetes/flexvolume/

sudo apt-get update; sudo apt-get install –y jq

wget https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb; sudo dpkg -i packages-microsoft-prod.deb; sudo apt-get update; sudo apt-get install blobfuse
``` 
