/*
 * This is the Javascript file that makes requests to our controller.
 * We have prepared one API that makes requests in two unique ways
 * The filter option requests for data to be displayed and the download option 
 * requests for data to be in a downloadable form
 */


// Bills
$('#filter-bill').click(function() {
	//Reload the page to display the new data.
	//You could optionally work with Ajax
	window.location.href="/bills?name=" + $("#billauthor").val()
});

$('#download-bill').click(function() {
	window.location.href="/bills?format=csv&name=" + $("#billauthor").val()
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
