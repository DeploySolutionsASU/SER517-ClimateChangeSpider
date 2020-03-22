import os
import shutil
import subprocess
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

    riot_path = '/tmp/fuseki/apache-jena-3.14.0/bin/riot'
    os.chmod(riot_path, 0o777)
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
        validation_result = run_command(command_template.format(file_path=output_file_path).split())
        for result in validation_result:
            result = str(result)
            splits = result.split("::")
            print('result----', result)
            print('splits[0]----', splits[0])
            if re.search('ERROR riot', splits[0]):
                error_line_nos.add(int(re.findall(r'[0-9]+', splits[1])[0]))
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


def run_command(command):
    print('command---', command)
    file_output = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
    return iter(file_output.stdout.readline, b'')
