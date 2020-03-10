$(document).ready(function () {
    var words = ['Climate Change', 'Climate breakdown', 'Flooding', 'Flood', 'sea level rise', 'deluge rain event',
    'ocean solidification', 'natural disaster', 'winter storm', 'drought', 'ice storm', 'tornado', 'hail',
    'bushfire', 'wildfire', 'waves', 'heat wave', 'cold wave', 'hurricane', 'earthquake', 'tsunami',
    'landslide', 'Storm surge', 'coastal erosion', 'ice dam', 'permafrost erosion', 'permafrost melt'];

    keywords = document.getElementById("keywords");

    for (var i = 0; i < words.length; i++){
        var newKeyWord = document.createElement('option');
        newKeyWord.innerHTML = words[i];
        keywords.appendChild(newKeyWord);   
    }
});
