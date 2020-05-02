import json

from ElasticSearchManager import create_bulk_index

if __name__ == '__main__':
    file_name = 'FILE_NAME.json'
    val = 'INDEX_NAME'
    temp_entry = ''
    id = 1
    processed_entry = {}
    response = json.load(open(file_name, 'r', encoding='utf-8'))
    end = len(response['results']['bindings'])
    entry = response['results']['bindings']

    # Adding indexes to query response
    for line in range(0, end):
        test = '{ "index" : { "_index" : "' + val.lower() + '", "_type" : "_doc", "_id" : "' + str(id) + '" } }\n'
        for i in entry[line]:
            kval = entry[line][i]["value"]
            processed_entry[i] = kval
        temp_entry += test + json.dumps(processed_entry) + '\n'
        id += 1

        # Write every 200 line to a new json file to send it as an input to elastic search

        if (line != 0 and line % 200 == 0) or line == end - 1:
            file_name = val + str(id) + '.json'
            outfile = open(file_name, "w")
            outfile.write(temp_entry)
            temp_entry = ""
            processed_entry = {}
            outfile.close()
            create_bulk_index(val.lower(), file_name)