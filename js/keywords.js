$(document).ready(function () {
    const url = 'http://www.mocky.io/v2/5e67e73e3100005c00230e29';
    var words = [];
    $.getJSON(url, function(data){
            for(var i = 0; i < data['keywords'].length; i++){
                words.push(data['keywords'][i]);
            }
    console.log(words);
    keywords = document.getElementById("keywords");

    for (var i = 0; i < words.length; i++){
        var newKeyWord = document.createElement('option');
        newKeyWord.innerHTML = words[i];
        keywords.appendChild(newKeyWord);   
    }
    });
    
});
