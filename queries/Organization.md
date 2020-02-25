PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?ID ?url ?name ?address ?telephone ?sameAs ?Logo ?isBasedOnUrl ?description
WHERE { 
  GRAPH ?ID{
  {{ ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
             FILTER(CONTAINS(str(?object), "Organization")) 
  }
    UNION{
    			?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
             FILTER(CONTAINS(lcase(str(?object)), "organization"))
    }	
             OPTIONAL{?subject <http://rdf.data-vocabulary.org/#url> ?url;
             <http://rdf.data-vocabulary.org/#name> ?name;
                             <http://rdf.data-vocabulary.org/#address> ?address;
                             <http://rdf.data-vocabulary.org/#tel> ?telephone}} UNION 		
   { {?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
              FILTER(CONTAINS(str(?object), "Organization")) 
  }
    UNION{
    			?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
             FILTER(CONTAINS(lcase(str(?object)), "organization"))
    }	
              OPTIONAL{?subject <http://schema.org.408ss.com/#url> ?url;
             <http://schema.org.408ss.com/#name> ?name;
                             <http://schema.org.408ss.com/#address> ?address;
            <http://schema.org.408ss.com/#tel> ?telephone;
            <http://schema.org/Organization/sameAs> ?sameAs;
            <https://schema.org/Organization/logo> ?Logo;
            <http://schema.org.408ss.com/Organization/isBasedOnUrl> ?isBasedOnUrl;
            <http://schema.org/Organization/description> ?description}} UNION
    { {?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
               FILTER(CONTAINS(str(?object), "Organization")) 
  }
    UNION{
    			?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
             FILTER(CONTAINS(lcase(str(?object)), "organization"))
    }	
              OPTIONAL{?subject <http://schema.org/#url> ?url;
             <http://schema.org/#name> ?name;
                             <http://schema.org/#address> ?address;
            <http://schema.org/#tel> ?telephone}}UNION
    { {?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
               FILTER(CONTAINS(str(?object), "Organization")) 
  }
    UNION{
    			?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
             FILTER(CONTAINS(lcase(str(?object)), "organization"))
    }	
              OPTIONAL{?subject <http://www.w3.org/2006/vcard/ns#organization-name> ?name;
                             <http://www.w3.org/2006/vcard/ns#adr> ?address;
            				 <http://www.w3.org/2006/vcard/ns#tel> ?telephone}}
  }
  FILTER(CONTAINS(str(?ID), "fire") || CONTAINS(str(?ID), "environment") || CONTAINS(str(?ID), "flood") || CONTAINS(str(?ID), "weather") || CONTAINS(str(?ID), "climate"))
}
LIMIT 2000