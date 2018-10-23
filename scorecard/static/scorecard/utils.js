selectedButtonColor = "blue"
deSelectedButtonColor = "black"

$(document).ready(function() {
    $("body").css("overflow", "auto");
    $(".procbutton").click();
});

$(".techbutton").click(function() {
    hideAll();
    $(".technology").show();
    $(".techbutton").css("color", selectedButtonColor);
    $(".techbutton").blur();
});

$(".compbutton").click(function() {
    hideAll();
    $(".compliance").show();
    $(".compbutton").css("color", selectedButtonColor);
    $(".compbutton").blur();
});

$(".procbutton").click(function() {
    hideAll();
    $(".process").show();
    $(".procbutton").css("color", selectedButtonColor);
    $(".procbutton").blur();
});

function hideAll() {
    $(".compliance").hide();
    $(".process").hide();
    $(".technology").hide();
    $(".techbutton").css({"color": deSelectedButtonColor});
    $(".compbutton").css("color", deSelectedButtonColor);
    $(".procbutton").css("color", deSelectedButtonColor);
}