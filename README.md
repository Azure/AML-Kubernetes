# AML CMK8s -- Private Preview
This repository is intended to serve as an information hub for customers and partners who are participating in the private preview for AML CMK8s(Custmer managed Kubernetes cluster). Use this repository for onboarding and testing instructions as well as an avenue to provide feedback, issues, enhancement requests and stay up to date as the preview progresses.

## overview
CMK8s project enable customer to use their exsiting K8s cluster as AML training workload (will also support in the near future). The DataScientists will have some experience as other compute target, they can submit different type training jobs to CMK8s compute target. CMK8s Will first support SDK, CIL and restapi will be supported later.

CMK8s project support two type K8s clutser: AKS(Azure managed), Arc (Azure not managed), we will first support CMAKS.

## Getting Started

To use CMAKS compute in private preview, you need follow these steps:

1. [Provision a GPU enabled AKS cluster](https://github.com/Azure/CMK8s-Sample/blob/master/docs/1.%20Provision%20a%20GPU%20enabled%20AKS%20cluster.md)
2. [Install AML operator manually](https://github.com/Azure/CMK8s-Sample/blob/master/docs/2.%20Install%20AML%20operator%20manually.markdown)
3. [Attach CMAKS compute](https://github.com/Azure/CMK8s-Sample/blob/master/docs/4.%20Attach%20CMAKS%20compute.markdown)
4. [Submit AML training jobs to CMASK compute](https://github.com/Azure/CMK8s-Sample/blob/master/docs/4.%20Submit%20AML%20training%20jobs%20to%20CMASK%20compute.markdown)
5. [View metrics in Compute level and runs level](https://github.com/Azure/CMK8s-Sample/blob/master/docs/5.%20View%20metrics%20in%20Compute%20level%20and%20runs%20level.markdown)


# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
