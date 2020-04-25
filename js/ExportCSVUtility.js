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
    var cols = []
    if(response["hits"] != undefined)
    {
        const cols_json = response["hits"]["hits"]

        if(cols_json.length > 0) {
         for (colum in cols_json[0]["_source"]) {
           cols.push(colum);
         }
     }

    resultList.push(cols)
    for (i = 0; i < cols_json.length; i++) {
        var currentRow = []
        for (let j = 0; j < cols.length; j++) {
                if (cols_json[i]["_source"] != null) {
                    var r = cols_json[i]['_source'][cols[j]]
                    if(r != undefined){
                        currentRow.push(r.replace(/,/g, ';'));
                    }
                } else {
                    currentRow.push("N/A");
                }


        }
        resultList.push(currentRow)
    }
    }
    return resultList;
}


function exportCSVFile(items, fileTitle) {
    if(items.length > 0) {
        var csv = this.convertToCSV(items);
        var exportedFilenmae = fileTitle + '.csv' || 'export.csv';
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
        hiddenElement.target = '_blank';
        hiddenElement.download = exportedFilenmae;
        hiddenElement.click();
    }

}
