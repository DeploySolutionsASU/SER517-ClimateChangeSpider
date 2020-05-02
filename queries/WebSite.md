PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?g ?url ?description ?keywords ?match_keyword
WHERE { 
  GRAPH ?g{
    	?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(lcase(str(?object)), "website")).
    
    OPTIONAL{
        ?subject ?pred ?language.
    	FILTER(CONTAINS(lcase(str(?pred)), "lang") && CONTAINS(lcase(str(?language)), "en")).
    }
    
    OPTIONAL {
      ?subject <http://schema.org/WebSite/url> ?url.
    }
    OPTIONAL{
     ?subject <http://schema.org/WebSite/description> ?description. 
    }
    OPTIONAL{
      ?subject <http://schema.org/WebSite/keywords> ?keywords.
    }
    VALUES ?match_keyword { "climate change" "climate breakdown" "flooding" "flood" "sea level rise" "deluge rain event" "ocean solidification" "natural disaster" "winter storm" "drought" "ice storm" "tornado" "hail" "bushfire" "wildfire" "waves" "heat wave" "cold wave" "hurricane" "earthquake" "tsunami" "landslide" "storm surge" "coastal erosion" "ice dam" "permafrost erosion" "permafrost melt" "climate" "climate-change" "climate-breakdown" "sea-level-rise" "deluge-rain-event" "ocean-solidification" "natural-disaster" "winter-storm" "ice-storm" "heat-wave" "cold-wave" "storm-surge" "coastal-erosion" "ice-dam" "permafrost-erosion" "permafrost-melt" }
   
    FILTER(CONTAINS(lcase(str(?url)),  ?match_keyword) || CONTAINS(lcase(str(?description)),  ?match_keyword) || CONTAINS(lcase(str(?keywords)),  ?match_keyword)).
     }
}