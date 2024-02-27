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
const newSelectEl = document.createElement("select")

const newDivEl = document.createElement("div")

import  {storage, token}  from "./modules/storage.js"



if(!localStorage.getItem("cacheFresh")){
  localStorage.setItem("cacheFresh", "true")
}
if(JSON.parse(localStorage.getItem("cacheFresh"))){
  window.location.reload()
  
  localStorage.setItem("cacheFresh", "false")
}
closePopup.onclick = function() {
  overlay.style.display = 'none';
  popup.style.display = 'none';
  generateEl.textContent = "Generating Link ...";
  passLink.value = ""
  newInputEl.value = ""
  inputElDiv.innerHTML = ""
  while(newSelectEl.firstChild) {
    newSelectEl.removeChild(newSelectEl.lastChild)
  }
 newDivEl.remove()
  popupContent1.innerHTML = popupcontent_old
  customEl.style.display = 'inline'
};

const optionObject = {
  "": "Is Preview?",
  "true": "Yes [Default]", 
  "false": "No"
}



customEl.addEventListener("click", () => {
  customEl.style.display = 'none'
  
    inputElDiv.appendChild(newInputEl)
    inputElDiv.appendChild(newDivEl)
    newDivEl.appendChild(newSelectEl)
    inputElDiv.appendChild(newAnchorEl)
    newAnchorEl.setAttribute('type', "submit")
    newAnchorEl.innerText = "randomize?"
    newAnchorEl.classList.add("randomise")
    newInputEl.classList.add("newInputEl")
    newSelectEl.classList.add("newSelectEl")
    newInputEl.placeholder = "Type Custom code"

    console.log(Object.keys(optionObject).length)

    
    for(let i = 0; i < Object.keys(optionObject).length; i++) {
      const newOptionEl = document.createElement("option")
      if(i == 0) {
        newOptionEl.value = Object.keys(optionObject)[i]
        newOptionEl.text =  Object.values(optionObject)[i]
        newSelectEl.add(newOptionEl)
      } else {
      newOptionEl.value = Object.keys(optionObject)[i]
      newOptionEl.text =  Object.values(optionObject)[i]
      newOptionEl.classList.add("option")
      newSelectEl.add(newOptionEl)
      }
    }

})

newAnchorEl.addEventListener("click", () => {
  inputElDiv.removeChild(newInputEl)
  inputElDiv.removeChild(newAnchorEl)
  
  while(newSelectEl.firstChild) {
    newSelectEl.removeChild(newSelectEl.lastChild)
  }
 newDivEl.removeChild(newSelectEl)
  // inputElDiv.removeChild(newSelectEl)
  customEl.style.display = 'inline'
})



passSubmit.addEventListener("click",async function() {

  let inputValue = passLink.value
  if(inputValue === "") {
    alert("Enter Link")
  } else {

    let payload = {
      link: inputValue, 
      is_preview: true,
      token: await token()
    }
  if(newSelectEl.value != "") {
    payload['is_preview'] = newSelectEl.value
    console.log(payload)
  }
  if(newInputEl.value != undefined & newInputEl.value != "" ){
    payload['short_link'] = newInputEl.value
  }
    overlay.style.display = 'block';
    popup.style.display = 'block';
    try {
      await fetch("/api/link", {
        method: "POST",
        body: JSON.stringify(payload),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
        .then((response) => response.json())
        
        .then((json) => {
          if(json.short_link){
          let data = "https://shrk.xyz/" + json.short_link
          document.getElementById("result").textContent = data
          storage(inputValue, json.short_link, json.unique_id)
          copyFunction()
        } else {
          popupContent1.innerHTML = "<p style='margin: 10px;''>Invalid Link!!</p>"
        }
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


