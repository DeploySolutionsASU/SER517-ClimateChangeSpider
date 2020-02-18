import wget
import logging


# Function to download
def download_file(url, output_path):
    try:
        wget.download(url, out=output_path)
    except Exception as e:
        logging.error(e)
