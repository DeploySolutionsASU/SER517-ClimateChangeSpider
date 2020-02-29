**SQS (Simple Queue Service) **
**Introduction**
•	Amazon Simple Queue Service (SQS) is a fully managed message queuing service that enables 
    you to decouple and scale microservices, distributed systems, and server less applications.
•	It can transfer any volume of data, at any level of throughput without losing the messages

**Benefits**
•	Eliminate administrative overhead, there is no upfront cost and no need to install.
•	Keep sensitive data secure, using server-side encryption we can keep the data secure and helps 
    to exchange sensitive data between the applications.
•	Multiple copies of every message are stored redundantly across multiple availability zones so that 
    they are available whenever needed.
•	Amazon SQS leverages the AWS cloud to dynamically scale based on demand.

**Types**
Standard queues:
•	Support unlimited number of transactions per second
•	A message is delivered at least once but occasionally more than one copy of the message will get 
    delivered
•	Occasionally the messages won't deliver in the proper order
FIFO queues:
•	By default, it supports 300 messages per second if we send the messages in batch-wise 
    (maximum 10 messages per operation) FIFO queue support 3000 messages per second
•	A message is delivered once and remains available until a consumer process and deletes it. 
    Duplicates aren't introduced into the queue.
•	The order in which messages are sent and received is strictly preserved (i.e. First-In-First-Out).

**Functionality**
•	Payload Size: Message payloads can contain up to 256KB of text in any format. Each 64KB ‘chunk’ 
    of the payload is billed as 1 request.
•	For example, a single API call with a 256KB payload will be billed as four requests. 
    To send messages larger than 256KB, you can use the
•	Amazon SQS Extended Client Library for Java, which uses Amazon S3 to store the message payload.
    A reference to the message payload is sent using SQS.
•	Batches: Send, receive, or delete messages in batches of up to 10 messages or 256KB.
•	Retain messages for up to 14 days
•	Messaging locking, the message will be locked when it is under processing which prevents other 
    computers to process the message simultaneously
•	Server-side encryption (SSE)
•	Dead Letter Queues (DLQ): Handle messages that have not been successfully processed by a consumer 
    with Dead Letter Queues.

**Pricing**
•	The first 1 million requests are free.
•	Up to 1 Gb of data transfer is free per month.
•	Refer this link to know more about pricing: https://aws.amazon.com/sqs/pricing/

**Queue Creation**
1.	Go to SQS console by searching it in the services
2.	Enter the name of the queue (Eg: Files Queue which I have a created)
3.	We can configure our queue with custom settings like
4.	Queue attributes:
    •	Message Retention Period: Can be between 1 to 14 days
    •	Visibility timeout is the amount of time the message is claimed out
    •	Maximum message size -> 1 to 256kb
    •	Receive message wait time to perform long pooling
    •	Dead letter queue: It is the fall back queue and when a message gets failed for 
        three times (default) it will be moved to separate queue which can be processed later
    •	AWS KMS for encryption when we are transmitting sensible data
5.	After creation, the queue will get selected or select the queue name. Under queue actions, 
    there are a list of options like send a message, configuration, delete queue and configure 
    trigger for lambda function
6.	To send a message to the queue:
    •	Click the send a message, a separate window will appear and we can provide the message body 
        and attributes
    •	Type the message in the message body and click send, after sending this message 
        will be consumed by the consumers
7.	We can connect our SQS with lambda in two ways
    - By adding a trigger in lambda
        •	Example: To set a trigger for lambda function when the SQS receive any message
        •	Create a lambda function first from lambda console and add policy (AmazonSQSFullAccess)
        •	Add trigger as SQS and attach the SQS which we have created already 
            (Now the SQS and Lambda has been connected)
    - Another way to connect lambda is using Configure trigger for lambda function in SQS 
      (This option is available under Queue Actions in SQS) there we can select the lambda to get triggered
8.	When we send a message to SQS, the corresponding lambda will get triggered and we can see 
    the logs in CloudWatch (Make sure to add CloudWatch policy to the lambda)

**To View CloudWatch logs**
    •	Go to Cloud watch management console
    •	Select Logs from the left panel
    •	Now we can see the list of log group and select the one which we want to see logs    

SQS also helps us to communicate from one lambda to another

**AWS Lambda**
•	AWS Lambda is a compute service that runs the code in response to events and automatically
    manages the underlying compute resources for us.
•	we can use AWS Lambda to extend other AWS services with custom logic or 
    create our back-end services that operate at AWS scale, performance, and security.

**References**
    - https://aws.amazon.com/getting-started/tutorials/send-messages-distributed-applications/
    - https://www.youtube.com/watch?v=JJQrVBRzlPg
    - https://aws.amazon.com/sqs/
