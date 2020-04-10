from ntpath import basename
import boto3
from requests import post as POST
from requests_toolbelt import MultipartEncoder

default_headers = {"Content-Type": "application/json"}
fuseki_url_template = '{protocol}://{ip_address}:{port_number}/{data_set_name}'
s3client = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FilePartitions')


def lambda_handler(event, context):
    record = event['Records'][0]
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']

    file_path = '/tmp/' + s3object
    print('file path of download', file_path)
    s3client.Bucket(s3bucket).download_file(s3object, file_path)
    print('Import to Fuseki server started..')

    import_data_to_fuseki('test_data_set', file_path, s3object)


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
        table.update_item(
            Key={
                'PartitionID': partition_id
            },
            UpdateExpression='SET FileStatus = :val1',
            ExpressionAttributeValues={
                ':val1': 'failed'
            }
        )
    else:
        table.update_item(
            Key={
                'PartitionID': partition_id
            },
            UpdateExpression='SET FileStatus = :val1',
            ExpressionAttributeValues={
                ':val1': 'imported'
            }
        )
        print("POST request success for " + response.url)


def build_url(data_set, protocol="http", ip_address="18.189.3.57", port_number=3030):
    if not data_set:
        data_set = "test_data_set"

    url_template = fuseki_url_template + "/data"
    url = url_template.format(protocol=protocol, ip_address=ip_address,
                              port_number=port_number, data_set_name=data_set)
    return url


