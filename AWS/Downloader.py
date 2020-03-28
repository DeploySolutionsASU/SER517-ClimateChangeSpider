import json

import gzip
import urllib.request
from io import BytesIO

import boto3
import time
from botocore.exceptions import ClientError
from pip._internal.utils import logging


def download_file(url, output_path):
    start_time = time.time()
    print("Download start time : ", start_time)
    try:
        urllib.request.urlretrieve(url, output_path)
    except Exception as e:
        print(e)
    else:
        print("Download end time : ", time.time() - start_time)


def upload_file_to_s3(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name.split("/")[-1]

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        start_time = time.time()
        print(file_name, "Upload start time is :", start_time)

        s3_client.upload_fileobj(  # upload a new obj to s3
            Fileobj=gzip.GzipFile(  # read in the output of gzip -d
                None,  # just return output as BytesIO
                'rb',  # read binary
                fileobj=BytesIO(open(file_name, "rb").read())),
            Bucket=bucket,  # target bucket, writing to
            Key=object_name)  # target key, writing to

        print(file_name + "upload file done for ", file_name, " at ", time.time() - start_time)
    except ClientError as e:
        logging.error(e)
        return False
    else:
        print("Upload end time : ", time.time() - start_time)

    return True


def update_job_status(job_id, job_status):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FileDownloads')
    table.update_item(
        Key={
            'JobID': job_id,
        },
        UpdateExpression='SET FileStatus = :status',
        ExpressionAttributeValues={
            ':status': job_status
        }
    )
    print("updated the job status as ", job_status)


def lambda_handler(event, context):
    # # source_file_name = event["Records"][0]["s3"]["object"]["key"]
    # print(event,"\n", context)
    # return

    splits = event["Records"][0]["body"].split(",")
    url = splits[0]
    key = splits[1]

    print(url, key)

    file_path = "/tmp/" + key + ".gz"

    download_file(url, file_path)
    upload_file_to_s3(file_path, "climatechange-downloads", key + ".nq")
    update_job_status(key, "downloaded")


