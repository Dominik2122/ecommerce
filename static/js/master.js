$(function() {
// This function gets cookie with a given name
function getCookie(name) {
var cookieValue = null;
if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
return cookieValue;
}
var csrftoken = getCookie('csrftoken');

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
// test that a given url is a same-origin URL
// url could be relative or scheme relative or absolute
var host = document.location.host; // host + port
var protocol = document.location.protocol;
var sr_origin = '//' + host;
var origin = protocol + sr_origin;
// Allow absolute or scheme relative URLs to same origin
return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
    (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
    // or any other URL that isn't scheme relative or absolute i.e relative.
    !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        // Send the token to same-origin, relative URLs only.
        // Send the token only if the method warrants CSRF protection
        // Using the CSRFToken value acquired earlier
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
}
});
});



// just a quick js option to make autosearch after 1,5s after the end of typing
$(document).ready(function(){
  var searchForm = $(".search-form")
  var searchInput = searchForm.find("[name='q']")
  var typingTimer;
  var typingInterval = 1000;

  searchForm.keydown(function(event){
    clearTimeout(typingTimer)
  });

  searchForm.keyup(function(event){
    tyingTimer = setTimeout(performSearch, typingInterval)
  });



  function performSearch(){
  var query = searchInput.val()
  $.ajax({
      url : "/search/?q="+query,
      type : "GET",
      data : {'search': query},
      success : function(json) {
        searchResults(json['products'])
          },
          error : function(xhr,errmsg,err) {
          }
      });
    }
  });

function searchResults(products){

  var searchOutput = $('.search-output')
  searchOutput.empty();
  if (products){
  for (var product of products) {
    if (product === 'Sorry, not found'){
      searchOutput.append(`<div class='search-item'><h3 class='seach-text'>Sorry, not found</h3></div>`)
    } else {
    searchOutput.append(`<div class='search-item'><a href ='/products/${product['slug']}'> <h3 class='seach-text'><img src = "${product['url']}" class = 'search-img'> ${product['title']}</h3><h3  class = 'seach-text'> ${product['price']}$</h3></a></div>`)
  }}}
}




  $(document).ready(function(){
      let form = $('.ajax-cart')
      form.submit(function(event){
        event.preventDefault();
        let thisForm = $(this)
        let actionEndPoint = thisForm.attr('action')
        let formData = thisForm.serialize();
        $.ajax({
          url: actionEndPoint,
          method: "POST",
          data: formData,
          success: function(json){
            let counter = $('.fa-shopping-cart')[0]
            counter.innerHTML= json['counter']
            let buttonPlace = $('.form-changer')
            if (json['added']){
              buttonPlace.html(`<button type="submit" name="button" class='btn btn-danger'>Remove?</button>`)
            } else {
              buttonPlace.html(`<button type="submit" name="button" class='btn btn-success'>Add?</button>`)
            }





          } ,
          error: function(errorData){
          }
        })
      })
    })
