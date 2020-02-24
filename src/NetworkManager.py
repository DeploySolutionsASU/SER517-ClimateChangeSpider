
from requests import get as GET
from requests import post as POST
from Logger import log_message
from JsonParser import string_to_json
from ExceptionHandler import handle_exception

default_headers = {"Content-Type": "application/json"}


def make_http_get_request(url, params=None, headers=default_headers):
    try:
        request_headers = {**default_headers, **headers}
        response = GET(url, headers=request_headers, params=params)
        response.raise_for_status()
        json = string_to_json(response.text)
    except Exception as ex:
        handle_exception(ex)
    else:
        log_message("POST request success for " + response.url)
        return json


def make_http_post_request(url, payload=None, headers=default_headers):
    try:
        request_headers = {**default_headers, **headers}
        response = POST(url=url, data=payload, headers=request_headers)
        response.raise_for_status()
        json = string_to_json(response.text)
    except Exception as ex:
        handle_exception(ex)
    else:
        log_message("POST request success for " + response.url)
        return json
