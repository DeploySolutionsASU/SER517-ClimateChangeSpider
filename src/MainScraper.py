import logging
import os
import urllib.request
import wget
import gzip

from time import time
from bs4 import BeautifulSoup

root_dir = os.path.abspath('..')
root_dir = root_dir.replace('\\', '/')
output_path = root_dir + '/downloads'


def download_file(url):
    try:
        wget.download(url, out=output_path)
    except Exception as e:
        logging.error(e)


def create_directory(file_path):
    try:
        os.makedirs(file_path)
    except OSError as error:
        logging.warning(error)



def unzip_files(eachfile, input_file):
    curr_path = root_dir +'/data'
    file_name_output = input_file.split('.gz')[0] #+ '.txt'
    output_path = curr_path + '/' +file_name_output
    fp = open(output_path, "wb")
    with gzip.open(eachfile, "rb") as f:
        bindata = f.read()
    fp.write(bindata)
    fp.close()


if __name__ == '__main__':

    mainFile_path = os.path.join(root_dir, 'mainFile')
    downloads_path = os.path.join(root_dir, 'downloads')

    create_directory(mainFile_path)
    create_directory(downloads_path)

    given_url = 'http://webdatacommons.org/structureddata/2019-12/stats/how_to_get_the_data.html'
    search_text = ['rdfa', 'microdata', 'embedded', 'mf-hcard']

    page = urllib.request.urlopen(given_url)
    soup = BeautifulSoup(page, 'html.parser')

    down_dir = root_dir + '/mainFile'

    output_url = set()
    for a in soup.findAll('a', href=True):
        for find_text in search_text:
            if find_text in a.text:
                index = a.get('href').index('/')
                trim_url = 'http://webdatacommons.org/structureddata/2019-12' + a.get('href')[index:]
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
        download_file(url)

    print("Time to download", time() - start)

    extraction_path = os.path.join(root_dir, 'data')
    create_directory(extraction_path)

    # Read the files from the directory and unzip
    for filename in os.listdir(output_path):
        if filename.endswith(".gz"):
            file_name_input = filename
            each_file = os.path.join(output_path, filename)
            unzip_files(each_file, file_name_input)
        else:
            continue
