## GKE setup
1. Select Ubuntu OS image during cluster create
2. A minimum of 3 nodes is required; need enough resources for arc agent and amlk8s agent installation
3. DO NOT select smaller VM's than 'medium' size

GKE console -> +Create Cluster -> Node Pools -> Default-pool -> Nodes
![GKEClusterCreate](/docs/media/gkecreate.png)


4. Once the installation is complete, you need to SSH into each node in your cluster (can be found in Compute Engine under VM instances, SSH tool found under connect column).

![GKEClusterSSH](/docs/media/gke-ssh.png)

5. Execute the following commands in each node:

  ```bash
  sudo ln -s /etc/kubernetes/volumeplugins/azure~blobfuse /home/kubernetes/flexvolume/

  sudo apt-get update; sudo apt-get install jq

  wget https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb; sudo dpkg -i packages-microsoft-prod.deb; sudo apt-get update; sudo apt-get install blobfuse
  ```
