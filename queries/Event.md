PREFIX prefix: <http://prefix.cc/>
SELECT distinct (?g as ?url) ?name (lang(?language_value) as ?language) ?description ?match_keyword
WHERE { 
  GRAPH ?g{
      ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Event>;
               <http://schema.org/Event/inLanguage> ?language_value;
               FILTER(CONTAINS(lcase(str(?language_value)), "en")).
    
    
    ?subject <http://schema.org/Event/description> ?description;
             <http://schema.org/Event/name> ?name;
            

    VALUES ?match_keyword { "climate change" "climate breakdown" "flooding" "flood" "sea level rise" "deluge rain event" "ocean solidification" "natural disaster" "winter storm" "drought" "ice storm" "tornado" "hail" "bushfire" "wildfire" "waves" "heat wave" "cold wave" "hurricane" "earthquake" "tsunami" "landslide" "storm surge" "coastal erosion" "ice dam" "permafrost erosion" "permafrost melt" "climate" "climate-change" "climate-breakdown" "sea-level-rise" "deluge-rain-event" "ocean-solidification" "natural-disaster" "winter-storm" "ice-storm" "heat-wave" "cold-wave" "storm-surge" "coastal-erosion" "ice-dam" "permafrost-erosion" "permafrost-melt" }
    
    FILTER(CONTAINS(lcase(str(?tags)),  ?match_keyword) || CONTAINS(lcase(str(?description)),  ?match_keyword)).
    
  }

}