## This document is WIP!
# Azure Arc-enabled Machine Learning Trouble Shooting
This document is used to help customer solve problems when using AzureML extension. 
* [General Guide](#general-guide)
* [Extension Installation Guide](#extension-installation-guide)
* [Training Guide](#training-guide)
* [Inference Guide](#inference-guide)


## General Guide

## Extension Installation Guide

### 1. How is AzureML extension installed   
AzureML extension is released as a helm chart and installed by Helm V3. By default, all resources of AzureML extension are installed in azureml namespace. Currently, we don't find a way customise the installation error messages for a helm chart. The error message user received is the original error message returned by helm. This is why sometimes vague error messages are returned. But you can utilize the [built-in health check job](#2-do-health-check-for-extension) or the following commands to help you debug.
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
### 2. Do health check for extension   
If the installation fails, you can use the built-in health check job to make a comprehensive check on the extension, and the check will also produce a report. This report can facilitate us to better locate the problem. We recommend that you send us these reports when you need our help to solve the installation problems. The report is saved in configmap named "amlarc-healthcheck" under azureml namespace.
```bash
# trigger the built-in test to generate a health report of the extension
helm test -n azureml <extension-name> --logs
# get a summary of the report
kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.status-test}"
# get detailed information of the report
kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.reports-test}"

# for versions that is older than 1.0.75, the commands should be those
kubectl get configmap -n azureml amlarc-healthcheck --output="jsonpath={.data.status-test-success}"
kubectl get configmap -n azureml amlarc-healthcheck --output="jsonpath={.data.reports-test-success}"
```
> Note: When running "helm test" command, Error like "unable to get pod logs for healthcheck-config: pods 'healthcheck-config' not found" should be ignored. 
### 3. Inference HA(High availability)  
For inference azureml-fe agent, HA feature is enabled by default. So, by default, the inference feature requires at least 3 nodes to run. The phenomenon that this kind of issue may lead to is that some azureml-fe pods are pending on scheduling and error message of the pod could be like "0/1 nodes are available: 1 node(s) didn't match pod anti-affinity rules".
### 4. Inference scoring endpoint  
It's very important for inference to expose scoring endpoint. According to the cluster configuration and testing scenarios, we have three ways to expose scoring services: **public loadbalancer, private endpoint and nodeport**. Public loadbalancer is used by default. ```privateEndpointNodeport``` and ```privateEndpointILB``` flags are used for the rest two scenarios. For detailed flag usage, please refer to [doc](./deploy-extension.md#review-azureml-deployment-configuration-settings). Many customers got problems in setting up loadbalancer, so we strongly recommend reading the relevant documents and doing some checks before the installation. If you find that inference-operator pod is crashed and azureml-fe service is in pending or unhealthy state, it is likely that endpoint flags are not set properly. 
### 5. Error: resources cannot be imported into the current release: invalid ownership metadata
If you get error like ```CustomResourceDefinition "queues.scheduling.volcano.sh" in namespace "" exists and cannot be imported into the current release: invalid ownership metadata; label validation error: missing key "app.kubernetes.io/managed-by": must be set to "Helm"; annotation validation error: missing key "meta.helm.sh/release-name": must be set to "amlarc-extension"; annotation validation error: missing key "meta.helm.sh/release-namespace": must be set to "azureml"```, that means there is a confliction between existing cluster resources and AzureML extension. Follow the steps below to mitigate the issue.
* Check who owns the problematic resources and if the resource can be deleted or modified. 
* If the resource is used only by AzureML extension and can be deleted, we can manually add labels to mitigate the issue. Taking the previous error message as an example, we can run commands ```kubectl label crd queues.scheduling.volcano.sh "app.kubernetes.io/managed-by=Helm" ``` and ```kubectl annotate crd queues.scheduling.volcano.sh "meta.helm.sh/release-namespace=azureml" "meta.helm.sh/release-name=<extension-name>"```. Please replace \<extension-name\> with your own extension name. By setting labels and annotations to the resource, it means the resource is managed by helm and owned by AzureML extension. 
* If the resource is also used by other components in your cluster and can't be modified. Please refer to [doc](./deploy-extension.md#review-azureml-deployment-configuration-settings) to see if there is a flag to disable the resource from AzureML extension side. Taking the previous error message as an example, it's a resource of [Volcano Scheduler](https://github.com/volcano-sh/volcano). If Volcano Scheduler has been installed in your cluster, you can set ```volcanoScheduler.enable=false``` flag to disable it to avoid the confliction.

### 6. Skip installation of volcano in the extension  
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

### 7. How to validate private workspace endpoint 
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
## Training Guide

## Inference Guide





