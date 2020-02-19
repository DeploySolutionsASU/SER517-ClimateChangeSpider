PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?ID ?name ?url 
WHERE { 
  GRAPH ?ID{
  { ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/WebSite>;
              OPTIONAL{
             ?subject <http://schema.org/WebSite/name> ?name;
            <http://schema.org/WebSite/url> ?url.}} UNION
    {?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Article>;
              OPTIONAL{
             ?subject <http://schema.org/name> ?name;
            <http://schema.org/url> ?url.}}
  }
  FILTER(CONTAINS(str(?ID), "environment") || CONTAINS(str(?ID), "climate") || CONTAINS(str(?ID), "weather") || CONTAINS(str(?ID), "flood") || CONTAINS(str(?ID), "fire"))
}
LIMIT 100



