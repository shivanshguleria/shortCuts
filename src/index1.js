const passLink = document.getElementById('pass-link')
const passSubmit = document.getElementById('pass-submit')
const copyBtn = document.getElementById("copy-button")
const searchFlexLink = document.getElementById("search-flex-link")
const closePopup = document.getElementById("popupclose");
const overlay = document.getElementById("overlay");
const popup = document.getElementById("wrapper");
const customEl = document.getElementById("custom-link")
const popupContent1 = document.getElementById("popupcontent")
const inputElDiv = document.getElementById("inputElDiv")
const popupcontent_old = popupContent1.innerHTML
const generateEl = document.getElementById("result")

const newInputEl = document.createElement("input")
const newAnchorEl = document.createElement("a")
import  {storage}  from "./modules/storage.js"

closePopup.onclick = function() {
  overlay.style.display = 'none';
  popup.style.display = 'none';
  generateEl.textContent = "Generating Link ...";
  passLink.value = ""
  newInputEl.value = ""
  inputElDiv.innerHTML = ""
  popupContent1.innerHTML = popupcontent_old
  customEl.style.display = 'inline'
};

customEl.addEventListener("click", () => {
  customEl.style.display = 'none'
  
    inputElDiv.appendChild(newInputEl)
    inputElDiv.appendChild(newAnchorEl)
    newAnchorEl.setAttribute('type', "submit")
    newAnchorEl.innerText = "randomize?"
    newAnchorEl.classList.add("randomise")
    newInputEl.classList.add("newInputEl")
    newInputEl.placeholder = "Type Custom code"
})

newAnchorEl.addEventListener("click", () => {
  inputElDiv.removeChild(newInputEl)
  inputElDiv.removeChild(newAnchorEl)
  customEl.style.display = 'inline'
})



passSubmit.addEventListener("click",async function() {
  console.log("posted")
  let inputValue = passLink.value
  if(inputValue === "") {
    alert("Enter Link")
  } else if(isValidUrl(inputValue) === false) {
    alert("Enter Valid Url")
  } else {
    let payload = {
      link: inputValue, 
      is_preview: true
    }
  if(newInputEl.value != undefined & newInputEl.value != ""){
    payload['customLink'] = newInputEl.value
  }
    console.log(newInputEl.value)
    console.log(payload)
    overlay.style.display = 'block';
    popup.style.display = 'block';
    try {
      await fetch("/link", {
        method: "POST",
        body: JSON.stringify(payload),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
        .then((response) => response.json())
        
        .then((json) => {
          console.log(json.message)
          let data = "https://shrk.xyz/" + json.message.short_link
          console.log(generateEl.textContent, data)
          document.getElementById("result").textContent = data
          storage(inputValue, json.message.short_link)
          copyFunction()
         
        }) 
    } catch (error) {
      console.log(error)
      popupContent1.innerHTML = "<p style='margin: 10px;''>Custom Code Exists try something else!!</p>"
      
    }
  }
} )



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


function isValidUrl(uri) {
  try {
    if(uri === "test"){
      return true
    }
    const newUrl = new URL(uri);
    return true;
    
  } catch (err) {
    return false;
  }
}