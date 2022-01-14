#!/bin/bash

set -e

subscription_id="<YOUR_SUBSCRIPTION_ID>"
resource_group="<YOUR_RESOURCE_GROUP>"
workspace_name="<YOUR_WORKSPACE_NAME>"
v1_compute="<YOUR_COMPUTE_TARGET>" # Compute target of your aks/aci service
v1_service_name="<YOUR_SERVICE_NAME>" # Service name of your aks/aci service
local_dir="<PATH_TO_DOWNLOAD_EXPORTED_FILES>"

migrate_type="<MIGRATION_TYPE>" # AmlArc/Managed
cluster_name="<CLUSTER_NAME>" # required for AmlArc
compute_name="arcml-compute" # required for AmlArc
compute_namespace="<COMPUTE_NAMESPACE>"
online_endpoint_name="<ONLINE_ENDPOINT_NAME>"
online_deployment_name="<ONLINE_DEPLOYMENT_NAME>"

# OPTIONAL STEP) Attach compute for AmlArc, make sure your cluster have installed AmlArc successfully
if [[ $migrate_type == "AmlArc" ]]
then
  resource_id="/subscriptions/$subscription_id/resourceGroups/$resource_group/providers/Microsoft.ContainerService/managedClusters/$cluster_name"
  # If you are providing an arc-enabled cluster, using the resource id below
  # resource_id="/subscriptions/$subscription_id/resourceGroups/$resource_group/providers/Microsoft.ContainerService/managedClusters/$cluster_name"
  az ml compute attach -n "$compute_name" --namespace "$compute_namespace" -g "$resource_group" -w "$workspace_name" --resource-id "$resource_id" -t Kubernetes --only-show-errors
  migrate_compute=$(az ml compute show -n "$compute_name" -g "$resource_group" -w "$workspace_name" --only-show-errors -o json| jq -r '.id')
fi

# STEP1 Export services
echo 'Export services...'
output=$(python3 export-service-util.py --export --export-json -w $workspace_name -g $resource_group -s $subscription_id| tee /dev/tty)
read -r storage_account blob_folder < <(echo "$output" |tail -n1| jq -r '"\(.storage_account) \(.blob_folder)"')

# STEP2 Download template & parameters files
echo 'Download files...'
az storage blob directory download -c azureml --account-name "$storage_account" -s "$blob_folder" -d $local_dir --recursive --subscription $subscription_id --only-show-errors 1> /dev/null

# STEP3 Overwrite parameters
echo 'Overwrite parameters...'
echo
params_file="$local_dir/$blob_folder/$v1_compute/$migrate_type/$v1_service_name.params.json"
template_file="$local_dir/$blob_folder/online.endpoint.template.json"
output=$(python3 export-service-util.py --overwrite-parameters -mp "$params_file" -mc "$migrate_compute" -me "$online_endpoint_name" -md "$online_deployment_name"| tee /dev/tty)
params=$(echo "$output"|tail -n1)

# STEP4 Deploy to AMLArc/MIR
echo
echo "Params have been saved to $params"
echo "Deploy $migrate_type service $online_endpoint_name..."
deployment_name="Migration-$online_endpoint_name-$(echo $RANDOM | md5sum | head -c 4)"
az deployment group create --name "$deployment_name" --resource-group "$resource_group" --template-file "$template_file" --parameters "$params" --subscription $subscription_id

