
// key: search_level
// value: search_results_json
var searchResults = {}

var selectedLevels = [];

$(document).ready(function () {
    let selectedKeywords = "";

    $('.loader').hide();
    $('#resultBtn').hide();

    $('#resultBtn').click(function () {
        for(var searchLevel in searchResults) {
            exportCSVFile(getRowItems(searchResults[searchLevel]), searchLevel);
        }
    });

    // Search generation button handler
    $('#searchBtn').click(function () {
        selectedKeywords = $("#keywords").val();
        selectedLevels = []
        let inputElements = document.getElementsByClassName('form-check-input');
        for(let i=0; inputElements[i]; ++i){
              if(inputElements[i].checked){
                selectedLevels.push(inputElements[i].value);
              }
        }

        console.log(getQuery(selectedLevels[0], selectedKeywords))
        document.getElementById("all_results").innerHTML = "";

        if(selectedLevels.length > 0 && selectedKeywords.length > 0) {
            $('.loader').show();
            for (var j = 0; j < selectedLevels.length; j++) {
                var sectionName = "section"+j
                addNewResultSection(sectionName, selectedLevels[j])
                fetch(getQuery(selectedLevels[j], selectedKeywords), sectionName, selectedLevels[j])
            }
        } else {
            alert("Please check the keywords or select alteast one search level!");
        }
    });


});



function readMore(current) {
    $(current).hide();
    $(current).parent().find('.more').show();
    $(current).parent().find('#readLess').show();
}

 function readLess(current) {
    $(current).hide();
    $(current).parent().find('.more').hide();
    $(current).parent().find('#readMore').show();
}

function addNewResultSection(sectionName, searchLevel) {
    var section = document.createElement("div");
    section.id = sectionName
    section.classList.add("container-fluid")
    var sectionTitle = document.createElement("h4");
    sectionTitle.innerHTML = searchLevel + " Results"
    document.getElementById("all_results").appendChild(section)
    document.getElementById(sectionName).appendChild(sectionTitle)
}

var queryType = {
    Article: `PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?g ?url ?image ?title ?author ?date_modified ?date_published ?article_section ?comment ?headline ?part_of ?main_page ?value_of_desc
WHERE {
  GRAPH ?g{
  {
    {
        ?subject <http://opengraphprotocol.org/schema/type> ?object;
        FILTER(CONTAINS(str(?object), "Article"))
    }
    UNION
    {
    	?subject <http://opengraphprotocol.org/schema/type> ?object;
        FILTER(CONTAINS(lcase(str(?object)), "article"))
    }
    ?subject ?desc ?value_of_desc.
     OPTIONAL
     {
        ?subject <http://opengraphprotocol.org/schema/url> ?url;
                 <http://opengraphprotocol.org/schema/image> ?image;
                 <http://opengraphprotocol.org/schema/title> ?title.
     }
  }
  UNION
  {
    {
        ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(str(?object), "Article"))
    }
    UNION
    {
    	?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(lcase(str(?object)), "article"))
    }
    ?subject ?desc ?value_of_desc.
    OPTIONAL
    {
       ?subject <http://schema.org/Article/author> ?author;
                <http://schema.org/Article/dateModified> ?date_modified;
                <http://schema.org/Article/datePublished> ?date_published;
                <http://schema.org/Article/publisher> ?publisher;
                <http://schema.org/Article/articleSection> ?article_section;
                <http://schema.org/Article/commentCount> ?comment;
                <http://schema.org/Article/headline> ?headline;
                <http://schema.org/Article/isPartOf> ?part_of;
                <http://schema.org/Article/mainEntityOfPage> ?main_page.
    }
  }
  UNION
  {
    {
        ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Article>;
        FILTER(CONTAINS(str(?object), "Article"))
    }
    UNION
    {
        ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(lcase(str(?object)), "article"))
    }
    ?subject ?desc ?value_of_desc.
    OPTIONAL
    {
       ?subject <http://schema.org/author> ?author;
                <http://schema.org/dateModified> ?date_modified;
                <http://schema.org/datePublished> ?date_published;
                <http://schema.org/publisher> ?publisher;
                <http://schema.org/articleSection> ?article_section;
                <http://schema.org/commentCount> ?comment;
                <http://schema.org/headline> ?headline;
                <http://schema.org/isPartOf> ?part_of;
                <http://schema.org/mainEntityOfPage> ?main_page.
    }
  }
  }
  `,

    Event: `SELECT DISTINCT ?g ?name ?url (CONCAT(?street_address, ", " ,?addressRegion, ", " ,?locality, ", " ,?country ) AS ?some) ?value_of_desc
WHERE
{
  GRAPH ?g{
	{
	    ?subject ?predicate ?object;
                 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Event>;
                 <http://schema.org/location> ?location;
			     <http://schema.org/name> ?name;
			     <http://schema.org/url> ?url.
	    ?subject ?desc ?value_of_desc.
        ?location  <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Place>;
                   <http://schema.org/name> ?place_name;
    			   <http://schema.org/address> ?address.
        ?address <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/PostalAddress>;
     	         <http://schema.org/streetAddress> ?street_address;
    	         <http://schema.org/addressRegion> ?addressRegion;
     	         <http://schema.org/addressLocality> ?locality;
                 <http://schema.org/addressCountry> ?country.
    }
    UNION
    {
        ?subject ?predicate ?object;
                 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Event>;
                 <http://schema.org/location> ?location;
			     <http://schema.org/name> ?name;
			     <http://schema.org/url> ?url.
        ?subject ?desc ?value_of_desc.
        ?location  <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Place>;
                   <http://schema.org/name> ?place_name;
    		       <http://schema.org/address> ?address.
        ?address <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/PostalAddress>;
     	         <http://schema.org/streetAddress> ?street_address;
    	         <http://schema.org/addressRegion> ?addressRegion;
     	         <http://schema.org/addressLocality> ?locality;
                 <http://schema.org/addressCountry> ?country.
    }
  }`,

    Organization: `PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?g ?url ?name ?address ?telephone ?sameAs ?Logo ?isBasedOnUrl ?description ?value_of_desc
WHERE {
  GRAPH ?g{
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
        ?subject <http://rdf.data-vocabulary.org/#url> ?url;
                 <http://rdf.data-vocabulary.org/#name> ?name;
                 <http://rdf.data-vocabulary.org/#address> ?address;
                 <http://rdf.data-vocabulary.org/#tel> ?telephone
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
        ?subject <http://schema.org/#url> ?url;
                 <http://schema.org/#name> ?name;
                 <http://schema.org/#address> ?address;
                 <http://schema.org/#tel> ?telephone
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
  }`,

    Website: `PREFIX prefix: <http://prefix.cc/>
SELECT distinct ?g ?object ?name ?url ?value_of_desc
WHERE {
  GRAPH ?g{
  {
    {
        ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
		FILTER(CONTAINS(str(?object), "WebSite"))
    }
    UNION
    {
    	?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(lcase(str(?object)), "website"))
    }
    ?subject ?desc ?value_of_desc.
    OPTIONAL
    {
       ?subject <http://schema.org/WebSite/name> ?name;
                <http://schema.org/WebSite/url> ?url.
    }
  }
  UNION
  {
    {
        ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(str(?object), "WebSite"))
    }
    UNION
    {
    	?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?object;
        FILTER(CONTAINS(lcase(str(?object)), "website"))
    }
    ?subject ?desc ?value_of_desc.
    OPTIONAL
    {
        ?subject <http://schema.org/name> ?name;
                 <http://schema.org/url> ?url.
    }
  }
  }
  `
}

