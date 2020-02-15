PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?ID ?main_page ?part_of ?url ?image ?title ?author ?headline ?publisher ?date_published ?date_modified ?comment 
WHERE { 
  GRAPH ?ID{
  { ?subject <http://opengraphprotocol.org/schema/type> "article";
             OPTIONAL{
             ?subject <http://opengraphprotocol.org/schema/url> ?url;
            <http://opengraphprotocol.org/schema/image> ?image;
            <http://opengraphprotocol.org/schema/title> ?title.}} UNION 		
   { ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Article>;
              OPTIONAL{
             ?subject <http://schema.org/Article/author> ?author;
            <http://schema.org/Article/dateModified> ?date_modified;
            <http://schema.org/Article/datePublished> ?date_published;
            <http://schema.org/Article/publisher> ?publisher;
            <http://schema.org/Article/articleSection> ?article_section;
            <http://schema.org/Article/commentCount> ?comment;
            <http://schema.org/Article/headline> ?headline;
           <http://schema.org/Article/isPartOf> ?part_of;
            <http://schema.org/Article/mainEntityOfPage> ?main_page.}} UNION
    {?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Article>;
              OPTIONAL{
             ?subject <http://schema.org/author> ?author;
            <http://schema.org/dateModified> ?date_modified;
            <http://schema.org/datePublished> ?date_published;
            <http://schema.org/publisher> ?publisher;
            <http://schema.org/articleSection> ?article_section;
            <http://schema.org/commentCount> ?comment;
            <http://schema.org/headline> ?headline;
           <http://schema.org/isPartOf> ?part_of;
            <http://schema.org/mainEntityOfPage> ?main_page.}}
  }
  FILTER(CONTAINS(str(?ID), "environment") || CONTAINS(str(?ID), "climate") || CONTAINS(str(?ID), "weather") || CONTAINS(str(?ID), "flood") || CONTAINS(str(?ID), "fire"))
}
LIMIT 100



