PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?subject ?title ?url ?description ?language ?site_name ?tags ?match_keyword
WHERE { 
  GRAPH ?g{
      ?subject <http://opengraphprotocol.org/schema/type> ?object;
               FILTER(CONTAINS(lcase(str(?object)), "article")).
    
    OPTIONAL {
      ?subject <http://opengraphprotocol.org/schema/language> ?language;
               FILTER(CONTAINS(lcase(str(?language)), "en")).
    }
    
     OPTIONAL
     {
        ?subject <http://opengraphprotocol.org/schema/title> ?title;
                 <http://opengraphprotocol.org/schema/url> ?url;
                 <http://opengraphprotocol.org/schema/description> ?description;
                 <http://opengraphprotocol.org/schema/site_name> ?site_name;
     }
    
    OPTIONAL {
	     ?subject <http://opengraphprotocol.org/schema/tags> ?tags;
    }
    
VALUES ?match_keyword { "climate change" "climate breakdown" "flooding" "flood" "sea level rise" "deluge rain event" "ocean solidification" "natural disaster" "winter storm" "drought" "ice storm" "tornado" "hail" "bushfire" "wildfire" "waves" "heat wave" "cold wave" "hurricane" "earthquake" "tsunami" "landslide" "storm surge" "coastal erosion" "ice dam" "permafrost erosion" "permafrost melt" "climate" "climate-change" "climate-breakdown" "sea-level-rise" "deluge-rain-event" "ocean-solidification" "natural-disaster" "winter-storm" "ice-storm" "heat-wave" "cold-wave" "storm-surge" "coastal-erosion" "ice-dam" "permafrost-erosion" "permafrost-melt" }
    
    FILTER(CONTAINS(lcase(str(?tags)),  ?match_keyword) || CONTAINS(lcase(str(?description)),  ?match_keyword)).
  }

}