# Azure Arc-enabled Machine Learning

As part of Azure Machine Learning (AzureML) service capabilities,  Azure Arc enabled ML extends Azure ML service capabilities seamlessly to Kubernetes clusters, and enables customer to train and deploy models on Kubernetes anywhere at scale. With a simple AzureML extension deployment, customer can instantly onboard their data science team with productivity tools for full ML lifecycle, and have access to both Azure managed compute and customer managed Kubernetes anywhere. Customer is flexible to train and deploy models wherever and whenever business requires so. With built-in AzureML pipeline and MLOps support for Kubernetes, customer can scale machine learning adoption in their organization easily. Built on top of Azure Arc hybrid cloud platform, Arc enabled ML natively supports on-premise machine learning with Kubernetes.

This repository is intended to serve as an information hub for customers and partners who are interested in Azure Arc enabled ML public preview. Use this repository for onboarding and testing instructions as well as an avenue to provide feedback, issues, enhancement requests and stay up to date as the preview progresses. 

## Prerequisites

1. An Azure subscription. If you don't have an Azure subscription, [create a free account](https://aka.ms/AMLFree) before you begin.
1. A Kubernetes cluster up and running - **We recommend minimum of 4 vCPU cores and 8GB memory, around 2 vCPU cores and 3GB memory will be used by Azure Arc agent and AzureML extension components**.
1. A ```kubeconfig``` file and context pointing to the Kubernetes cluster.
1. Install the [latest release of Helm 3](https://helm.sh/docs/intro/install/).
1. The Kubernetes cluster is [connected to Azure Arc](https://docs.microsoft.com/azure/azure-arc/kubernetes/quickstart-connect-cluster). For Azure Kubernetes Services (AKS) cluster, connection to Azure Arc is optional.
1. (**Optional**) If the Kubernetes cluster is behind of [an outbound proxy server](https://docs.microsoft.com/azure/azure-arc/kubernetes/quickstart-connect-cluster?tabs=azure-cli#4a-connect-using-an-outbound-proxy-server) or [firewall](https://docs.microsoft.com/azure/firewall/protect-azure-kubernetes-service), please ensure to meet [network requirements](./docs/network-requirements.md). 
1. Meet the pre-requisites listed under the [generic cluster extensions documentation](https://docs.microsoft.com/azure/azure-arc/kubernetes/extensions#prerequisites).
   * Azure CLI version >=**2.24.0**
   * Azure CLI extension k8s-extension version >=**1.0.0**.
1. [Create an AzureML workspace](https://docs.microsoft.com/azure/machine-learning/how-to-manage-workspace?tabs=python) if you don't have one already.
   * [Install and setup the latest AzureML CLI v2](https://docs.microsoft.com/azure/machine-learning/how-to-configure-cli).

## Getting started

Getting started with ArcML is easy with following steps:

* [Deploy AzureML extension Kubernetes cluster](./docs/deploy-extension.md)
* [Attach Kubernetes cluster to AzureML workspace and create a compute target](./docs/attach-compute.md)
* [Train image classification model with AzureML CLI v2](./docs/simple-train-cli.md)
* [Train image classification model with AzureML Python SDK 1.30 or above](./examples/training/simple-train-sdk/img-classification-training.ipynb)
* [Deploy an image classification model - create an endpoint with blue/green deployment](./docs/simple-flow.md)
* [Use AKS on Azure Stack HCI for on-premises machine learning](https://aka.ms/aks-hci-ml)

## Supported AzureML built-features and ArcML unique features

Azure Arc enabled ML essentially brings a new compute target to Azure Machine Learning service. With this new Kubernetes compute target, customer can use existing Azure ML tools and service capabilities to train or deploy model on Kubernetes anywhere. You can git clone available Azure ML examples on the internet, with simple change of compute target name, and those examples will run seamlessly on Kubernetes.

|AzureML built-in features  |ArcML support  |
   |--|--|
   |[Train with the CLI (v2)](https://docs.microsoft.com/azure/machine-learning/how-to-train-cli?view=azure-devops) |&check;|
   |[Train with the job creation UI](https://docs.microsoft.com/azure/machine-learning/how-to-train-with-ui) |&check;|
   |[Train with the Python SDK](https://docs.microsoft.com/azure/machine-learning/how-to-set-up-training-targets) |&check;|
   |[Train with the REST API](https://docs.microsoft.com/azure/machine-learning/how-to-train-with-rest) |&check;|
   |[Basic Python training job](https://docs.microsoft.com/azure/machine-learning/how-to-train-cli?view=azure-devops#basic-python-training-job) |&check;|
   [Distributed training - PyTorch](https://docs.microsoft.com/azure/machine-learning/how-to-train-cli?view=azure-devops#pytorch)|&check;|
   [Distributed training - TensorFlow](https://docs.microsoft.com/azure/machine-learning/how-to-train-cli?view=azure-devops#tensorflow)|&check;|
   [Distributed training - MPI](https://docs.microsoft.com/azure/machine-learning/how-to-train-cli?view=azure-devops#mpi)|&check;|
   [Sweep hyperparameters](https://docs.microsoft.com/azure/machine-learning/how-to-train-cli?view=azure-devops#sweep-hyperparameters)|&check;|
   [Batch Inference](https://docs.microsoft.com/azure/machine-learning/tutorial-pipeline-batch-scoring-classification?view=azure-devops)|&check;|
   |[Deploy model with Online Endpoint - safe production rollout with blue/green deployment](https://docs.microsoft.com/azure/machine-learning/how-to-deploy-managed-online-endpoints)|&check;|
   |[Deploy model with Online Endpoint - REST endpoint with public/private IP and full TLS encryption](https://docs.microsoft.com/azure/machine-learning/how-to-deploy-managed-online-endpoints)|&check;|
   |[Deploy model with isolated Azure Kubernetes Service - VNET and private link support](https://docs.microsoft.com/azure/machine-learning/how-to-deploy-managed-online-endpoints)|&check;|
   |[Build and use ML Pipeline (Python)](https://docs.microsoft.com/azure/machine-learning/how-to-create-machine-learning-pipelines)|&check;|
   |[Train with Designer pipeline](https://docs.microsoft.com/azure/machine-learning/how-to-track-designer-experiments)|&check;|
   |[Train and deploy with AutoML (Python)](https://docs.microsoft.com/azure/machine-learning/how-to-configure-auto-train)|&check;|
   |[Use managed identity to access Azure resources](./docs/managed-identity)|&check;|
   |[Deploy model with Designer UI](https://docs.microsoft.com/azure/machine-learning/how-to-deploy-model-designer)|Coming soon|
   |[Train and deploy with AutoML (Studio UI)](https://docs.microsoft.com/azure/machine-learning/how-to-use-automated-ml-for-ml-models)|Coming soon|
   |[Deploy model with Batch Endpoint](https://docs.microsoft.com/azure/machine-learning/how-to-deploy-managed-online-endpoints)|Coming soon|


In addition to above built-in AzureML features, ArcML also supports following unique machine learning features:

* [Target different instance typs (node types) for training or inference workload deployment](./docs/instance-type.md) 
<!-- * [Train model with NFS](./docs/setup-ephemeral-nfs-volume.md) -->
* [Train model with PV/PVC storage mount](./docs/pvc.md)
* [Assign managed identity to the compute](./docs/managed-identity.md)
* Use managed identity for your endpoint
* [Custom container registry support](https://github.com/Azure/azure-arc-kubernetes-preview/blob/master/docs/custom-registry/connect-cluster.md)
* Multiple AzureML workspaces share the same Kubernetes cluster
* [Deploy model using customer container with built-in model or entry script](./docs/inference-byoc.md). In this case, the model and the entry script will not be saved at the cloud, but in local.
* [Interactive job](https://github.com/Azure/azureml-previews/tree/main/previews/interactive-job) to access your training compute using VS Code, Jupyter Notebook, Jupyter Lab, and summarize metrics with Tensorboard. Sign up [here](https://forms.office.com/pages/responsepage.aspx?id=v4j5cvGGr0GRqy180BHbR8PsZ1-HON9JqtABfkUgwtpUNUtMWTEyRklBQUk2RzZQTUZGTjBUQzJINy4u) to get access to its Github repo.

## Supported Kubernetes distributions and versions

* Azure Kubernetes Services (AKS)
* AKS Engine
* AKS on Azure Stack HCI
* Azure RedHat OpenShift Service (ARO)
* OpenShift Container Platform (OCP)
* Google GKE  
* Canonical Kubernetes Distribution
* Amazon EKS 
* Kind
* K3s-Lightweight Kubernetes 
* Kubernetes 1.18.x, 1.19.x, 1.20.x, 1.21.x

## [Frequently Asked Questions](./docs/faq.md)

## [Release notes](./docs/release-notes.md) 

## [Limitations and known issues](./docs/limitations-and-known-issues.md)

## Support

We are always looking for feedback on our current experiences and what we should work on next. If there is anything you would like us to prioritize, please feel free to suggest so via our [GitHub Issue Tracker](https://github.com/Azure/AML-Kubernetes/issues). You can submit a bug report, a feature suggestion or participate in discussions.

Or reach out to us: amlarc-pm@microsoft.com if you have any questions or feedback.

## Activities

* [Check for known issues](https://github.com/Azure/amlk8s-preview/labels/known-issue)
* [View general feedback](https://github.com/Azure/amlk8s-preview/labels/feedback)
* [Browse roadmap items](https://github.com/Azure/amlk8s-preview/labels/roadmap)
* [Open a bug, provide feedback, or suggest an improvement](https://github.com/Azure/amlk8s-preview/issues/new/choose)

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

![Impressions](https://PixelServer20190423114238.azurewebsites.net/api/impressions/CMK8s-Samples/README.png)

## Disclaimer

The lifecycle management (health, kubernetes version upgrades, security updates to nodes, scaling, etc.) of the AKS or Arc enabled Kubernetes cluster is the responsibility of the customer.

For AKS, read what is managed and what is shared responsibility [here](https://docs.microsoft.com/azure/aks/support-policies)

All preview features are available on a self-service, opt-in basis and are subject to breaking design and API changes. Previews are provided "as is" and "as available," and they're excluded from the service-level agreements and limited warranty.
