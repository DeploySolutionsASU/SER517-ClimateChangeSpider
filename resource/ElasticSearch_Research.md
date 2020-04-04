**Elastic Search**
Elasticsearch is a search engine based on the Lucene library. It provides a distributed, 
multitenant-capable full-text search engine with an HTTP web interface and schema-free JSON documents.
Its distributed architecture helps to analyze and search a huge amount of data. 
It uses an inverted index method in which it maps the unique words with the list of documents 
containing that word which makes it possible to locate the documents containing the keyword very quickly.
By default, Elastic search uses a document-based database internally we don’t need to use another document
 DB like MongoDB to store the data from the Fuseki server and then run an elastic search over top of that.

**Basic definitions**
    Index – It is similar to the ‘Database’ in RDMS
    Type – Similar to ‘Table’ in RDMS
    Document – Similar to ‘Record/Row’ in RDMS
    
**Basic APIs**
   Index name: twitter
   **Create Index**
        CURL command to create index
        curl -X PUT "localhost:9200/twitter?pretty"
   **GET index**
        Curl command to get index information
        curl -X GET "localhost:9200/twitter?pretty"
   **GET field mapping API**
        Field name: user
        CURL command: 
        curl -X GET "localhost:9200/twitter/_mapping/field/user?pretty"
           Bulk indexing is possible but each document contains the information about the Index and Type. 
           We can also execute multiple commands in single request like
        Bulk Index Curl command:
        curl -X POST "localhost:9200/_bulk?pretty" -H 'Content-Type: application/json' -d'
        { "index" : { "_index" : "test", "_id" : "1" } }
        { "field1" : "value1" }
        { "delete" : { "_index" : "test", "_id" : "2" } }
        { "create" : { "_index" : "test", "_id" : "3" } }
        { "field1" : "value3" }
        { "update" : {"_id" : "1", "_index" : "test"} }
        { "doc" : {"field2" : "value2"} }
   **Search API**
        Curl command for query string:
        curl -X GET "localhost:9200/_search?pretty" -H 'Content-Type: application/json' -d'
        {
            "query": {
                "query_string" : {
                    "query" : "(new york) OR (tempe)",
                    "default_field" : "content"
                }
            }
        }
        
“New York” and “Tempe” are query strings since we are using OR operator it will be searched in 
the field content and return the matching documents.

**Reference**
https://www.elastic.co/blog/what-is-an-elasticsearch-index
https://sematext.com/guides/elasticsearch/
https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html

