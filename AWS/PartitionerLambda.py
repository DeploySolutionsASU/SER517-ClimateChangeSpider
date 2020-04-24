import boto3
import uuid
import math
import json
from subprocess import call

sqs_q = {
    "url_q": 'https://sqs.us-east-1.amazonaws.com/967866184802/url_queue',
    "status_q": 'https://sqs.us-east-1.amazonaws.com/967866184802/status_queue.fifo'
}

def send_message(queue_url, body, q_type="STD"):
    sqs = boto3.client('sqs')
    if q_type == "FIFO":
        response = sqs.send_message(
                                    QueueUrl=queue_url,
                                    DelaySeconds=0,
                                    MessageAttributes={},
                                    MessageGroupId="status_update",
                                    MessageDeduplicationId=str(uuid.uuid4()),
                                    MessageBody=(body))
    else:
        response = sqs.send_message(
                                    QueueUrl=queue_url,
                                    DelaySeconds=0,
                                    MessageAttributes={},
                                    MessageBody=(body))

def delete_file():
    call('rm -rf /tmp/*', shell=True)


def update_primary_table(job_id):
    payload = {
        'Op': 'update_item',
        'Table': 'FileDownloads',
        'Key': {
            'JobID': job_id,
        },
        'UpdateExpression':'SET FileStatus = :status',
        'ExpressionAttributeValues': {
            ':status': 'partitioned'
    }
    }
    send_message(sqs_q["status_q"], json.dumps(payload), "FIFO")


def update_secondary_table(job_id, partition_id):
    payload = {
        'Op': 'put_item',
        'Table': 'FilePartitions',
        'Item': {
            'JobID': job_id,
            'PartitionID': partition_id,
            'FileStatus': 'partitioned',
    }
    }
    send_message(sqs_q["status_q"], json.dumps(payload), "FIFO")


def splitter(data, bucket_key, threshold=50000):
    # File partitioned for the given threshold
    
    file_count = 0
    total_file = math.ceil(len(data) / 50000)
    
    for i in range(0, len(data), threshold):
        file_count += 1;
        counter = str(uuid.uuid4());
        chunk = data[i:min(i + threshold, len(data))]
        filename = 'part_' + counter + ".nq"
        
        with open('/tmp/' + filename, 'w') as file:
            for line in chunk:
                file.write('%s\n' % line.decode('utf-8'))
    
        news3 = boto3.client('s3')
        file_path = '/tmp/' + filename
        
        # Upload the files to the new S3
        response = news3.upload_file(file_path, 'climatechange-partitions',
                                     filename)
        delete_file()
        update_secondary_table(bucket_key, filename)

        # Update the table for the status
        if file_count == total_file:
            update_primary_table(bucket_key)



def lambda_handler(event, context):
    # Access the S3
    record = event['Records'][0]
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']
    s3 = boto3.resource('s3')
    
    # Fetch the file from S3
    s3_client = boto3.client('s3')
    start = 0
    limit = 500000000
    base_limit = 500000000
    # create byte range as string
    rec = s3_client.head_object(Bucket=s3bucket, Key=s3object)
    end = rec['ContentLength']
    
    #print("RECORD LEN ", rec['ContentLength'])
    n = rec['ContentLength'] / limit
    n = math.ceil(n)
    
    for i in range(0, n):
        rangeString = 'bytes=' + str(start) + '-' + str(limit - 1)
        print('start: ', start)
        print('limit: ', limit)
        record = s3_client.get_object(Bucket=s3bucket, Key=s3object, Range=rangeString)
        final_content = record["Body"].read().splitlines()

        
        Job_key = s3object.split('.nq')[0]

        try:
            splitter(final_content, Job_key)
            print('Upload success!!')
        except Exception as ex:
            print("Error in Partitioner", ex)
      
        if limit >= end:
            break
        else:
            start = limit
            limit = limit + base_limit
