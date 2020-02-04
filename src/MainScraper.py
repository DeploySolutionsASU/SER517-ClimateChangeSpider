import os
import urllib.request
import wget
import gzip

from time import time
from bs4 import BeautifulSoup


root_dir = os.path.abspath('..')
root_dir = root_dir.replace('\\', '/')
output_path = root_dir + '/files'
extraction_path = root_dir + '/data'


def download_file(url):
    try:
        wget.download(url, out=output_path)
    except Exception as e:
        print(e)


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

    # given_url = 'http://webdatacommons.org/structureddata/2019-12/stats/how_to_get_the_data.html'
    # search_text = 'rdfa'
    #
    # page = urllib.request.urlopen(given_url)
    # soup = BeautifulSoup(page, 'html.parser')
    #
    #
    # down_dir = root_dir + '/downloads'
    #
    # output_url = set()
    # for a in soup.findAll('a', href=True):
    #     if search_text in a.text:
    #         index = a.get('href').index('/')
    #         trim_url = 'http://webdatacommons.org/structureddata/2019-12' + a.get('href')[index:]
    #         output_url.add(trim_url)
    #
    # file_path = os.path.join(down_dir, 'urls.txt')
    # for out_url in output_url:
    #     urllib.request.urlretrieve(out_url, file_path)
    #
    # fileHandler = open(file_path, "r")
    # Lines = fileHandler.readlines()
    # fileHandler.close()
    #
    # url_list = set()
    # count = 0
    # for line in Lines:
    #     # Testing download functionality with only 5 URLs
    #     #url_list.append(line.strip())
    #     if count == 5:
    #         break
    #     else:
    #         url_list.add(line.strip())
    #         count = count + 1
    #
    #
    # start = time()
    #
    # for link in url_list:
    #     download_file(link)
    #
    # print("Time to download", time() - start)

    # Read the files from the directory and unzip
    for filename in os.listdir(output_path):
        if filename.endswith(".gz"):
            file_name_input = filename
            each_file = os.path.join(output_path, filename)
            unzip_files(each_file, file_name_input)
        else:
            continue


