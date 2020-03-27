# http://data.dws.informatik.uni-mannheim.de/structureddata/2019-12/quads/dpef.html-rdfa.nq-00000.gz
# http://data.dws.informatik.uni-mannheim.de/structureddata/2019-12/quads/dpef.html-rdfa.nq-00001.gz
# http://data.dws.informatik.uni-mannheim.de/structureddata/2019-12/quads/dpef.html-rdfa.nq-00002.gz
# http://data.dws.informatik.uni-mannheim.de/structureddata/2019-12/quads/dpef.html-rdfa.nq-00003.gz
# http://data.dws.informatik.uni-mannheim.de/structureddata/2019-12/quads/dpef.html-rdfa.nq-00004.gz
# http://data.dws.informatik.uni-mannheim.de/structureddata/2019-12/quads/dpef.html-rdfa.nq-00005.gz
# http://data.dws.informatik.uni-mannheim.de/structureddata/2019-12/quads/dpef.html-rdfa.nq-00006.gz
import boto3
import wget
import time





from botocore.exceptions import ClientError
from pip._internal.utils import logging


def download_file(url, output_path):

    start_time = time.time()
    print("Download start time : ", start_time)
    try:
        wget.download(url, out=output_path)
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
        s3_client.upload_file(file_name, bucket, object_name)
        print(file_name + "upload file done for ", file_name, " at ", time.time()-start_time)
    except ClientError as e:
        logging.error(e)
        return False
    else:
        print("Upload end time : ", time.time() - start_time)

    return True


def lambda_handler(event, context):

    # update dyna status

    url = "http://data.dws.informatik.uni-mannheim.de/structureddata/2019-12/quads/dpef.html-rdfa.nq-00000.gz"
    key = "11"

    file_path = "./tmp1/" + key + ".nq"

    # download_file(url, file_path)
    upload_file_to_s3(file_path, "climatechange-downloads", key + ".nq")


if __name__ == '__main__':
    lambda_handler(None, None)
