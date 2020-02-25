from enum import Enum

global_config = {
    "riot_path": ""
}

# For windows provide apache jena riot path from bat folder
# D:/apache-jena-3.14.0/apache-jena-3.14.0/bat/riot.bat

# For Mac provide it from bin folder
# riot_path: "/Users/aj/Developer/apache-jena-3.14.0/bin/riot"

path_config = {
    "site_url": "http://webdatacommons.org/structureddata/2019-12/stats/how_to_get_the_data.html",
    "server_url": "http://apache.mirrors.lucidnetworks.net/jena/binaries/apache-jena-fuseki-3.14.0.zip",
    "data_source_url": "http://webdatacommons.org/structureddata/2019-12",
    "server_name": "apache-jena-fuseki-3.14.0.zip",
    "extract_folder": "data",
    "download_folder": "downloads",
    "server_folder": "server",
    "data_source": "dataSource",
    "csv_folder": "csv",
    "data_set_name": "test_data_set"
}

query_config = {
    "keywords": ['Climate Change', 'Climate breakdown', 'Flooding', 'Flood', 'sea level rise', 'deluge rain event',
                 'ocean solidification', 'natural disaster', 'winter storm', 'drought', 'ice storm', 'tornado', 'hail',
                 'bushfire', 'wildfire', 'waves', 'heat wave', 'cold wave', 'hurricane', 'earthquake', 'tsunami',
                 'landslide', 'Storm surge', 'coastal erosion', 'ice dam', 'permafrost erosion', 'permafrost melt'],
    "query_types": ['Article', 'Event', 'Organization', 'Website']

}

data_formats_config = {
    "search_text": ['rdfa', 'microdata', 'embedded', 'mf-hcard']
}


class BaseQuery(Enum):
    Article = """PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?ID ?main_page ?part_of ?url ?image ?title ?author ?headline ?publisher ?date_published ?date_modified ?comment
WHERE {
  GRAPH ?ID{
  { ?subject <http://opengraphprotocol.org/schema/type> "article";
             OPTIONAL{
             ?subject <http://opengraphprotocol.org/schema/url> ?url;
            <http://opengraphprotocol.org/schema/image> ?image;
            <http://opengraphprotocol.org/schema/title> ?title.}} UNION
   { ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Article>;
              OPTIONAL{
             ?subject <http://schema.org/Article/author> ?author;
            <http://schema.org/Article/dateModified> ?date_modified;
            <http://schema.org/Article/datePublished> ?date_published;
            <http://schema.org/Article/publisher> ?publisher;
            <http://schema.org/Article/articleSection> ?article_section;
            <http://schema.org/Article/commentCount> ?comment;
            <http://schema.org/Article/headline> ?headline;
           <http://schema.org/Article/isPartOf> ?part_of;
            <http://schema.org/Article/mainEntityOfPage> ?main_page.}} UNION
    {?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Article>;
              OPTIONAL{
             ?subject <http://schema.org/author> ?author;
            <http://schema.org/dateModified> ?date_modified;
            <http://schema.org/datePublished> ?date_published;
            <http://schema.org/publisher> ?publisher;
            <http://schema.org/articleSection> ?article_section;
            <http://schema.org/commentCount> ?comment;
            <http://schema.org/headline> ?headline;
           <http://schema.org/isPartOf> ?part_of;
            <http://schema.org/mainEntityOfPage> ?main_page.}}
  }
  """

    Event = """SELECT DISTINCT ?name ?url (CONCAT(?street_address, ", " ,?addressRegion, ", " ,?locality, ", " ,?country ) AS ?some)
WHERE
{
  GRAPH ?g{
{ ?subject ?predicate ?object;
        <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Event>;
        <http://schema.org/location> ?location;	
        <http://schema.org/name> ?name;
        <http://schema.org/url> ?url.
    
?location  <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Place>;
        <http://schema.org/name> ?place_name;
        <http://schema.org/address> ?address.
    
?address <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/PostalAddress>;
    <http://schema.org/streetAddress> ?street_address;
    <http://schema.org/addressRegion> ?addressRegion;
    <http://schema.org/addressRegion> ?addressRegion;
    <http://schema.org/addressLocality> ?locality;
    <http://schema.org/addressCountry> ?country.} UNION
{ ?subject ?predicate ?object;
    <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Event>;
    <http://schema.org/location> ?location;	
    <http://schema.org/name> ?name;
    <http://schema.org/url> ?url.
    
?location  <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Place>;
    <http://schema.org/name> ?place_name;
    <http://schema.org/address> ?address.
    
?address <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/PostalAddress>;
    <http://schema.org/streetAddress> ?street_address;
    <http://schema.org/addressRegion> ?addressRegion;
    <http://schema.org/addressLocality> ?locality;
    <http://schema.org/addressCountry> ?country.} 
  }
  """


Organization = """PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?g ?url ?name ?address ?telephone ?sameAs ?Logo ?isBasedOnUrl ?description
WHERE { 
  GRAPH ?g{
  { ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://rdf.data-vocabulary.org/#Organization>;
             OPTIONAL{?subject <http://rdf.data-vocabulary.org/#url> ?url;
             <http://rdf.data-vocabulary.org/#name> ?name;
                             <http://rdf.data-vocabulary.org/#address> ?address;
                             <http://rdf.data-vocabulary.org/#tel> ?telephone}} UNION 		
   { ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org.408ss.com/Organization>;
              OPTIONAL{?subject <http://schema.org.408ss.com/#url> ?url;
             <http://schema.org.408ss.com/#name> ?name;
                             <http://schema.org.408ss.com/#address> ?address;
            <http://schema.org.408ss.com/#tel> ?telephone;
            <http://schema.org/Organization/sameAs> ?sameAs;
            <https://schema.org/Organization/logo> ?Logo;
            <http://schema.org.408ss.com/Organization/isBasedOnUrl> ?isBasedOnUrl;
            <http://schema.org/Organization/description> ?description}} UNION
    { ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Organization>;
              OPTIONAL{?subject <http://schema.org/#url> ?url;
             <http://schema.org/#name> ?name;
                             <http://schema.org/#address> ?address;
            <http://schema.org/#tel> ?telephone}}
  }
  """

Website = """PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?ID ?name ?url 
WHERE { 
  GRAPH ?ID{
  { ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/WebSite>;
              OPTIONAL{
             ?subject <http://schema.org/WebSite/name> ?name;
            <http://schema.org/WebSite/url> ?url.}} UNION
    {?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Article>;
              OPTIONAL{
             ?subject <http://schema.org/name> ?name;
            <http://schema.org/url> ?url.}}
  }
  """
