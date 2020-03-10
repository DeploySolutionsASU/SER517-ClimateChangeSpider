
var queryResults = {}


$(document).ready(function () {
    let selectedKeywords = "";
    let selectedLevel = "";

    $('.dropdown-menu a').on('click', function () {
        selectedLevel = $(this).html();
        $('.dropdown-toggle').html(selectedLevel);
    })

    // Result generation button handler
    $('#resultBtn').click(function () {
        var fileTitle = 'QueryResults';
        exportCSVFile(getRowItems(queryResults), fileTitle);
    });

    // Search generation button handler
    $('#searchBtn').click(function () {
        selectedKeywords = $("#keywords").val();
        console.log(getQuery(selectedLevel, selectedKeywords))
        document.getElementById("section1").innerHTML = "";
        fetch(getQuery(selectedLevel, selectedKeywords), "section1")
    });
});

var queryType = {
    Article: `PREFIX prefix: <http://prefix.cc/> SELECT distinct ?ID ?main_page ?part_of ?url ?image ?title 
    ?author ?headline ?publisher ?date_published ?date_modified ?comment WHERE { GRAPH ?ID{ {{ ?subject 
    <http://opengraphprotocol.org/schema/type> ?object; FILTER(CONTAINS(str(?object), "Article")) } UNION{ ?subject 
    <http://opengraphprotocol.org/schema/type> ?object; FILTER(CONTAINS(lcase(str(?object)), "article")) } 

                         OPTIONAL{
                         ?subject <http://opengraphprotocol.org/schema/url> ?url;
                        <http://opengraphprotocol.org/schema/image> ?image;
                        <http://opengraphprotocol.org/schema/title> ?title.}} UNION 		
               { {?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
                          FILTER(CONTAINS(str(?object), "Article")) 
              }
                UNION{
                            ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
                         FILTER(CONTAINS(lcase(str(?object)), "article"))
                }	
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
                {{?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Article>;
                          FILTER(CONTAINS(str(?object), "Article")) 
              }
                UNION{
                            ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
                         FILTER(CONTAINS(lcase(str(?object)), "article"))
                }	
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
              `,

    Event: `SELECT DISTINCT ?name ?url (CONCAT(?street_address, ", " ,?addressRegion, ", " ,?locality, ", " ,
    ?country ) AS ?some) WHERE { GRAPH ?ID{ { ?subject ?predicate ?object; 
    <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Event>; <http://schema.org/location> 
    ?location; <http://schema.org/name> ?name; <http://schema.org/url> ?url. 

                ?location  <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Place>;
                           <http://schema.org/name> ?place_name;
                            <http://schema.org/address> ?address.

                ?address <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/PostalAddress>;
                    <http://schema.org/streetAddress> ?street_address;
                    <http://schema.org/addressRegion> ?addressRegion;
                    <http://schema.org/addressLocality> ?locality;
                  <http://schema.org/addressCountry> ?country.} UNION
              {?subject ?predicate ?object;
                      <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Event>;
                       <http://schema.org/location> ?location;	
                        <http://schema.org/name> ?name;
                        <http://schema.org/url> ?url.

                ?location  <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Place>;
                           <http://schema.org/name> ?place_name;
                            <http://schema.org/address> ?address.

                ?address <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/PostalAddress>;
                    <http://schema.org/streetAddress> ?street_address;
                    <http://schema.org/addressRegion> ?addressRegion;
                    <http://schema.org/addressLocality> ?locality;
                  <http://schema.org/addressCountry> ?country.} 
              }
              `,

    Organization: `PREFIX prefix: <http://prefix.cc/>
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
                  `,

    Website: `PREFIX prefix: <http://prefix.cc/>
            SELECT distinct ?ID ?object ?name ?url 
            WHERE { 
              GRAPH ?ID{
              { {?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
                    FILTER(CONTAINS(str(?object), "WebSite")) 
            }
            UNION{
                            ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
                         FILTER(CONTAINS(lcase(str(?object)), "website"))
                }	
                          OPTIONAL{
                         ?subject <http://schema.org/WebSite/name> ?name;
                        <http://schema.org/WebSite/url> ?url.}} UNION
                {{?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
            FILTER(CONTAINS(str(?object), "WebSite")) 
            }
            UNION{
                            ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
                         FILTER(CONTAINS(lcase(str(?object)), "website"))
                }

                          OPTIONAL{
                         ?subject <http://schema.org/name> ?name;
                        <http://schema.org/url> ?url.}}
                  }
                  `
}

function executeQuery(query, containerId) {
    $.post(query, {},
        function (data, status) {
            queryResults = data
            console.log("Data: " + JSON.stringify(queryResults)  + "\nStatus: " + status);
            var table = convertJsonToTable(data)
            table.classList.add("table");
            document.getElementById(containerId).appendChild(table)
        });
}

function convertJsonToTable(data) {

    var cols = [];

    var cols_json = data.head.vars
    for (var i = 0; i < cols_json.length; i++) {
        cols.push(cols_json[i]);
    }

    // Create a table element 
    var table = document.createElement("table");

    // Create table row tr element of a table 
    var tr = table.insertRow(-1);

    for (var i = 0; i < cols.length; i++) {

        // Create the table header th element 
        var theader = document.createElement("th");
        theader.innerHTML = cols[i];

        // Append columnName to the table row 
        tr.appendChild(theader);
    }

    // Adding the data to the table 
    var list = data.results.bindings
    for (var i = 0; i < list.length; i++) {

        // Create a new row 
        trow = table.insertRow(-1);
        for (var j = 0; j < cols.length; j++) {
            var cell = trow.insertCell(-1);

            // Inserting the cell at particular place 

            if (list[i][cols[j]] != null) {
                cell.innerHTML = list[i][cols[j]]["value"]
            } else {
                cell.innerHTML = "N/A"
            }
        }
    }
    return table
}


function getQuery(selectedLevel, keywords) {
    console.log(selectedLevel)
    var baseQuery = queryType[selectedLevel]
    baseQuery += ' FILTER('
    for (var i = 0; i < keywords.length; i++) {
        if (i != keywords.length - 1) {
            baseQuery += 'CONTAINS(str(?ID), "' + keywords[i] + '") || '
        }
        else {
            baseQuery += 'CONTAINS(str(?ID), "' + keywords[i] + '"))}'
        }
    }
    return baseQuery
}


function fetch(query, containerID) {
    var encodedStr = encodeURIComponent(query)
    var queryURL = "http://35.226.155.243:3030/test_data_set/query?query=" + encodedStr
    executeQuery(queryURL, containerID)
}


