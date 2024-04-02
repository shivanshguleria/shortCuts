import { renderUser } from "../utils/helper.js"
import { count, delete_link } from "../utils/send_req.js"
import { getUniqueId , remove_link_from_cache} from "../utils/storage.js"

renderUser()

const cache = document.getElementById('clear-cache')

if(cache != null) {

    cache.addEventListener('click', ()=> {
          
      localStorage.removeItem(1)
      alert("Local storage cleared")
      renderUser()
    })
}


let element = document.getElementById('link');

element.addEventListener('click', async (e) => {
  if(e.target.classList.contains('refresh')) {
    console.log(e.target.parentNode.parentElement.childNodes[1].firstElementChild.innerText)
    const unique_id = getUniqueId(e.target.parentNode.parentElement.childNodes[1].firstElementChild.innerText)

    const new_count = await count(unique_id)
    if (new_count != -1) {
    e.target.parentNode.parentElement.childNodes[3].textContent = new_count.count
    let a = JSON.parse(localStorage.getItem(1))
    for(let i = 0; i < a.length; i++) {
      if(a[i].unique_id === unique_id) {
        a[i].isRefreshed = true
        a[i].clicks = new_count.count
        a[i].analytics = new_count.analytics
        if(a[i].analytics){
        a[i].analytics = new_count.analytics 
      }
        localStorage.setItem(1,JSON.stringify(a))
      }
    }
  } else {
    alert("Link has been deleted, refreshing cache")
remove_link_from_cache(unique_id)
  }
}
  // if(e.target.classList.contains('edit')) {
  //   console.log(`some event content here on edit`);
  // }
  if(e.target.classList.contains('delete')) {
    try {
      console.log(e.target)
      let short_link = e.target.parentNode.parentElement.childNodes[1].firstElementChild.innerText
      delete_link(getUniqueId(short_link))
      // renderUser()

    } catch (error) {
      console.log(error)
    }
  }

  // if(e.target.classList.contains('edit')) {
  //   try {
  //     let short_link = e.target.parentNode.parentElement.childNodes[1].firstElementChild.innerText
  //     edit_link(short_link) 
  //   }
  // }
});

