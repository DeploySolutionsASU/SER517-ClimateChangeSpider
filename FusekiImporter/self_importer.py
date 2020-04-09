import subprocess
import time
import boto3
import urllib.request
from os.path import basename
from subprocess import call
from requests_toolbelt import MultipartEncoder
from requests import post as POST


default_headers = {"Content-Type": "application/json"}
fuseki_url_template = '{protocol}://{ip_address}:{port_number}/{data_set_name}'


def receive_msg(msg_count):
    client = boto3.client('sqs', region_name='us-east-1')
    response = client.receive_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/967866184802/import_queue',
        AttributeNames=['All'],
        MaxNumberOfMessages=msg_count,
        VisibilityTimeout=30,
        WaitTimeSeconds=0,
        ReceiveRequestAttemptId='string'
    )

    if u'Messages' in response and len(response[u'Messages']) > 0:
        return response[u'Messages']
    else:
        print("No Message in the Queue")
        return None


def delete_msg(receipt_handle):
    client = boto3.client('sqs', region_name='us-east-1')
    response = client.delete_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/967866184802/import_queue',
        ReceiptHandle=receipt_handle
    )
    print(response)
    # return True


def download_file(obj_name, file_path):
    s3 = boto3.resource('s3')
    s3.Bucket("climatechange-parsed-files").download_file(obj_name, file_path)


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


def import_data_to_fuseki(data_set_name, file_path, partition_id):
    file_name = basename(file_path)

    multipart_data = MultipartEncoder(fields={'file': (file_name,
                                                       open(file_path, 'rb'),
                                                       'text/plain')})
    url = build_url(data_set=data_set_name)
    print('Request url---', url)
    make_http_post_request(url, partition_id=partition_id,
                           payload=multipart_data,
                           headers={'Content-Type': multipart_data.content_type})


def make_http_post_request(url, partition_id, payload=None, headers=default_headers):
    try:
        request_headers = {**default_headers, **headers}
        response = POST(url=url, data=payload, headers=request_headers)
        response.raise_for_status()

    except Exception as ex:
        print("Exception: ", str(ex))
        update_job_status(partition_id, "Failed")
        restart()

    else:
        update_job_status(partition_id, "Imported")

        print("POST request success for " + response.url)


def build_url(data_set, protocol="http", ip_address="localhost", port_number=3030):
    if not data_set:
        data_set = "test_data_set"

    url_template = fuseki_url_template + "/data"
    url = url_template.format(protocol=protocol, ip_address=ip_address,
                              port_number=port_number, data_set_name=data_set)
    return url


def delete_file(file_path):
    call('rm -rf '+file_path, shell=True)


def handle_message(s3_url, partition_id):
    try:
        file_path = "/tmp/"+partition_id
        download_file(partition_id, file_path)
        import_data_to_fuseki("test_data_set", file_path, partition_id)
        delete_file(file_path)
    except Exception as ex:
        print(ex)
        return False
    else:
        return True


def run_command(command):
    file_output = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
    return iter(file_output.stdout.readline, b'')


def restart():
    run_command("sh restart.sh".split())
    time.sleep(20)


if __name__ == '__main__':
    i = 0
    while True:
        msgs = receive_msg(10)
        print(msgs)
        if msgs is not None:
            for msg in msgs:

                s3_url, partition_id = msg[u'Body'].split(",")
                receipt_handle = msg[u'ReceiptHandle']
                handle_message(s3_url, partition_id)
                delete_msg(receipt_handle)
                if i % 100 == 0:
                    restart()
                i += 1
                print("i value is ", i)


