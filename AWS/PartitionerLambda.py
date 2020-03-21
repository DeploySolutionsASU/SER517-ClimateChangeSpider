import json
import boto3
import io
import uuid
import re
from subprocess import call
from subprocess import check_output


def delete_file():
    call('rm -rf /tmp/*', shell=True)


def splitter(data, threshold=50000):
    # File partitioned for the given threshold
    for i in range(0, len(data), threshold):
        counter = str(uuid.uuid4());
        chunk = data[i:min(i + threshold, len(data))]
        filename = 'part_' + counter + ".nq"

        with open('/tmp/' + filename, 'w') as file:
            for line in chunk:
                file.write('%s\n' % line.decode('utf-8'))

        news3 = boto3.client('s3')
        file_path = '/tmp/' + filename

        # Upload the files to the new S3
        response = news3.upload_file(file_path, 'partitionedfiles',
                                     filename)
        delete_file()


def lambda_handler(event, context):
    # Access the S3
    record = event['Records'][0]
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']
    s3 = boto3.resource('s3')

    # Fetch the file from S3
    s3_client = boto3.client('s3')
    record = s3_client.get_object(Bucket=s3bucket, Key=s3object)
    final_content = record["Body"].read().splitlines()

    splitter(final_content)
    print('Upload success!!')