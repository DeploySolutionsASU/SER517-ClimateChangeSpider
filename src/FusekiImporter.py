
from requests_toolbelt import MultipartEncoder
from ntpath import basename
from NetworkManager import make_http_post_request
from UrlBuilder import build_url


def import_data_to_fuseki(data_set, file_path):
    file_name = basename(file_path)
    url_type = "upload_data"
    multipart_data = MultipartEncoder(fields={'file': (file_name,
                                                       open(file_path, 'rb'),
                                                       'text/plain')})

    url = build_url(data_set=data_set, url_type=url_type)
    make_http_post_request(url, payload=multipart_data, headers={'Content-Type': multipart_data.content_type})
