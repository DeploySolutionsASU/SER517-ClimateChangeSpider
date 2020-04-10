**********Elasticsearch setup on AWS Cloud**********

Setting up Elastic search on AWS includes following steps:

1. Creating Amazon ES Domain
    Here you can provide the domain name, number of data nodes and Elastic search version. (Recommended : Latest version)

2. Configuring Amazon ES Domain
    Here you can configure the instance count, instance type and storage configuration. We can also use the 
    elasticsearch-cluster-config option to configure your Amazon ES cluster by using the AWS CLI
     
3.Configuring EBS-based Storage    
4. Modifying VPS access configuration
5. Configuring Amazon Cognito Authentication for Kibana
6. Configuring Access Policies
7. Configuring Advanced Options
8. Configuring Logs
    If we configure to enable error logs, Amazon ES publishes log lines of WARN, ERROR, and FATAL to CloudWatch. They can be helpful
    in troubleshooting indexing issues, snapshot failures and invalid queries.
