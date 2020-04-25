$(document).ready(function () {
    const url = 'http://www.mocky.io/v2/5e67e73e3100005c00230e29';
    var words = [];
    var data = {
        "keywords": [
          "Climate change",
          "Climate Breakdown",
          "Flooding",
          "Flood",
          "Sea level rise",
          "Deluge rain event",
          "Ocean solidification",
          "Natural disaster",
          "Winter storm",
          "Drought",
          "Ice storm",
          "Tornado",
          "Hail",
          "Bushfire",
          "Wildfire",
          "Waves",
          "Heat wave",
          "Cold wave",
          "Hurricane",
          "Earthquake",
          "Tsunami",
          "Landslide",
          "Storm surge",
          "Coastal erosion",
          "Ice dam",
          "Permafrost erosion",
          "Permafrost melt"
          ]
      }

    for(var i = 0; i < data['keywords'].length; i++){
        words.push(data['keywords'][i]);
    }

    keywords = document.getElementById("keywords");

    for (var i = 0; i < words.length; i++){
        var newKeyWord = document.createElement('option');
        newKeyWord.innerHTML = words[i];
        keywords.appendChild(newKeyWord);
    }
});
