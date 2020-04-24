import boto3
import urllib.request
import json
import uuid

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

            MessageBody=(body))
    else:
        response = sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=0,
            MessageAttributes={},
            MessageBody=(body))
        print(body, response)


def insert_into_db(job_id, url_value):
    payload = {
        'Op': 'put_item',
        'Table': 'FileDownloads',
        'Item': {
            'JobID': job_id,
            "Url": url_value,
            'FileStatus': 'tobedownloaded'
        }
    }
    send_message(sqs_q["status_q"], json.dumps(payload), "FIFO")


def download_file(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')
    return text


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
        print("Total url count for {alist} is {c}".format(alist=url, c=len(values)))
        for value in values:
            insert_into_db(str(job_id), value)
            send_message(sqs_q["url_q"], '{url},{id}'.format(url=value, id=job_id))
            job_id += 1
