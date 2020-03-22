import os
import shutil
import boto3
import re
from subprocess import call


def delete_file():
    call('rm -rf /tmp/*', shell=True)


def lambda_handler(event, context):
    record = event['Records'][0]
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']
    s3_client = boto3.client('s3')
    record = s3_client.get_object(Bucket=s3bucket, Key=s3object)
    final_content = record["Body"].read().splitlines()
    if not os.path.isdir('/tmp/fuseki'):
        shutil.copytree('/var/task/fuseki', '/tmp/fuseki')
        print('Folder copied')

    if not os.path.isdir('/tmp/fuseki/apache-jena-3.14.0/bin'):
        print('not exits')
    else:
        print('exists')

    riot_path = '/tmp/fuseki/apache-jena-3.14.0/bin/riot'
    riot_path1 = '/tmp/fuseki/apache-jena-3.14.0/bin'
    riot_path2 = '/tmp/fuseki/apache-jena-3.14.0'
    # command = "export" + " " + "PATH" + "=" + "/tmp/fuseki/apache-jena-3.14.0/bin"
    # set_environment(command)
    os.chmod(riot_path, 0o777)
    os.chmod(riot_path1, 0o777)
    os.chmod(riot_path2, 0o777)
    mask = oct(os.stat(riot_path).st_mode)[-3:]
    print("File permission--", mask)
    parse_file(s3object, final_content)



def parse_file(filename, data):
    riot_path = '/tmp/fuseki/apache-jena-3.14.0/bin/riot'
    command_template = riot_path + " " + "--validate" + " " + "{file_path}"
    try:
        output_file_path = '/tmp/' + filename

        print('start creating file')
        with open(output_file_path, 'w') as file:
            for line in data:
                file.write('%s\n' % line.decode('utf-8'))


        error_line_nos = set()

        if len(error_line_nos) == 0:
            news3 = boto3.client('s3')
            file_path = '/tmp/' + filename
            news3.upload_file(file_path, 's3parsedfiles',
                                         filename)
            print('Upload success!!')
            return True

        print("error no", error_line_nos)
        for error_line_no in error_line_nos:
            del data[error_line_no - 1]

        parse_file(filename, data)

    except Exception as exc:
        print('error--', exc)
        return False
    else:
        print(filename, "done")
