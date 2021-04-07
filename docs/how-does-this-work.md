## How does AML work with Azure Kubernetes Service(AKS) and Azure Arc for Kubernetes?

### What is the AML agent ?
   
   The Azure ML agent is a set of Kubernetes pods consisting of Kubernetes Operators, CRD's, pods, init jobs etc that can be deployed on an OSS Kubernetes cluster. Attaching 
   a Kubernetes cluster(with the AML agent) to an [Azure ML workspace](https://docs.microsoft.com/azure/machine-learning/concept-workspace) allows the AML control plane to be able to talk to this Kubernetes cluster and deploy Azure ML workloads on this cluster.

### How does the integration with Azure Kubernetes Service work?

   Currently, when you attach an AKS cluster in the AML Studio, the AML control plane deploys the AML agent on the AKS cluster through a Helm Chart deployment. Once this chart is deployed successfully, you should verify all the pods are running successfully.
   
   ```
    sauryadas@Sauryas-MacBook-Pro  ~  kubectl get pods -n azureml
    NAME                                             READY   STATUS      RESTARTS   AGE
    aml-mpi-operator-847689c694-kvwdc                1/1     Running     31         84d
    aml-operator-55bb7d4784-h2v6t                    1/1     Running     38         84d
    aml-pytorch-operator-7fd644b97c-c44j6            1/1     Running     31         84d
    aml-tf-job-operator-7c5848bd4c-lmbqw             1/1     Running     31         84d
    azureml-connector-admission-59bdc7489-64xwr      1/1     Running     0          84d
    azureml-connector-admission-init-flv9w           0/1     Completed   0          84d
    azureml-connector-controllers-7c6fc78b6b-xzm9b   1/1     Running     0          84d
    azureml-connector-scheduler-7845fc897b-2lvvq     1/1     Running     0          84d
    cmaks-init-job-94mpp                             0/1     Completed   0          84d
    compute-exporter-d5866df74-f4zjt                 1/1     Running     0          84d
    job-exporter-rwgt5                               1/1     Running     0          84d
    job-exporter-vtzkt                               1/1     Running     0          84d
    job-exporter-zl6g9                               1/1     Running     0          12d
    metric-reporter-6756b7dbf8-zdllv                 1/1     Running     0          84d
    prometheus-deployment-696b5c8bf8-nqj29           1/1     Running     0          84d
    relay-server-6c476c7477-phpm4                    1/1     Running     0          84d
    rest-server-6b76db489c-2jngc                     1/1     Running     0          84d
   ```
   
  ##### NOTE: This behavior is going to change when AKS enables [Cluster extensions](https://docs.microsoft.com/azure/azure-arc/kubernetes/conceptual-extensions). At that time, we will require the use of the k8s extensions API/clients to install the AML agent before attaching an AKS cluster to an Azure ML workspace


### How does the integration with Azure Arc enabled Kubernetes work?
    
  - Learn about Azure Arc Enabled Kubernetes [here](https://docs.microsoft.com/en-us/azure/azure-arc/kubernetes/overview); once a kubernetes cluster is registered in Azure (given an ARM id), one can view those clusters in the AKS portal
  - Azure Arc enabled Kubernetes has a [cluster extensions](https://docs.microsoft.com/azure/azure-arc/kubernetes/extensions) functionality that enables the ability to install various agents including Azure policy, monitoring, ML, etc.
  - Azure ML requires the use of the cluster extension to deploy the Azure ML agent on the Arc Kubernetes cluster
  - Once the above step is complete, one can attach the Kubernetes cluster to the Azure ML workspace
  
