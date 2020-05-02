PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?g ?url ?article_body ?headline ?name ?maincontent ?desc ?comment ?keywords ?mentions ?match_keyword
WHERE { 
GRAPH ?g{
?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/WebPage>;
 
 <https://schema.org/WebPage/url>  ?url;
 
 optional {
      {
        ?subject <https://schema.org/WebPage/inLanguage>  ?lang;
         FILTER(CONTAINS(lcase(str(?lang)), "en")).
      }
      UNION
      {
        ?subject <https://schema.org/WebPage/InLanguage>  ?lang;
         FILTER(CONTAINS(lcase(str(?lang)), "en")).
      }
    }
  
    
    optional {?subject <https://schema.org/WebPage/articleBody> ?article_body.}
    optional{?subject<https://schema.org/WebPage/headline> ?headline.
}
    
    optional{    ?subject<https://schema.org/WebPage/name> ?name.
}
    
    optional{?subject<https://schema.org/mainContentOfPage> ?maincontent.
}
    
    optional {    ?subject   <https://schema.org/WebPage/description> ?desc.
}
    optional{
      ?subject   <https://schema.org/WebPage/comment> ?comment;
}

    optional{
   ?subject <https://schema.org/WebPage/keywords> ?keywords;    
  }

    optional{  ?subject  <https://schema.org/WebPage/mentions> ?mentions;
}
    
     VALUES ?match_keyword { "climate change" "climate breakdown" "flooding" "flood" "sea level rise" "deluge rain event" "ocean solidification" "natural disaster" "winter storm" "drought" "ice storm" "tornado" "hail" "bushfire" "wildfire" "waves" "heat wave" "cold wave" "hurricane" "earthquake" "tsunami" "landslide" "storm surge" "coastal erosion" "ice dam" "permafrost erosion" "permafrost melt" "climate" "climate-change" "climate-breakdown" "sea-level-rise" "deluge-rain-event" "ocean-solidification" "natural-disaster" "winter-storm" "ice-storm" "heat-wave" "cold-wave" "storm-surge" "coastal-erosion" "ice-dam" "permafrost-erosion" "permafrost-melt" "sea level" "deluge rain" "sea rise" "ocean level rise" "ocean rise" }
    
    FILTER(CONTAINS(lcase(str(?keywords)),  ?match_keyword) || CONTAINS(lcase(str(?desc)),  ?match_keyword)
    || CONTAINS(lcase(str(?name)),  ?match_keyword)
    || CONTAINS(lcase(str(?headline)),  ?match_keyword)
    || CONTAINS(lcase(str(?article_body)),  ?match_keyword)
    || CONTAINS(lcase(str(?maincontent)),  ?match_keyword)).


}
}