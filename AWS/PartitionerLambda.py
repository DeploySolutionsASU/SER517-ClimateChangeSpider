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
    for i in range(0, len(data), threshold):
        counter = str(uuid.uuid4());
        chunk = data[i:min(i + threshold, len(data))]
        filename = 'part_' + counter + ".nq"

        with open('/tmp/' + filename, 'w') as file:
            for line in chunk:
                file.write('%s\n' % line.decode('utf-8'))

        news3 = boto3.client('s3')
        file_path = '/tmp/' + filename
        response = news3.upload_file(file_path, 'partitionedfiles',
                                     filename)
        delete_file()
