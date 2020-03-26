import boto3
import uuid
import math
from subprocess import call


def delete_file():
    call('rm -rf /tmp/*', shell=True)


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

        # Insert in the secondary table  with job_id and uu_id

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('FilePartitions')
        table.put_item(
            Item={
                'JobID': bucket_key,
                'PartitionID': filename,
                'FileStatus': 'partitioned',
            }
        )
        print("entry made in the secondary table")

    # Update the table for the status
    if file_count == total_file:
        # Update DynamoDB main table

        table = dynamodb.Table('FileDownloads')
        table.update_item(
            Key={
                'JobID': bucket_key
            },
            UpdateExpression='SET FileStatus = :val1',
            ExpressionAttributeValues={
                ':val1': 'partitioned'
            }
        )
        print("updated the primary table")


def lambda_handler(event, context):
    # Access the S3
    record = event['Records'][0]
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']
    s3 = boto3.resource('s3')

    # Fetch the file from S3
    s3_client = boto3.client('s3')
    start = 0
    limit = 1000000000
    base_limit = 1000000000
    # create byte range as string
    rec = s3_client.head_object(Bucket=s3bucket, Key=s3object)
    end = rec['ContentLength']

    print("RECORD LEN ", rec['ContentLength'])
    n = rec['ContentLength'] / limit
    n = math.ceil(n)

    for i in range(0, n):
        rangeString = 'bytes=' + str(start) + '-' + str(limit - 1)
        print('start: ', start)
        print('limit: ', limit)
        record = s3_client.get_object(Bucket=s3bucket, Key=s3object, Range=rangeString)
        final_content = record["Body"].read().splitlines()
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('FileDownloads')

        result = table.get_item(
            Key={
                'JobID': s3object
            }
        )

        job_table_status = result['Item']['FileStatus']
        print('job_table_status', job_table_status)

        if i >= n and job_table_status == 'downloaded':
            table.update_item(
                Key={
                    'JobID': s3object
                },
                UpdateExpression='SET FileStatus = :val1',
                ExpressionAttributeValues={
                    ':val1': 'tobepartitioned'
                }
            )

        if job_table_status != 'tobepartitioned':
            print("updated the primary table")
            splitter(final_content, s3object)
            print('Upload success!!')
        else:
            print('This file is already done')

        if limit >= end:
            break
        else:
            start = start + limit
            limit = limit + base_limit