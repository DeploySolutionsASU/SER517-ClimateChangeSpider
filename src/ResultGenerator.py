import logging
import os
import pandas as pd

from Config import path_config
from HelperManager import get_root_directory, create_directory


# from QueryGenerator import generate_query;


def result_generator(csv_export_path):
    print("Start result generation")
    try:
        # Testing the csv export with dummy json
        df = pd.read_json(r'C:\Yuvan\Studies\Fourth_sem\ser517-github\SER517-ClimateChangeSpider\Json\places.json')
        export_csv = df.to_csv(csv_export_path + "/" + path_config["csv_output"], header=True)
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    csv_path = os.path.join(get_root_directory(), path_config["csv_folder"])
    create_directory(csv_path)
    result_generator(csv_path)
