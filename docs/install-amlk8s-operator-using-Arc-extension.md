# Install amlk8s operator using Arc extension

**Note: To install the amlk8s operator through Arc extension, you should connect your Kubernetes cluster to Azure using Arc with extension enabled first. The detailed instruction can be found in this [guide](https://github.com/Azure/AML-Kubernetes/blob/master/docs/enable-arc-kubernetes-cluster.md).**

1. Install the preview version of k8s-extensions CLI extension provided in this [repo](https://github.com/Azure/AML-Kubernetes/tree/master/files):

   ```bash
   az extension add --source ./k8s_extension-0.1PP.15-py2.py3-none-any.whl
   ```

2. Install `Microsoft.AzureML.Kubernetes` extension on your Arc cluster:

   ```bash
   az k8s-extension create --sub <sub_id> -g <rg_name> -c <arc_cluster_name> --cluster-type connectedClusters  --extension-type Microsoft.AzureML.Kubernetes -n azureml-kubernetes-connector --release-train preview --config enableTraining=True
   ```

   After running this command, it will create service bus and relay resource for you under the same resource group of the Arc cluster with tag `managed_by: amlk8s`.

   Once the extension is ready, you can see it using `helm list -n azureml` or `kubectl get pods -n azureml`

3. You can use the following command to check the detail status of the extension:

   ```bash
   az k8s-extension show --sub <sub_id> -g <rg_name> -c <arc_cluster_name> --cluster-type connectedclusters -n azureml-kubernetes-connector
   ```

4. To delete the extension in the cluster, using the following command:

   ```bash
   az k8s-extension delete --sub <sub_id> -g <rg_name> -c <arc_cluster_name> --cluster-type connectedclusters -n azureml-kubernetes-connector
   ```