selectedButtonColor = "blue"
deSelectedButtonColor = "black"

$(document).ready(function() {
    $("body").css("overflow", "auto");
    $(".processbutton").click();
});

$(".techbutton").click(function() {
    hideAll();
    $(".technology").show();
    $(".techbutton").css("color", selectedButtonColor);
    $(".techbutton").blur();
});

$(".NISTbutton").click(function() {
    hideAll();
    $(".NIST").show();
    $(".NISTbutton").css("color", selectedButtonColor);
    $(".NISTbutton").blur();
});

$(".processbutton").click(function() {
    hideAll();
    $(".process").show();
    $(".processbutton").css("color", selectedButtonColor);
    $(".processbutton").blur();
});

function hideAll() {
    $(".NIST").hide();
    $(".process").hide();
    $(".technology").hide();
    $(".techbutton").css({"color": deSelectedButtonColor});
    $(".NISTbutton").css("color", deSelectedButtonColor);
    $(".processbutton").css("color", deSelectedButtonColor);
}