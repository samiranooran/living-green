// Accessibility
function speak(){
    voices = speechSynthesis.getVoices();
    speechSynthesis.speak(new SpeechSynthesisUtterance("Forgot password."));

    var inputs = document.querySelectorAll("input");

    inputs[0].onmousedown = function(){
        speechSynthesis.speak(new SpeechSynthesisUtterance("Please enter your email."));
    }
    inputs[1].onmousedown = function(){
        speechSynthesis.speak(new SpeechSynthesisUtterance("Submit your request."));
    }

}