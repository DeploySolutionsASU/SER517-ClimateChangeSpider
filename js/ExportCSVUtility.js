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