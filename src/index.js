const passLink = document.getElementById('pass-link')
const passSubmit = document.getElementById('pass-submit')
const generateEl = document.getElementById('result')
const copyBtn = document.getElementById("copy-button")
const searchFlexLink = document.getElementById("search-flex-link")
const closePopup = document.getElementById("popupclose");
const overlay = document.getElementById("overlay");
const popup = document.getElementById("wrapper");

closePopup.onclick = function() {
  overlay.style.display = 'none';
  popup.style.display = 'none';
  generateEl.textContent = "Generating Link ...";
  passLink.value = ""
};

passSubmit.addEventListener("click",async function() {
    let inputValue = passLink.value
    if(inputValue === "") {
      alert("Enter Link")
    } else {
      overlay.style.display = 'block';
      popup.style.display = 'block';
      await fetch("/link/preview", {
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
        copyFunction()
      }) 
    }
})

function copyFunction() {
  copyBtn.addEventListener('click', function(){

  const storage = document.createElement('textarea');
  storage.value = generateEl.innerHTML;searchFlexLink.appendChild(storage);
  storage.select();
  storage.setSelectionRange(0, 35);
  document.execCommand('copy');
  searchFlexLink.removeChild(storage);
  console.log("Copied ")
  })
}