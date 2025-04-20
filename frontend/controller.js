// $(document).ready(function () {
//     eel.expose(DisplayMessage);
//     function DisplayMessage(message) {
//         $("#live-text").text(message);
//     }

//     eel.expose(DisplaySpokenText);
//     function DisplaySpokenText(text) {
//         $("#spoken-text").text(text);
//     }

//     eel.expose(HideListeningShowSiri);
//     function HideListeningShowSiri() {
//         $("#listening-container").fadeOut();
//         $("#speaking-container").fadeIn();
//         $("#live-text").text("Assistant is responding...");
//     }

// eel.expose(AssistantFinished);
// function AssistantFinished() {
//     console.log("✅ Assistant finished speaking. Resetting UI.");

//     $("#speaking-container").fadeOut(100, function () {
//         $("#listening-container").hide();  // ✅ Hide listening GIF
//         $("#TextInput, .text").fadeIn();   // ✅ Restore input box
//     });

//     $("#spoken-text").text("");  // ✅ Clear spoken text
//     $("#TextInput, .text").fadeIn(); 
// }
// eel.expose(HideListeningShowSiri);
// function HideListeningShowSiri() {
//     $("#listening-container").hide();
//     $("#speaking-container").hide();
//     $("#SiriWave").show();
// }

// // 📝 Display text on Siri screen (centered)
// eel.expose(DisplayOnSiriScreen);
// function DisplayOnSiriScreen(message) {
//     $("#SiriWave").show(); // Ensure Siri wave is visible
//     $("#siri-container").html(
//         `<p class="text-light siri-message" style="font-size: 28px;">${message}</p>`
//     );
// }

// // ✅ Optional: Reset screen after assistant finishes speaking
// eel.expose(AssistantFinished);
// function AssistantFinished() {
//     setTimeout(() => {
//         $("#SiriWave").hide();
//         $("#siri-container").html(""); // Clear the screen
//     }, 3000); // 3-second delay, adjust as needed
// }
// });
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

});