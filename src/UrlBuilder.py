from Logger import log_error, log_message

fuseki_url_template = '{protocol}://{ip_address}:{port_number}/{data_set_name}/data'


def build_url(data_set, protocol="http", ip_address="localhost.com", port_number=3030):
    if not data_set:
        log_error("Data set name is empty or null")
        return None

    url = fuseki_url_template.format(protocol=protocol, ip_address=ip_address,
                                     port_number=port_number, data_set_name=data_set)
    log_message("Url Build Success: ", url)
    return url
