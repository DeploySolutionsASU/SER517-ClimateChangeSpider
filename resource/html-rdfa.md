# SER517-ClimateChangeSpider

Querying html-rdfa Data:

The November 2019 of Html-rdfa data can be found at [http://webdatacommons.org/structureddata/2019-12/stats/how_to_get_the_data.html]

The below url downloads the file that contains all the zip files of Html-rdfa data.
[http://webdatacommons.org/structureddata/2019-12/files/html-rdfa.list]

**Steps needed to filter the data:**
1. Download each zip file of html-rdfa data
2. Extract the downloaded zip file and get the html-rdfa data which is N-Quads[http://www/w3.org/TR/n-quads/]
3. Import the html-rdfa data to the Fuseki server.
4. Query the data using SPARQL and store the result as JSON.
5. Provide the JSON results to store in secondary storage.(AWS)

**Challenges faced**
Here we are trying to automate the above steps through a python scripts. And the dat in these files have non Parasable characters which should
eliminated in order to parse the content of the url.

Non Parsable data means looking for the characters that are not supposed to be as part of the url. Solution is to identify a tool that has the ability to 
identify these lines which has the non parsable characters and remove them, in order to process the content, through a script.



