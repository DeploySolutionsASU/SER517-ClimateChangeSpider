import os
import pandas as pd

from Config import path_config, query_config
from HelperManager import get_root_directory, create_directory
from Logger import log_error
from NetworkManager import make_http_post_request
from QueryGenerator import generate_query
from UrlBuilder import build_url


def result_generator(json_input, file_name, csv_export_path):
    print("Start result generation")
    try:
        # Testing the csv export with dummy json
        # df = pd.read_json(r'C:\Yuvan\Studies\Fourth_sem\ser517-github\SER517-ClimateChangeSpider\Json\places.json')
        df = pd.read_json(json_input)
        export_csv = df.to_csv(csv_export_path + "/" + file_name + ".csv", header=True)
    except Exception as ex:
        log_error(ex)


if __name__ == '__main__':
    url_type = "query_data"
    csv_path = os.path.join(get_root_directory(), path_config["csv_folder"])
    create_directory(csv_path)

    for query_type in query_config['query_types']:
        article_query = generate_query(query_type, query_config['keywords'])
        url = build_url(data_set=path_config['data_set_name'],  url_type=url_type)
        response = make_http_post_request(url, payload=article_query)
        result_generator(response, query_type, csv_path)
