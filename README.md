# Azure Machine Learning anywhere with Kubernetes (AzureML anywhere)

As part of Azure Machine Learning (AzureML) service capabilities, AzureML anywhere extends AzureML service capabilities seamlessly from Azure cloud setting to any infrastructure across on-premises, multicloud, and the edge. With a simple AzureML extension deployment, you can instantly onboard your teams of ML professionals with productivity tools for full ML lifecycle, and have access to both Azure managed compute and customer managed Kubernetes anywhere. Your teams of ML professionals are flexible to build, train, and deploy models wherever and whenever business requires so and get consistent ML experience across different infrastructures.

This repository is intended to serve as an information hub for customers and partners who are interested in Azure Machine Learning anywhere with Kubernetes. Use this repository for onboarding and testing instructions as well as an avenue to provide feedback, issues, enhancement requests and stay up to date as the product evolves. 

## Prerequisites

1. A Kubernetes cluster up and running - **We recommend minimum of 4 vCPU cores and 8GB memory, around 2 vCPU cores and 3GB memory will be used by Azure Arc agent and AzureML extension components**.
1. Other than Azure Kubernetes Services (AKS) cluster in Azure, you must connect your Kubernetes cluster to Azure Arc. Please follow instructions in [connect existing Kubernetes cluster to Azure Arc](https://docs.microsoft.com/azure/azure-arc/kubernetes/quickstart-connect-cluster).
   * if you have Azure RedHat OpenShift Service (ARO) cluster or OpenShift Container Patform (OCP) cluster, follow additional prerequisite step [here](./docs/deploy-on-ocp.md) before AzureML extension deployment.
1. If you have AKS cluster in Azure, Azure Arc connection is not required. Register the AKS-ExtensionManager feature flag by using the ```az feature register``` command, as shown in the following example:
   ```azurecli
   az feature register --namespace "Microsoft.ContainerService" --name "AKS-ExtensionManager"
   ```
1. [Install or upgrade Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli) to version >=2.16.0
1. Install Azure CLI extension ```k8s-extension``` (version>=1.0.0) by running ```az extension add --name k8s-extension```

## Getting started

Getting started with AzureML anywhere is easy with following steps:

1. [Deploy AzureML extension](./docs/deploy-extension.md)
1. [Attach Kubernetes cluster to AzureML workspace and create a compute target](./docs/attach-compute.md)
1. [Train image classification model with AzureML CLI v2](./docs/simple-train-cli.md)
1. [Deploy a trained image classification model](./docs/simple-flow.md)
1. [Trouble shooting guide](./docs/troubleshooting.md)

## Supported AzureML built-in features and unique features for Kubernetes

AzureML anywhere essentially brings a new compute target to Azure Machine Learning service. With this new Kubernetes compute target, you can use existing AzureML tools and service capabilities to build, train, and deploy model on Kubernetes cluster anywhere. This seamless integration supports many AzureML built-in features , and existing [AzureML examples](https://github.com/Azure/azureml-examples) can run on Kubernetes cluster with a smple change of compute target name.

In addition to many built-in AzureML features support, AzureML anywhere also supports following unique features leveraging native Kubernetes capability:

* [Run training or inference workload with custom instance types for resource efficiency](./docs/instance-type.md) 
* [Train model with PV/PVC storage mount](./docs/pvc.md)
* [Assign managed identity to the compute](./docs/managed-identity.md)
* Use managed identity for your endpoint
* [Custom container registry support](https://github.com/Azure/azure-arc-kubernetes-preview/blob/master/docs/custom-registry/connect-cluster.md)
* Multiple AzureML workspaces share the same Kubernetes cluster
* [Deploy model using custom container with built-in model or entry script](./docs/inference-byoc.md). In this case, the model and the entry scripts will stay on-premises localy and not uploaded to Azure cloud.

## Supported Kubernetes distributions, versions and locations

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
* Kubernetes 1.18.x, 1.19.x, 1.20.x, 1.21.x, 1.22.x
* Azure location availability: East US, East US 2, South Central US, West US 2, Australia East, Southeast Asia, North Europe, UK South, West Europe, West Central US, Central US, North Central US, West US, Korea Central, France Central

## Additional resources

### [Use AKS on Azure Stack HCI for on-premises machine learning](https://aka.ms/aks-hci-ml)

### [Frequently Asked Questions](./docs/faq.md)

### [Release notes](./docs/release-notes.md) 

### [Limitations and known issues](./docs/limitations-and-known-issues.md)

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
