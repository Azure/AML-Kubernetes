## Meet network requirements
Clusters running behind an outbound proxy server or firewall need additional network configurations. Fulfill [Azure Arc network requirements](https://docs.microsoft.com/en-us/azure/azure-arc/kubernetes/quickstart-connect-cluster?tabs=azure-cli#meet-network-requirement) needed by Azure Arc agents. 

Considering the parameter --proxy-skip-range when installing Arc, please make sure that `127.0.0.1` and `localhost` are added for ArcML.

Besides that, the following outbound URLs are required for Azure Machine Learning,

| Outbound Endpoint| Port | Description|Training |Inference |
|--|--|--|--|--|
| *.kusto.windows.net,<br> \*.table.core.windows.net, <br>\*.queue.core.windows.net | https:443 | Required to upload system logs to Kusto. You can skip this if you have a data exfiltration concern to add table and queue FQDNs, but you cannot get the error diagnosis support from Microsoft.|**&check;**|**&check;**|
| \<your ACR name>\.azurecr.io<br>\<your ACR name>\.\<region name>\.data.azurecr.io | https:443 | Azure container registry, required to pull docker images used for machine learning workloads.|**&check;**|**&check;**|
| \<your Storage Account name>\.blob.core.windows.net | https:443 | Azure blob storage, required to fetch machine learning project scripts,data or models, and upload job logs/outputs.|**&check;**|**&check;**|
| \<your AML workspace ID\>.workspace.\<region\>.api.azureml.ms ,<br>  \<region\>.experiments.azureml.net, <br> \<region\>.api.azureml.ms | https:443 | Azure mahince learning service API.|**&check;**|**&check;**|
| pypi.org | https:443 | Python package index, to install pip packages used for training job environment initialization.|**&check;**|N/A|

> [!NOTE]
> `<region>` is the lowcase full spelling of Azure Region, for example, eastus, southeastasia.
>
> `<your AML workspace ID>` can be found in Azure portal - your Machine Learning resource page - Properties - Workspace ID.
