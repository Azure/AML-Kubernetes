# Stand Alone TFServing Setup On Kubernetes Clusters

In this article, you will set up stand alone KFServing on a kubernetes clusters. KFserving depends on a few
components. You will install:

*	Istio for service management
*	Knative
*	Cert-manager 
*	KFserving

## Prerequisites

*   Make sure you have access to a kubernetes cluster with version kubernetes 1.5.x
*   Termial access to the kubernetes master node

## Install Istio

### istio 1.6.1 supports kubernetes 1.5.

*  download the package:


    ```$ cd ~```

    ```$ curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.6.1 sh -```


*  Check istio-1.6.1 is downloaded:

    ```$ ls```

    ```istio-1.6.1``` 

*  Update PATH:
   
    ```export PATH="$PATH:/home/azureuser/istio-1.6.1/bin"```
   
*  Run a Pre-check:
   
    ```istioctl x precheck```

*  Install:
   
    ```istioctl install --set profile=demo -y```

*  Verify:

    ```istioctl verify-install```

*  View deployed kubernetes resources:

    ```kubectl get all -n istio-system```

    More details is at https://istio.io/latest/docs/setup/getting-started/

## Install Knative




https://knative.dev/v0.18-docs/install/any-kubernetes-cluster/
https://github.com/kubeflow/kfserving/blob/master/docs/DEVELOPER_GUIDE.md#install-knative-on-a-kubernetes-cluster


Installing Knative (v0.14 support kubernetes 1.15)

$ kubectl apply --filename https://github.com/knative/serving/releases/download/v0.14.0/serving-crds.yaml

kubectl apply --filename https://github.com/knative/serving/releases/download/v0.14.0/serving-core.yaml


#Install the Knative Istio controller
 kubectl create namespace knative-serving
kubectl apply --filename https://github.com/knative/net-istio/releases/download/v0.14.0/release.yaml

#Configure DNS (using xip.io) (Error, failed) 
kubectl apply --filename https://github.com/knative/serving/releases/download/v0.14.0/serving-default-domain.yaml

fixes: https://github.com/knative/serving/issues/7487

kubectl apply --filename "C:\Users\v-songshanli\PycharmProjects\kubeflow\play\serving-default-domain-knative-1-4-0.yaml"

kubectl delete job/default-domain  -n knative-serving

kubectl get pods --namespace knative-serving


#install cert-manager
https://cert-manager.io/docs/installation/kubernetes/

# Kubernetes <1.16
$ kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v1.1.0/cert-manager-legacy.yaml


#install KFserving

https://www.kubeflow.org/docs/components/serving/kfserving/
https://github.com/kubeflow/kfserving#standalone-kfserving-installation

kubectl apply -f https://github.com/kubeflow/kfserving/tree/master/install/v0.4.1/kfserving.yaml --validate=false

###note the above yaml file have issues. fixed at:
kubectl apply -f C:\Users\v-songshanli\PycharmProjects\kubeflow\play\kfserving_v1_4_1.yaml --validate=false

kubectl get issuer -n kfserving-system

kubectl get po -n kfserving-system

#Create KFServing test inference service

 kubectl create namespace kfserving-test
 kubectl apply -f C:\Users\v-songshanli\PycharmProjects\kubeflow\play\kfserving_sample.yaml -n kfserving-test

    
