SELECT DISTINCT ?name ?url (CONCAT(?street_address, ", " ,?addressRegion, ", " ,?locality, ", " ,?country ) AS ?some)
WHERE
{
  GRAPH ?g{
	?subject ?predicate ?object;
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
      <http://schema.org/addressCountry> ?country.
    	
  }
 FILTER(CONTAINS(str(?g), "weather") || CONTAINS(str(?g), "climate"))
 
 
}
LIMIT 100