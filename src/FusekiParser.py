import os
import subprocess
import time
import uuid
import re

from os import walk
from Config import global_config
from ThreadPoolManager import start_job
from collections import defaultdict
from HelperManager import create_directory
from HelperManager import get_root_directory
from FusekiImporter import import_data_to_fuseki

riot_path = global_config["riot_path"]
command_template = riot_path + " " + "--validate" + " " + "{file_path}"

temp_folder = os.path.join(get_root_directory(), 'temp')
create_directory(temp_folder)

temp_dir = get_root_directory() + "/temp/"
data_dir = "../data/"
n_quads_extension = ".nq"
data_set_name = "test_data_set"


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
            splits = result.split("::")

            if re.search('ERROR riot', splits[0]):
                error_line_nos.add(int(re.findall(r'[0-9]+', splits[1])[0]))

        print(error_line_nos)

        if len(error_line_nos) == 0:
            import_data_to_fuseki(data_set_name, output_file_path)
            return True

        for error_line_no in error_line_nos:
            del data[error_line_no - 1]

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
    print("Files to Process: ", files_to_process)

    for file_path in files_to_process:
        if file_path.endswith(n_quads_extension):
            start_job(splitter(file_path), parse_file, 50)
