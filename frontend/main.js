$(document).ready(function () {
    $("#MicBtn").click(function () {
        console.log("🎤 Mic button clicked");
        activateVoiceInput();
    });

    function doc_keyUp(e) {
        console.log('Key pressed: ${e.key}, Code: ${e.code}, Shift: ${e.shiftKey}');

        if (e.shiftKey && (e.key.toLowerCase() === 'e' || e.code === 'KeyE')) {
            console.log("✅ Shift + E detected - Activating voice input");
            eel.playAssistantSound();
            activateVoiceInput();
        }
    }

    function activateVoiceInput() {
        console.log("🚀 Activating Voice Input...");
        
        // Hide & Show elements correctly
        $("#SiriWave").hide(); // Ensure SiriWave is hidden
        $("#TextInput, .text").hide();
        $("#listening-container").fadeIn();
        $("#spoken-text").text("Listening...");

        eel.allCommands()().then((recognizedText) => {
            console.log(`📝 Recognized Text: ${recognizedText}`);
            $("#spoken-text").text(recognizedText).css("color", "yellow"); // Keep text in yellow for visibility

            setTimeout(() => {
                console.log("⌛ Hiding listening container & processing response...");
                $("#listening-container").fadeOut();
                
                $("#SiriWave").hide(); // Double-check SiriWave is hidden
                $(".status-text").text("Assistant is responding...");

                eel.speakResponse(recognizedText)().then(() => {
                    console.log("🔊 Response spoken, showing text input again.");
                    $("#speaking-container").fadeOut();
                    $("#TextInput, .text").fadeIn();
                    $("#snake-image").fadeIn();
                });
            }, 1000);
        });
    }

    document.addEventListener('keyup', doc_keyUp, false);
});