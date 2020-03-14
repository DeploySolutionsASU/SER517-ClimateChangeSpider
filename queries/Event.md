SELECT DISTINCT ?g ?name ?url (CONCAT(?street_address, ", " ,?addressRegion, ", " ,?locality, ", " ,?country ) AS ?some) ?value_of_desc
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