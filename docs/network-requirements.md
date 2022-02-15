## Meet network requirements
Clusters running behind an outbound proxy server or firewall need additional network configurations. Fulfill [Azure Arc network requirements](https://docs.microsoft.com/en-us/azure/azure-arc/kubernetes/quickstart-connect-cluster?tabs=azure-cli#meet-network-requirement) needed by Azure Arc agents. Besides that, the following outbound URLs are required for Azure Machine Learning,

| Outbound Endpoint| Port | Description|Training |Inference |
|--|--|--|--|--|
| *.kusto.windows.net,<br> *.table.core.windows.net, <br>*.queue.core.windows.net | https:443 | Required to upload system logs to Kusto. |**&check;**|**&check;**|
| *.azurecr.io | https:443 | Azure container registry, required to pull docker images used for machine learning workloads.|**&check;**|**&check;**|
| *.blob.core.windows.net | https:443 | Azure blob storage, required to fetch machine learning project scripts,data or models, and upload job logs/outputs.|**&check;**|**&check;**|
| *.workspace.\<region\>.api.azureml.ms ,<br>  \<region\>.experiments.azureml.net, <br> \<region\>.api.azureml.ms | https:443 | Azure mahince learning service API.|**&check;**|**&check;**|
| pypi.org | https:443 | Python package index, to install pip packages used for training job environment initialization.|**&check;**|N/A|
| archive.ubuntu.com, <br> security.ubuntu.com,<br> ppa.launchpad.net | http:80 | Required to download the necessary security patches. |**&check;**|N/A|

> [!NOTE]
> `<region>` is the lowcase full spelling of Azure Region, for example, eastus, southeastasia.
