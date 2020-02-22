import requests
from Config import BaseQuery


def get_data():
    request_data = requests.get('http://www.mocky.io/v2/5e4ddd0a2f00002b0016a28a')
    data = request_data.json()
    return data['keywords']


def generate_query(query_type, data):
    query = ""

    if query_type == "Article":
        query = BaseQuery.Article.value
    if query_type == "Event":
        query = BaseQuery.Event.value
    if query_type == "Organization":
        query = BaseQuery.Organization.value
    if query_type == "Website":
        query = BaseQuery.Website.value

    filter_query = []
    filter_query += ' FILTER('

    for d in range(len(data)):
        if d != len(data) - 1:
            filter_query += 'CONTAINS(str(?ID), "' + data[d] + '") || '
        else:
            filter_query += 'CONTAINS(str(?ID), "' + data[d] + '"))\n}\nLIMIT 100'

    query += ''.join(filter_query)

    return query


