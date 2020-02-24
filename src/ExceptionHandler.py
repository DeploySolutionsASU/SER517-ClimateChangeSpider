
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from Logger import log_error


def handle_exception(ex):

    ex_type = type(ex)
    if ex_type is HTTPError:
        log_error("Http Error:", str(ex), ex.response.text)
    elif ex_type is ConnectionError:
        log_error("Connection Error:", str(ex), ex.response.text)
    elif ex_type is Timeout:
        log_error("Timeout Error:", str(ex), ex.response.text)
    elif ex_type is RequestException:
        log_error("Request Exception: ", str(ex), ex.response.text)
    else:
        log_error("Unknown Exception", str(ex))
