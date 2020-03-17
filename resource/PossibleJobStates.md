**Introduction**

This document is to list all the possible states that a job/task may go through while in the AWS pipeline.
These states form the values of ***status*** column in both Primary and Secondary tables in DynamoDB.

The various states are as follows:

1. ***Yet to be processed*** : This state indicates that a task/job is yet be to  started. For example, URL Downloader Lambda may not have started the downloading process of a particular URL. Thus, the table may reflect this by having a 'yet to be proccesed' value in the status column. 

2. ***Processing*** : This state indicates that a job/task is currently in progress. For example, Downloader Lambda may change the status of a job/task in the table to processing, if it is being downloaded at present.

3. ***Processed*** : This is the final state of a job/task. If the task is over, then status column gets updated as ***'processed'***.

