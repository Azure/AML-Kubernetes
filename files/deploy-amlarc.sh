#!/bin/bash

set -e

subscription_id="<YOUR_SUBSCRIPTION_ID>"
resource_group="<YOUR_RESOURCE_GROUP>"
cluster_name="<YOUR_AKS_CLUSTER_NAME>"

arcml_extension_name="arcml-extension"

ssl_cname="<YOUR_SSL_CNAME>"
ssl_cert_pem_file="<YOUR_CERT_PEM_FILE>"
ssl_key_pem_file="<YOUR_KEY_PEM_FILE>"

# STEP1 Register feature providers
echo 'Register features...'
az feature register --namespace Microsoft.ContainerService -n AKS-ExtensionManager --subscription "$subscription_id"
echo 'Waiting for feature register...'
while [ "$(az feature list --query "[?contains(name, 'Microsoft.ContainerService/AKS-ExtensionManager')].[properties.state]" -o json |jq '.[0][0]')" == 'Registered' ]
do
  sleep 5
done
az provider register -n Microsoft.ContainerService 1


# STEP2 Deploy AmlArc extension
# OPTION A) AKS service has public https endpoint
az k8s-extension create --cluster-name $cluster_name --cluster-type managedClusters -n $arcml_extension_name \
--extension-type Microsoft.AzureML.Kubernetes --scope cluster --configuration-settings enableInference=True \
sslCname=$ssl_cname --config-protected sslCertPemFile=$ssl_cert_pem_file sslKeyPemFile=$ssl_key_pem_file \
--subscription $subscription_id -g $resource_group --auto-upgrade-minor-version False

# OPTION B) AKS service has public http endpoint
#az k8s-extension create --cluster-name $cluster_name --cluster-type managedClusters -n $arcml_extension_name \
#--extension-type Microsoft.AzureML.Kubernetes --scope cluster --configuration-settings enableInference=True allowInsecureConnections=true \
#--subscription $subscription_id -g $resource_group --auto-upgrade-minor-version False

# OPTION C) AKS service has private http endpoint
#az k8s-extension create --cluster-name $cluster_name --cluster-type managedClusters -n $arcml_extension_name \
#--extension-type Microsoft.AzureML.Kubernetes --scope cluster --configuration-settings enableInference=True allowInsecureConnections=true \
#privateEndpointILB=True --subscription $subscription_id -g $resource_group --auto-upgrade-minor-version False


extension_install_state=$(az k8s-extension show --name $arcml_extension_name  --cluster-type managedClusters --cluster-name "$cluster_name"   --resource-group "$resource_group" --subscription "$subscription_id" | jq -r '.provisioningState')
echo "$extension_install_state"
if [[ $extension_install_state == "Succeeded" ]]
then
  echo "AzureML extention created successfully"
else
  echo "AzureML extention creation failed"
  exit 1
fi
