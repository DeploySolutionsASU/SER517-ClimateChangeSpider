$(document).ready(function() {
    let selectedKeywords = "";
    let selectedLevel = "";

    $('.dropdown-menu a').on('click', function(){
        selectedLevel = $(this).html();
        $('.dropdown-toggle').html(selectedLevel);
    })

    // Search button handler
    $('#searchBtn').click(function () {
        selectedKeywords = $("#keywords").val();
        console.log(selectedKeywords);
        console.log(selectedLevel);
    });

    // Result generation button handler
    $('#resultBtn').click(function () {

    });
});