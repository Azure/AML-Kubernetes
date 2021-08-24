## Meet network requirements

If the cluster is behind the outbound proxy or firewall with strict outbound network, make sure both of the following protocols/ports/outbound URLs to function.

- HTTPs on port 443: https://:443

```
*.azurecr.io
*.blob.core.windows.net
*.cdn.mscr.io
*.data.mcr.microsoft.com
*.hcp.*.azmk8s.io
*.kusto.windows.net
*.quay.io
*.queue.core.windows.net
*.servicebus.windows.net
*.table.core.windows.net
*.vault.azure.net
*.workspace.<region>.api.azureml.ms
<region-code>.his.arc.azure.com
<region>.api.azureml.ms
<region>.dp.kubernetesconfiguration.azure.com
<region>.experiments.azureml.net
acs-mirror.azureedge.net
apt.dockerproject.org
archive.ubuntu.com
auth.docker.io
changelogs.ubuntu.com
cloudflare.docker.com
data.policy.core.windows.net
dc.services.visualstudio.com
gbl.his.arc.azure.com
gcr.io
go.microsoft.com
guestnotificationservice.azure.com
login.microsoftonline.com
management.azure.com
management.azure.com
mcr.microsoft.com
nvidia.github.io
onegetcdn.azureedge.net
packages.microsoft.com
ppa.launchpad.net
production.cloudflare.docker.com
pypi.org
quay.io
registry-1.docker.io
security.ubuntu.com
storage.googleapis.com
store.policy.core.windows.net
sts.windows.net
us.download.nvidia.com
```

- HTTP on port 80: http://80
```
*.mp.microsoft.com
auth.docker.io
azure.archive.ubuntu.com
changelogs.ubuntu.com
ctldl.windowsupdate.com
gcr.io
production.cloudflare.docker.com
registry-1.docker.io
security.ubuntu.com
storage.googleapis.com
www.msftconnecttest.com
```

>Note: `<region-code>` mapping for Azure cloud regions: eus (East US), weu (West Europe), wcus (West Central US), scus (South Central US), sea (South East Asia), uks (UK South), wus2 (West US 2), ae (Australia East), eus2 (East US 2), ne (North Europe), fc (France Central). `<region>` is the lowcase full spelling, e.g., eastus, southeastasia.
