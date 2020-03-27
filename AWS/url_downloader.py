import boto3
import urllib.request


def download_file(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')
    return text



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
        for value in values[:1]:
            insert_into_db(str(job_id), value)
            job_id += 1

if __name__ == '__main__':
    lambda_handler(None,None)

