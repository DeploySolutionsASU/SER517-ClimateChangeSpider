**Introduction**

This document is to list all the possible states that a job/task may go through while in the AWS pipeline.
These states form the values of ***status*** column in both Job and Partition tables in DynamoDB.

The various states are as follows:

1. ***Yet to be processed*** : This state indicates that a task/job is yet be to  started. For example, URL Downloader Lambda may not have started the downloading process of a particular URL. Thus, the table may reflect this by having a 'yet to be proccesed' value in the status column. 

2. ***Processing*** : This state indicates that a job/task is currently in progress. For example, Downloader Lambda may change the status of a job/task in the table to processing, if it is being downloaded at present.

3. ***Processed*** : This is the final state of a job/task. If the task is over, then status column gets updated as ***'processed'***.

In addition to these general states, each lambda function may have their own states. They may be as follows:

1. ***URL Downloader Lambda*** : After a job is initiated, URL downloaeder lambda, downloads a URL and pushes it into the SQS queue. It then updates DynamoDB, with the status, ***Downloaded***.

2. ***Downloader Lambda*** : After this lambda function picks a URL to be downloaded from the SQS queue, it updates the DynamoDB with ***to be processed***.
When it starts downloading a URL, the status gets updated to ***downloading***.
Finally, when the download is complete, status is updated to ***downloaded***.

3. ***Partitioner Lambda*** : Downloaded files stored in the S3 bucket, is picked one by one to be partitioned into many parts, for further processing. When a file is picked by the partitioner lambda, the status gets updated to ***to be partitioned***. When a file has been partitioned, status gets updated to ***partitioned***.

4. ***Parser Lambda*** : Partitions are stored in a S3 bucket. These files are then picked for parsing by the parser lambda. When a file is picked by the parser lambda, the status gets updated to ***to be parsed***. When a file has been partitioned, status gets updated to ***parsed***.

5. ***Importer Lambda*** : Parsed files are stored in a S3 bucket. These files are then picked for parsing by the importer lambda. When a file is picked by the importer lambda, the status gets updated to ***to be imported***. When a file has been imported to the fuseki server, status gets updated to ***imported***.



**Working with tables in DynamoDB**

DynamoDB is a NoSQL database that supports key-value and document data models. Boto3 SDk can be used to easily interact with various services of AWS including DynamoDB, in python. When creating tables in DynamoDB, only the partition key (Primary Key) and it's attributes should be mentioned before hand in the schema
of a table. 

All other attributes (Columns) can be added later during run-time. Since this is NoSQL database, there is no concept of table join or foreign key like SQL databases. All these functions have to be performed in the backend (using python in this case).

A guide to working with tables in DynamoDB, using boto3 sdk can be found here:
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html