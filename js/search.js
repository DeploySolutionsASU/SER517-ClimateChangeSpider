
// key: search_level
// value: search_results_json
let searchResults = {};
let selectedLevels = [];

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
        searchResults = {}
        let inputElements = document.getElementsByClassName('form-check-input');
        for(let i=0; inputElements[i]; ++i){
              if(inputElements[i].checked){
                selectedLevels.push(inputElements[i].value);
              }
        }

        //console.log(getQuery(selectedLevels[0], selectedKeywords))
        document.getElementById("all_results").innerHTML = "";

        if(selectedLevels.length > 0 && selectedKeywords.length > 0) {

            $('.loader').show();
            for (var j = 0; j < selectedLevels.length; j++) {
                var sectionName = "section"+j
                addNewResultSection(sectionName, selectedLevels[j])
                elasticSearchResult(selectedLevels[j].toLowerCase(), sectionName, selectedKeywords);
                // fetch(getQuery(selectedLevels[j], selectedKeywords), sectionName, selectedLevels[j])
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
    const section = document.createElement("div");
    section.id = sectionName
    section.classList.add("container-fluid")
    const sectionTitle = document.createElement("h4");
    sectionTitle.innerHTML = searchLevel + " Results"
    document.getElementById("all_results").appendChild(section)
    //document.getElementById(sectionName).appendChild(sectionTitle)
}

const queryType = {
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
};



function convertJsonToTable(data, searchLevel) {
    let i;
    const cols = []
    const cols_json = data.hits.hits;

    for(colum in cols_json[0]["_source"]) {
        cols.push(colum);
    }
    debugger;

    // Create a table element
    const table = document.createElement("table");
    table.class = "collapse in";
    table.id = searchLevel;

    // Create table row tr element of a table
    const tr = table.insertRow(-1);
    for (i = 0; i < cols.length; i++) {
        // Create the table header th element
        const theader = document.createElement("th");
        theader.innerHTML = formatTableColumn(cols[i]);
        // Append columnName to the table row
        tr.appendChild(theader);
    }

    // Adding the data to the table
    const list = cols_json;
    let trow;
    for (i = 0; i < list.length; i++) {
        // Create a new row
        trow = table.insertRow(-1);
        for (let j = 0; j < cols.length; j++) {
            const cell = trow.insertCell(-1);
            // Inserting the cell at particular place
             if (j != 0) {
                 if (j == 1){
                    if (list[i]["_source"] != null) {
                        const content = (list[i]['_source'][cols[j]]);
                        addToolTip(cell, content);
                    } 
                 }
                else if (list[i]["_source"] != null) {
                    const content = (list[i]['_source'][cols[j]]);
                    formatContent(cell, content);
                } else {
                    cell.innerHTML = "N/A"
                }
            } else {
                 if (list[i]['_source'][cols[j]]!= null) {
                    if (j == 0) {
                        cell.innerHTML = '<a target="_blank" href="' + list[i]['_source'][cols[j]] + '">' + list[i]['_source'][cols[j]] + '</a>';
                    } else {
                        const content = formatTableColumn(list[i]['_source'][cols[j]]);
                        formatContent(cell, content)
                    }
                } else {
                    cell.innerHTML = "N/A"
                }
             }
            cell.style.wordWrap = "break-word"
        }
    }
    return table
}

function formatContent(cell, content) {
      if(content.length > 40) {
          const lessContent = content.substring(0, 40);
          const moreContent = content.substring(40, content.length);
          cell.innerHTML = '<span>'+ lessContent +'</span>' + '<span style="display: none" class="more">'+moreContent+'</span>'
            + '<div class="readMoreCls" onclick="readMore(this)" id="readMore">read more..</div>'
            + '<div style="display: none" onclick="readLess(this)" id="readLess" class="readLessCls">read less</div>'
        } else {
            cell.innerHTML = content
        }
}

function addToolTip(cell, content) {
    if(content.length > 40) {
        const lessContent = content.substring(0, 40);
        const moreContent = content.substring(40, content.length);
        cell.innerHTML = '<span>'+ lessContent +'</span>' + '<span style="display: none" class="more">'+moreContent+'</span>'
          + '<div class="readMoreCls" title="'+content+'" onclick="readMore(this)" id="readMore">read more..</div>'
          + '<div style="display: none" onclick="readLess(this)" id="readLess" class="readLessCls">read less</div>'
      } else {
          cell.innerHTML = content
      }
}

function formatTableColumn(columnName) {
    let formattedName = "";
    debugger;
    if(columnName.includes('_')) {
        columnName.split('_').forEach(function (item) {
            formattedName += (item.charAt(0).toUpperCase() + item.slice(1));
            formattedName += " ";
        });
        return formattedName;
    }
    else {
        return  columnName
    }
}

function elasticSearchResult(searchLevel, sectionName, keywords) {
    let list_keywords = "";
    keywords.forEach(function (words) {
        list_keywords += "("+ words + ")" + " OR "
    })

    list_keywords = list_keywords.trim()
    const data = {
        "query": {
            "query_string": {
                "query": "*"
            }
        }
    };

    // AWS URL: https://search-cc14-prototype-s5q5rjhkogrxzrmfzutzt4umnm.ca-central-1.es.amazonaws.com
    $.ajax({
      method: "POST",
      url: "http://localhost:9200/"+searchLevel+"/_search?pretty",
      crossDomain: true,
      async: false,
      data: JSON.stringify(data),
      dataType : 'json',
      contentType: 'application/json',
    })
    .done(function( data ) {
        debugger;
        if(data.hits.hits.length > 0) {
            searchResults[searchLevel] = data
            console.log("Data: " + JSON.stringify(searchResults) + "\nStatus: " + status);
            const table = convertJsonToTable(data, searchLevel);
            table.classList.add("table");
            const sectionCount = document.createElement("p");
            sectionCount.innerHTML = searchLevel + " Count: " + data.hits.hits.length;
            document.getElementById(sectionName).appendChild(sectionCount);
            const btnToggle = document.createElement("button");
            btnToggle.className = "btn btn-info";
            btnToggle.innerText = searchLevel + " Results";
            btnToggle.style.marginBottom = "10px";
            btnToggle.setAttribute("data-toggle", "collapse");
            btnToggle.setAttribute("data-target", "#" + searchLevel);
            document.getElementById(sectionName).appendChild(btnToggle);
            document.getElementById(sectionName).appendChild(table);
            const hrline = document.createElement("hr");
            document.getElementById(sectionName).appendChild(hrline);
            if (Object.keys(searchResults).length == selectedLevels.length) {
                $('.loader').hide();
                $('#resultBtn').show();
            }
            console.log(data);
        }
    })
    .fail(function( data ) {
        searchResults[searchLevel] = data
        debugger
        $('.loader').hide();
      console.log(data);
    });

}
