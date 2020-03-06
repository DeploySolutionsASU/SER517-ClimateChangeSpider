function convertToCSV(objArray) {
    var csv = "";
    objArray.forEach(function (row) {
        csv += row.join(',');
        csv += "\n";
    });

    return csv;
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
   headers =JSON.parse(JSON.stringify(jsonObject)).head.vars;
   return headers
}


function getItems(headers, response) {
	var resultList = []
	//safest way to parse a JSON
	var jsonData=JSON.parse(JSON.stringify(response));
	//head variable anyway a list.
	var headList = jsonData.head.vars;
    resultList.push(headList);
	//started parsing
	for(x in jsonData.results.bindings){
		var bindingData = jsonData.results.bindings[x];
        var row = new Array(headList.length);
		for(var key in bindingData){
			//if element exists in head variable list
			if(headList.includes(key)){
				//updating row with binding value
                row[headList.indexOf(key)]=bindingData[key].value;
			}
		}
        resultList.push(row);
	}
	return resultList;
}


function exportCSVFile(items, fileTitle) {

    var csv = this.convertToCSV(items);
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


function main() {

var fileTitle = 'CSV';
headers = getHeaders(response)
exportCSVFile(getItems(headers, response), "fileTitle");
}

//main()