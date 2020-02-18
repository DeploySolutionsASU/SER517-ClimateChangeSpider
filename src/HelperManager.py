import os
import logging


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
