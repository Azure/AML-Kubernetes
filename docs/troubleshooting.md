## This document is WIP!
# Azure Arc-enabled Machine Learning Trouble Shooting
This document is used to help customer solve problems when using AzureML extension. 

* [Extension Installation Guide](#extension-installation-guide)
    * [How is AzureML extension installed](#how-is-extension-installed)
    * [HealthCheck of extension](#healthcheck)
    * [Inference HA (High availability)](#inference-ha)
    * [Service type of inference scoring endpoint](#inference-service-type)
    * [Skip installation of volcano in the extension](#skip-volcano)
    * [How to validate private workspace endpoint](#valid-private-workspace)
    * [Reuse Prometheus](#prometheus)
    * [Error: Failed pre-install: pod healthcheck failed](#error-healthcheck-failed)
    * [Error: Resources cannot be imported](#error-cannot-imported)
    * [Error: Cannot re-use a name that is still in use](#error-reuse-name)
    * [Error: Earlier operation is in progress](#error-operation-in-progress)
    * [Error: Extension is being terminated](#error-resource-terminating)
    * [Error: Failed in download the Chart path not found](#error-chart-not-found)
    * [Error Code of HealthCheck](#healthcheck-error-code)
* [Training Guide](#training-guide)
* [Inference Guide](#inference-guide)

## Extension Installation Guide
### How is AzureML extension installed <a name="how-is-extension-installed"></a>
AzureML extension is released as a helm chart and installed by Helm V3. By default, all resources of AzureML extension are installed in azureml namespace. Currently, we don't find a way customise the installation error messages for a helm chart. The error message user received is the original error message returned by helm. This is why sometimes vague error messages are returned. But you can utilize the [built-in health check job](#healthcheck) or the following commands to help you debug. You could get more detail Azureml extension information at [Install AzureML extension](./deploy-extension.md). 
```bash
# check helm chart status
helm list -a -n azureml
# check status of all agent pods
kubectl get pod -n azureml
# get events of the extension
kubectl get events -n azureml --sort-by='.lastTimestamp'
# get release history
helm history -n azureml --debug <extension-name>
```
### HealthCheck of extension <a name="healthcheck"></a>
When the installation failed, you can use the built-in health check job to make a comprehensive check on the extension. The job will output a report which is saved in a configmap named "arcml-healthcheck" under azureml namespace. The error codes and possible solutions for the report are list in [Error Code of HealthCheck](#healthcheck-error-code). The health check job will also be automatically triggered in pre-install, pre-upgrade, pre-rollback and pre-delete steps. When aksing [support](./../README.md#support), we recommend that you run the first command below and send the```healthcheck.logs``` file to us, as it can facilitate us to better locate the problem.
```bash
# collect all healthcheck logs when asking support
helm test -n azureml <extension-name> --logs | tee healthcheck.logs

# manually trigger the built-in health check test
helm test -n azureml <extension-name> --logs
# get the report in test step
kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.reports-test}"
# get the report in pre-install step
kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.reports-pre-install}"
# get the report in pre-upgrade step
kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.reports-pre-upgrade}"
# get the report in pre-rollback step
kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.reports-pre-rollback}"
# get the report in pre-delete step
kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.reports-pre-delete}"

# for versions that is older than 1.0.88 the commands should be those
# get a summary of the report
kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.status-test}"
# get detailed information of the report
kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.reports-test}
```
> Note: When running "helm test" command, Error like "unable to get pod logs for healthcheck-config: pods 'healthcheck-config' not found" should be ignored. 
### Inference HA (High availability) <a name="inference-ha"></a>
For inference azureml-fe agent, HA feature is enabled by default. So, by default, the inference feature requires at least 3 nodes to run. The phenomenon that this kind of issue may lead to is that some ```azureml-fe``` pods are pending on scheduling and error message of the pod could be like **"0/1 nodes are available: 1 node(s) didn't match pod anti-affinity rules"**.
### Service type of inference scoring endpoint  <a name="inference-service-type"></a>
It's very important for inference to expose scoring endpoint. According to the cluster configuration and testing scenarios, we have three ways to expose scoring services: **public loadbalancer, private endpoint and nodeport**. Public loadbalancer is used by default. ```privateEndpointNodeport``` and ```privateEndpointILB``` flags are used for the rest two scenarios. For detailed flag usage, please refer to [doc](./deploy-extension.md#review-azureml-deployment-configuration-settings). Many customers got problems in setting up loadbalancer, so we strongly recommend reading the relevant documents and doing some checks before the installation. If you find that inference-operator pod is crashed and azureml-fe service is in pending or unhealthy state, it is likely that endpoint flags are not set properly. 

### Skip installation of volcano in the extension  <a name="skip-volcano"></a>
If user have their own volcano suite installed, they can set `volcanoScheduler.enable=false`, so that the extension will not try to install the volcano scheduler. Volcano scheduler and volcano controller are required for job submission and scheduling.

1. The version of volcano we are using and run tests against with is `1.5.0`, other version may not work as expected.
2. The volcano scheduler config we are using is :  
    ```yaml
    volcano-scheduler.conf: |
        actions: "enqueue, allocate, backfill"
        tiers:
        - plugins:
            - name: task-topology
            - name: priority
            - name: gang
            - name: conformance
        - plugins:
            - name: overcommit
            - name: drf
            - name: predicates
            - name: proportion
            - name: nodeorder
            - name: binpack
    ```
    We are using `task-topology` plugins in the scheduler, if user have a volcano version greater than `1.3.0`, please consider to enable this plugin.

3. There is a bug in volcano admission, and it will break our job, so we disabled `job/validate` webhook explicitly in the volcano admission provided in our extension, user should also patch their volcano admission otherwise the common runtime job won’t work.
See this [issue](https://github.com/volcano-sh/volcano/issues/1680).

### How to validate private workspace endpoint  <a name="valid-private-workspace"></a>
If you setup private endpoint for your workspace, it's important to test its availability before using it. Otherwise, it may cause unknown errors, like installation errors. You can follow the steps below to test if the private workspace endpoint is available in your cluster.
1. The format of private workspace endpoint should be like this ```{workspace_id}.workspace.{region}.api.azureml.ms```. You can find workspace id and region in your workspace portal or through ```az ml workspace``` command.
1. Prepare a pod that can run ```curl``` and ```nslookup``` commands. If you have AzureML extension installed and enabled Inference features, azureml-fe pod is a good choice.
1. Login into the pod. Taking azureml-fe as an example, you need to run ```kubectl exec -it -n azureml $(kubectl get pod -n azureml | grep azureml-fe | awk '{print $1}' | head -1) bash``` 
1. If you don't configure proxy, just run ```nslookup {workspace_id}.workspace.{region}.api.azureml.ms```. If private link from cluster to workspace is set correctly, dns lookup will response an internal IP in VNET. The response should be something like this:
    ```
    Server:         10.0.0.10
    Address:        10.0.0.10:53

    Non-authoritative answer:
    ***

    Non-authoritative answer:
    ***
    ```
1. If you have proxy configured, please run ```curl https://{workspace_id}.workspace.{region}.api.azureml.ms/metric/v2.0/subscriptions/{subscription}/resourceGroups/{resource_group}/providers/Microsoft.MachineLearningServices/workspaces/{workspace_name}/api/2.0/prometheus/post -X POST -x {proxy_address} -d {} -v -k```. If you configured proxy and workspace with private link correctly, you can see it's trying to connect to an internal IP, and get response with http 401 (which is expected as you don't provide token for runhistory). The response should be something like this:
    ```
    Note: Unnecessary use of -X or --request, POST is already inferred. 
    * Trying 172.29.1.81:443... 
    * Connected to ***.workspace.eastus.api.azureml.ms (172.29.1.81) port 443 (#0) 
    * ALPN, offering h2 
    * ALPN, offering http/l.l 

    ***
    {
        "error": { 
            "code": "UserError",
            "severity": null, 
            "message": "Bearer token not provided.", 
            "messageFornat": null, 
            "messageParameters": null, 
            "innerError": { 
                "code": "AuthorizationError",
                "innerError": null
            }
            "debuglnfo" : null, 
            "additionallnfo" :  null 
        }
        ***
    }
    ```

### Reuse Prometheus  <a name="prometheus"></a>
TODO

### Error: Failed pre-install: pod healthcheck failed <a name="error-healthcheck-failed"></a>
Azureml extension contains a HealthCheck hook to check your cluster before the installation. If you got this error, it means some critical errors are found. You can follow [HealthCheck of extension](#healthcheck) to get detailed error message and follow [Error Code of HealthCheck](#healthcheck-error-code) to get some advice. But, in some corner cases, it may also be the problem of the cluster, such as unable to create a pod due to sandbox container issues or unable to pull the image due to network issues. So making sure the cluster is healthy is also very important before the installation.

### Error: resources cannot be imported into the current release: invalid ownership metadata <a name="error-cannot-imported"></a>
This error means there is a confliction between existing cluster resources and AzureML extension. A full error message could be like this: 
```
CustomResourceDefinition "jobs.batch.volcano.sh" in namespace "" exists and cannot be imported into the current release: invalid ownership metadata; label validation error: missing key "app.kubernetes.io/managed-by": must be set to "Helm"; annotation validation error: missing key "meta.helm.sh/release-name": must be set to "amlarc-extension"; annotation validation error: missing key "meta.helm.sh/release-namespace": must be set to "azureml"
```

Follow the steps below to mitigate the issue.
* If the conflict resource is ClusterRole "azureml-fe-role", ClusterRoleBinding "azureml-fe-binding", ServiceAccount "azureml-fe", Deployment "azureml-fe" or other resource related to "azureml-fe", please check if you have Inference AKS v1 installed in your cluster. If yes, please contact us for migration solution ([Support](./../README.md#support)). If not, please follow the steps below.
* Check who owns the problematic resources and if the resource can be deleted or modified. 
* If the resource is used only by AzureML extension and can be deleted, we can manually add labels to mitigate the issue. Taking the previous error message as an example, you can run commands ```kubectl label crd jobs.batch.volcano.sh "app.kubernetes.io/managed-by=Helm" ``` and ```kubectl annotate crd jobs.batch.volcano.sh "meta.helm.sh/release-namespace=azureml" "meta.helm.sh/release-name=<extension-name>"```. Please replace \<extension-name\> with your own extension name. By setting labels and annotations to the resource, it means the resource is managed by helm and owned by AzureML extension. 
* If the resource is also used by other components in your cluster and can't be modified. Please refer to [doc](./deploy-extension.md#review-azureml-deployment-configuration-settings) to see if there is a flag to disable the resource from AzureML extension side. For example, if it's a resource of [Volcano Scheduler](https://github.com/volcano-sh/volcano) and Volcano Scheduler has been installed in your cluster, you can set ```volcanoScheduler.enable=false``` flag to disable it to avoid the confliction or follow [Skip installation of volcano in the extension](#skip-volcano).

### Error: cannot re-use a name that is still in use <a name="error-reuse-name"></a>
This means the extension name you specified already exists. Run ```helm list -Aa``` to list all helm chart in your cluster. If the name is used by other helm chart, you need to use another name. If the name is used by Azureml extension, it depends. You can try to uninstall the extension and reinstall it if possible. Or maybe you need to wait for about an hour and try again after the unknown operation is completed.

### Error: Earlier operation for the helm chart is still in progress <a name="error-operation-in-progress"></a>
You need to wait for about an hour and try again after the unknown operation is completed.

### Error: unable to create new content in namespace azureml because it is being terminated <a name="error-resource-terminating"></a>
This happens when an uninstallation operation is unfinished and another installtion operation is triggered. You can run ```az k8s-extension show``` command to check the provision status of extension and make sure extension has been uninstalled before taking other actions.

### Error: Failed in download the Chart path not found <a name="error-chart-not-found"></a>
Most likely, you specified the wrong extension version. Or the ```--release-train``` flag and ```--version``` flag doesn't match. Please try the default value to mitigate this.


### Error Code of HealthCheck  <a name="healthcheck-error-code"></a>
This table shows how to troubleshoot the error codes returned by the HealthCheck report. For error codes lower than E45000, this is a critical error, which means that some problems must be solved before continuing the installation. For error codes larger than E45000, this is a diagnostic error, which requires further manual analysis of the log to identify the problem.

|Error Code |Error Message | Description |
|--|--|--|
|E40000 | UNKNOWN_ERROR | Unknown error happened. Need to check HealthCheck logs to identify the problem. |
|E40001 | LOAD_BALANCER_NOT_SUPPORT | Load balancer is not supported by your cluster. Please refer to [Service type of inference scoring endpoint](#inference-service-type) for solution |
|E40002 | INSUFFICIENT_NODE | The healthy nodes are insufficient. Maybe your node selector is not set properly. Or you may need to disable [Inference HA](#inference-ha)|
|E40003 | INTERNAL_LOAD_BALANCER_NOT_SUPPORT | Currently, internal load balancer is only supported by AKS. Please refer to [Service type of inference scoring endpoint](#inference-service-type) |
|E45001 | AGENT_UNHEALTHY |There are unhealty resources of AzureML extension. Resources checked by this checker are Pod, Job, Deployment, Daemonset and StatufulSet. From the HealthCheck logs, you can find out which resource is unhealthy. |
|E45002 | PROMETHEUS_CONFLICT | Please refer to [Reuse Prometheus](#prometheus) |
|E45003 | BAD_NETWORK_CONNECTIVITY | Please follow [network-requirements](./network-requirements.md) to check network connectivity. If you are using private link for workspace or other resources, you can refer to doc [private-link](./private-link.md)  |
|E45004 | AZUREML_FE_ROLE_CONFLICT | There exists an "azureml-fe-role" cluster role, but it doesn't belong Azureml extension. Usually, this is because Inference AKS V1 has been installed in your cluster. Please contact us for migration solution. [Support](./../README.md#support)|
|E45005 | AZUREML_FE_DEPLOYMENT_CONFLICT | There exists an "azureml-fe" deployment, but it doesn't belong Azureml extension. Usually, this is because Inference AKS V1 has been installed in your cluster. Please contact us for migration solution. [Support](./../README.md#support)|
|E49999 | CHECKER_PANIC | Checker run into panic. Need to check HealthCheck logs to identify the problem. |
## Training Guide

### UserError: AzureML Kubernetes job failed. : Dispatch Job Fail: Cluster does not support job type RegularJob
Please check whether you have enableTraining=True set when doing the AzureML extension installation. More details could be found at [here](https://github.com/Azure/AML-Kubernetes/blob/master/docs/deploy-extension.md).

### UserError: Unable to mount data store workspaceblobstore. Give either an account key or SAS token.
Credential less machine learning workspace default storage account is not supported right now for training jobs. 

### UserError: Failed to acquire CSI storage account credentials
Error message is:
```yaml
AzureML Kubernetes job failed. 400:{"Msg":"Failed to acquire CSI storage account credentials for mountVolume 'hbiws8397576437-2e2dc25af77dcceea86ae50b45bd1724-secrets', encountered an error: Encountered an error when attempting to connect to Storage Account 'hbiws8397576437': HTTP 403 Forbidden: {\"error\":{\"code\":\"AuthorizationFailed\",\"message\":\"The client '1d0028bc-c1ca-4bdc-8bc0-e5e19cc6f812' with object id '1d0028bc-c1ca-4bdc-8bc0-e5e19cc6f812' does not have authorization to perform action 'Microsoft.Storage/storageAccounts/listKeys/action' over scope '/subscriptions/4aaa645c-5ae2-4ae9-a17a-84b9023bc56a/resourceGroups/youhuaprivatelink/providers/Microsoft.Storage/storageAccounts/hbiws8397576437' or the scope is invalid. If access was recently granted, please refresh your credentials.\"}}","Code":400}
```
This should happen when using HBI workspace, please assign system assigned or user assigned managed identity of the attached compute the access of (“Storage Blob Data Contributor”) and Storage Account Contributor” to the machine learning workspace default storage account by following [this](https://github.com/Azure/AML-Kubernetes/blob/master/docs/managed-identity.md).

### UserError: Failed to acquire CSI storage account credentials
Error message is:
```yaml
AzureML Kubernetes job failed. 400:{"Msg":"Failed to acquire CSI storage account credentials for mountVolume 'hbipleusws6182689148-c8d2ee5daca188bde53fa0711010c53c-secrets', encountered an error: Encountered an error when attempting to connect to Storage Account 'hbipleusws6182689148': Failed to successfully make an http request after 10 attempts. Last inner exception: %!w(\u003cnil\u003e)","Code":400}
```

Please follow [Private Link troubleshooting section](https://github.com/Azure/AML-Kubernetes/blob/master/docs/private-link.md) to check your network settings.

### UserError: Unable to upload project files to working directory in AzureBlob because the authorization failed
Error message is:
```yaml
Unable to upload project files to working directory in AzureBlob because the authorization failed. Most probable reasons are:
 1. The storage account could be in a Virtual Network. To enable Virtual Network in Azure Machine Learning, please refer to https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-enable-virtual-network.
```

Please make sure the storage account has enabled the exceptions of “Allow Azure services on the trusted service list to access this storge account” and the aml workspace is in the resource instances list. And make sure the aml workspace has system assigned managed identity. 

### UserError: Encountered an error when attempting to connect to the Azure ML token service
Error message is:
```yaml
AzureML Kubernetes job failed. 400:{"Msg":"Encountered an error when attempting to connect to the Azure ML token service","Code":400}
```

It should be network issue. Please follow [Private Link troubleshooting section](https://github.com/Azure/AML-Kubernetes/blob/master/docs/private-link.md) to check your network settings. 

### ServiceError: AzureML Kubernetes job failed
Error message is:
```yaml
AzureML Kubernetes job failed. 137:PodPattern matched: {"containers":[{"name":"training-identity-sidecar","message":"Updating certificates in /etc/ssl/certs...\n1 added, 0 removed; done.\nRunning hooks in /etc/ca-certificates/update.d...\ndone.\n * Serving Flask app 'msi-endpoint-server' (lazy loading)\n * Environment: production\n   WARNING: This is a development server. Do not use it in a production deployment.\n   Use a production WSGI server instead.\n * Debug mode: off\n * Running on http://127.0.0.1:12342/ (Press CTRL+C to quit)\n","code":137}]}
```

Check your proxy setting and check whether 127.0.0.1 was added to proxy-skip-range when using “az connectedk8s connect” by following [this](https://github.com/Azure/AML-Kubernetes/blob/master/docs/network-requirements.md). 

## Inference Guide
### InferencingClientCallFailed: The k8s-extension of the Kubernetes cluster is not connectable.

Reattach your compute to the cluster and then try again. If it is still not working, use "kubectl get po -n azureml" to check the relayserver* pods are running. 

### How to check sslCertPemFile and sslKeyPemFile is correct?

Below commands could be used to validate. Expect the second command return "RSA key ok" without prompting you for passphrase.
```yaml
openssl x509 -in cert.pem -text -noout 
openssl rsa -in key.pem -check -noout
```

Below commands could be used to verify whether sslCertPemFile and sslKeyPemFile match:
```yaml
openssl x509 -noout -modulus -in cert.pem 
openssl rsa -noout -modulus -in key.pem 
```


