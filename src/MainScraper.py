import os
import urllib.request
import gzip
from zipfile import ZipFile
from Config import path_config, data_formats_config

from time import time
from bs4 import BeautifulSoup

from DownloadManager import download_file
from FileUtilities import unzip_files
from HelperManager import create_directory
from HelperManager import get_root_directory

output_path = get_root_directory() + '/downloads'
server_path = get_root_directory() + '/fuseki'

if __name__ == '__main__':

    mainFile_path = os.path.join(get_root_directory(), 'mainFile')
    downloads_path = os.path.join(get_root_directory(), 'downloads')
    fuseki_dir_path = os.path.join(get_root_directory(), 'fuseki')

    create_directory(mainFile_path)
    create_directory(downloads_path)
    create_directory(fuseki_dir_path)

    given_url = path_config["site_url"]
    search_text = data_formats_config["search_text"]
    fuseki_url = path_config["fuseki_url"]

    page = urllib.request.urlopen(given_url)
    soup = BeautifulSoup(page, 'html.parser')
    down_dir = get_root_directory() + '/mainFile'

    output_url = set()
    for a in soup.findAll('a', href=True):
        for find_text in search_text:
            if find_text in a.text:
                index = a.get('href').index('/')
                trim_url = path_config["data_source_url"] + a.get('href')[index:]
                output_url.add(trim_url)

    file_path = os.path.join(down_dir, 'urls.txt')
    for out_url in output_url:
        with urllib.request.urlopen(out_url) as response:
            data = response.read().decode("utf-8")
            # converting from binary to string before writing to file
            with open(file_path, "a+") as fp: fp.write(str(data))

    fileHandler = open(file_path, "r")
    Lines = fileHandler.readlines()
    fileHandler.close()

    url_list = set()
    count = 0
    for line in Lines:
        # Testing download functionality with only 5 URLs
        # url_list.append(line.strip())
        if count == 1:
            break
        else:
            url_list.add(line.strip())
            count = count + 1

    start = time()

    for url in url_list:
        download_file(url, output_path)

    print("Time to download", time() - start)

    extraction_path = os.path.join(get_root_directory(), path_config["extract_folder"])
    create_directory(extraction_path)

    # Read the files from the directory and unzip
    for filename in os.listdir(output_path):
        if filename.endswith(".gz"):
            file = os.path.join(output_path, filename)
            curr_path = get_root_directory() + "/" + path_config["extract_folder"]
            file_name_output = filename.split('.gz')[0]
            output_path = curr_path + '/' + file_name_output
            unzip_files(file, output_path)
        else:
            continue

    zip_file = os.path.join(server_path, path_config["server_name"])
    download_file(fuseki_url, server_path)
    with ZipFile(zip_file, 'r') as zipObj:
        # Extract all the contents of zip file in current directory
        zipObj.extractall(server_path)
