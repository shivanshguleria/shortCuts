import { count_routine } from "./storage.js";

const root = document.getElementById('link-container-root')
const ul = document.getElementById("link")

const searchFlexLink = document.getElementById("search-flex-link")
const generateEl = document.getElementById("result")

const copyBtn = document.getElementById("copy-button")


function copyFunction() {
copyBtn.addEventListener("click", function () {
    const storage = document.createElement('textarea');
    console.log(generateEl.textContent, generateEl.innerHTML)
    storage.value = generateEl.innerText;
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
  


  function renderUser(pointer = 1) {
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
    
        <span id="icon">
        <svg class="refresh" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M480-160q-134 0-227-93t-93-227q0-134 93-227t227-93q69 0 132 28.5T720-690v-110h80v280H520v-80h168q-32-56-87.5-88T480-720q-100 0-170 70t-70 170q0 100 70 170t170 70q77 0 139-44t87-116h84q-28 106-114 173t-196 67Z" fill="#ffffff"/></svg>
    <!--<span class="material-symbols-outlined edit icon-class">edit</span>
    <svg class="delete" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z" fill="#ffffff"/></svg>
  
    -->
    <button class="button">Analytics</button>
    </span>
  </div>
    `
  } 

  if (pointer) {
  count_routine()
  }
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