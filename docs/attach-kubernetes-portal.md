
## Attach Kubernetes Compute from UI

1. Goto AML studio [portal](https://ml.azure.com), Compute > Attached compute, click "+New" button, and select "Kubernetes service (Preview)"

![addKubernetesCompute](/docs/media/addKubernetesCompute.png)

2. Enter a compute name and check 'Azure Kubernetes service' radio button. In the dropdown below, you should see all your AKS clusters in that subscription. Select the cluster you want to attach to this AML workspace

![listAKS](/docs/media/listAKS.png)


(Optional) Browse & upload a profile config file
   * A profile config is a YAML file that defines a namespace and/or node selctors to which the data scientist is set up to deploy training jobs
   * If you skip this section, all jobs/pods will be deployed to the default namespace
   * Profile config schema is captured [here](/docs/profile-config/profile-schema-v1.0.yaml)
   * Profile config sample can be found [here](/docs/profile-config/profile-v1.0-sample-1.yaml)
   * #### It is expected that the IT operator sets up the kubernetes namespaces/node selectors, otherwise the jobs/pods will be deployed in the default namespace

![profileConfig](/docs/media/profileConfig.png)

3. Click 'Attach' button. You will see the 'provisioning state' as 'Creating'. If it succeeds, you will see a 'Succeeded' state or else 'Failed' state. The attach process takes about ~5 mins
![attach](/docs/media/attach.png)


### Detach compute from UI
1. Go to compute list and then Compute Details, click on Detach and confirm.
![detach](/docs/media/detach.png)
