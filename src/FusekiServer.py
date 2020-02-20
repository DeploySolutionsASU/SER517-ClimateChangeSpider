import os
from DownloadManager import download_file
from zipfile import ZipFile
from Config import path_config
from HelperManager import get_root_directory

server_path = get_root_directory() + "/" + path_config["server_folder"]

if __name__ == '__main__':
    server_url = path_config["server_url"]
    zip_file = os.path.join(server_path, path_config["server_name"])
    download_file(server_url, server_path)
    with ZipFile(zip_file, 'r') as zipObj:
        # Extract all the contents of zip file in current directory
        zipObj.extractall(server_path)