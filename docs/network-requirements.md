## Meet network requirements

If your cluster has Internect access, it's all done. Otherwise, If the cluster is behind the outbound proxy or firewall with strict outbound network, make sure following protocols/ports/outbound URLs to function.

AMLArc depends on Azure Arc connection. Please make sure to meet [Azure Arc network requirements](https://docs.microsoft.com/en-us/azure/azure-arc/kubernetes/quickstart-connect-cluster?tabs=azure-cli#meet-network-requirements) 

### AML extension
 
Need outbound access to following URLs when deploying ML extension to the cluster.

| Destination Endpoint| Port | Use |
|--|--|--|
| management.azure.com | https:443 | Required for the agent to connect to Azure and register the cluster. |
| <region>.dp.kubernetesconfiguration.azure.com | https:443 | Data plane endpoint for the agent to push status and fetch configuration information. |
| login.microsoftonline.com | https:443 | Required to fetch and update Azure Resource Manager tokens. |
|  mcr.microsoft.com| https:443 | Required to pull container images for Azure Arc agents. |
|  *.data.mcr.microsoft.com| https:443 | Required for MCR storage backed by the Azure content delivery network (CDN). |
|  gbl.his.arc.azure.com| https:443 | Required to get the regional endpoint for pulling system-assigned Managed Service Identity (MSI) certificates. |
|  <region-code>.his.arc.azure.com| https:443 | Required to pull system-assigned Managed Service Identity (MSI) certificates. |
| guestnotificationservice.azure.com, sts.windows.net, *.servicebus.windows.net| https:443 | For Cluster Connect and for Custom Location based scenarios. |
| quay.io, *.quay.io | https:443 | Quay.io registry, required to pull container images for AML extension components |
| gcr.io| https:443 | Google cloud repository, required to pull container images for AML extension components |
| storage.googleapis.com | https:443 | Google cloud storage, gcr images are hosted on |
| registry-1.docker.io, production.cloudflare.docker.com  | https:443 | Docker hub registry,required to pull container images for AML extension components |
| auth.docker.io| https:443 | Docker repository authentication, required to access docker hub registry |
| *.kusto.windows.net, *.table.core.windows.net, *.queue.core.windows.net | https:443 | Required to upload and anaylize system logs in Kusto |

### AML workload

Need outbound access to following URLs when submitting any AML workload (training or inference) to the cluster.
  
| Destination Endpoint| Port | Use |
|--|--|--|
| *.azurecr.io | https:443 | Azure container registry, required to pull container images to host training or inference jobs|
| *.blob.core.windows.net | https:443 | Azure blob storage, required to fetch ML project scripts, container images and job logs/metrics|
| *.workspace.<region>.api.azureml.ms ,  <region>.experiments.azureml.net,  <region>.api.azureml.ms | https:443 | Azure mahince learning service api, required to communucate with AML |

### Training job
 
 Need outbound access to following URLs when submitting AML training workloads to the cluster. If the cluster is only used for inferencing, the following URLs are not required.

| Destination Endpoint| Port | Use |
|--|--|--|
| pypi.org | https:443 | Python package index, to install pip packages used to initilize the job environment |
| archive.ubuntu.com, security.ubuntu.com, ppa.launchpad.net | http:80 | This address lets the init container download the required security patches and updates |


>Note: `<region-code>` mapping for Azure cloud regions: eus (East US), weu (West Europe), wcus (West Central US), scus (South Central US), sea (South East Asia), uks (UK South), wus2 (West US 2), ae (Australia East), eus2 (East US 2), ne (North Europe), fc (France Central). `<region>` is the lowcase full spelling, e.g., eastus, southeastasia.
