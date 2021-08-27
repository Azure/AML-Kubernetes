## Meet network requirements

If your cluster has Internect access, it's all done. Otherwise, If the cluster is behind the outbound proxy or firewall with strict outbound network, make sure following protocols/ports/outbound URLs to function.

- HTTPs on port 443: https://:443
    - Container registries to host Arc or ML related docker images
    ```
    *.azurecr.io
    *.quay.io
    auth.docker.io
    gcr.io
    quay.io
    registry-1.docker.io
    storage.googleapis.com
    production.cloudflare.docker.com
    mcr.microsoft.com
    ```
    - Azure related services
    ```
    *.blob.core.windows.net
    *.cdn.mscr.io
    *.data.mcr.microsoft.com
    *.hcp.*.azmk8s.io
    *.kusto.windows.net
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
    changelogs.ubuntu.com
    cloudflare.docker.com
    data.policy.core.windows.net
    dc.services.visualstudio.com
    gbl.his.arc.azure.com
    go.microsoft.com
    guestnotificationservice.azure.com
    login.microsoftonline.com
    management.azure.com
    management.azure.com
    nvidia.github.io
    onegetcdn.azureedge.net
    packages.microsoft.com
    ppa.launchpad.net
    pypi.org
    security.ubuntu.com
    store.policy.core.windows.net
    sts.windows.net
    us.download.nvidia.com
    ```

- HTTP on port 80: http://80
    - Container registries to host Arc or ML related 
    ```
    auth.docker.io
    gcr.io
    production.cloudflare.docker.com
    registry-1.docker.io
    storage.googleapis.com
    ```
    - Azure related services
    ```
    *.mp.microsoft.com
    azure.archive.ubuntu.com
    changelogs.ubuntu.com
    ctldl.windowsupdate.com
    security.ubuntu.com
    www.msftconnecttest.com
    ```

>Note: `<region-code>` mapping for Azure cloud regions: eus (East US), weu (West Europe), wcus (West Central US), scus (South Central US), sea (South East Asia), uks (UK South), wus2 (West US 2), ae (Australia East), eus2 (East US 2), ne (North Europe), fc (France Central). `<region>` is the lowcase full spelling, e.g., eastus, southeastasia.
