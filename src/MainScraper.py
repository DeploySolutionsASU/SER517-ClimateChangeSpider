import logging
import os
import urllib.request
import wget

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


if __name__ == '__main__':

    mainFile_path = os.path.join(root_dir, 'mainFile')
    downloads_path = os.path.join(root_dir, 'downloads')

    create_directory(mainFile_path)
    create_directory(downloads_path)

    given_url = 'http://webdatacommons.org/structureddata/2019-12/stats/how_to_get_the_data.html'
    search_text = 'rdfa'

    page = urllib.request.urlopen(given_url)
    soup = BeautifulSoup(page, 'html.parser')

    down_dir = root_dir + '/mainFile'

    output_url = set()
    for a in soup.findAll('a', href=True):
        if search_text in a.text:
            index = a.get('href').index('/')
            trim_url = 'http://webdatacommons.org/structureddata/2019-12' + a.get('href')[index:]
            output_url.add(trim_url)

    file_path = os.path.join(down_dir, 'urls.txt')
    for out_url in output_url:
        urllib.request.urlretrieve(out_url, file_path)

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
