import os
import urllib.request
from zipfile import ZipFile
from Config import path_config, data_formats_config
import logging

from bs4 import BeautifulSoup

from DownloadManager import download_file, download_from_list
from FileUtilities import read_files_to_unzip
from HelperManager import folders_creation
from HelperManager import get_root_directory

download_path = get_root_directory() + "/" + path_config["download_folder"]

def data_scraper(search_parameter, download_dir):
    try:
        print("Data scraper start")
        output_url = set()
        for a in soup.findAll('a', href=True):
            for find_text in search_parameter:
                if find_text in a.text:
                    index = a.get('href').index('/')
                    trim_url = path_config["data_source_url"] + a.get('href')[index:]
                    output_url.add(trim_url)

        file_path = os.path.join(download_dir, 'urls.txt')
        for out_url in output_url:
            with urllib.request.urlopen(out_url) as response:
                data = response.read().decode("utf-8")
                # converting from binary to string before writing to file
                with open(file_path, "a+") as fp: fp.write(str(data))

        file_handler = open(file_path, "r")
        lines = file_handler.readlines()
        file_handler.close()

        urls = set()
        count = 0
        for line in lines:
            if count == 1:
                break
            else:
                urls.add(line.strip())
                count = count + 1

        print("Data scraper end")
        return urls

    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    folders_creation()
    given_url = path_config["site_url"]
    search_text = data_formats_config["search_text"]

    page = urllib.request.urlopen(given_url)
    soup = BeautifulSoup(page, 'html.parser')
    down_source_dir = get_root_directory() + "/" + path_config["data_source"]

    # Scrap data from the web site
    url_list = data_scraper(search_text, down_source_dir)
    # Download urls from the list
    download_from_list(url_list, download_path)
    # read files to unzip
    read_files_to_unzip(download_path)
