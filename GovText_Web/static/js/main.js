/*
 * This is the Javascript file that makes requests to our controller.
 * We have prepared one API that makes requests in two unique ways
 * The filter option requests for data to be displayed and the download option 
 * requests for data to be in a downloadable form
 */

$( document ).ready(function() {
    // Bills
    $('#filter-bill').click(function() {
        //Reload the page to display the new data.
        //You could optionally work with Ajax
        window.location.href="/bills?name=" + $("#billauthor").val() + "&billdate=" + $("#billdate").val()
        + "&billparty=" + $("#billparty").val() + "&billlocation=" + $("#billlocation").val()
    });

    $('#download-bill').click(function() {
        window.location.href="/bills?format=csv&name=" + $("#billauthor").val()
    });

    // Appoints
    $('#filter-appoints').click(function() {
        //Reload the page to display the new data.
        //You could optionally work with Ajax
        window.location.href="/appoints?name=" + $("#appointee").val() + "&appointyear=" + $("#appointyear").val()
        + "&appointparty=" + $("#appointparty").val() + "&appointgender=" + $("#appointgender").val()
    });

    $('#download-appoints').click(function() {
        window.location.href="/appoints?format=csv&name=" + $("#appointee").val() + "&appointyear=" + $("#appointyear").val()
        + "&appointparty=" + $("#appointparty").val() + "&appointgender=" + $("#appointgender").val()
    });

    // Press
    $('#filter-press').click(function() {
        //Reload the page to display the new data.
        //You could optionally work with Ajax
        window.location.href="/press?postid=" + $("#postid").val() + "&location=" + $("#location").val()
        + "&year=" + $("#year").val() + "&month=" + $("#month").val()
    });


    // Speaker (Template)
    $('#filter-btn').click(function() {
        //Reload the page to display the new data.
        //You could optionally work with Ajax
        window.location.href="/speakers?name=" + $("#speaker").val()
    });

    $('#download-btn').click(function() {
        window.location.href="/speakers?format=csv&name=" + $("#speaker").val()
    });

});
