PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?subject ?title ?url ?description ?language ?site_name ?tags ?match_keyword
WHERE { 
  GRAPH ?g{
  {
    
    ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
    FILTER(CONTAINS(lcase(str(?object)), "organization"))

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
 VALUES ?match_keyword { "climate change" "climate breakdown" "flooding" "flood" "sea level rise" "deluge rain event" "ocean solidification" "natural disaster" "winter storm" "drought" "ice storm" "tornado" "hail" "bushfire" "wildfire" "waves" "heat wave" "cold wave" "hurricane" "earthquake" "tsunami" "landslide" "storm surge" "coastal erosion" "ice dam" "permafrost erosion" "permafrost melt" "climate" "climate-change" "climate-breakdown" "sea-level-rise" "deluge-rain-event" "ocean-solidification" "natural-disaster" "winter-storm" "ice-storm" "heat-wave" "cold-wave" "storm-surge" "coastal-erosion" "ice-dam" "permafrost-erosion" "permafrost-melt" }
    
    FILTER(CONTAINS(lcase(str(?tags)),  ?match_keyword) || CONTAINS(lcase(str(?description)),  ?match_keyword)).
}
