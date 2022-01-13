
export subscription_id="<YOUR_SUBSCRIPTION_ID>"
export resource_group="<YOUR_RESOURCE_GROUP>"
export workspace_name="<YOUR_WORKSPACE_NAME>"
export aks_cluster_name="<YOUR_AKS_CLUSTER_NAME>"
export service_name="<YOUR_SERVICE_NAME>"
export arcml_compute_name="arcml-compute"
export arcml_extension_name="arcml-extension"
export inference_compute_name="<YOUR_INFERENCE_COMPUTE_NAME>"

service_namespace=`kubectl get deployment -A -ojson | jq -r --arg service_name "$service_name" '.items[] | select(.metadata.name == $service_name) | .metadata.namespace'`

# Choose one option below to install AzureML extension based endpoint type of AKS service

# OPTION A) AKS service has public https endpoint
export ssl_cname="<YOUR_SSL_CNAME>"
export ssl_cert_pem_file="<YOUR_CERT_PEM_FILE>"
export ssl_key_pem_file="<YOUR_KEY_PEM_FILE>"

az k8s-extension create --cluster-name $aks_cluster_name --cluster-type managedClusters -n $arcml_extension_name \
--extension-type Microsoft.AzureML.Kubernetes --scope cluster --configuration-settings enableInference=True isAKSMigration=true \
scoringFe.namespace=default sslCname=$ssl_cname --config-protected sslCertPemFile=$ssl_cert_pem_file sslKeyPemFile=$ssl_key_pem_file \
--subscription $subscription_id -g $resource_group --auto-upgrade-minor-version False

# OPTION B) AKS service has public http endpoint
#az k8s-extension create --cluster-name $aks_cluster_name --cluster-type managedClusters -n $arcml_extension_name \
#--extension-type Microsoft.AzureML.Kubernetes --scope cluster --configuration-settings enableInference=True allowInsecureConnections=true \
#isAKSMigration=true scoringFe.namespace=default \
#--subscription $subscription_id -g $resource_group --auto-upgrade-minor-version False

# OPTION C) AKS service has private http endpoint
#az k8s-extension create --cluster-name $aks_cluster_name --cluster-type managedClusters -n $arcml_extension_name \
#--extension-type Microsoft.AzureML.Kubernetes --scope cluster --configuration-settings enableInference=True allowInsecureConnections=true \
#privateEndpointILB=True isAKSMigration=true scoringFe.namespace=default \
#--subscription $subscription_id -g $resource_group --auto-upgrade-minor-version False

extension_install_state=`az k8s-extension show --name $arcml_extension_name  --cluster-type managedClusters --cluster-name $aks_cluster_name   --resource-group $resource_group | jq -r '.provisioningState'`
echo $extension_install_state
if [[ $extension_install_state == "Succeeded" ]]
then
  echo "AzureML extention created successfully"
else
  echo "AzureML extention creation failed"
  exit 1
fi

python3 migrate-service-util.py $subscription_id $resource_group $workspace_name $aks_cluster_name $service_name $service_namespace $arcml_compute_name $inference_compute_name 
