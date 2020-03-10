function convertToCSV(objArray) {
    var csv = "";
    objArray.forEach(function (row) {
        csv += row.join(',');
        csv += "\n";
    });

    return csv;
}


function getRowItems(response) {
	var resultList = []
	//safest way to parse a JSON
	var jsonData=response;
	//head variable anyway a list.
	var headList = jsonData.head.vars;
    resultList.push(headList);
    //started parsing
    var rows = jsonData.results.bindings

    // iterating all the rows from the result json
    for (var i = 0; i < rows.length; i++) {
        // Create a new row 
        var currentRow = []
        // iterating all the headers
        for (var j = 0; j < headList.length; j++) {
            if (rows[i][headList[j]] != null) {
                //updating row with binding value
                currentRow.push(rows[i][headList[j]].value)
            } else {
                currentRow.push("N/A")
            }
        }
        resultList.push(currentRow)
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
