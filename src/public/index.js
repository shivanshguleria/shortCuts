let passLink = document.getElementById('pass-link')
let passSubmit = document.getElementById('pass-submit')
let generateEl = document.getElementById('result')

// Initialize Variables
var closePopup = document.getElementById("popupclose");
var overlay = document.getElementById("overlay");
var popup = document.getElementById("wrapper");

// Close Popup Event
closePopup.onclick = function() {
  overlay.style.display = 'none';
  popup.style.display = 'none';
  generateEl.textContent = "Generating Link ..."
};
// Show Overlay and Popup


passSubmit.addEventListener("click",async function() {
    let inputValue = passLink.value
    if(inputValue === "") {
      alert("Enter Link")
    } else {
     
        overlay.style.display = 'block';
        popup.style.display = 'block';
      
      
    await fetch("/link", {
  method: "POST",
  body: JSON.stringify({
    link: inputValue
  }),
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
})
  .then((response) => response.json())
  .then((json) => {
    let data = json.message[0].short_link
    generateEl.textContent = "https://shrink.fly.dev/" + data
    console.log(data)
    
  });}
})