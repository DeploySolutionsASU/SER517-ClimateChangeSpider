
// key: search_level
// value: search_results_json
let searchResults = {};
let selectedLevels = [];

$(document).ready(function () {
    let selectedKeywords = "";
    $('.loader').hide();
    $('#resultBtn').hide();

    // Export button handler
    $('#resultBtn').click(function () {
        for(var searchLevel in searchResults) {
            exportCSVFile(getRowItems(searchResults[searchLevel]), searchLevel);
        }
    });

    // Search button handler
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

        document.getElementById("all_results").innerHTML = "";
        if(selectedLevels.length > 0 && selectedKeywords.length > 0) {
            $('.loader').show();
            for (let j = 0; j < selectedLevels.length; j++) {
                const sectionName = "section" + j;
                addNewResultSection(sectionName, selectedLevels[j])
                elasticSearchResult(selectedLevels[j].toLowerCase(), sectionName, selectedKeywords);
            }
        } else {
            alert("Please check the keywords or select at least one search level!");
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

function readMoreTitle(current) {
    $(current).hide();
    $(current).parent().find('.more').show();
    $(current).parent().find('#readLess').show();
    $(current).parent().find('#less').hide();
}

 function readLessTitle(current) {
    $(current).hide();
    $(current).parent().find('.more').hide();
    $(current).parent().find('#readMore').show();
    $(current).parent().find('#less').show();
}

function addNewResultSection(sectionName, searchLevel) {
    const section = document.createElement("div");
    section.id = sectionName
    section.classList.add("container-fluid")
    section.style.marginBottom = "1%";
    const sectionTitle = document.createElement("h4");
    sectionTitle.innerHTML = searchLevel + " Results"
    document.getElementById("all_results").appendChild(section)
}


function convertJsonToTable(data, searchLevel) {
    let i;
    const cols = []
    const cols_json = data.hits.hits;

    for(colum in cols_json[0]["_source"]) {
        if(colum != "url" && colum != "subject") {
            cols.push(colum);
        }
    }

    // Create a table element
    const table = document.createElement("table");
    table.id = searchLevel;

    // Create table row tr element of a table
    const theadtag = document.createElement("thead");
    const tr = document.createElement("tr");
    for (i = 0; i < cols.length; i++) {
        // Create the table header th element
        const theader = document.createElement("th");
        theader.innerHTML = formatTableColumn(cols[i]);
        theader.style.cursor = "pointer";

        // Append columnName to the table row
        tr.appendChild(theader);
    }

    theadtag.appendChild(tr);
    table.appendChild(theadtag);

    // Adding the data to the table
    const tbodytag =  document.createElement("tbody");
    const list = cols_json;
    let trow;
    for (i = 0; i < list.length; i++) {
        // Create a new row
        trow = document.createElement("tr");
        for (let j = 0; j < cols.length; j++) {
            const cell = trow.insertCell(-1);
            // Inserting the cell at particular place
             if (cols[j] == "title"){
                if (list[i]["_source"] != null) {
                    const content = (list[i]['_source'][cols[j]]);
                    const url = (list[i]['_source']['subject']);
                    embedUrlInTitle(cell, content, url);
                }
             }
            else if (list[i]["_source"] != null && (list[i]['_source'][cols[j]]) != null) {
                const content = (list[i]['_source'][cols[j]]);
                formatContent(cell, content);
            } else {
                cell.innerHTML = "N/A"
            }
            cell.style.wordWrap = "break-word"
        }
        tbodytag.appendChild(trow);
    }

    table.appendChild(tbodytag);
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

function embedUrlInTitle(cell, content, url) {
    if(content.length > 40) {
        const lessContent = content.substring(0, 40);
        cell.innerHTML = '<span id="less">'+'<a href= "'+url+'" target="_blank">'+ lessContent + '</a>'+'</span>' + '<span style="display: none" class="more">'+'<a href= "'+url+'" target="_blank">'+ content + '</a>'+'</span>'
          + '<div class="readMoreCls" title="'+content+'" onclick="readMoreTitle(this)" id="readMore">read more..</div>'
          + '<div style="display: none" onclick="readLessTitle(this)" id="readLess" class="readLessCls">read less</div>'
      } else {
          cell.innerHTML = '<a href= "'+url+'" target="_blank">'+ content + '</a>'
      }
}

function formatTableColumn(columnName) {
    let formattedName = "";
    if(columnName.includes('_')) {
        columnName.split('_').forEach(function (item) {
            formattedName += (item.charAt(0).toUpperCase() + item.slice(1));
            formattedName += " ";
        });
        return formattedName;
    }
    else {
        return  upperCamelCase(columnName)
    }
}

function elasticSearchResult(searchLevel, sectionName, keywords) {
    let list_keywords = "";
    let multi_word = "";
    let single_word = "";
    keywords.forEach(function (words) {
        let sub_words = words.split(" ");
        if(sub_words.length > 1) {
            multi_word += "("
            for (let i=0;i<sub_words.length;i++) {
                if(i != sub_words.length - 1) {
                     multi_word += sub_words[i] + " AND ";
                } else {
                     multi_word += sub_words[i] + ")"
                }
            }
        } else {
            for (let i=0;i<sub_words.length;i++) {
                 if(multi_word.length > 0) {
                     single_word += " OR " + sub_words[i];
                } else {
                     single_word += " " +sub_words[i];
                }
            }
        }
    })

    list_keywords = multi_word + single_word;
    list_keywords = list_keywords.trim()
    const field_name = "match_keyword";
    const start = 0;
    const maxSize = 10000;
    const query_data = {
        "from": start, "size":maxSize,
        "query": {
            "query_string": {
                "query": list_keywords,
                "default_field" : field_name
            }
        }
    };

    // Update the URL based on EC2 instance address
    $.ajax({
      method: "POST",
      url : "http://18.191.69.111:8080/search-management/results"+"?searchLevel="+searchLevel,
      crossDomain: true,
      async: true,
      data: JSON.stringify(query_data),
      dataType : 'json',
      contentType: 'application/json',
    }).progress(function() {
        $('.loader').show();
    })
    .done(function( data ) {
        searchResults[searchLevel] = data;
        if(data.hits != undefined && data.hits.hits.length > 0) {
            const table = convertJsonToTable(data, searchLevel);
            table.classList.add("table");
            table.classList.add("collapse");
            databinding(sectionName, searchLevel, data);
            document.getElementById(sectionName).appendChild(table);
             $('#'+searchLevel).DataTable();
             $('.dataTables_length').addClass('bs-select');
             $('#'+searchLevel+'_wrapper').hide();
        } else {
            databinding(sectionName, searchLevel, data);
            handleNoData(sectionName, searchLevel);
        }

        if (Object.keys(searchResults).length == selectedLevels.length) {
                $('.loader').hide();
                $('#resultBtn').show();
        }
    })
    .fail(function( data ) {
         searchResults[searchLevel] = data
         databinding(sectionName, searchLevel, data);
         handleNoData(sectionName, searchLevel);
         if (Object.keys(searchResults).length == selectedLevels.length) {
                $('#resultBtn').show();
                $('.loader').hide();
            }
    });
}

/**
 * Function to handle empty result
 * @param sectionName
 * @param searchLevel
 */
function handleNoData(sectionName, searchLevel) {
     const msg = document.createElement("p");
      msg.innerText = "No data!";
      msg.id = searchLevel;
      msg.classList.add("collapse");
      msg.style.marginLeft = "50%";
     document.getElementById(sectionName).appendChild(msg);
}
/**
 * Function creating collapse button dynamically
 * @param sectionName
 * @param searchLevel
 * @param data
 */
function databinding(sectionName, searchLevel, data) {
        const btnToggle = document.createElement("button");
        btnToggle.className = "btn btn-info dropdown";
        btnToggle.id = "toggleBtn";
        btnToggle.style.marginLeft = "15%";
        btnToggle.style.marginBottom = "40px";
        btnToggle.style.width = "75%";
        btnToggle.addEventListener("click", toggleClass, false);

        if(data.hits != undefined) {
            btnToggle.innerText = upperCamelCase(searchLevel) + " ("+ data.hits.hits.length + ")";
        } else {
            btnToggle.innerText = upperCamelCase(searchLevel) + " ("+ 0 + ")";
        }

        btnToggle.style.marginBottom = "10px";
        btnToggle.setAttribute("data-toggle", "collapse");
        btnToggle.setAttribute("data-target", "#" + searchLevel);
        const iTag = document.createElement("i");
        iTag.id = "arrowID";
        iTag.className = "arrowDown";
        btnToggle.appendChild(iTag);
        document.getElementById(sectionName).appendChild(btnToggle);
}

function toggleClass() {
    const levelID = $(this).attr('data-target');
    $(this).find('#arrowID').toggleClass("arrowDown arrowUp");
    $(levelID +'_wrapper').toggle();
}

 /**
 * Method to convert normal string to upper camel case
 * @param str
 * @returns {string}
 */
 function upperCamelCase(str) {
        return str.replace(/(?:^\w|[A-Z]|\b\w)/g, function(word, index) {
            return word.toUpperCase();
        }).replace(/\s+/g, '');
 }
