PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?subject ?object ?name ?url 
WHERE { 
  GRAPH ?g{
  { {?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
		FILTER(CONTAINS(str(?object), "WebSite")) 
}
UNION{
    			?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
             FILTER(CONTAINS(lcase(str(?object)), "website"))
    }	
              OPTIONAL{
             ?subject <http://schema.org/WebSite/name> ?name;
            <http://schema.org/WebSite/url> ?url.}} UNION
    {{?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
FILTER(CONTAINS(str(?object), "WebSite")) 
}
UNION{
    			?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
             FILTER(CONTAINS(lcase(str(?object)), "website"))
    }

              OPTIONAL{
             ?subject <http://schema.org/name> ?name;
            <http://schema.org/url> ?url.}}
  }
  FILTER(CONTAINS(str(?subject), "environment") || CONTAINS(str(?subject), "climate") || CONTAINS(str(?subject), "weather") || CONTAINS(str(?subject), "flood") || CONTAINS(str(?subject), "fire"))
}
LIMIT 100



