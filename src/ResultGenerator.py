import csv
import os

from Config import path_config, query_config
from HelperManager import get_root_directory, create_directory
from Logger import log_error, log_message
from NetworkManager import make_http_post_request
from QueryGenerator import generate_query
from UrlBuilder import build_url


def result_generator(json_input, file_name, csv_export_path):
    log_message("Start result generation..")
    try:
        csv_output = csv_export_path + "/" + file_name + ".csv"
        headers = json_input['head']['vars'] if "vars" in json_input["head"] else []
        f = csv.writer(open(csv_output, "w"))
        f.writerow(headers)

        for json_data in json_input['results']['bindings']:
            row_data = []
            for index, value in enumerate(headers):
                row_data.append(json_data[value]['value'] if value in json_data else "")

            f.writerow(row_data)

        log_message("End result generation..")

    except Exception as ex:
        log_error(ex)


if __name__ == '__main__':
    url_type = "query_data"
    csv_path = os.path.join(get_root_directory(), path_config["csv_folder"])
    create_directory(csv_path)

    for query_type in query_config['query_types']:
        query = generate_query(query_type, query_config['keywords'])
        url = build_url(data_set=path_config['data_set_name'], url_type=url_type)
        response = make_http_post_request(url, payload={"query": query},
                                          headers={'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'})
        result_generator(response, query_type, csv_path)
