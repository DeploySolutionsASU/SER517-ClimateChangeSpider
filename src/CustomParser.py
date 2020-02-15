import os
import subprocess
import time
import uuid

from os import walk
import re

from ThreadPoolManager import start_job

from collections import defaultdict


root_dir = os.path.abspath('..')
root_dir = root_dir.replace('\\', '/')
data_directory_path = root_dir + '/data/'

riot_path = "/Users/aj/Developer/apache-jena-3.14.0/bin/riot"

command_template = riot_path + " " + "--validate" + " " + "{file_path}"

pwd = "./"

temp_dir = root_dir + "/temp/"
data_dir = "../data/"


def splitter(file_path, threshold=50000):
    all_data = defaultdict(list)
    start = time.process_time()


    with open(file_path, "r") as file:
        data = file.readlines()
        for i in range(0, len(data), threshold):
            chunk = data[i:min(i + threshold, len(data))]
            all_data[str(uuid.uuid4())] = chunk

    print("read time: ", time.process_time() - start)

    return all_data


def parse_file(guid, data):
    print(guid, "started...")
    try:
        output_file_path = temp_dir + guid + ".nq"

        # write to a file for validation
        with open(output_file_path, 'w') as file:
            file.writelines(data)


        validation_result = run_command(command_template.format(file_path=output_file_path).split())

        error_line_nos = set()

        for result in validation_result:
            result = str(result)
            print(result)
            splits = result.split("::")

            if re.search('ERROR riot', splits[0]):
                error_line_nos.add(int(re.findall(r'[0-9]+', splits[1])[0]))

        print(error_line_nos)

        if len(error_line_nos) == 0:
            print("Parsing done")
            return True

        for erro_line_no in error_line_nos:
            del data[erro_line_no - 1]

        parse_file(guid, data)
    except Exception as exc:
        print(exc)
        return False
    else:
        print(guid, "done")


def run_command(command):
    file_output = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
    return iter(file_output.stdout.readline, b'')


if __name__ == '__main__':

    files_to_process = []
    for (dir_path, dir_names, file_name) in walk(data_dir):
        files_to_process.extend([dir_path + "/" + file for file in file_name])
        break
    print(files_to_process)

    for file_path in ['../data//dpef.html-embedded.nq']:
        start_job(splitter(file_path), parse_file, 50)
