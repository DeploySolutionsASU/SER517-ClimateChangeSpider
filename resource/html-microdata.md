***Research on Querying techniques of html-microdata***

The November 2019 snapshot of html-microdata can be found at :
[http://webdatacommons.org/structureddata/2019-12/stats/how_to_get_the_data.html]

The below url downloads the file that contains all the zip files of html-microdata.
[http://webdatacommons.org/structureddata/2019-12/files/html-microdata.list]

The command used to fetch all the files from the list is as follows:
[wget -i http://webdatacommons.org/structureddata/2019-12/files/html-microdata.list]

**Steps needed to filter data:**

1. Download each zip file of html-microdata.
2. Extract the downloaded zip file and get the microdata in N-Quads[http://www.w3.org/TR/n-quads/] extension
3. Clean the data that is extracted using the N-Quads
4. Import the microdata to Apache Jena Fuseki server to support querying on top of the data
5. Execute the SPARQL queries and filter environment related data 
6. Fetch the filtered results as json and store it in the secondary storage(AWS)
