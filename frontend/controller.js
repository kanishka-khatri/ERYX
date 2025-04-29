$(document).ready(function () {
    eel.expose(DisplayMessage);
    function DisplayMessage(message) {
        $("#live-text").text(message);
    }

    eel.expose(DisplaySpokenText);
    function DisplaySpokenText(text) {
        $("#spoken-text").text(text);
    }

    eel.expose(HideListeningShowSiri);
    function HideListeningShowSiri() {
        $("#listening-container").fadeOut();
        $("#speaking-container").fadeIn();
        // $("#live-text").text("Assistant is responding...");
    }

eel.expose(AssistantFinished);
function AssistantFinished() {
    console.log("✅ Assistant finished speaking. Resetting UI.");

    $("#speaking-container").fadeOut(100, function () {
        $("#listening-container").hide();  // ✅ Hide listening GIF
        $("#TextInput, .text").fadeIn();   // ✅ Restore input box
    });

    $("#spoken-text").text("");  // ✅ Clear spoken text
}

eel.expose(ReturnToHomeScreen);
function ReturnToHomeScreen() {
    console.log("🏠 Returning to home screen UI...");

    $("#listening-container").fadeOut();
    $("#speaking-container").fadeOut();
    $("#SiriWave").hide();
    $("#spoken-text").text("");

    $("#TextInput, .text").fadeIn();
    $("#snake-image").fadeIn();
}

});