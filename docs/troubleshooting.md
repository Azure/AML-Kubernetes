## This document is WIP!
# Azure Arc-enabled Machine Learning Trouble Shooting
This document is used to help customer solve problems when using AzureML extension. 
* [General Guide](#general-guide)
* [Extension Installation Guide](#extension-installation-guide)
* [Training Guide](#training-guide)
* [Inference Guide](#inference-guide)


## General Guide

## Extension Installation Guide

1. Check extension resources   
    AzureML extension is released as a helm chart and installed by helm v3. By default, all resources of AzureML extension are installed in azureml namespace. Run ```helm list -a -n azureml``` to check helm chart status. Run ```kubectl get pod -n azureml``` to check status of all agent pods. Run ```kubectl get events -n azureml --sort-by='.lastTimestamp'``` to get events of extension.
1. Do health check for extension   
    If the installation fails, you can use the built-in health check job to make a comprehensive check on the extension, and the check will also produce a report. This report can facilitate us to better locate the problem. Run ```helm test -n azureml <extension-name> --logs``` to trigger the build-in test to generate a health report of the extension. The report is saved in cofigmap named "amlarc-healthcheck" under azureml namespace. Run ```kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.status-test}"``` to get a summary of the report. Run ```kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.reports-test}"``` to get detailed infomation of the report. We recommend that you send us these reports when you need our help to solve the installation problems.
    > Note: The commands of old version are  ```kubectl get configmap -n azureml amlarc-healthcheck --output="jsonpath={.data.status-test-success}"``` and ```kubectl get configmap -n azureml amlarc-healthcheck --output="jsonpath={.data.reports-test-success}"```. When running "helm test" command, Error like "unable to get pod logs for healthcheck-config: pods 'healthcheck-config' not found" should be ignored. 
2. Inference HA  
    For inference azureml-fe agent, HA feature is enabled by default. So, by default, inference feature requires at least 3 nodes to run. The phenomenon that this kind of problem may lead to is that some azureml-fe pods are pending on scheduling and error message of the pod could be like "0/1 nodes are available: 1 node(s) didn't match pod anti-affinity rules".
3. Scoring endpoint  
    If you find that inference-operator pod is crashed and azureml-fe service is in pending or unhealthy state, it is likely that endpoint flags are not set properly. We have ```privateEndpointNodeport``` and ```privateEndpointILB``` flags to control how to expose scoring service. By default public loadbalancer is enabled. For detailed flag usage, please refer to [doc](./deploy-extension.md#review-azureml-deployment-configuration-settings).

4. Skip installation of volcano in the extension
   
   If user have their own volcano suite installed, they can set `volcanoScheduler.enable=false` , so that the extension will not try to install the volcano scheduler. Volcano scheduler and volcano controller are required for job submission and scheduling.

    1. The version of volcano we are using and run tests against with is `1.5.0` , other version may not work as expected.
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
    
        We are using `task-topology` plugins in the scheduler, if user have a volcano version greater than `1.3.0` , please consider enable this plugin.
    
    3. There is a bug in volcano admission and it will break our job, so we disabled `job/validate` webhook explicitly in the volcano admission provided in our extension, user should also patch their volcano admission otherwise the common runtime job won’t work.
    See this [issue](https://github.com/volcano-sh/volcano/issues/1680).

## Training Guide

## Inference Guide





