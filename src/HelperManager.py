import os
import logging

from Config import path_config


# Function to create directory
def create_directory(file_path):
    try:
        os.makedirs(file_path)
    except OSError as error:
        logging.warning(error)


# Function to get root path
def get_root_directory():
    root_dir = os.path.abspath('..')
    root_dir = root_dir.replace('\\', '/')
    return root_dir


# Function to create folders
def folders_creation():
    data_source_path = os.path.join(get_root_directory(), path_config["data_source"])
    downloads_path = os.path.join(get_root_directory(), path_config["download_folder"])
    server_dir_path = os.path.join(get_root_directory(), path_config["server_folder"])

    create_directory(data_source_path)
    create_directory(downloads_path)
    create_directory(server_dir_path)
