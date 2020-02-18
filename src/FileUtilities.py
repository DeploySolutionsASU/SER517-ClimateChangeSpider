import gzip
import os
import logging

from Config import path_config
from HelperManager import get_root_directory


# unzip files
def unzip_file(file, output_path):
    try:
        fp = open(output_path, "wb")
        with gzip.open(file, "rb") as f:
            bind_data = f.read()
        fp.write(bind_data)
        fp.close()
    except Exception as e:
        logging.error(e)


# Read the files from the directory and unzip
def read_files_to_unzip(download_path):
    print("Unzip start")
    for filename in os.listdir(download_path):
        if filename.endswith(".gz"):
            file = os.path.join(download_path, filename)
            curr_path = get_root_directory() + "/" + path_config["extract_folder"]
            file_name_output = filename.split('.gz')[0]
            download_path = curr_path + '/' + file_name_output
            unzip_file(file, download_path)
        else:
            continue
    print("Unzip end")