function executeQuery(query, containerId) {
    $.post(query, {},
        function (data, status) {
            searchResults[searchLevel] = data
            console.log("Data: " + JSON.stringify(searchResults)  + "\nStatus: " + status);
            var table = convertJsonToTable(data)
            table.classList.add("table");
            document.getElementById(containerId).appendChild(table)
            $('.loader').hide();

        }).error(function () {
            $('.loader').hide();
           console.log("HTTP request failed");
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
        theader.innerHTML = formatTableColumn(cols[i]);

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
                if(j == 0) {
                    cell.innerHTML = '<a target="_blank" href="'+list[i][cols[j]]["value"]+'">'+ list[i][cols[j]]["value"]+'</a>';
                } else {
                    var content = list[i][cols[j]]["value"];
                    if(content.length > 40) {
                        var lessContent = content.substring(0, 40);
                        var moreContent = content.substring(40, content.length);
                        cell.innerHTML = '<span>'+ lessContent +'</span>' + '<span style="display: none" class="more">'+moreContent+'</span>'
                            + '<div class="readMoreCls" onclick="readMore(this)" id="readMore">read more..</div>'
                            + '<div style="display: none" onclick="readLess(this)" id="readLess" class="readLessCls">read less</div>'
                    } else {
                        cell.innerHTML = content
                    }

                }
                cell.style.wordWrap = "break-word"
            } else {
                cell.innerHTML = "N/A"
            }
        }
    }
    return table
}


function formatTableColumn(columnName) {
    let formattedName = "";
    columnName.split('_').forEach(function(item){
         formattedName += (item.charAt(0).toUpperCase() + item.slice(1));
         formattedName += " ";
    });
    return formattedName;
}


function getQuery(selectedLevel, keywords) {
    console.log(selectedLevel)
    var baseQuery = queryType[selectedLevel]
    baseQuery += ' FILTER('
    for (var i = 0; i < keywords.length; i++) {
        if (i != keywords.length - 1) {
            baseQuery += 'CONTAINS(str(?value_of_desc), "' + keywords[i] + '") || '
        }
        else {
            baseQuery += 'CONTAINS(str(?value_of_desc), "' + keywords[i] + '"))}'
        }
    }
    return baseQuery
}


function fetch(query, containerID, searchLevel) {
    var encodedStr = encodeURIComponent(query)
    var queryURL = "http://localhost:3030/test_data_set/query?query=" + encodedStr
    executeQuery(queryURL, containerID, searchLevel)
}

function executeQuery(query, containerId, searchLevel) {
    $.post(query, {},
        function (data, status) {
            searchResults[searchLevel] = data
            console.log("Data: " + JSON.stringify(searchResults)  + "\nStatus: " + status);
            var table = convertJsonToTable(data)
            table.classList.add("table");
            document.getElementById(containerId).appendChild(table)

            console.log(Object.keys(searchResults).length)
            console.log(selectedLevels.length)
            console.log(searchResults)
            if (Object.keys(searchResults).length == selectedLevels.length) {
                $('.loader').hide();
                 $('#resultBtn').show();
            }
        })

}


