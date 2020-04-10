import json
import sys

from requests import post as POST

#from ElasticSearchManager import create_bulk_index
from ElasticSearchManager import create_bulk_index

default_headers = {"Content-Type": "application/json"}
fuseki_url_template = '{protocol}://{ip_address}:{port_number}/{data_set_name}'


def build_url(data_set, protocol="http", ip_address="localhost", port_number=3030):
    if not data_set:
        return None

    url_template = fuseki_url_template + '/query'
    url = url_template.format(protocol=protocol, ip_address=ip_address,
                              port_number=port_number, data_set_name=data_set)

    return url


def make_http_post_request(url, payload=None, headers=default_headers):
    try:
        request_headers = {**default_headers, **headers}
        response = POST(url=url, data=payload, headers=request_headers)
        response.raise_for_status()
        json = string_to_json(response.text)
    except Exception as ex:
        print(ex)
    else:
        return json


def string_to_json(response_str):
    try:
        return json.loads(response_str)
    except ValueError as error:
        print("JsonParsing Error: ", error, file=sys.stderr)


def generate_result(data_set):
    url = build_url(data_set=data_set)
    query_types = ['Article', 'Organization', 'Event', 'Website']
    for val in query_types:
        if val == 'Article':
            query = article
        elif val == 'Organization':
            query = organization
        elif val == 'Event':
            query = event
        elif val == 'Website':
            query = website

        response = make_http_post_request(url, payload={"query": query},
                                          headers={'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'})
        temp_entry = ''
        id = 1
        processed_entry = {}
        end = len(response['results']['bindings'])
        entry = response['results']['bindings']

        # Adding indexes to query response
        for line in range(0, end):
            test =  '{ "index" : { "_index" : "'+val.lower()+'", "_type" : "_doc", "_id" : "' + str(id) + '" } }\n'
            for i in entry[line]:
                kval = entry[line][i]["value"]
                processed_entry[i] = kval
            temp_entry += test + json.dumps(processed_entry) + '\n'
            id +=1

            # Write every 100 line to a new json file to send it as an input to elastic search
            if line % 100 == 0 or line == end - 1:
                file_name = val+str(id)+'.json'
                outfile = open(file_name, "w")
                outfile.write(temp_entry)
                temp_entry = ""
                processed_entry = {}
                outfile.close()
                create_bulk_index(val.lower(), file_name)




article = """PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?g ?url ?image ?title ?author ?date_modified ?date_published ?article_section ?comment ?headline ?part_of ?main_page ?value_of_desc 
WHERE { 
  GRAPH ?g{
  {
    { 
        ?subject <http://opengraphprotocol.org/schema/type> ?object;
        FILTER(CONTAINS(str(?object), "Article")) 
    }
    UNION
    {
    	?subject <http://opengraphprotocol.org/schema/type> ?object;
        FILTER(CONTAINS(lcase(str(?object)), "article"))
    }	
    ?subject ?desc ?value_of_desc.
     OPTIONAL
     {
        ?subject <http://opengraphprotocol.org/schema/url> ?url;
                 <http://opengraphprotocol.org/schema/image> ?image;
                 <http://opengraphprotocol.org/schema/title> ?title.
     }
  } 
  UNION 		
  { 
    {
        ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(str(?object), "Article")) 
    }
    UNION
    {
    	?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(lcase(str(?object)), "article"))
    }	
    ?subject ?desc ?value_of_desc.
    OPTIONAL
    {
       ?subject <http://schema.org/Article/author> ?author;
                <http://schema.org/Article/dateModified> ?date_modified;
                <http://schema.org/Article/datePublished> ?date_published;
                <http://schema.org/Article/publisher> ?publisher;
                <http://schema.org/Article/articleSection> ?article_section;
                <http://schema.org/Article/commentCount> ?comment;
                <http://schema.org/Article/headline> ?headline;
                <http://schema.org/Article/isPartOf> ?part_of;
                <http://schema.org/Article/mainEntityOfPage> ?main_page.
    }
  } 
  UNION
  {
    {
        ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Article>;
        FILTER(CONTAINS(str(?object), "Article")) 
    }
    UNION
    {
        ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(lcase(str(?object)), "article"))
    }	
    ?subject ?desc ?value_of_desc.
    OPTIONAL
    {
       ?subject <http://schema.org/author> ?author;
                <http://schema.org/dateModified> ?date_modified;
                <http://schema.org/datePublished> ?date_published;
                <http://schema.org/publisher> ?publisher;
                <http://schema.org/articleSection> ?article_section;
                <http://schema.org/commentCount> ?comment;
                <http://schema.org/headline> ?headline;
                <http://schema.org/isPartOf> ?part_of;
                <http://schema.org/mainEntityOfPage> ?main_page.
    }
  } 
  }
  FILTER(CONTAINS(str(?value_of_desc), "environment") || CONTAINS(str(?value_of_desc), "climate") || CONTAINS(str(?value_of_desc), "weather") || CONTAINS(str(?value_of_desc), "flood") || CONTAINS(str(?value_of_desc), "fire"))
  FILTER ((lang(?value_of_desc)= "en") ||lang(?value_of_desc)="en-US" || lang(?value_of_desc)="")
  FILTER(CONTAINS(str(?g), "environment") || CONTAINS(str(?g), "climate") || CONTAINS(str(?g), "weather") || CONTAINS(str(?g), "flood") || CONTAINS(str(?g), "fire"))
}"""

