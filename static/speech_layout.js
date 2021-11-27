
// Accessibility
function speak(){
    //onhover sound at navtop
     var inputs = document.querySelectorAll(".navtop a");
    for (var i = 0; i < inputs.length; i++) {
        console.log(inputs[i].innerText);
        inputs[i].onmouseenter = function(){
           
               voices = speechSynthesis.getVoices();
               speechSynthesis.speak(new SpeechSynthesisUtterance(this.innerText)); 
        }
    }

    //Page = "Home Page" | "Profile Page" | "Edit Page"
    var page = $('h2').text();
    voices = speechSynthesis.getVoices();
    if(page == "Home Page"){
        speechSynthesis.speak(new SpeechSynthesisUtterance($('#greeting').text(), ""));
        homePageDataVoice();
    }
    else{
    speechSynthesis.speak(new SpeechSynthesisUtterance(page));
    }
    if(page == "Profile Page"){
        var editButtion = document.querySelectorAll("a")[3];
        editButtion.onmouseenter = function(){
               voices = speechSynthesis.getVoices();
               speechSynthesis.speak(new SpeechSynthesisUtterance(editButtion.innerText));
           
        }
    }
  

    if(page == "Edit Profile"){
        var edit_inputs = document.querySelectorAll("input");
        for (var i = 0; i < edit_inputs.length; i++) {
            // Save Button
            if(i == 3){
                var saveButton =edit_inputs[i];
                saveButton.onmouseenter = function(){
                       voices = speechSynthesis.getVoices();
                       speechSynthesis.speak(new SpeechSynthesisUtterance(saveButton.value));
                   
                }
            }
            //update Text inputs [username, new password, email]
            else{
                edit_inputs[i].onmouseenter = function(){
                    voices = speechSynthesis.getVoices();
                    speechSynthesis.speak(new SpeechSynthesisUtterance(this.placeholder));
                }
            }
        }

        //updated! | ""
        if($('#updated').text() == "Updated!"){
           
            voices = speechSynthesis.getVoices();
            speechSynthesis.speak(new SpeechSynthesisUtterance("Account has been updated!"));
        }  
        
    }
   
}


function homePageDataVoice(){
        var tds = document.querySelectorAll('td');

        for (var i = 0; i < tds.length; i++) {
            console.log(tds[i].innerText);
            if(tds[i].innerText.toLowerCase().indexOf('email') === -1){
                tds[i].onmouseenter = function(){
                       voices = speechSynthesis.getVoices();
                       speechSynthesis.speak(new SpeechSynthesisUtterance(this.innerText)); 
                }

            }
        }
}