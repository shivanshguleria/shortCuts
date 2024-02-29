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
const newSelectEl2 = document.createElement("select")
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
  while(newSelectEl2.firstChild) {
    newSelectEl2.removeChild(newSelectEl2.lastChild)
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

const deleteObj = {
  "0": "Schedule Link Delete",
  "1": "10 Minutes",
  "2": "1 Hour",
  "3": "1 Day",
  "4": "1 Month",
  "5": "1 year"
}

customEl.addEventListener("click", () => {
  customEl.style.display = 'none'
  
    inputElDiv.appendChild(newInputEl)
    newDivEl.appendChild(newSelectEl2)
    newDivEl.appendChild(newSelectEl)
    inputElDiv.appendChild(newDivEl)
    inputElDiv.appendChild(newAnchorEl)
    newAnchorEl.setAttribute('type', "submit")
    newAnchorEl.innerText = "randomize?"
    newAnchorEl.classList.add("randomise")
    newInputEl.classList.add("newInputEl")
    newSelectEl.classList.add("newSelectEl")
    newSelectEl2.classList.add("newSelectEl")
    newInputEl.placeholder = "Type Custom code"

    console.log(Object.keys(optionObject).length)

    
    for(let i = 0; i < Object.keys(deleteObj).length; i++) {
      const newOptionEl1 = document.createElement("option")
      if(i == 0) {
        newOptionEl1.value = Object.keys(deleteObj)[i]
        newOptionEl1.text =  Object.values(deleteObj)[i]
        newSelectEl2.add(newOptionEl1)
      } else {
      newOptionEl1.value = Object.keys(deleteObj)[i]
      newOptionEl1.text =  Object.values(deleteObj)[i]
      newOptionEl1.classList.add("option")
      newSelectEl2.add(newOptionEl1)
      }
    }
    
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
    console.log(newSelectEl.lastChild)
    newSelectEl.removeChild(newSelectEl.lastChild)
  }

  while(newSelectEl2.firstChild) {
    console.log(newSelectEl2.lastChild)
    newSelectEl2.removeChild(newSelectEl2.lastChild)
  }
 newDivEl.removeChild(newSelectEl)
 newDivEl.removeChild(newSelectEl2)
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
  if(newSelectEl2.value != "0") {
    payload['schedule_delete'] = get_date(newSelectEl2.value)
  } 

  console.log(newSelectEl2.value)
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

function get_date(option) {
  const dateObj = new Date() 
  switch(option) {
    case "1":
      dateObj.setMinutes(dateObj.getMinutes + 10)
    case "2":
      dateObj.setHours(dateObj.getHours() + 1)
      break;
    case "3":
      dateObj.setDate(dateObj.getDate() + 1)
      break;
    case "4":
      dateObj.setMonth(dateObj.getMonth() + 1)
      break;
      case "5":
      dateObj.setFullYear(dateObj.getFullYear() + 1)
  }

  return dateObj.toISOString()
}
