import os
import urllib.request
import gzip
from zipfile import ZipFile
from Config import path_config

from time import time
from bs4 import BeautifulSoup

from DownloadManager import download_file
from HelperManager import create_directory
from HelperManager import get_root_directory


output_path = get_root_directory() + '/downloads'
fuseki_path = get_root_directory + '/fuseki'

def unzip_files(eachfile, input_file):
    curr_path = get_root_directory +'/data'
    file_name_output = input_file.split('.gz')[0] #+ '.txt'
    output_path = curr_path + '/' +file_name_output
    fp = open(output_path, "wb")
    with gzip.open(eachfile, "rb") as f:
        bindata = f.read()
    fp.write(bindata)
    fp.close()


if __name__ == '__main__':

    mainFile_path = os.path.join(get_root_directory, 'mainFile')
    downloads_path = os.path.join(get_root_directory, 'downloads')
    fuseki_dir_path = os.path.join(get_root_directory, 'fuseki')

    create_directory(mainFile_path)
    create_directory(downloads_path)
    create_directory(fuseki_dir_path)

    given_url = path_config["site_url"]
    search_text = ['rdfa', 'microdata', 'embedded', 'mf-hcard']
    fuseki_url = path_config["fuseki_url"]

    page = urllib.request.urlopen(given_url)
    soup = BeautifulSoup(page, 'html.parser')
    down_dir = get_root_directory + '/mainFile'

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

    extraction_path = os.path.join(get_root_directory, 'data')
    create_directory(extraction_path)

    # Read the files from the directory and unzip
    for filename in os.listdir(output_path):
        if filename.endswith(".gz"):
            file_name_input = filename
            each_file = os.path.join(output_path, filename)
            unzip_files(each_file, file_name_input)
        else:
            continue

    zip_file = os.path.join(fuseki_path, 'apache-jena-fuseki-3.14.0.zip')
    download_file(fuseki_url, fuseki_path)
    with ZipFile(zip_file, 'r') as zipObj:
        # Extract all the contents of zip file in current directory
        zipObj.extractall(fuseki_path)
