PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?g ?url ?name ?address ?telephone ?sameAs ?Logo ?isBasedOnUrl ?description
WHERE { 
  GRAPH ?g{
  { ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://rdf.data-vocabulary.org/#Organization>;
             OPTIONAL{?subject <http://rdf.data-vocabulary.org/#url> ?url;
             <http://rdf.data-vocabulary.org/#name> ?name;
                             <http://rdf.data-vocabulary.org/#address> ?address;
                             <http://rdf.data-vocabulary.org/#tel> ?telephone}} UNION 		
   { ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org.408ss.com/Organization>;
              OPTIONAL{?subject <http://schema.org.408ss.com/#url> ?url;
             <http://schema.org.408ss.com/#name> ?name;
                             <http://schema.org.408ss.com/#address> ?address;
            <http://schema.org.408ss.com/#tel> ?telephone;
            <http://schema.org/Organization/sameAs> ?sameAs;
            <https://schema.org/Organization/logo> ?Logo;
            <http://schema.org.408ss.com/Organization/isBasedOnUrl> ?isBasedOnUrl;
            <http://schema.org/Organization/description> ?description}} UNION
    { ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Organization>;
              OPTIONAL{?subject <http://schema.org/#url> ?url;
             <http://schema.org/#name> ?name;
                             <http://schema.org/#address> ?address;
            <http://schema.org/#tel> ?telephone}}
  }
}
