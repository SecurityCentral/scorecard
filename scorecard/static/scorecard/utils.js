$(document).ready(function() {
    $(".technology").hide();
    $(".NIST").hide();
    $("body").css("overflow", "auto");
});

$(".techbutton").click(function() {
    $(".NIST").hide();
    $(".technology").show();
});

$(".NISTbutton").click(function() {
    $(".NIST").show();
    $(".technology").hide();
});

$(".processbutton").click(function() {
    $(".NIST").hide();
    $(".technology").hide();
});

$(".peoplebutton").click(function() {
    $(".NIST").hide();
    $(".technology").hide();
});

$(".productsbutton").click(function() {
    window.location.replace("/productsview/");
});
