# AMLArc with AzureCNI AKS cluster and Private Link AML Workspace

Using an AMLArc enabled AzureCNI AKS cluster for compute in a workspace allow s for further security and does not require too much more setup than a publicly exposed cluster and workspace.

### Setting up VNET:

The Azure VNET can be created independently or during the creation of the AKS cluster explained in the next section.

The VNET does need to have a sufficiently  large address space, The default address space of 10.0.0.0/16 has worked in our testing. The subnet also needs to be large enough to accommodate the AKS cluster, In general, you'll want 128 addresses per node in your cluster, if using default settings. More documentation on creating an Azure VNET can be found here:
https://docs.microsoft.com/en-us/azure/virtual-network/quick-create-portal.

### Setting up AKS cluster:

Setting up your AKS cluster with Azure CNI is documented here:
https://docs.microsoft.com/en-us/azure/aks/configure-azure-cni

As mentioned in the VNET setup section of this document the VNET being used can either be created independently or during setup of the AKS cluster through the portal. The portal has the added convenience of making sure your subnet is large enough for your cluster.

### Installing AMLArc:

All instructions for connecting to an AKS AzureCNI cluster are the same as a public AKS cluster:
https://docs.microsoft.com/en-us/azure/machine-learning/how-to-attach-arc-kubernetes

Do take note however that all commands must be run from a VM within the VNET to be able to communicate and install the Arc and AMLArc extensions on the cluster.

### Setting up AzureML Workspace:

Private link workspace which is required if using an AzureCNI cluster.
Documentation for a private link workspace is provided here:
https://docs.microsoft.com/en-us/azure/machine-learning/how-to-configure-private-link?tabs=python

Notably, if one wants to access the workspace on a browser one has to either enable public access to the cluster, or connect to the VNET with. How to enable public access is described in the document above. Notably if using the Python SDK the Workspace.update() command should be called from a VM or other machine in the VNET.
