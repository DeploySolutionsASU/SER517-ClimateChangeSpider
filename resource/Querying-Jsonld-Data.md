
**Querying Jsonld Data:**

The November 2019 snapshot of Html-embedded-jsonld-data can be found at [http://webdatacommons.org/structureddata/2019-12/stats/how_to_get_the_data.html]

The below url downloads the file that contains all the zip files of Html-embedded-jsonld-data.
[http://webdatacommons.org/structureddata/2019-12/files/html-embedded-jsonld.list]

**Steps needed to filter data:**

1. Download each zip file of jsonld data
2. Extract the downloaded zip file and get the jsonld data in N-Quads[http://www.w3.org/TR/n-quads/] extension
3. Import the jsonld data to Apache Jena Fuseki server to support querying on top of the data
4. Execute the SPARQL queries and filter environment related data 
5. Fetch the filtered results as json and store it in the secondary storage(AWS)

**Challenges:**

Our goal is to automate the steps mentioned above through a python script but the meta-data in web data
commons is not perfect and has some non-parsable characters.

_Non-parsable Data:_
Few N-Quads tuples consists of URL's that has characters which are not allowed in a URL. Other failure cases include 
 data that contains special characters which cannot be represented in UTF-8 encoding. 
 
Importing the raw downloaded data from the Web Data Commons into the Fuseki Sever results in 90% (out of 10 cases that 
I tried) failure because of the non-parsable data issue. Importing into the Fuseki server is important
as to run SPARQL queries which filters the environment related data. This failure while importing the data
has to avoided for complete results to be fetched during the filter process.

_Proposed Solution:_
The solution is to pre-process the data through a script and remove the non-parsable characters before 
importing the data to the Fuseki server. We can also optimize the import process by parallely running few threads that 
does the pre-processing and data import. 
  

 




