
#### Recommended AKS cluster resources

We recommend you use a at least 3 nodes cluster, each node having at least 2C 4G. And if you want to running GPU jobs, you need some GPU nodes.

#### Why the nodes run occupied in a run is more than node count in run list?

The node count in the number of worker, for distribute training job, such as ps-worker or MPI/horovod they may need extra launcher node or ps node, they may also ocuppy one node. We will optimise this in following version.

#### What Azure storage does Azure Arc-enabled ML support?

Azure Arc-enabled ML compute only support Azure blob container, if your data is in other Azure storage, please move it to Azure blob first. We will support other Azure storage in following iteration.

#### How do I use AMLK8s compute in China Region?

Firstly, make sure you have switched the active cloud to AzureChinaCloud with [az cloud set](https://docs.microsoft.com/cli/azure/manage-clouds-azure-cli?view=azure-cli-latest) command. Then you can use the SDK and CLI sample in this repo.