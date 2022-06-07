# Tutorial

These tutorials help illustrate how to integrate [Azure Application Gateway](https://azure.microsoft.com/en-us/services/application-gateway/) with AzureML extension over HTTP or HTTPS.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Deploy AzureML extension](#deploy-azureml-extension)
- [Expose services over HTTP](#expose-services-over-http)
- [Expose services over HTTPS](#expose-services-over-https)

## Prerequisites

- Install the latest k8s-extension and ml cli.
  - `az extension add -n k8s-extension --upgrade`
  - `az extension add -n ml --upgrade`
- Setup Application Gateway.
  - [**Greenfield Deployment**](https://docs.microsoft.com/en-us/azure/application-gateway/tutorial-ingress-controller-add-on-new): If you are starting from scratch, refer to these instructions.
  - [**Brownfield Deployment**](https://docs.microsoft.com/en-us/azure/application-gateway/tutorial-ingress-controller-add-on-existing): If you have an existing AKS cluster and Application Gateway, refer to these instructions.
- If you want to use HTTPS on this application, you will need a x509 certificate and its private key.

## Deploy AzureML extension

[Deploy extension](https://github.com/Azure/AML-Kubernetes/blob/master/docs/deploy-extension.md#azureml-extension-deployment-scenarios) with `inferenceRouterServiceType=ClusterIP` and `allowInsecureConnections=True`, so that the Application gateway can handle TLS termination by itself instead of handing it over to azureml-fe (azureml inference router created by extension) when service is exposed over HTTPS.


## Expose services over HTTP

In order to expose the azureml-fe we will using the following ingress resource:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: azureml-fe
  namespace: azureml
spec:
  ingressClassName: azure-application-gateway
  rules:
  - http:
      paths:
      - path: /
        backend:
          service:
            name: azureml-fe
            port:
              number: 80
        pathType: Prefix
```

This ingress will expose the `azureml-fe` service and the selected deployment as a default backend of the Application Gateway.

Save the above ingress resource as `ing-azureml-fe.yaml`.

1. Deploy `ing-azureml-fe.yaml` by running:

    ```bash
    kubectl apply -f ing-azureml-fe.yaml
    ```

2. Check the log of the ingress controller for deployment status.

3. Now the `azureml-fe` application should be available. You can check this by visiting the public address of the Application Gateway.

4. [Create an inference job and invoke](https://github.com/Azure/AML-Kubernetes/blob/master/docs/simple-flow.md).

    *NOTE:* Replace the ip of scoring_uri with public address of the Application Gateway before invoking.

## Expose services over HTTPS

1. Before deploying ingress, you need to create a kubernetes secret to host the certificate and private key. You can create a kubernetes secret by running

    ```bash
    kubectl create secret tls <ingress-secret-name> -n azureml --key <path-to-key> --cert <path-to-cert>
    ```

2. Define the following ingress. In the ingress, specify the name of the secret in the `secretName` section.

    ```yaml
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: azureml-fe
      namespace: azureml
    spec:
      ingressClassName: azure-application-gateway
      tls:
      - hosts:
        - <domain>
        secretName: <ingress-secret-name>
      rules:
      - host: <domain>
        http:
          paths:
          - path: /
            backend:
              service:
                name: azureml-fe
                port:
                  number: 80
            pathType: Prefix
    ```

    *NOTE:* Replace `<domain>` and `<ingress-secret-name>` in the above Ingress Resource with the domain pointing to the Application Gateway and the name of your secret. Store the above Ingress Resource in a file name `ing-azureml-fe-tls.yaml`.

1. Deploy ing-azureml-fe-tls.yaml by running

    ```bash
    kubectl apply -f ing-azureml-fe-tls.yaml
    ```

2. Check the log of the ingress controller for deployment status.

3. Now the `azureml-fe` application will be available on HTTPS. You can check this by visiting the public address of the Application Gateway.

4. [Create an inference job and invoke](https://github.com/Azure/AML-Kubernetes/blob/master/docs/simple-flow.md).

    *NOTE:* Replace the protocol and ip of scoring_uri with https and domain pointing to the Application Gateway before invoking.
