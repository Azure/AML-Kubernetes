## This script is used to run training test on AmlArc-enabled compute

# Global variables
LOCK_FILE=$0.lock

# Init environment variables
init_env_variables(){
    set -x

    SUBSCRIPTION="${SUBSCRIPTION:-6560575d-fa06-4e7d-95fb-f962e74efd7a}"  
    RESOURCE_GROUP="${RESOURCE_GROUP:-azureml-examples-rg}"  
    WORKSPACE="${WORKSPACE:-amlarc-ws}"  # $((1 + $RANDOM % 100))
    LOCATION="${LOCATION:-eastus}"
    ARC_CLUSTER_PREFIX="${ARC_CLUSTER_PREFIX:-amlarc-arc}"
    AKS_CLUSTER_PREFIX="${AKS_CLUSTER_PREFIX:-amlarc-aks}"
    AMLARC_RELEASE_TRAIN="${AMLARC_RELEASE_TRAIN:-staging}"
    AMLARC_RELEASE_NAMESPACE="${AMLARC_RELEASE_NAMESPACE:-azureml}"
    EXTENSION_NAME="${EXTENSION_NAME:-amlarc-extension}"
    EXTENSION_TYPE="${EXTENSION_TYPE:-Microsoft.AzureML.Kubernetes}"
   
    RESULT_FILE=amlarc-test-result.txt

    touch $LOCK_FILE
    [ "$(cat $LOCK_FILE)" == "" ] && echo $(date) > $LOCK_FILE || true 

    if (( 10#$(date -d "$(cat $LOCK_FILE)" +"%H") < 12 )); then
        AMLARC_RELEASE_TRAIN=experimental
    fi

    if [ "$INPUT_AMLARC_RELEASE_TRAIN" != "" ]; then
        AMLARC_RELEASE_TRAIN=$INPUT_AMLARC_RELEASE_TRAIN
    fi
    
    if [ "$AMLARC_RELEASE_TRAIN" == "experimental" ]; then
        LOCATION=eastus2euap
    fi

    AKS_LOCATION=eastus

    WORKSPACE=${WORKSPACE}-${LOCATION}
    ARC_CLUSTER_PREFIX=${ARC_CLUSTER_PREFIX}-${LOCATION}
    AKS_CLUSTER_PREFIX=${AKS_CLUSTER_PREFIX}-${AKS_LOCATION}

}

install_dependency(){
    set -x

    # TODO： install az

    az extension add -n connectedk8s --yes
    az extension add -n k8s-extension --yes
    az extension add -n ml --yes

    curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl \
    && chmod +x ./kubectl  \
    && sudo mv ./kubectl /usr/local/bin/kubectl  

    pip install azureml-core
    
    az version || true
    pip show azureml-core || true
}

waitForResources(){
    available=false
    max_retries=60
    sleep_seconds=5
    RESOURCE=$1
    NAMESPACE=$2
    for i in $(seq 1 $max_retries); do
        if [[ ! $(kubectl wait --for=condition=available ${RESOURCE} --all --namespace ${NAMESPACE}) ]]; then
            sleep ${sleep_seconds}
        else
            available=true
            break
        fi
    done
    
    echo "$available"
}

# Setup cluster resources
setup_cluster(){
    set -x -e

    rm -f $LOCK_FILE

    init_env_variables

    VM_SKU="${1:-Standard_NC12}"
    MIN_COUNT="${2:-4}"
    MAX_COUNT="${3:-8}"

    ARC_CLUSTER_NAME=$(echo ${ARC_CLUSTER_PREFIX}-${VM_SKU} | tr -d '_')
    AKS_CLUSTER_NAME=$(echo ${AKS_CLUSTER_PREFIX}-${VM_SKU} | tr -d '_')

    # Create resource group if not exists
    az group show \
        --subscription $SUBSCRIPTION \
        -n "$RESOURCE_GROUP" || \
    az group create \
        --subscription $SUBSCRIPTION \
        -l "$LOCATION" \
        -n "$RESOURCE_GROUP" 

    # Create aks cluster if not exists
    az aks show \
        --subscription $SUBSCRIPTION \
        --resource-group $RESOURCE_GROUP \
        --name $AKS_CLUSTER_NAME || \
    az aks create \
        --subscription $SUBSCRIPTION \
        --resource-group $RESOURCE_GROUP \
	    --location $AKS_LOCATION \
        --name $AKS_CLUSTER_NAME \
        --enable-cluster-autoscaler \
        --node-count $MIN_COUNT \
        --min-count $MIN_COUNT \
        --max-count $MAX_COUNT \
        --node-vm-size ${VM_SKU} \
        --no-ssh-key

    # Get aks kubeconfig
    az aks get-credentials \
        --subscription $SUBSCRIPTION \
        --resource-group $RESOURCE_GROUP \
        --name $AKS_CLUSTER_NAME \
        --overwrite-existing

    # Attach cluster to Arc
    az connectedk8s show \
        --subscription $SUBSCRIPTION \
        --resource-group $RESOURCE_GROUP \
        --name $ARC_CLUSTER_NAME || \
    az connectedk8s connect \
        --subscription $SUBSCRIPTION \
        --resource-group $RESOURCE_GROUP \
        --location $LOCATION \
        --name $ARC_CLUSTER_NAME 

    # Wait for resources in ARC ns
    waitSuccessArc="$(waitForResources deployment azure-arc)"
    if [ "${waitSuccessArc}" == false ]; then
        echo "deployment is not avilable in namespace - azure-arc"
    fi

    # Remove extension if exists
    helm status -n $AMLARC_RELEASE_NAMESPACE $EXTENSION_NAME && \ 
    helm uninstall -n $AMLARC_RELEASE_NAMESPACE $EXTENSION_NAME  || true
    az k8s-extension show \
        --cluster-name $ARC_CLUSTER_NAME \
        --cluster-type connectedClusters \
        --subscription $SUBSCRIPTION \
        --resource-group $RESOURCE_GROUP \
        --name $EXTENSION_NAME && \
    az k8s-extension delete \
        --cluster-name $ARC_CLUSTER_NAME \
        --cluster-type connectedClusters \
        --subscription $SUBSCRIPTION \
        --resource-group $RESOURCE_GROUP \
        --name $EXTENSION_NAME \
        --yes || true

    sleep 60 

    # Install extension
    az k8s-extension create \
        --cluster-name $ARC_CLUSTER_NAME \
        --cluster-type connectedClusters \
        --subscription $SUBSCRIPTION \
        --resource-group $RESOURCE_GROUP \
        --name $EXTENSION_NAME \
        --extension-type $EXTENSION_TYPE \
        --scope cluster \
        --release-train $AMLARC_RELEASE_TRAIN \
        --configuration-settings  enableTraining=True allowInsecureConnections=True
   
    sleep 60 
    # Wait for resources in amlarc-arc ns
    waitSuccessAmlArc="$(waitForResources deployment $AMLARC_RELEASE_NAMESPACE)"
    if [ "${waitSuccessAmlArc}" == false ]; then
        echo "deployment is not avilable in namespace - $AMLARC_RELEASE_NAMESPACE"
    fi
}

# Setup compute
setup_compute(){
    set -x -e

    init_env_variables

    VM_SKU="${1:-Standard_NC12}"
    COMPUTE_NAME="${2:gpu-compute}"

    ARC_CLUSTER_NAME=$(echo ${ARC_CLUSTER_PREFIX}-${VM_SKU} | tr -d '_')
    AKS_CLUSTER_NAME=$(echo ${AKS_CLUSTER_PREFIX}-${VM_SKU} | tr -d '_')

    # create workspace
    az ml workspace show \
        --subscription $SUBSCRIPTION \
        --resource-group $RESOURCE_GROUP \
        --workspace-name $WORKSPACE || \
    az ml workspace create \
        --subscription $SUBSCRIPTION \
        --resource-group $RESOURCE_GROUP \
        --location $LOCATION \
        --workspace-name $WORKSPACE 

    # attach compute
    ARC_RESOURCE_ID="/subscriptions/$SUBSCRIPTION/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Kubernetes/connectedClusters/$ARC_CLUSTER_NAME"
    python attach_compute.py \
        "$SUBSCRIPTION" "$RESOURCE_GROUP" "$WORKSPACE" \
	"$COMPUTE_NAME" "$ARC_RESOURCE_ID" "$VM_SKU"

    sleep 60
}


# Cleanup
clean_up_cluster(){
    set -x +e

    init_env_variables

    VM_SKU="${1:-Standard_NC12}"

    ARC_CLUSTER_NAME=$(echo ${ARC_CLUSTER_PREFIX}-${VM_SKU} | tr -d '_')
    AKS_CLUSTER_NAME=$(echo ${AKS_CLUSTER_PREFIX}-${VM_SKU} | tr -d '_')

    # get aks kubeconfig
    az aks get-credentials \
        --subscription $SUBSCRIPTION \
        --resource-group $RESOURCE_GROUP \
        --name $AKS_CLUSTER_NAME \
        --overwrite-existing
     
    # delete extension
    az k8s-extension delete \
        --cluster-name $ARC_CLUSTER_NAME \
        --cluster-type connectedClusters \
        --subscription $SUBSCRIPTION \
        --resource-group $RESOURCE_GROUP \
        --name $EXTENSION_NAME \
        --yes 
    
    # delete helm charts
    helm uninstall -n $AMLARC_RELEASE_NAMESPACE $EXTENSION_NAME
    
    # delete arc
    az connectedk8s delete \
        --subscription $SUBSCRIPTION \
        --resource-group $RESOURCE_GROUP \
        --name $ARC_CLUSTER_NAME \
        --yes

    # delete aks
    #az aks delete \
    #    --subscription $SUBSCRIPTION \
    #    --resource-group $RESOURCE_GROUP \
    #    --name $AKS_CLUSTER_NAME \
    #    --yes

}

# Run cli test
run_test(){
    set -x

    init_env

    JOB_YML="${1:-jobs/train/fastai/mnist/job.yml}"

    SRW=" --subscription $SUBSCRIPTION --resource-group $RESOURCE_GROUP --workspace-name $WORKSPACE "

    run_id=$(az ml job create $SRW -f $JOB_YML --query name -o tsv)
    az ml job stream $SRW -n $run_id
    status=$(az ml job show $SRW -n $run_id --query status -o tsv)
    echo $status
    if [[ $status == "Completed" ]]
    then
        echo "Job $JOB_YML completed" | tee -a $RESULT_FILE
    elif [[ $status ==  "Failed" ]]
    then
        echo "Job $JOB_YML failed" | tee -a $RESULT_FILE
        exit 1
    else 
        echo "Job $JOB_YML unknown" | tee -a $RESULT_FILE 
	exit 2
    fi
}


attach_workspace(){
    set -x

    init_env

    az ml folder attach -w $WORKSPACE -g $RESOURCE_GROUP --subscription-id $SUBSCRIPTION 
}

# Run python test
run_py_test(){
    set -x

    init_env

    JOB_YML="${1:-python-sdk/workflows/train/fastai/mnist/job.py}"

    python $JOB_YML 

    status=$?
    echo $status
    if [[ "$status" == "0" ]]
    then
        echo "Job $JOB_YML completed" | tee -a $RESULT_FILE
    else
        echo "Job $JOB_YML failed" | tee -a $RESULT_FILE
        exit 1
    fi
}

# Check test result
check_test_result(){

    init_env
	
    echo "RESULT:"
    cat $RESULT_FILE
    
    [ ! -f $RESULT_FILE ] && echo "No test has run!" && exit 1 
    [ "$(grep -c Job $RESULT_FILE)" == "0" ] && echo "No test has run!" && exit 1
    unhealthy_num=$(grep Job $RESULT_FILE | grep -ivc completed)
    [ "$unhealthy_num" != "0" ] && echo "There are $unhealthy_num unhealthy jobs."  && exit 1
    
    echo "All tests passed."

    # TODO: generate test result
}


if [ "$0" = "$BASH_SOURCE" ]; then
    $@
fi



