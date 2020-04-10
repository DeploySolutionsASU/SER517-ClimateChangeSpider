import requests


# Bulk Indexing from JSON file to Elastic Search Server
def create_bulk_index(index_name, file_path):
    headers = {
        'Content-Type': 'application/x-ndjson',
    }
    params = (
        ('pretty', ''),
    )
    # Json file path
    data = open(file_path, 'rb').read()
    # Elastic search URL
    url = 'http://localhost:9200/' + index_name + '/_doc/_bulk'
    response = requests.post(url, headers=headers, params=params, data=data)

    print(response)
    print('Created index in elastic search')