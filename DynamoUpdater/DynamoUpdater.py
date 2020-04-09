
import json
import boto3


dynamodb = boto3.resource('dynamodb')


def receive_msg(msg_count):
    client = boto3.client('sqs', region_name='us-east-1')
    response = client.receive_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/967866184802/status_queue.fifo',
        AttributeNames=['All'],
        MaxNumberOfMessages=msg_count,
        VisibilityTimeout=10,
        WaitTimeSeconds=0
    )

    if u'Messages' in response and len(response[u'Messages']) > 0:
        return response[u'Messages']
    else:
        print("No Message in the Queue")
        return None


def handle_message(data):
    print(json)
    if data["Op"] == "put_item":
        dynamodb.Table(data['Table']).put_item(Item=data["Item"])
    elif data["Op"] == "update_item":
        table = dynamodb.Table(data['Table'])
        table.update_item(
            Key=data["Key"],
            UpdateExpression=data["UpdateExpression"],
            ExpressionAttributeValues=data["ExpressionAttributeValues"])
    else:
        pass


def delete_msg(receipt_handle):
    client = boto3.client('sqs', region_name='us-east-1')
    response = client.delete_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/967866184802/status_queue.fifo',
        ReceiptHandle=receipt_handle
    )
    print(response)


if __name__ == '__main__':

    while True:
        msgs = receive_msg(10)
        print(msgs)
        if msgs is not None:
            for msg in msgs:
                msg_body = json.loads(msg[u'Body'])
                receipt_handle = msg[u'ReceiptHandle']
                handle_message(msg_body)
                delete_msg(receipt_handle)
