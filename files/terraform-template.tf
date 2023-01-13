
terraform {
  required_version = ">=0.12"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>2.0"
    }
    azapi = {
      source  = "Azure/azapi"
    }
  }
}

provider "azurerm" {
  features {}
}

provider "azapi" {
  # More information on the authentication methods supported by
  # the AzureRM Provider can be found here:
  # https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs

  # subscription_id = "..."
  # client_id       = "..."
  # client_secret   = "..."
  # tenant_id       = "..."
}

resource "azapi_resource" "mlextension" {
  type = "Microsoft.KubernetesConfiguration/extensions@2022-03-01"
  name = "{extension-name}"
  parent_id = "/subscriptions/{subscription}/resourcegroups/{resource-group}/providers/Microsoft.ContainerService/managedClusters/{cluster-name}"
  identity {
    type = "SystemAssigned"
  }
  body = jsonencode({
    "properties"= {
        "extensionType"= "microsoft.azureml.kubernetes"
        "releaseTrain"= "stable"
        "scope"= {
            "cluster"= {
                "releaseNamespace"= "azureml"
            }
        }
        "configurationSettings"= {
            "enableTraining"= "True"
            "enableInference"= "True"
            "allowInsecureConnections"= "True"
            "inferenceRouterServiceType"= "loadBalancer"
            "cluster_name"= "/subscriptions/{subscription}/resourcegroups/{resource-group}/providers/Microsoft.ContainerService/managedClusters/{cluster-name}"
            "domain"= "{region}.cloudapp.azure.com"
            "location"= "{region}"
            "jobSchedulerLocation"= "eastus"
            "cluster_name_friendly"= "{cluster-name}"
            "servicebus.enabled"= "false"
            "relayserver.enabled"= "false"
            "nginxIngress.enabled"= "true"
            "clusterId"= "/subscriptions/{subscription}/resourcegroups/{resource-group}/providers/Microsoft.ContainerService/managedClusters/{cluster-name}"
            "prometheus.prometheusSpec.externalLabels.cluster_name"= "/subscriptions/{subscription}/resourcegroups/{resource-group}/providers/Microsoft.ContainerService/managedClusters/{cluster-name}"
        },
        "configurationProtectedSettings"= {}
    }
  })
}
