## Supported Distributions (Cloud Native Computing Foundation (CNCF) certified Kubernetes clusters)
1. [AKS - Engine](https://github.com/Azure/aks-engine/blob/master/docs/tutorials/quickstart.md)
2. [GKE](https://console.cloud.google.com/kubernetes)
3. Azure Stack Hub - TBD

## Install AMLK8s extension using Arc

#### Prerequisite: You need to connect your Kubernetes cluster to Arc before installing the AMlK8s extension.  
1. Follow the guide [here](https://docs.microsoft.com/en-us/azure/azure-arc/kubernetes/quickstart-connect-cluster) to install the correct `connectedk8s` CLI version.  

   Next, install the **preview version of the Arc extensions CLI** as follows:

2. Install the preview version of k8s-extensions CLI extension.  You can find the Python wheel file under `files` from the root of this repository. Download the file to your local machine and set the correct path
```bash
az extension add --source ./k8s_extension-0.1PP.15-py3-none-any.whl
```

3. Install `Microsoft.AzureML.Kubernetes` extension on your Arc cluster:

```bash
az k8s-extension create --sub <sub_id> -g <rg_name> -c <arc_cluster_name> --cluster-type connectedClusters  --extension-type Microsoft.AzureML.Kubernetes -n azureml-kubernetes-connector --release-train preview --config enableTraining=True
```

Running this command will create a Service Bus and Relay resource under the same resource group as the Arc cluster.  These resources are used to communicate with the cluster and modifying them will break attached compute targets.

Once the extension is ready, you can inspect it using `helm list -n azureml` or `kubectl get pods -n azureml`.

4. You can use the following command to show the properties of the extension including installation state:

```bash
az k8s-extension show --sub <sub_id> -g <rg_name> -c <arc_cluster_name> --cluster-type connectedclusters -n azureml-kubernetes-connector
```

5. To delete the extension in the cluster, use the following command:

```bash
az k8s-extension delete --sub <sub_id> -g <rg_name> -c <arc_cluster_name> --cluster-type connectedclusters -n azureml-kubernetes-connector
```

## GKE specifics
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
