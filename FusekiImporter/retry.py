import boto3
import json
from boto3.dynamodb.conditions import Key



def send_sqs_message(url, job_id):
    # Create SQS client
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/967866184802/import_queue'

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=0,
        MessageAttributes={},
        MessageBody=('{url},{id}'.format(url=url, id=job_id)))
    print(response['MessageId'])


def update_job_status(job_id, job_status):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FilePartitions')
    table.update_item(
        Key={
            'PartitionID': job_id,
        },
        UpdateExpression='SET FileStatus = :status',
        ExpressionAttributeValues={
            ':status': job_status
        }
    )
    print("updated the job status as ", job_status)

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('FilePartitions')

# fe = Key('FileStatus').
pe = "PartitionID, JobID, #yr"
# Expression Attribute Names for Projection Expression only.
ean = { "#yr": "FileStatus", }
esk = None


response = table.scan(
    ProjectionExpression=pe,
    ExpressionAttributeNames=ean
    )

for i in response['Items']:
    update_job_status(i["PartitionID"], "Parsed")

    send_sqs_message("https://climatechange-parsed-files.s3.amazonaws.com/"+ i["PartitionID"],
                     i["PartitionID"])


while 'LastEvaluatedKey' in response:
    response = table.scan(
        ProjectionExpression=pe,
        FilterExpression=fe,
        ExpressionAttributeNames= ean,
        ExclusiveStartKey=response['LastEvaluatedKey']
        )

    for i in response['Items']:
        print(json.dumps(i))
