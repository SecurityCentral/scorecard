selectedButtonColor = "blue"
deSelectedButtonColor = "black"

$(document).ready(function() {
    $("body").css("overflow", "auto");
    $(".peoplebutton").click();
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
    $(".processbutton").css("color", selectedButtonColor);
    $(".processbutton").blur();
});

$(".peoplebutton").click(function() {
    hideAll();
    $(".people").show();
    $(".peoplebutton").css("color", selectedButtonColor);
    $(".peoplebutton").blur();
});

function hideAll() {
    $(".NIST").hide();
    $(".people").hide();
    $(".technology").hide();
    $(".techbutton").css({"color": deSelectedButtonColor});
    $(".NISTbutton").css("color", deSelectedButtonColor);
    $(".processbutton").css("color", deSelectedButtonColor);
    $(".peoplebutton").css("color", deSelectedButtonColor);
}