var language = "en";
$(document).ready(function() {
    if ($(".ajax-form").length) {
        $(".ajax-form").submit(function(event) {
            var form = $(this);
            var url = form.attr('action');
            $.ajax({
                type: "POST",
                url: url,
                data: form.serialize(),
                success: function(data) {
                    if (data == "Success") {
                        window.location.href = "home";
                    } else {
                        $(".msg").text(data);
                    }
                }
            });
            event.preventDefault();
        });
    }

    // Accessbility 
    // in case of bilingual switch
    language = $('#ln').text(); // 'en' / 'fr'
});


function startSpeechSynthesis(){

    //sessionStorage.setItem("isSpeechOn", true);
    
         
    var inputs = document.querySelectorAll('input');
    
    if(inputs[3].id == "email"){
        //current page is register
        if (language == "en") {
            voices = speechSynthesis.getVoices();
        speechSynthesis.speak(new SpeechSynthesisUtterance("Welcome to the register page."));
        } else {
            voices = speechSynthesis.getVoices();
            speechSynthesis.speak(new SpeechSynthesisUtterance("Bienvenue sur la page d'inscription."));
        }
        inputs[0].onmousedown = function(){
            voices = speechSynthesis.getVoices();
            if (language == "en") {
                speechSynthesis.speak(new SpeechSynthesisUtterance("Please fill out the User Name."));
            } else {
                speechSynthesis.speak(new SpeechSynthesisUtterance("Veuillez remplir le nom d'utilisateur."));
            }

        }
        inputs[1].onmousedown = function(){
            voices = speechSynthesis.getVoices();
            if (language == "en") {
                speechSynthesis.speak(new SpeechSynthesisUtterance("Please fill out the Password."));
            } else { 
                speechSynthesis.speak(new SpeechSynthesisUtterance("Veuillez remplir le mot de passe."));
            }
        }
        inputs[2].onmousedown = function(){
            voices = speechSynthesis.getVoices();
            if (language == "en") {
                speechSynthesis.speak(new SpeechSynthesisUtterance("Please confirm the password."));
            } else {
                speechSynthesis.speak(new SpeechSynthesisUtterance("Veuillez confirmer le mot de passe."));
            }
        }
        inputs[3].onmousedown = function(){
            voices = speechSynthesis.getVoices();
            if (language == "en") {
                speechSynthesis.speak(new SpeechSynthesisUtterance("Please fill out the email."));
            } else {
                speechSynthesis.speak(new SpeechSynthesisUtterance("Veuillez remplir l'e-mail."));
            }
        }
        inputs[4].onmousedown = function(){
            voices = speechSynthesis.getVoices();
            if (language == "en") {
                speechSynthesis.speak(new SpeechSynthesisUtterance("Submit the register form."));
            } else {
                speechSynthesis.speak(new SpeechSynthesisUtterance("Envoyez le formulaire d'inscription."));
            }
        }
    }
    else{
        //current page is login
        voices = speechSynthesis.getVoices();
        if (language == "en") {
            speechSynthesis.speak(new SpeechSynthesisUtterance("Welcome to the login page."));
        } else {
            speechSynthesis.speak(new SpeechSynthesisUtterance("Bienvenue sur la page de connexion."));
        }

        inputs[0].onmousedown = function(){
            voices = speechSynthesis.getVoices();
            if (language == "en") {
                speechSynthesis.speak(new SpeechSynthesisUtterance("Please fill out the User Name."));
            } else {
                speechSynthesis.speak(new SpeechSynthesisUtterance("Veuillez remplir le nom d'utilisateur."));
            }
        }
        inputs[1].onmousedown = function(){
            voices = speechSynthesis.getVoices();
            if (language == "en") {
                speechSynthesis.speak(new SpeechSynthesisUtterance("Please fill out the Password."));
            } else {
                speechSynthesis.speak(new SpeechSynthesisUtterance("Veuillez remplir le mot de passe."));
            }
        }
        inputs[2].parentNode.onmousedown = function(){
            voices = speechSynthesis.getVoices();
            if (language == "en") {
                speechSynthesis.speak(new SpeechSynthesisUtterance("Remember me."));
            } else {
                
                speechSynthesis.speak(new SpeechSynthesisUtterance("Souviens-toi de moi."));
            }
        }
       
        inputs[4].onmousedown = function(){
            voices = speechSynthesis.getVoices();
            if (language == "en") {
                speechSynthesis.speak(new SpeechSynthesisUtterance("Click to Login to the system."));
            } else {
                speechSynthesis.speak(new SpeechSynthesisUtterance("Cliquez pour vous connecter au système."));
            }
        }
    }

}





