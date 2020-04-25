PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?subject ?title ?url ?description ?language ?site_name ?tags ?match_keyword
WHERE { 
  GRAPH ?g{
  {
    
    ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
    FILTER(CONTAINS(lcase(str(?object)), "organization"))

    ?subject ?desc ?value_of_desc.
     GRAPH ?g{
      ?subject <http://opengraphprotocol.org/schema/type> ?object;
               FILTER(CONTAINS(lcase(str(?object)), "org")).
    
    OPTIONAL {
      ?subject <http://opengraphprotocol.org/schema/language> ?language;
               FILTER(CONTAINS(lcase(str(?language)), "en")).
    }
  } 
  UNION 		
  { 
   
    	?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(lcase(str(?object)), "organization"))
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
      OPTIONAL
     {
        ?subject <http://opengraphprotocol.org/schema/title> ?title;
                 <http://opengraphprotocol.org/schema/url> ?url;
                 <http://opengraphprotocol.org/schema/description> ?description;
                 <http://opengraphprotocol.org/schema/site_name> ?site_name;
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
       OPTIONAL
     {
        ?subject <http://opengraphprotocol.org/schema/title> ?title;
                 <http://opengraphprotocol.org/schema/url> ?url;
                 <http://opengraphprotocol.org/schema/description> ?description;
                 <http://opengraphprotocol.org/schema/site_name> ?site_name;
     }
    
  }
  }
 VALUES ?match_keyword { "climate change" "climate breakdown" "flooding" "flood" "sea level rise" "deluge rain event" "ocean solidification" "natural disaster" "winter storm" "drought" "ice storm" "tornado" "hail" "bushfire" "wildfire" "waves" "heat wave" "cold wave" "hurricane" "earthquake" "tsunami" "landslide" "storm surge" "coastal erosion" "ice dam" "permafrost erosion" "permafrost melt" "climate" "climate-change" "climate-breakdown" "sea-level-rise" "deluge-rain-event" "ocean-solidification" "natural-disaster" "winter-storm" "ice-storm" "heat-wave" "cold-wave" "storm-surge" "coastal-erosion" "ice-dam" "permafrost-erosion" "permafrost-melt" }
    
    FILTER(CONTAINS(lcase(str(?tags)),  ?match_keyword) || CONTAINS(lcase(str(?description)),  ?match_keyword)).
}
