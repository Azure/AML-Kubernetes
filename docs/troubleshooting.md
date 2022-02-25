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
1. Check extension agent status locally  
    By default, AzureML extension is installed in azureml namespace. Run ```helm list -a -n azureml``` to check helm chart status. Run ```kubectl get pod -n azureml``` to check status of all agent pods. Run ```kubectl get events -n azureml --sort-by='.lastTimestamp'``` to get events of extension.
1. Get health check report of extension  
    Run ```helm test -n azureml <extension-name> --logs``` to trigger the build-in test to generate a health report of the extension. The report is saved in cofigmap named "amlarc-healthcheck" under azureml namespace. Run ```kubectl get configmap -n azureml amlarc-healthcheck --output="jsonpath={.data.status-test-success}"``` to get a summary of the report. Run ```kubectl get configmap -n azureml amlarc-healthcheck --output="jsonpath={.data.reports-test-success}"``` to get detailed infomation of the report. 

## Training Guide

## Inference Guide





