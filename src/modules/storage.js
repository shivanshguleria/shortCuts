async function count(shortUrl) {
    const response = await fetch(`/count/${shortUrl}`);
    const count1 = await response.json();
    console.log(count1)
    return count1
  }

function storage(link, shortLink) {
    let length = localStorage.length 
    localStorage.setItem(length = length + 1, JSON.stringify({link: link, shortLink: shortLink, key: length })) 
}

const ul = document.getElementById("main-user")

async function renderUser() {
  const createUl = document.createElement("ul")
  const localStorageLength = localStorage.length
  let liString = ""
  for(let i = 0; i < localStorageLength; i++) {
    let l = i + 1
    let linkInJson = JSON.parse(localStorage.getItem(l)) 
    liString += `<div id="liFlex">
    <p id="search-flex-link">Link - ${linkInJson['link']}</p>
                    <p id="search-flex-link">Shortlink - ${linkInJson['shortLink']}</p>
                    <p id="search-flex-link">Count- ${await count(linkInJson['shortLink'])}</p>
                    <div id="hr"></div>`
                  }
                  ul.innerHTML = liString
  }
  
renderUser()
export {storage}
  


