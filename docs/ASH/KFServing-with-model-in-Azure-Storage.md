# KFServing with Azure Storage Blob

In this article, you will create a KFServing InferenceService resource on a kubernetes cluster with KFserving installed. 
The machine learning model used is in tensorflow saved model format. It is saved as Azure Storage blob. 

## Prerequisites

*   Make sure you have access to a kubernetes cluster with KFserving installed. 
    
    Please refer [KFserving installation guide](KFServing-setup.md) for details of installing KFServing.
    
*   A tensorflow saved model is stored as Azure Storage Blobs.

    One can perform a distributed training using Azure Machine Service and register the trained model with the AML 
    workspace as documented [here](notebooks/distributed-tf2-cifar10/distributed-tf2-cifar10.ipynb);
    The registered model can then be downloaded/uploaded to azure storage blobs as shown in this 
    [notebook](notebooks/AML-model-download-upload.ipynb).
    
    For KFServing to securely download the blobs to the kubernetes cluster, they are granted to a service principal with 
    "Storage Blob Data Owner" role. For how to create a service principal in azure active directory, please refer to 
    [here](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal). For 
    azure storage access with role assignment, please refer to this [document](https://docs.microsoft.com/en-us/azure/storage/common/storage-auth-aad-rbac-portal)
    

## Deploy KFserving InferenceService

*  Create a kubernetes secret (use kubectl apply -f ):

   The data in Secret is encoded in base64. Here is a simple way to encode a plain string in base64 in Linux:

<pre> $ echo -n "mystring" | base64 </pre>

   please make sure the "-n" option is used. To decode:

<pre> $ echo -n "base64-string" | base64 -d </pre>


   The manifesto for the secret is:

<pre>
apiVersion: v1
kind: Secret
metadata:
  name: azcreds
type: Opaque
data:
  AZ_CLIENT_ID: "base64 encoded"
  AZ_CLIENT_SECRET: "base64 encoded"
  AZ_SUBSCRIPTION_ID: "base64 encoded"
  AZ_TENANT_ID: "base64 encoded"
</pre>


*  Create a kubernetes service account with Secret created above (use kubectl apply -f ):

<pre>
apiVersion: v1
kind: ServiceAccount
metadata:
  name: azuresa
secrets:
- name: azcreds
</pre>


*  Create KFServing InferenceService (use kubectl apply -f ):

    Note the ServiceAccount created above is referenced under "predictor"

<pre>
apiVersion: "serving.kubeflow.org/v1alpha2"
kind: "InferenceService"
metadata:
  name: "cifar10"
spec:
  default:
    predictor:
      tensorflow:
        storageUri: "https://backupsli.blob.core.windows.net/cifar10model/slcifar10"
      serviceAccountName: azuresa
</pre>

Check if the inferenceService is ready or not by running:

<pre>kubectl get inferenceService -n default </pre>

##  Get xip.io url for Testing:

If you configured DNS with xip.io as mentioned in [KFserving installation guide](KFServing-setup.md), you can get the
xip.io url and use a web test tool like Insomnia or Postman to test your service.

*  Get host url:

<pre>
$ kubectl get ksvc
NAME                        URL                                                             LATESTCREATED                     LATESTREADY                                          READY   REASON
cifar10-predictor-default   http://cifar10-predictor-default.default.38.102.181.86.xip.io   cifar10-predictor-default-l9f6s   cifar10-predict                   or-default-l9f6s   True
</pre>

As displayed, host url is http://cifar10-predictor-default.default.38.102.181.86.xip.io
*  The whole url:

    The whole url is composed as host_url + "/v1/models/<inferenceService-name>:predict"
    For this particular example, it is:

    http://cifar10-predictor-default.default.38.102.181.86.xip.io/v1/models/cifar10:predict

*  Test data:
    The predictor used here is tensorflow serving. Here is the 
   [instruction](https://www.tensorflow.org/tfx/tutorials/serving/rest_simple) about how to generate test input. 
   
    An example of Cifar10 is given at [cifar10_test_input](test-data/cifar10_test_input.json)
   