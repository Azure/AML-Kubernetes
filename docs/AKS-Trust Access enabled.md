# Trust Access enabled AKS integration with AzureML

Right now, we support the integration with Trusted Access enabled AKS which is still in **private preview**, the following two scenarios in the previous limitations can be supported then:
-	[Disabling local accounts](https://learn.microsoft.com/en-us/azure/aks/managed-aad#disable-local-accounts) for AKS is supported now by Azure Machine Learning.
-	If your AKS cluster has an [Authorized IP range enabled to access the API server](https://learn.microsoft.com/en-us/azure/aks/api-server-authorized-ip-ranges), enable the AzureML control plane IP ranges for the AKS cluster is not required anymore. 
This article is to guide you how to integrate AKS cluster in above two scenarios with AzureML for both model training and model inferencing.



## Prerequisites

1.  To gain access this AKS new feature that is still in privare preview, you can provide your information in this [form](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR9S7K-kdeMpBoc3jEmzkKMVUREwxSjhQTVNaM1I4RlVENklYQ1hRTFFSTC4u) to add to whitelist.

2. An existing AKS cluster which has disabled local account, or has enabled authorized IP range.
    - If you are using an AKS cluster has an authorized IP range enabled to access the API Server, you will no longer need to manually enable the AzureML control plane IP ranges with enabled Trust Access. In addition, you can also remove the added Azureml IP range.

3.	If you are using [Kubernetes compute v2](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-attach-kubernetes-anywhere), the AzureML extension should have been deployed to AKS cluster.

Please follow the steps below to enable Trust Access in your AKS clusters.

## Create AzureML rolebinding in your AKS cluster

To be accessible to your AKS cluster which has enabled local account or has authorized IP range, two AzureML roles are required to be bound in your AKS clusters:
- Microsoft.MachineLearningServices/workspaces/inference-v1
- Microsoft.MachineLearningServices/workspaces/mlworkload

You can use ` az aks trustedaccess rolebinding create` command to create AzureML rolebinding in your cluster, while  pecifying the AzureML roles to this rolebinding, the example is as follows: 

### Uing AKS in Azure for a quick POC, both training and inference workloads support

```azurecli
    az aks trustedaccess rolebinding create –resource group <resource-group> --cluster-name <cluster-name> --name <rolebinding-name> --source-resource-id /subscriptions/ <subscriptions-id> /resourceGroups/ <resource-group> /providers/Microsoft.MachineLearningServices/workspaces/< workspaces-name> --roles Microsoft.MachineLearningServices/workspaces/inference-v1,Microsoft.MachineLearningServices/workspaces/mlworkload
```

The creation may take 5 to 10 seconds.

> **<span stype="color:orane">Important**:</span>
   > * Each rolebinding is **only valid for one workspace** you specified during its creation.
   > * If one AKS cluster has/need to been attached to **multiple workspaces**, you must create the rolebinding for each workspace resource in this AKS cluster.

> **<span stype="color:orane">Notes**:</span>
   > * You need to make sure to specify both `inference-v1` and `mlworkload` roles at one time when creating/updating a rolebinding.
   > * Each name of rolebinding must be unique in one AKS cluster.



## Verify and manage the role binding

After creation, you can run the command below to verify whether the role-binding has been successfully added:

```azurecli
    az aks trustedaccess rolebinding show --name <rolebinding-name>  --resource-group <resource-group> --cluster-name <cluster-name>
```

```azurecli
    az aks trustedaccess rolebinding list --resource-group <resource-group> --cluster-name <cluster-name>
```

You can also delete the rolebinding in your cluster by running the command below:

```azurecli
    az aks trustedaccess rolebinding delete --name <rolebinding-name>  --resource-group <resource-group> --cluster-name <cluster-name>
```

## Attach new compute targets/reuse existing compute targets in workspace

After the rolebinding for an AzureML workspace has created in the AKS cluster, either **existing compute targets** or **new compute targets** attached from this AKS cluster can be used for ml workloads in this workspace.

- If the AKS cluster has been attached to your workspace before, you can directly use the existing compute targets for ml workloads in your workspace.

- If this is a new AKS cluster, you can follow [this document](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-attach-kubernetes-to-workspace) to attach the AKS cluster to your workspace.



