# Azure Arc-enabled Machine Learning Trouble Shooting
This document is used to help customer solve problems when using AzureML extension. 

* [Extension Installation Guide](#extension-installation-guide)
    * [How is AzureML extension installed](#how-is-extension-installed)
    * [HealthCheck of extension](#healthcheck)
    * [Inference HA](#inference-ha)
    * [Inference router service type](#inference-service-type)
    * [Skip installation of volcano in the extension](#skip-volcano)
    * [How to validate private workspace endpoint](#valid-private-workspace)
    * [Prometheus operator](#prom-op)
    * [DCGM exporter](#dcgm)
    * [Error: Timed out or status not populated](#error-timeout)
    * [Error: Failed pre-install: pod healthcheck failed](#error-healthcheck-failed)
    * [Error: Resources cannot be imported](#error-cannot-imported)
    * [Error: Cannot re-use a name that is still in use](#error-reuse-name)
    * [Error: Earlier operation is in progress](#error-operation-in-progress)
    * [Error: Extension is being terminated](#error-resource-terminating)
    * [Error: Failed in download the Chart path not found](#error-chart-not-found)
    * [Error Code of HealthCheck](#healthcheck-error-code)
* [Training Guide](#training-guide)
* [Inference Guide](#inference-guide)

## Extension Installation Guide
### How is AzureML extension installed <a name="how-is-extension-installed"></a>
AzureML extension is released as a helm chart and installed by Helm V3. By default, all resources of AzureML extension are installed in azureml namespace. The error message user received is the original error message returned by helm. This is why sometimes vague error messages are returned. But you can utilize the [built-in health check job](#healthcheck) or the following commands to help you debug. You could get more detail Azureml extension information at [Install AzureML extension](./deploy-extension.md). 
```bash
# check helm chart status
helm list -a -n azureml
# check status of all agent pods
kubectl get pod -n azureml
# get events of the extension
kubectl get events -n azureml --sort-by='.lastTimestamp'
# get release history
helm history -n azureml --debug <extension-name>
```
### HealthCheck of extension <a name="healthcheck"></a>
When the installation failed, you can use the built-in health check job to make a comprehensive check on the extension. The job will output a report which is saved in a configmap named "arcml-healthcheck" under azureml namespace. The error codes and possible solutions for the report are list in [Error Code of HealthCheck](#healthcheck-error-code). The health check job will also be automatically triggered in pre-install, pre-upgrade, pre-rollback and pre-delete steps. When asking [support](./../README.md#support), we recommend that you run the first command below and send the```healthcheck.logs``` file to us, as it can facilitate us to better locate the problem.
```bash
# collect all healthcheck logs when asking support
helm test -n azureml <extension-name> --logs | tee healthcheck.logs

# manually trigger the built-in health check test
helm test -n azureml <extension-name> --logs
# get the report in test step
kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.reports-test}"
# get the report in pre-install step
kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.reports-pre-install}"
# get the report in pre-upgrade step
kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.reports-pre-upgrade}"
# get the report in pre-rollback step
kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.reports-pre-rollback}"
# get the report in pre-delete step
kubectl get configmap -n azureml arcml-healthcheck --output="jsonpath={.data.reports-pre-delete}"
```
> Note: When running "helm test" command, Error like "unable to get pod logs for healthcheck-config: pods 'healthcheck-config' not found" should be ignored. 
### Inference HA <a name="inference-ha"></a>
For the high availability of inference service, azureml-fe agent will be deployed to three different nodes by default. Azureml-fe agent is used for load balancing, cooperative routing and security authentication. It's very important, especially for production environment. For a single azureml-fe agent, it requires about 0.5 cpu and 500Mi memory. Inference HA is enabled by default and requires at least 3 nodes to run, so, in many test scenarios, installation will fail due to insufficient resources. Set ```inferenceRouterHA``` flag to ```false``` to disable Inference HA.

The phenomenon that this kind of issue may lead to is that some ```azureml-fe``` pods are pending on scheduling and error message of the pod could be like **"0/1 nodes are available: 1 node(s) didn't match pod anti-affinity rules"**.

### Inference router service type  <a name="inference-service-type"></a>
According to the cluster configuration and testing scenarios, you may need different ways to expose our inference scoring services. you can specify ```loadBalancer```, ```clusterIP``` and ```nodePort``` service type with ```inferenceRouterServiceType``` flag. And you can enable internal loadBalancer with ```internalLoadBalancerProvider``` flag, but internal loadBalancer is only supported by AKS cluster currently. 

Please note that ```loadBalancer``` is not supported by raw k8s, like Minikube and Kind. Usually, ```loadBalancer``` are implemented by cloud provider, like AKS, GKE and EKS. If you are trying to use ```loadBalancer``` in a cluster which doesn't support ```loadBalancer```, you may get timeout error from cli and ```LOAD_BALANCER_NOT_SUPPORT``` error from healthcheck report. If you find that inference-operator pod is crashed and azureml-fe service is in pending or unhealthy state, it is likely that you are using the wrong service type or your cluster has something wrong to support the service type you specified. 

### Skip installation of volcano in the extension  <a name="skip-volcano"></a>
If user have their own volcano suite installed, they can set `volcanoScheduler.enable=false`, so that the extension will not try to install the volcano scheduler. Volcano scheduler and volcano controller are required for job submission and scheduling.

1. The version of volcano we are using and run tests against with is `1.5.0`, other version may not work as expected.
2. The volcano scheduler config we are using is :  
    ```yaml
    volcano-scheduler.conf: |
        actions: "enqueue, allocate, backfill"
        tiers:
        - plugins:
            - name: task-topology
            - name: priority
            - name: gang
            - name: conformance
        - plugins:
            - name: overcommit
            - name: drf
            - name: predicates
            - name: proportion
            - name: nodeorder
            - name: binpack
    ```
    We are using `task-topology` plugins in the scheduler, if user have a volcano version greater than `1.3.0`, please consider to enable this plugin.

3. There is a bug in volcano admission, and it will break our job, so we disabled `job/validate` webhook explicitly in the volcano admission provided in our extension, user should also patch their volcano admission otherwise the common runtime job won’t work.
See this [issue](https://github.com/volcano-sh/volcano/issues/1680).

### How to validate private workspace endpoint  <a name="valid-private-workspace"></a>
If you setup private endpoint for your workspace, it's important to test its availability before using it. Otherwise, it may cause unknown errors, like installation errors. You can follow this [doc](./private-link.md#private-link-issue) to test if the private workspace endpoint is available in your cluster. For how to setup private link with AzureML extension, please refer to [private link](./private-link.md).


### Prometheus operator <a name="prom-op"></a>
[Promtheus operator](https://github.com/prometheus-operator/prometheus-operator) is an open source framework to help build metric monitoring system in kubernetes. AzureML extension also utilizes promtheus operator to help monitor resource utilization of jobs. The following lists the open source components used for collecting metrics in AzureML extension:
1. Promtheus operator serves to make running Prometheus on top of Kubernetes as easy as possible, while preserving Kubernetes-native configuration options.
1. Promtheus serves to collect, calculate and upload metrics. 
1. CAdvisor is an open-source agent integrated into the kubelet binary that monitors resource usage and analyzes the performance of containers. CAdvisor produces the original metrics.
1. Kube-state-metrics (KSM) generates metrics about the state of the objects in Kubernetes. Those metrics are used for performing correlation operations.
1. Dcgm-exporter is used for collecting gpu metrics. Please refer to [DCGM exporter](#dcgm) for more information.

If prometheus operator has already been installed in cluster by other service, you can specify ```installPromOp=false``` to disable prometheus operator in AzureML extension side to avoid conflictions between two prometheus operators.
In this case, all prometheus instances will be managed by the existing promtheus operator. And to make sure prometheus works properly, the following things need to be paid attention when you disable promtheus operator in Azureml extension side.
1. Check if prometheus in azureml namespace is managed by prometheus operator. In some scenarios, prometheus operator is set to only monitor some specific namespaces. If so, please make sure azureml namespace is in the white list. Refer to [command flags](https://github.com/prometheus-operator/prometheus-operator/blob/b475b655a82987eca96e142fe03a1e9c4e51f5f2/cmd/operator/main.go#L165) for more information.
2. Check if kubelete-service is enabled in prometheus operator. Kubelet-service contains all the endpoints of kubelet. Refer to [command flags](https://github.com/prometheus-operator/prometheus-operator/blob/b475b655a82987eca96e142fe03a1e9c4e51f5f2/cmd/operator/main.go#L149) for more information. And also need to make sure that kubelet-service has a label named k8s-app and it's value is kubelet
3. Create ServiceMonitor for kubelet-service. Run the following command with variables replaced:
    ```bash
    cat << EOF | kubectl apply -f -
    apiVersion: monitoring.coreos.com/v1
    kind: ServiceMonitor
    metadata:
      name: prom-kubelet
      namespace: azureml
      labels:
        release: "<extension-name>"     # Please replace to your Azureml extension name
    spec:
      endpoints:
      - port: https-metrics
        scheme: https
        path: /metrics/cadvisor
        honorLabels: true
        tlsConfig:
          caFile: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
          insecureSkipVerify: true
        bearerTokenFile: /var/run/secrets/kubernetes.io/serviceaccount/token
        relabelings:
        - sourceLabels:
          - __metrics_path__
          targetLabel: metrics_path
      jobLabel: k8s-app
      namespaceSelector:
        matchNames:
        - "<namespace-of-your-kubelet-service>"  # Please change this to the same namespace of your kubelet-service
      selector:
        matchLabels:
          k8s-app: kubelet    # Please make sure your kubelet-service has a label named k8s-app and it's value is kubelet

    EOF
    ```

### DCGM exporter <a name="dcgm"></a>
[Dcgm-exporter](https://github.com/NVIDIA/dcgm-exporter) is the official tool recommended by NVIDIA for collecting GPU metrics. We have integrated it into Azureml extension. But, by default, dcgm-exporter is not enabled, and no GPU metrics are collected. You can specify ```installDcgmExporter``` flag to ```true``` to enable it. As it's NVIDIA's official tool, you may already have it installed in your GPU cluster. If so, you can follow the steps below to integrate your dcgm-exporter into Azureml extension. Another thing to note is that dcgm-exporter allows user to config which metrics to expose. For Azureml extension, please make sure ```DCGM_FI_DEV_GPU_UTIL```, ```DCGM_FI_DEV_FB_FREE``` and ```DCGM_FI_DEV_FB_USED``` metris are exposed. 

1. Make sure you have Aureml extension and dcgm-exporter installed successfully. Dcgm-exporter can be installed by [Dcgm-exporter helm chart](https://github.com/NVIDIA/dcgm-exporter) or [Gpu-operator helm chart](https://github.com/NVIDIA/gpu-operator)

1. Check if there is a service for dcgm-exporter. If it doesn't exist or you don't know how to check , run the command below to create one.
    ```bash
    cat << EOF | kubectl apply -f -
    apiVersion: v1
    kind: Service
    metadata:
      name: dcgm-exporter-service
      namespace: "<namespace-of-your-dcgm-exporter>" # Please change this to the same namespace of your dcgm-exporter
      labels:
        app.kubernetes.io/name: dcgm-exporter
        app.kubernetes.io/instance: "<extension-name>" # Please replace to your Azureml extension name
        app.kubernetes.io/component: "dcgm-exporter"
      annotations:
        prometheus.io/scrape: 'true'
    spec:
      type: "ClusterIP"
      ports:
      - name: "metrics"
        port: 9400  # Please replace to the correct port of your dcgm-exporter. It's 9400 by default
        targetPort: 9400  # Please replace to the correct port of your dcgm-exporter. It's 9400 by default
        protocol: TCP
      selector:
        app.kubernetes.io/name: dcgm-exporter  # Those two labels are used to select dcgm-exporter pods. You can change them according to the actual label on the service
        app.kubernetes.io/instance: "<dcgm-exporter-helm-chart-name>" # Please replace to the helm chart name of dcgm-exporter
    EOF
    ```
1. Check if the service in previous step is set correctly
    ```bash
    kubectl -n <namespace-of-your-dcgm-exporter> port-forward service/dcgm-exporter-service 9400:9400
    # run this command in a separate terminal. You will get a lot of dcgm metrics with this command.
    curl http://127.0.0.1:9400/metrics
    ```
1. Setup ServiceMonitor to expose dcgm-exporter service to Azureml extension. Run the following command and it will take effect in a few minutes.
    ```bash
    cat << EOF | kubectl apply -f -
    apiVersion: monitoring.coreos.com/v1
    kind: ServiceMonitor
    metadata:
      name: dcgm-exporter-monitor
      namespace: azureml
      labels:
        app.kubernetes.io/name: dcgm-exporter
        release: "<extension-name>"   # Please replace to your Azureml extension name
        app.kubernetes.io/component: "dcgm-exporter"
    spec:
      selector:
        matchLabels:
          app.kubernetes.io/name: dcgm-exporter
          app.kubernetes.io/instance: "<extension-name>"   # Please replace to your Azureml extension name
          app.kubernetes.io/component: "dcgm-exporter"
      namespaceSelector:
        matchNames:
        - "<namespace-of-your-dcgm-exporter>"  # Please change this to the same namespace of your dcgm-exporter
      endpoints:
      - port: "metrics"
        path: "/metrics"
    EOF
    ```

### Error: Timed out or status not populated <a name="error-timeout"></a>
If installation is pending on some resources or process for more than 15 minutes, it will throw out error like the followings. For example, it may be due to insufficient CPU, memory and nodes. Or because the loadbalancer cannot be assigned an public IP address. In this case, please run [HealthCheck](#healthcheck) to get more debug information. ```status not populated``` error is a known Arc error. It can be triggered by timeout error. In order to avoid ```status not populated``` error as much as possible, you can manaually upgrade the arc agents to the latest version by running ```az connectedk8s upgrade --subscription <subscription> -g <resource-group> -n <name>```. If you cluster is not connected through Arc, that is Azureml extension is installed directly in a raw managed AKS, Arc agents will be upgraded automatically.
```
release amlarc-extension failed, and has been uninstalled due to atomic being set: timed out waiting for the condition
```
or
```
Error : Retry for given duration didn't get any results with err {status not populated}
```

### Error: Failed pre-install: pod healthcheck failed <a name="error-healthcheck-failed"></a>
Azureml extension contains a HealthCheck hook to check your cluster before the installation. If you got this error, it means some critical errors are found. You can follow [HealthCheck of extension](#healthcheck) to get detailed error message and follow [Error Code of HealthCheck](#healthcheck-error-code) to get some advice. But, in some corner cases, it may also be the problem of the cluster, such as unable to create a pod due to sandbox container issues or unable to pull the image due to network issues. So making sure the cluster is healthy is also very important before the installation.

### Error: resources cannot be imported into the current release: invalid ownership metadata <a name="error-cannot-imported"></a>
This error means there is a confliction between existing cluster resources and AzureML extension. A full error message could be like this: 
```
CustomResourceDefinition "jobs.batch.volcano.sh" in namespace "" exists and cannot be imported into the current release: invalid ownership metadata; label validation error: missing key "app.kubernetes.io/managed-by": must be set to "Helm"; annotation validation error: missing key "meta.helm.sh/release-name": must be set to "amlarc-extension"; annotation validation error: missing key "meta.helm.sh/release-namespace": must be set to "azureml"
```

Follow the steps below to mitigate the issue.
* If the conflict resource is ClusterRole "azureml-fe-role", ClusterRoleBinding "azureml-fe-binding", ServiceAccount "azureml-fe", Deployment "azureml-fe" or other resource related to "azureml-fe", please check if you have Inference AKS V1 installed in your cluster. If yes, you need to clean up all resources related to Inference AKS V1 first by following this [doc](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-create-attach-kubernetes?tabs=python%2Cakscreate#delete-azureml-fe-related-resources), or contact us for migration solution ([Support](./../README.md#support)). If not, please follow the steps below.
* Check who owns the problematic resources and if the resource can be deleted or modified. 
* If the resource is used only by AzureML extension and can be deleted, we can manually add labels to mitigate the issue. Taking the previous error message as an example, you can run commands ```kubectl label crd jobs.batch.volcano.sh "app.kubernetes.io/managed-by=Helm" ``` and ```kubectl annotate crd jobs.batch.volcano.sh "meta.helm.sh/release-namespace=azureml" "meta.helm.sh/release-name=<extension-name>"```. Please replace \<extension-name\> with your own extension name. By setting labels and annotations to the resource, it means the resource is managed by helm and owned by AzureML extension. 
* If the resource is also used by other components in your cluster and can't be modified. Please refer to [doc](./deploy-extension.md#review-azureml-deployment-configuration-settings) to see if there is a flag to disable the conflict resource from AzureML extension side. For example, if it's a resource of [Volcano Scheduler](https://github.com/volcano-sh/volcano) and Volcano Scheduler has been installed in your cluster, you can set ```volcanoScheduler.enable=false``` flag to disable it to avoid the confliction or follow [Skip installation of volcano in the extension](#skip-volcano).

### Error: cannot re-use a name that is still in use <a name="error-reuse-name"></a>
This means the extension name you specified already exists. Run ```helm list -Aa``` to list all helm chart in your cluster. If the name is used by other helm chart, you need to use another name. If the name is used by Azureml extension, you can try to uninstall the extension and reinstall it if possible. Or you need to wait for about an hour and try again later.

### Error: Earlier operation for the helm chart is still in progress <a name="error-operation-in-progress"></a>
You need to wait for about an hour and try again after the unknown operation is completed.

### Error: unable to create new content in namespace azureml because it is being terminated <a name="error-resource-terminating"></a>
This happens when an uninstallation operation is unfinished and another installtion operation is triggered. You can run ```az k8s-extension show``` command to check the provision status of extension and make sure extension has been uninstalled before taking other actions.

### Error: Failed in download the Chart path not found <a name="error-chart-not-found"></a>
Most likely, you specified the wrong extension version. Or the ```--release-train``` flag and ```--version``` flag doesn't match. You need to make sure the version or the release-train you specified really exists. Or you don't specify ```--version``` flag to use the default value to mitigate this error.

### Error Code of HealthCheck  <a name="healthcheck-error-code"></a>
This table shows how to troubleshoot the error codes returned by the HealthCheck report. For error codes lower than E45000, this is a critical error, which means that some problems must be solved before continuing the installation. For error codes larger than E45000, this is a diagnostic error, which requires further manual analysis of the log to identify the problem.

|Error Code |Error Message | Description |
|--|--|--|
|E40000 | UNKNOWN_ERROR | Unknown error happened. Need to check HealthCheck logs to identify the problem. |
|E40001 | LOAD_BALANCER_NOT_SUPPORT | Load balancer is not supported by your cluster. Please refer to [Service type of inference scoring endpoint](#inference-service-type) for solution |
|E40002 | INSUFFICIENT_NODE | The healthy nodes are insufficient. Maybe your node selector is not set properly. Or you may need to disable [Inference HA](#inference-ha)|
|E40003 | INTERNAL_LOAD_BALANCER_NOT_SUPPORT | Currently, internal load balancer is only supported by AKS. Please refer to [Service type of inference scoring endpoint](#inference-service-type) |
|E40004 | INVALID_SSL_SETTING | The SSL settings for extension installation is invalid. Please make sure both SSL key and certificate are provided, and check the integrity of the SSL key and certificate. Also, the CNAME should be compatible with the certificate. You can refer to [Validate SSL settings](#check-ssl-key-cert) for further information. |
|E45001 | AGENT_UNHEALTHY |There are unhealty resources of AzureML extension. Resources checked by this checker are Pod, Job, Deployment, Daemonset and StatufulSet. From the HealthCheck logs, you can find out which resource is unhealthy. |
|E45002 | PROMETHEUS_CONFLICT | Please refer to [Prometheus operator](#prom-op) |
|E45003 | BAD_NETWORK_CONNECTIVITY | Please follow [network-requirements](./network-requirements.md) to check network connectivity. If you are using private link for workspace or other resources, you can refer to doc [private-link](./private-link.md)  |
|E45004 | AZUREML_FE_ROLE_CONFLICT | There exists an "azureml-fe-role" cluster role, but it doesn't belong Azureml extension. Usually, this is because Inference AKS V1 has been installed in your cluster. Please contact us for migration solution. [Support](./../README.md#support)|
|E45005 | AZUREML_FE_DEPLOYMENT_CONFLICT | There exists an "azureml-fe" deployment, but it doesn't belong Azureml extension. Usually, this is because Inference AKS V1 has been installed in your cluster. Please contact us for migration solution. [Support](./../README.md#support)|
|E49999 | CHECKER_PANIC | Checker run into panic. Need to check HealthCheck logs to identify the problem. |
## Training Guide

### UserError: AzureML Kubernetes job failed. : Dispatch Job Fail: Cluster does not support job type RegularJob
Please check whether you have enableTraining=True set when doing the AzureML extension installation. More details could be found at [here](https://github.com/Azure/AML-Kubernetes/blob/master/docs/deploy-extension.md).

### UserError: Unable to mount data store workspaceblobstore. Give either an account key or SAS token.
Credential less machine learning workspace default storage account is not supported right now for training jobs. 

### UserError: Failed to acquire CSI storage account credentials
Error message is:
```yaml
AzureML Kubernetes job failed. 400:{"Msg":"Failed to acquire CSI storage account credentials for mountVolume 'hbiws8397576437-2e2dc25af77dcceea86ae50b45bd1724-secrets', encountered an error: Encountered an error when attempting to connect to Storage Account 'hbiws8397576437': HTTP 403 Forbidden: {\"error\":{\"code\":\"AuthorizationFailed\",\"message\":\"The client '1d0028bc-c1ca-4bdc-8bc0-e5e19cc6f812' with object id '1d0028bc-c1ca-4bdc-8bc0-e5e19cc6f812' does not have authorization to perform action 'Microsoft.Storage/storageAccounts/listKeys/action' over scope '/subscriptions/4aaa645c-5ae2-4ae9-a17a-84b9023bc56a/resourceGroups/youhuaprivatelink/providers/Microsoft.Storage/storageAccounts/hbiws8397576437' or the scope is invalid. If access was recently granted, please refresh your credentials.\"}}","Code":400}
```
This should happen when using HBI workspace, please assign system assigned or user assigned managed identity of the attached compute the access of (“Storage Blob Data Contributor”) and Storage Account Contributor” to the machine learning workspace default storage account by following [this](https://github.com/Azure/AML-Kubernetes/blob/master/docs/managed-identity.md).

### UserError: Failed to acquire CSI storage account credentials
Error message is:
```yaml
AzureML Kubernetes job failed. 400:{"Msg":"Failed to acquire CSI storage account credentials for mountVolume 'hbipleusws6182689148-c8d2ee5daca188bde53fa0711010c53c-secrets', encountered an error: Encountered an error when attempting to connect to Storage Account 'hbipleusws6182689148': Failed to successfully make an http request after 10 attempts. Last inner exception: %!w(\u003cnil\u003e)","Code":400}
```

Please follow [Private Link troubleshooting section](https://github.com/Azure/AML-Kubernetes/blob/master/docs/private-link.md) to check your network settings.

### UserError: Unable to upload project files to working directory in AzureBlob because the authorization failed
Error message is:
```yaml
Unable to upload project files to working directory in AzureBlob because the authorization failed. Most probable reasons are:
 1. The storage account could be in a Virtual Network. To enable Virtual Network in Azure Machine Learning, please refer to https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-enable-virtual-network.
```

Please make sure the storage account has enabled the exceptions of “Allow Azure services on the trusted service list to access this storge account” and the aml workspace is in the resource instances list. And make sure the aml workspace has system assigned managed identity. 

### UserError: Encountered an error when attempting to connect to the Azure ML token service
Error message is:
```yaml
AzureML Kubernetes job failed. 400:{"Msg":"Encountered an error when attempting to connect to the Azure ML token service","Code":400}
```

It should be network issue. Please follow [Private Link troubleshooting section](https://github.com/Azure/AML-Kubernetes/blob/master/docs/private-link.md) to check your network settings. 

### ServiceError: AzureML Kubernetes job failed
Error message is:
```yaml
AzureML Kubernetes job failed. 137:PodPattern matched: {"containers":[{"name":"training-identity-sidecar","message":"Updating certificates in /etc/ssl/certs...\n1 added, 0 removed; done.\nRunning hooks in /etc/ca-certificates/update.d...\ndone.\n * Serving Flask app 'msi-endpoint-server' (lazy loading)\n * Environment: production\n   WARNING: This is a development server. Do not use it in a production deployment.\n   Use a production WSGI server instead.\n * Debug mode: off\n * Running on http://127.0.0.1:12342/ (Press CTRL+C to quit)\n","code":137}]}
```

Check your proxy setting and check whether 127.0.0.1 was added to proxy-skip-range when using “az connectedk8s connect” by following [this](https://github.com/Azure/AML-Kubernetes/blob/master/docs/network-requirements.md). 

## Inference Guide
### InferencingClientCallFailed: The k8s-extension of the Kubernetes cluster is not connectable.

Reattach your compute to the cluster and then try again. If it is still not working, use "kubectl get po -n azureml" to check the relayserver* pods are running. 

### How to check sslCertPemFile and sslKeyPemFile is correct? <a name="check-ssl-key-cert"></a>

Below commands could be used to validate. Expect the second command return "RSA key ok" without prompting you for passphrase.
```yaml
openssl x509 -in cert.pem -text -noout 
openssl rsa -in key.pem -check -noout
```

Below commands could be used to verify whether sslCertPemFile and sslKeyPemFile match:
```yaml
openssl x509 -noout -modulus -in cert.pem 
openssl rsa -noout -modulus -in key.pem 
```


