## This document is WIP!
# AzureML Extension Trouble Shooting
This document is used to help customer solve problems when using AzureML extension. 
* [General Guide](#general-guide)
* [Installation Guide](#installation-guide)
* [Training Guide](#training-guide)
* [Inference Guide](#inference-guide)


## General Guide

## Installation Guide

1. Installation framework  
    AzureML extension is released as a helm chart and installed by helm v3.
1. Check extension agents status locally  
    By default, AzureML extension is installed in azureml namespace. Run ```helm list -a -n azureml``` to check helm chart status. Run ```kubectl get pod -n azureml``` to check status of all agent pods. Run ```kubectl get events -n azureml --sort-by='.lastTimestamp'``` to get events of extension.
1. Get health check report of extension  
    Run ```helm test -n azureml <extension-name> --logs``` to trigger the build-in test to generate a health report of the extension. The report is saved in cofigmap named "amlarc-healthcheck" under azureml namespace. Run ```kubectl get configmap -n azureml amlarc-healthcheck --output="jsonpath={.data.status-test-success}"``` to get a summary of the report. Run ```kubectl get configmap -n azureml amlarc-healthcheck --output="jsonpath={.data.reports-test-success}"``` to get detailed infomation of the report. You can debug the installation errors according to the report or send the report back to us for debug.
1. Inference HA  
    For inference scoring-fe agent, HA feature is enabled by default. So, by default, inference feature requires at least 3 nodes to run. The phenomenon that this kind of problem may lead to is that some azureml-fe pods are pending on scheduling and error message of the pod could be like "0/1 nodes are available: 1 node(s) didn't match pod anti-affinity rules".
1. Scoring endpoint 
    If you find that inference-operator pod is crashed and azureml-fe service is in pending or unhealthy state, it is likely that endpoint flags are not set properly. We have ```privateEndpointNodeport``` and ```privateEndpointILB``` flags to control how to expose scoring service. By default public loadbalancer is enabled. For detailed flag usage, please refer to [doc](./deploy-extension.md#review-azureml-deployment-configuration-settings).

## Training Guide

## Inference Guide





