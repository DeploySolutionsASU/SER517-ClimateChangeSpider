import boto3
import urllib.request


def download_file(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')
    return text


def send_sqs_message(url, job_id):
    # Create SQS client
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/967866184802/url_queue'

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=0,
        MessageAttributes={},
        MessageBody=('{url},{id}'.format(url=url, id=job_id)))
    print(response['MessageId'])


def insert_into_db(job_id, url_value):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FileDownloads')
    table.put_item(
        Item={
            'JobID': job_id,
            "Url": url_value,
            'FileStatus': 'tobedownloaded',
        }
    )


def lambda_handler(event, context):
    urls = ["http://webdatacommons.org/structureddata/2019-12/files/html-rdfa.list",
            "http://webdatacommons.org/structureddata/2019-12/files/html-microdata.list",
            "http://webdatacommons.org/structureddata/2019-12/files/html-embedded-jsonld.list",
            "http://webdatacommons.org/structureddata/2019-12/files/html-mf-geo.list",
            "http://webdatacommons.org/structureddata/2019-12/files/html-mf-hcalendar.list",
            "http://webdatacommons.org/structureddata/2019-12/files/html-mf-hcard.list",
            "http://webdatacommons.org/structureddata/2019-12/files/html-mf-adr.list",
            "http://webdatacommons.org/structureddata/2019-12/files/html-mf-hrecipe.list",
            "http://webdatacommons.org/structureddata/2019-12/files/html-mf-hlisting.list",
            "http://webdatacommons.org/structureddata/2019-12/files/html-mf-hresume.list",
            "http://webdatacommons.org/structureddata/2019-12/files/html-mf-hreview.list",
            "http://webdatacommons.org/structureddata/2019-12/files/html-mf-species.list",
            "http://webdatacommons.org/structureddata/2019-12/files/html-mf-xfn.list"]

    job_id = 0

    for url in urls:
        values = download_file(url).split("\n")
        for value in values:
            insert_into_db(str(job_id), value)
            send_sqs_message(value, job_id)
            job_id += 1


