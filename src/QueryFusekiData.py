import json
import sys

from requests import post as POST

default_headers = {"Content-Type": "application/json"}
fuseki_url_template = '{protocol}://{ip_address}:{port_number}/{data_set_name}'


def url_builder(data_set, protocol="http", ip_address="localhost", port_number=3030):
    if not data_set:
        return None

    url_template = fuseki_url_template + '/query'
    url = url_template.format(protocol=protocol, ip_address=ip_address,
                              port_number=port_number, data_set_name=data_set)

    return url


def http_post_request(url, payload=None, headers=default_headers):
    try:
        request_headers = {**default_headers, **headers}
        response = POST(url=url, data=payload, headers=request_headers)
        response.raise_for_status()
        json = string_to_json(response.text)
    except Exception as ex:
        print(ex)
    else:
        return json


def string_to_json(response_str):
    try:
        return json.loads(response_str)
    except ValueError as error:
        print("JsonParsing Error: ", error, file=sys.stderr)


def generate_result(data_set):
    url = url_builder(data_set=data_set)
    query = ""
    response = http_post_request(url, payload={"query": query},
                                      headers={'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'})

    outfile = open('article-data.json', "w")
    outfile.write(response)
    outfile.close()


if __name__ == '__main__':
    generate_result('test_data_set')
