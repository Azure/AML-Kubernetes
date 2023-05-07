CLI tool to generate k8s quotaoverrides custom resource file accourding to user's config file
```
usage: get_quotaoverrides_cr.py [-h] --config CONFIG --output OUTPUT --name NAME

give a config yaml, generate quotaoverrides custom resource yaml, suggests to run [az login] first before using the command

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  yaml file path of user's quota override config file
  --output OUTPUT  yaml file path of generated k8s quotaoverrides custom resource file
  --name NAME      name of quotaoverrides custom resource
```
the user config file should be like this:
```yaml
tierOverrides:
  <tier_to_override>:
    <quota_resource_type>: <quota_resource_value>
userIdentifiers:
  users:
    - <user_mail>
  groups:
    - <group_id>
```

## example
### edit the config file in current path, name it config.yaml
```yaml
tierOverrides:
  my_tier1:
    myquota1: myquota1
    myquota2: myquota2
  my_tier2:
    myquota1: myquota1
    myquota2: myquota2
userIdentifiers:
  users:
    - my-first-user
    - my-second-user
  groups:
    - my-first-group
    - my-second-group
```
### run the CLI command, set the output file in current path
```
get_quotaoverrides_cr.py --config ./config.yaml --output ./output.yaml --name example
```
### check output.yaml in current path
```yaml
apiVersion: amlarc.azureml.com/v1
kind: QuotaOverride
metadata:
  labels:
    app.kubernetes.io/instance: example
    app.kubernetes.io/name: quotaoverride
  name: example
spec:
  tierOverrides:
    my_tier1:
      myquota1: myquota1
      myquota2: myquota2
    my_tier2:
      myquota1: myquota1
      myquota2: myquota2
  userIdentifiers:
  - userIdentifiers
```