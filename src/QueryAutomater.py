import requests

def query_automater():
    request_data = requests.get('http://www.mocky.io/v2/5e4ddd0a2f00002b0016a28a')
    data = request_data.json()

    query = "SELECT * WHERE {GRAPH ?g {?s ?p ?o}"   # basic n-quads query format
    filter_query = []
    filter_query += ' FILTER('

    for d in range(len(data['keywords'])):
        if d != len(data['keywords'])-1:
            filter_query += 'CONTAINS(str(?ID), "' + data['keywords'][d] + '") || '
        else:
            filter_query += 'CONTAINS(str(?ID), "' + data['keywords'][d] + '"))}'

    query += ''.join(filter_query)
    
    return query
