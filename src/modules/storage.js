const root = document.getElementById('link-container-root')
const ul = document.getElementById("link")

async function count(shortUrl) {
  const response = await fetch(`/api/count/${await token()}/${shortUrl}`);
  const count1 = await response.json();
  return count1.count
}

function storage(link, shortLink) {
  if(localStorage.getItem(1) == null) {
    localStorage.setItem(1, JSON.stringify([{link: link, shortLink: shortLink, clicks: 0, isRefreshed: false }])) 
  } else  {
    let a = JSON.parse(localStorage.getItem(1))
    a.push({link: link, shortLink: shortLink, clicks: 0, isRefreshed: false })
    localStorage.setItem(1, JSON.stringify(a))
  }
}

function update_cache(object) {
  localStorage.setItem(2, JSON.stringify("true"))
  for(let i = 0 ; i < object.length; i++) {
    object[i]["isRefreshed"] = false
  }
  localStorage.setItem(1, JSON.stringify(object))
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
      <span class="material-symbols-outlined delete icon-class">delete</span>
      </div>
</div>
  `
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

async function count_routine(){
  let links = JSON.parse(localStorage.getItem(1))
  if(!JSON.parse(localStorage.getItem(2))){
update_cache(links)

  } 
  for(let j = 0; j < links.length; j++) {
    if(links[j].isRefreshed){
    links[j].isRefreshed = false
    }else {
      let updatedClicks =  await count(links[j]['shortLink'])
      links[j]['clicks'] = updatedClicks
    }
  }
  localStorage.setItem(1, JSON.stringify(links))
}


async function token() {
  if(!localStorage.getItem(3)) {
    await fetch("/api/token").then((response) => response.json())
    .then((json) => {
      localStorage.setItem(3, json.token)
      return json.token
    })}
    return localStorage.getItem(3)
  // }
}

export {token, storage, renderUser, count_routine, count}







      // <span class="material-symbols-outlined edit">edit</span>
      // <span class="material-symbols-outlined delete">delete</span>
