import time
import boto3
import paramiko
import os
from typing import re
from requests_toolbelt import MultipartEncoder
from ntpath import basename
from requests import post as POST
from subprocess import call

default_headers = {"Content-Type": "application/json"}
fuseki_url_template = '{protocol}://{ip_address}:{port_number}/{data_set_name}'


def lambda_handler(event, context):
    # Access the S3
    record = event['Records'][0]
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']
    s3client = boto3.resource('s3')
    file_path = '/tmp/' + s3object
    print('file path of download', file_path)
    s3client.Bucket(s3bucket).download_file(s3object, file_path)

    ec2 = boto3.resource('ec2', region_name='us-east-2')
    instance_id = 'i-0371b3b5285cb71fb'
    instance = ec2.Instance(instance_id)
    instance.start()
    time.sleep(60)

    print("----------------------------------------------------")
    print("Instance id - ", instance.id)
    print("Instance public IP - ", instance.public_ip_address)
    print("Instance private IP - ", instance.private_ip_address)
    print("Public dns name - ", instance.public_dns_name)
    print("----------------------------------------------------")

    s3client = boto3.resource('s3')
    s3client.Bucket('climatechange-importer').download_file('FusekiEC2.pem', '/tmp/FusekiEC2.pem')
    if os.path.isfile('/tmp/FusekiEC2.pem'):
        print('File exists')
    else:
        print('File not found')

    # Allowing few seconds for the download to complete
    time.sleep(20)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privkey = paramiko.RSAKey.from_private_key_file('/tmp/FusekiEC2.pem')
    ssh.connect(
        instance.public_dns_name, username='ec2-user', pkey=privkey
    )

    stdin, stdout, stderr = ssh.exec_command('echo "ssh to ec2 instance successful"')
    stdin.flush()
    data = stdout.read().splitlines()
    for line in data:
        print(line)
    ssh.close()
    # instance.stop()

    print('Import to fuseki server')

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FilePartitions')

    result = table.get_item(
        Key={
            'JobID': s3object
        }
    )

    job_table_status = result['Item']['FileStatus']
    print('job_table_status', job_table_status)

    if job_table_status == 'parsed':
        table.update_item(
            Key={
                'JobID': s3object
            },
            UpdateExpression='SET FileStatus = :val1',
            ExpressionAttributeValues={
                ':val1': 'tobeimported'
            }
        )

        import_data_to_fuseki('test_data_set', file_path)
        print('Import done')
        delete_file()
        print('Temp file deleted')

        table.update_item(
            Key={
                'JobID': s3object
            },
            UpdateExpression='SET FileStatus = :val1',
            ExpressionAttributeValues={
                ':val1': 'imported'
            }
        )
    else:
        print('File status not parsed or completed')






def import_data_to_fuseki(data_set_name, file_path):
    file_name = basename(file_path)
    multipart_data = MultipartEncoder(fields={'file': (file_name,
                                                       open(file_path, 'rb'),
                                                       'text/plain')})

    url = build_url(data_set=data_set_name)
    print('Request url---', url)
    make_http_post_request(url, payload=multipart_data, headers={'Content-Type': multipart_data.content_type})


def make_http_post_request(url, payload=None, headers=default_headers):
    try:
        request_headers = {**default_headers, **headers}
        response = POST(url=url, data=payload, headers=request_headers)
        response.raise_for_status()
        json = re(response.text)
    except Exception as ex:
        print(ex)
    else:
        print("POST request success for " + response.url)
        return json


def build_url(data_set, protocol="http", ip_address="3.16.50.118", port_number=3030):
    if not data_set:
        print("Data set name is empty or null")
        return None

    url_template = fuseki_url_template + "/data"
    url = url_template.format(protocol=protocol, ip_address=ip_address,
                              port_number=port_number, data_set_name=data_set)
    return url


def delete_file():
    call('rm -rf /tmp/*', shell=True)
