## This document is WIP!
# Azure Arc-enabled Machine Learning Trouble Shooting
This document is used to help customer solve problems when using AzureML extension. 
* [General Guide](#general-guide)
* [Extension Installation Guide](#extension-installation-guide)
* [Training Guide](#training-guide)
* [Inference Guide](#inference-guide)


## General Guide

## Extension Installation Guide

### 1. Check extension resources   
AzureML extension is released as a helm chart and installed by helm v3. By default, all resources of AzureML extension are installed in azureml namespace. Run ```helm list -a -n azureml``` to check helm chart status. Run ```kubectl get pod -n azureml``` to check status of all agent pods. Run ```kubectl get events -n azureml --sort-by='.lastTimestamp'``` to get events of extension.
### 2. Do health check for extension   
If the installation fails, you can use the built-in health check job to make a comprehensive check on the extension, and the check will also produce a report. This report can facilitate us to better locate the problem. Run ```helm test -n azureml <extension-name> --logs``` to trigger the built-in test to generate a health report of the extension. The report is saved in configmap named "amlarc-healthcheck" under azureml namespace. Run ```kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.status-test}"``` to get a summary of the report. Run ```kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.reports-test}"``` to get detailed information of the report. We recommend that you send us these reports when you need our help to solve the installation problems.
> Note: The commands of old version are  ```kubectl get configmap -n azureml amlarc-healthcheck --output="jsonpath={.data.status-test-success}"``` and ```kubectl get configmap -n azureml amlarc-healthcheck --output="jsonpath={.data.reports-test-success}"```. When running "helm test" command, Error like "unable to get pod logs for healthcheck-config: pods 'healthcheck-config' not found" should be ignored. 
### 3. Inference HA  
For inference azureml-fe agent, HA feature is enabled by default. So, by default, the inference feature requires at least 3 nodes to run. The phenomenon that this kind of issue may lead to is that some azureml-fe pods are pending on scheduling and error message of the pod could be like "0/1 nodes are available: 1 node(s) didn't match pod anti-affinity rules".
### 4. Scoring endpoint  
If you find that inference-operator pod is crashed and azureml-fe service is in pending or unhealthy state, it is likely that endpoint flags are not set properly. We have ```privateEndpointNodeport``` and ```privateEndpointILB``` flags to control how to expose scoring service. By default, public loadbalancer is enabled. For detailed flag usage, please refer to [doc](./deploy-extension.md#review-azureml-deployment-configuration-settings).
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

### 7. Verify Workspace private endpoint 

## Training Guide

## Inference Guide