organization = """
PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?g ?url ?name ?address ?telephone ?sameAs ?Logo ?isBasedOnUrl ?description ?value_of_desc
WHERE { 
  GRAPH ?g{
  {
    { 
        ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(str(?object), "Organization")) 
    }
    UNION
    {
    	?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(lcase(str(?object)), "organization"))
    }	
    ?subject ?desc ?value_of_desc.
    OPTIONAL
    {
        ?subject <http://rdf.data-vocabulary.org/#url> ?url;
                 <http://rdf.data-vocabulary.org/#name> ?name;
                 <http://rdf.data-vocabulary.org/#address> ?address;
                 <http://rdf.data-vocabulary.org/#tel> ?telephone
    }
  } 
  UNION 		
  { 
    {
        ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(str(?object), "Organization")) 
    }
    UNION
    {
    	?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(lcase(str(?object)), "organization"))
    }	
    ?subject ?desc ?value_of_desc.
    OPTIONAL
    {
        ?subject <http://schema.org.408ss.com/#url> ?url;
                 <http://schema.org.408ss.com/#name> ?name;
                 <http://schema.org.408ss.com/#address> ?address;
                 <http://schema.org.408ss.com/#tel> ?telephone;
                 <http://schema.org/Organization/sameAs> ?sameAs;
                 <https://schema.org/Organization/logo> ?Logo;
                 <http://schema.org.408ss.com/Organization/isBasedOnUrl> ?isBasedOnUrl;
                 <http://schema.org/Organization/description> ?description
    }
  } 
  UNION
  { 
    {
        ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(str(?object), "Organization")) 
    }
    UNION
    {
    	?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(lcase(str(?object)), "organization"))
    }	
    ?subject ?desc ?value_of_desc.
    OPTIONAL
    {
        ?subject <http://schema.org/#url> ?url;
                 <http://schema.org/#name> ?name;
                 <http://schema.org/#address> ?address;
                 <http://schema.org/#tel> ?telephone
    }
  }
  UNION
  { 
    {
        ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(str(?object), "Organization")) 
    }
    UNION
    {
    	?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(lcase(str(?object)), "organization"))
    }	
     ?subject ?desc ?value_of_desc.
     OPTIONAL
     {
        ?subject <http://www.w3.org/2006/vcard/ns#organization-name> ?name;
                 <http://www.w3.org/2006/vcard/ns#adr> ?address;
            	 <http://www.w3.org/2006/vcard/ns#tel> ?telephone
     }
  }
  }
 FILTER(CONTAINS(str(?value_of_desc), "environment") || CONTAINS(str(?value_of_desc), "climate") || CONTAINS(str(?value_of_desc), "weather") || CONTAINS(str(?value_of_desc), "flood") || CONTAINS(str(?value_of_desc), "fire"))
 FILTER ((lang(?value_of_desc)= "en") ||lang(?value_of_desc)="en-US" || lang(?value_of_desc)="")
 FILTER(CONTAINS(str(?g), "environment") || CONTAINS(str(?g), "climate") || CONTAINS(str(?g), "weather") || CONTAINS(str(?g), "flood") || CONTAINS(str(?g), "fire"))
}
LIMIT 2000
"""

