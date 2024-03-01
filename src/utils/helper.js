import { count_routine } from "./storage.js";

const root = document.getElementById('link-container-root')
const ul = document.getElementById("link")

const searchFlexLink = document.getElementById("search-flex-link")
const generateEl = document.getElementById("result")

const copyBtn = document.getElementById("copy-button")


function copyFunction() {
copyBtn.addEventListener("click", function () {
    const storage = document.createElement('textarea');
    storage.value = generateEl.innerHTML;
    searchFlexLink.appendChild(storage);
    storage.select();
    storage.setSelectionRange(0, 35);
    document.execCommand('copy');
    searchFlexLink.removeChild(storage);
    console.log("Copied ")
    })
}
  function get_date(option) {
    console.log("i Ran")
    const dateObj = new Date() 
    switch(option) {
      case "1":
        dateObj.setMinutes(dateObj.getMinutes() + 10)
        break;
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
  


  function renderUser() {
    let liString = ""
    if(localStorage.getItem(1) == null || localStorage.getItem(1) == '[]') {
      root.style.display = "none"
      liString = "No links here yet"
    } else {
      let links = JSON.parse(localStorage.getItem(1))
      for(let i =0; i < links.length; i++) {
    //     liString += `<div >
    // <p id="search-flex-link">Link - ${links[i]['link']}</p>
    // <p id="search-flex-link">Shortlink - ${links[i]['shortLink']}</p>
    // <p id="search-flex-link">Count- ${links[i]['clicks']}</p>
    // <div id="hr"></div>`
    liString += `
    <div id="link-container">
    
        <a href="/${links[i]['shortLink']}" target="_blank" id="links-short">${document.location.hostname+ "/"}<p  style="display: inline;">${links[i]['shortLink']}</p></a>
    
        <p>${links[i]['clicks']}</p>
    
    <div id="icon">
        <span class="material-symbols-outlined refresh icon-class">refresh</span>
        <!--<span class="material-symbols-outlined edit icon-class">edit</span>-->
        <span class="material-symbols-outlined delete icon-class">delete</span>
        </div>
  </div>
    `
  } 
  count_routine()
  // liString += '<button id="clear-cache">Clear Cache</button>'
  // const cache = document.getElementById('clear-cache')
  // cache.addEventListener('click', ()=> {
        
  //   localStorage.removeItem(1)
  //   alert("Local storage cleared")
  // })
  
  
  }
  ul.innerHTML = liString
  
  }

  export {renderUser, copyFunction, get_date}