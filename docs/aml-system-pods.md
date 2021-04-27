| Component Name      | Description |
| ----------- | ----------- |
| aml-operator-* | Manages and executes job requests represented by **amljob** resources|                     
| cluster-status-reporter-* ||              
| fluent-bit-* |Metrics and logs from the training jobs deployed|                                                                          
| frameworkcontroller-* ||                                
| gateway-* | Converts incoming job requests to **amljob** resources and communicates job and cluster status to the Job Scheduler service|                            
| metrics-controller-manager-* ||                                               
| nfd-* | Detects hardware features and system configuration, exposing as labels on nodes ([third-party](https://github.com/kubernetes-sigs/node-feature-discovery)) |                                                                        
| prom-operator-* | Reporting AML training jobs metrics back to Azure. Not collecting metrics for other workloads deployed|                       
| prometheus-prom-prometheus-* ||                          
| relayserver-* | Relay server service enables you to securely expose services that run in your corporate network to the public cloud|                                                     
| tls-creator-* ||                                     
| trainingcompute-kube-state-metrics-* ||   
| webhook-patcher-* ||                                 
