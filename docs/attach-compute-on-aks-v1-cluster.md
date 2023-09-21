Sure, here is a possible better version of the markdown document:

# How to use an existing AKS v1 compute as a v2 Kubernetes compute (Preview)

## Introduction

Azure Machine Learning (AML) supports two types of Kubernetes compute targets: AKS v1 and Kubernetes v2. AKS v1 compute is a managed AKS cluster that can only run inference workloads. Kubernetes v2 compute is a generic Kubernetes cluster that can run both training and inference workloads, and supports Azure Arc-enabled Kubernetes clusters.

If you have an existing AKS cluster that is already attached as an AKS v1 compute to your AML workspace, you may want to use it as a Kubernetes v2 compute as well, without creating a new cluster. This document will guide you through the steps to achieve this. By using an existing AKS v1 compute as a Kubernetes v2 compute, you can leverage the benefits of both types of compute targets, such as:

- Reduce the cost and complexity of managing multiple clusters
- Use the same cluster for both training and inference scenarios
- Take advantage of the features and capabilities of Kubernetes v2 compute

## Prerequisites

Before you begin, make sure you have the following:

- An AKS cluster that is already attached as an AKS v1 compute to your AML workspace.
- The Microsoft.AzureML.Kubernetes extension type registered in your subscription. You can use the following command to register it:

```bash
az provider register --namespace Microsoft.AzureML.Kubernetes --wait
```

## Steps

### Step 1: Add an annotation to the existing deployment

You need to add an annotation "azureml-fe-enable-upgrade"=true to the existing deployment "azureml-fe" in the default namespace. You can use the following command to add this annotation:

```bash
kubectl annotate deployment azureml-fe azureml-fe-enable-upgrade=true
```

You should see a message like this:

```bash
deployment.apps/azureml-fe annotated
```

### Step 2: Install the extension with extra configuration

When installing the extension, you need to provide an extra configuration "scoringFe.enableUpgrade=true" to enable the upgrade feature. This configuration will allow the extension to install on a cluster with an existing azureml-fe. Here's an example command with this extra configuration:

```bash
az k8s-extension create --name <extension-name> --extension-type Microsoft.AzureML.Kubernetes --config enableTraining=True enableInference=True inferenceRouterServiceType=LoadBalancer scoringFe.enableUpgrade=true --config-protected sslCertPemFile=<file-path-to-cert-PEM> sslCertKeyFile=<file-path-to-cert-KEY> --cluster-type managedClusters --cluster-name <your-cluster-name> --resource-group <your-RG-name> --scope cluster
```

You can check the status of the extension installation by using this command:

```bash
az k8s-extension show --name <extension-name> --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <your-RG-name>
```
More details about installing the extension can be found in this document: [Deploy AzureML extension to your Kubernetes cluster](./deploy-extension.md)

### Step 3: Attach the cluster to the workspace as a v2 Kubernetes compute

After installing the extension, you can attach the cluster to your workspace as a v2 Kubernetes compute as normal. You can use the Azure ML CLI, the Azure ML Studio UI, or the Azure ML Python SDK to do this. For more details, you can refer to this document: [Attach Kubernetes cluster to AzureML workspace and create a compute target](./attach-compute.md)

## Limitations

* The scoring URL for v1 compute and the scoring URL for v2 compute are not segregated. This means that both deployments can access and serve the models and online deployments that are registered on either compute. This may cause some confusion or conflicts when deploying or consuming models on different computes.
* When attaching v2 Kubernetes compute, the namespace should not be the same as the v1 compute's namespace. Otherwise, the online deploymentes on v2 compute may conflict with the webservices on v1 compute. The namespace for v1 compute follows the pattern: `azureml-<workspace-name>`.