PREFIX prefix: <http://prefix.cc/>
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