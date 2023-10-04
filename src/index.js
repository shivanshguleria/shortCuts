const passLink = document.getElementById('pass-link')
let passSubmit = document.getElementById('pass-submit')
let generateEl = document.getElementById('result')
let copyBtn = document.getElementById("copy-button")
let searchFlexLink = document.getElementById("search-flex-link")
// Initialize Variables
var closePopup = document.getElementById("popupclose");
var overlay = document.getElementById("overlay");
var popup = document.getElementById("wrapper");

// Close Popup Event

closePopup.onclick = function() {
  overlay.style.display = 'none';
  popup.style.display = 'none';
  generateEl.textContent = "Generating Link ...";
  passLink.value = "Paste your Long URL"
};

// Show Overlay and Popup
passLink.addEventListener("click", function() {
  passLink.value = ""
})

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
    let data = "https://shrink.fly.dev/" + json.message[0].short_link
    generateEl.textContent =  data
    console.log(data)
    copyBtn.addEventListener('click', function(){


      const storage = document.createElement('textarea');
      storage.value = generateEl.innerHTML;
      searchFlexLink.appendChild(storage);
      storage.select();
      storage.setSelectionRange(0, 35);
      document.execCommand('copy');
      searchFlexLink.removeChild(storage);
    
      
      
     console.log("Copied ")
    })
  });}
})