event = """SELECT DISTINCT ?g ?name ?url (CONCAT(?street_address, ", " ,?addressRegion, ", " ,?locality, ", " ,?country ) AS ?some) ?value_of_desc
WHERE
{
  GRAPH ?g{
	{ 
	    ?subject ?predicate ?object;
                 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Event>;
                 <http://schema.org/location> ?location;	
			     <http://schema.org/name> ?name;
			     <http://schema.org/url> ?url.
	    ?subject ?desc ?value_of_desc.
        ?location  <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Place>;
                   <http://schema.org/name> ?place_name;
    			   <http://schema.org/address> ?address. 
        ?address <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/PostalAddress>;
     	         <http://schema.org/streetAddress> ?street_address;
    	         <http://schema.org/addressRegion> ?addressRegion;
     	         <http://schema.org/addressLocality> ?locality;
                 <http://schema.org/addressCountry> ?country.
    }
    UNION
    {
        ?subject ?predicate ?object;
                 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Event>;
                 <http://schema.org/location> ?location;	
			     <http://schema.org/name> ?name;
			     <http://schema.org/url> ?url.
        ?subject ?desc ?value_of_desc.
        ?location  <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Place>;
                   <http://schema.org/name> ?place_name;
    		       <http://schema.org/address> ?address.
        ?address <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/PostalAddress>;
     	         <http://schema.org/streetAddress> ?street_address;
    	         <http://schema.org/addressRegion> ?addressRegion;
     	         <http://schema.org/addressLocality> ?locality;
                 <http://schema.org/addressCountry> ?country.
    } 
  }
  FILTER(CONTAINS(str(?value_of_desc), "environment") || CONTAINS(str(?value_of_desc), "climate") || CONTAINS(str(?value_of_desc), "weather") || CONTAINS(str(?value_of_desc), "flood") || CONTAINS(str(?value_of_desc), "fire"))
  FILTER ((lang(?value_of_desc)= "en") ||lang(?value_of_desc)="en-US" || lang(?value_of_desc)="")
  FILTER(CONTAINS(str(?g), "fire") || CONTAINS(str(?g), "environment") || CONTAINS(str(?g), "flood") || CONTAINS(str(?g), "weather") || CONTAINS(str(?g), "climate"))
}
LIMIT 2000

"""

website = """PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?g ?object ?name ?url ?value_of_desc
WHERE { 
  GRAPH ?g{
  { 
    {
        ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
		FILTER(CONTAINS(str(?object), "WebSite")) 
    }
    UNION
    {
    	?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(lcase(str(?object)), "website"))
    }	
    ?subject ?desc ?value_of_desc.
    OPTIONAL
    {
       ?subject <http://schema.org/WebSite/name> ?name;
                <http://schema.org/WebSite/url> ?url.
    }
  } 
  UNION
  {
    {
        ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(str(?object), "WebSite")) 
    }
    UNION
    {
    	?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(lcase(str(?object)), "website"))
    }
    ?subject ?desc ?value_of_desc.
    OPTIONAL
    {
        ?subject <http://schema.org/name> ?name;
                 <http://schema.org/url> ?url.
    }
  }
  }
  FILTER(CONTAINS(str(?value_of_desc), "environment") || CONTAINS(str(?value_of_desc), "climate") || CONTAINS(str(?value_of_desc), "weather") || CONTAINS(str(?value_of_desc), "flood") || CONTAINS(str(?value_of_desc), "fire"))
  FILTER ((lang(?value_of_desc)= "en") ||lang(?value_of_desc)="en-US" || lang(?value_of_desc)="")
  FILTER(CONTAINS(str(?g), "environment") || CONTAINS(str(?g), "climate") || CONTAINS(str(?g), "weather") || CONTAINS(str(?g), "flood") || CONTAINS(str(?g), "fire"))
}
LIMIT 2000
"""



if __name__ == '__main__':
    generate_result('test_data_set')