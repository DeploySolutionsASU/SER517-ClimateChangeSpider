**Introduction**

hCard is a simple, open format for publishing people, companies, organizations on the web, using a 1:1 representation of vCard (RFC2426) properties and values in HTML.<br/> hCard is one of several open microformat standards suitable for embedding data in HTML/HTML5, and Atom/RSS/XHTML or other XML.

_Properties :_
<br/> Some of the common properties/class names that are found in this microformat are: <br/>
1. org - (Organization)
2. url
3. email
4. tel - (telephone)
5. adr - (structured address, container for):
        * street
        * postal-code
        * country
A full list of properties can be found here : [http://microformats.org/wiki/hcard#Property_List]

**Querying html-mf-hCard Data**

The November 2019 snapshot of html-mf-hCard can be found at [http://webdatacommons.org/structureddata/#results-2019-1]

The below url downloads the file that contains all the zip files of  html-mf-hCard data. [http://webdatacommons.org/structureddata/2019-12/files/html-mf-hcard.list]

The above mentioned class names can be used to filter out data in the required format.

**Steps needed to filter data**

1. Download each zip file of jsonld data
2. Extract the downloaded zip file and get the html-mf-hCard data in N-Quads[http://www.w3.org/TR/n-quads/] extension
3. Import the html-mf-hCard data to Apache Jena Fuseki server to support querying on top of the data
4. Execute the SPARQL queries and filter environment related data
5. Fetch the filtered results as json and store it in the secondary storage(AWS)
