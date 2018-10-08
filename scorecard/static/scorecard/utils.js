$(document).ready(function() {
    $("body").css("overflow", "auto");
});

$(".techbutton").click(function() {
    hideAll();
    $(".technology").show();
});

$(".NISTbutton").click(function() {
    hideAll();
    $(".NIST").show();
});

$(".processbutton").click(function() {
    hideAll();
});

$(".peoplebutton").click(function() {
    hideAll();
    $(".people").show();
});

function hideAll() {
    $(".NIST").hide();
    $(".people").hide();
    $(".technology").hide();
}