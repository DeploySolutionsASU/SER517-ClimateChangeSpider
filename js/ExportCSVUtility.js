function convertToCSV(objArray) {
    var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
    var str = '';

    for (var i = 0; i < array.length; i++) {
        var line = '';
        for (var index in array[i]) {
            if (line != '') line += ','

            line += array[i][index];
        }

        str += line + '\r\n';
    }

    return str;
}

//hardcoded the response for testing
var response = {
  "head": {
    "vars": [ "g" , "main_page" , "part_of" , "url" , "image" , "title" , "author" , "headline" , "publisher" , "date_published" , "date_modified" , "comment" ]
  } ,
  "results": {
    "bindings": [

      {
        "g": { "type": "uri" , "value": "https://www.climate-change-guide.com/contact.html" } ,
        "url": { "type": "literal" , "value": "https://www.climate-change-guide.com/contact.html" } ,
        "image": { "type": "literal" , "value": "https://www.climate-change-guide.com/climate-change-fb.jpg" } ,
        "title": { "type": "literal" , "value": "Contact Climate-Change-Guide.com" }
      },
            {
        "g": { "type": "uri" , "value": "http://www.firesciencenorthatlantic.org/research-publications-1/2015/4/8/managing-fuels-in-northeastern-barrens-cape-cod-national-seashore-w8zen" }
      }
	  ]
	  }
	  };


function getHeaders(jsonObject) {
   var headers = jsonObject["head"];
   //console.log(headers)
   return headers

}

//Parsing of the response
function getItems(headers, response) {
	rows = []
  for(var r in  response["results"]["bindings"]){
    row_data = {}
    row_item_json = response["results"]["bindings"][r]
    row_item_json = JSON.stringify(row_item_json)
    for(var h in headers.vars) {
    header_name = JSON.stringify(headers.vars[h])
     if(JSON.stringify(row_item_json[header_name]) != null){
       console.log(row_item_json[header_name]["value"])
       row_data[header_name] = JSON.stringify(row_item_json[header_name]["value"])
     } else {
       console.log("inv")
     }

    }
    console.log(row_data)
    rows.push(row_data)

  }
}


function exportCSVFile(headers, items, fileTitle) {
    if (headers) {
        items.unshift(headers);
    }

    // Convert Object to JSON
    var jsonObject = JSON.stringify(items);

    var csv = this.convertToCSV(jsonObject);

    var exportedFilenmae = fileTitle + '.csv' || 'export.csv';

    var blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    if (navigator.msSaveBlob) { // IE 10+
        navigator.msSaveBlob(blob, exportedFilenmae);
    } else {
        var link = document.createElement("a");
        if (link.download !== undefined) { // feature detection
            // Browsers that support HTML5 download attribute
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", exportedFilenmae);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}


