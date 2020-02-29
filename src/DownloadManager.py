import wget
import logging
from time import time


# Function to download
def download_file(url, output_path):
    try:
        wget.download(url, out=output_path)
    except Exception as e:
        logging.error(e)


# Function to download files from the list
def download_from_list(url_list, download_path):
    print("Download start")
    start = time()
    for url in url_list:
        download_file(url, download_path)

    print("Time to download", time() - start)
