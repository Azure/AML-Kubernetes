New features are released at a biweekly cadance. 

**Aug 29, 2022 Release**

Version 1.1.9
* Improved health check logic
* Fixed some bugs

**Jun 23, 2022 Release**

Version 1.1.6
* Bugs fix

**Jun 15, 2022 Release**

Version 1.1.5
* Updated training to use new common runtime to run jobs
* Removed Azure Relay usage for Aks extension
* Removed service bus usage from the extension
* Updated security context usage
* Updated inference scorefe to v2
* Updated to use Volcano as training job scheduler
* Bugs fix

**Oct 14, 2021 Release**

* [PV/PVC volume mount support in AMLArc training job](./pvc.md).

**Sept 16, 2021 Release**

* New regions available, WestUS, CentralUS, NorthCentralUS, KoreaCentral.
* Job queue explanability. See job queue details in AML Workspace Studio.
* Auto-killing policy. Support `max_run_duration_seconds` in ``ScriptRunConfig``. The system will attempt to automatically cancel the run if it took longer than the setting value.
* Performance improvement on cluster autoscale support.
* [Arc agent and ML extension deployment from on-prem container registry](https://github.com/Azure/azure-arc-kubernetes-preview/blob/master/docs/custom-registry/connect-cluster.md) 

**August 24, 2021 Release**

* [Compute instance type is supported in job YAML](./docs/simple-train-cli.md).  
* [Assign Managed Identity to AMLArc compute](./docs/managed-identity.md)

**August 10, 2021 Release**

* New Kubernetes distribution support, K3S - Lightweight Kubernetes. 
* [Deploy AzureML extension to your AKS cluster without connecting via Azure Arc](./docs/deploy-ml-extension-on-AKS-without-arc.md).
* [Automated Machine Learning (AutoML) via Python SDK](https://docs.microsoft.com/en-us/azure/machine-learning/concept-automated-ml) 
* [Use 2.0 CLI to attach the Kubernetes cluster to AML Workspace](./docs/attach-compute.md#Create-compute-target-via-Azure-ML-2.0-CLI)
* Optimize AzureML extension components CPU/memory resources utilization. 

**July 2, 2021 Release**

* New Kubernetes distributions support, OpenShift Kubernetes and GKE (Google Kubernetes Engine). 
* Autoscale support. If the user-managed Kubernetes cluster enables the autoscale, the cluster will be automatically scaled out or scaled in according to the volume of active runs and deployments.  
* Performance improvement on job laucher, which shortens the job execution time to a great deal.
