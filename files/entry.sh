#!/bin/bash

AZ_K8S_EXTENSION_VERSION='1.2.2'
AZ_CONNECTED_K8S_VERSION='1.2.8'

az extension add --name connectedk8s --version $AZ_CONNECTED_K8S_VERSION
az extension add --name k8s-extension --version $AZ_K8S_EXTENSION_VERSION

python deploy.py
