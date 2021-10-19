
# Frequently Asked Questions 

## Who is Azure Arc enabled Machine Learning intended for?

With increasing adoption of Kubernetes for machine learning among enterprises, Azure Machine Learning provides enterprise ML infrastructure team to easily setup and enable Kubernetes for their data science teams to use. At the same time, data scientists can focus on building high quality models and model deployment professionals can focus on scaling models production without getting involved about Kubernetes technical details. 

## Why should I use Azure Arc enabled Machine Learning for model deployment?

Many enterprises want to start machine learning now with where data lives today, which could be in multi-cloud or on-premises. Enterprises also want to optimize IT operation to leverage wherever workload is available. With flexibility of cloud-native development provided by Kubernetes, enterprises now can spin up Kubernetes cluster anywhere to meet their machine learning needs, at the same time to address security and privacy compliance requirements in a highly regulated environment. With Azure Arc enabled Machine Learning, enterprises now can have hybrid machine learning lifecycle such as train models in cloud and deploy models on-premises, or train models on-premises and deploy models in cloud, to leverage where compute and data available and broaden service access.

## How do I use Azure Arc enabled Machine Learning?

Enterprise IT operator can easily setup and enable Kubernetes for Azure Machine Learning with the following steps:

* Spin up a Kubernetes cluster anywhere
* Connect Kubernetes cluster to Azure cloud via Azure Arc
* Deploy AzureML extension to Azure Arc enabled Kubernetes cluster
* Attach Azure Arc enabled Kubernetes cluster to Azure ML workspace and create compute target for data science teams to use

Once Kubernetes cluster is enabled for Azure Machine Learning, data science professionals can discover Kubernetes compute targets in AzureML workspace or through CLI command, and use those compute targets to submit training job or deploy model.

## How does model deployment with Azure Arc enabled Machine Learning compare to Azure Machine Learning Managed Online Endpoint?

Azure Machine Learning aims to provide different model deployment funnels to serve enterprise needs. For enterprises who want to scale model production by leveraging powerful CPU or GPU in cloud and leave Azure to manage compute, Azure Machine Learning Managed Online Endpoint is the preferred choice. For enterprises who want to deploy and serve model in multi-cloud and on-premises, and want to manage their own compute infrastructure, Azure Arc enabled Machine Learning would be the preferred choice. Regardless of which underlying model deployment infrastructure, Azure Machine Learning model deployment shares the same concepts such as online endpoint and the same CLI/SDK/Studio UI tooling.

## How does Azure Arc enabled Machine Learning AKS support compare to current AzureML AKS inference support that is in GA?

## Recommended AKS cluster resources

We recommend you use a at least 3 nodes cluster, each node having at least 2C 4G. And if you want to running GPU jobs, you need some GPU nodes.

## Why the nodes run occupied in a run is more than node count in run list?

The node count in the number of worker, for distribute training job, such as ps-worker or MPI/horovod they may need extra launcher node or ps node, they may also ocuppy one node. We will optimise this in following version.

## What Azure storage does Azure Arc-enabled ML support?

Azure Arc-enabled ML compute only support Azure blob container, if your data is in other Azure storage, please move it to Azure blob first. We will support other Azure storage in following iteration.
