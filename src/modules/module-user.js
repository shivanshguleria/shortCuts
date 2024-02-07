import { count_routine, renderUser, count } from "./storage.js";
import { delete_link} from "./utils.js";
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

function getUniqueId(short_link){
	let a = JSON.parse(localStorage.getItem(1))
	for(let i = 0 ; i < localStorage.length; i++) {
	if(a[i].shortLink == short_link) {
		return a[i].unique_id
		}
	}
	return false
}
element.addEventListener('click', async (e) => {
  if(e.target.classList.contains('refresh')) {
    console.log(e.target.parentNode.parentElement.childNodes[1].firstElementChild.innerText)
    const unique_id = getUniqueId(e.target.parentNode.parentElement.childNodes[1].firstElementChild.innerText)
    console.log(unique_id)
    const new_count = await count(unique_id)

    e.target.parentNode.parentElement.childNodes[3].textContent = new_count
    let a = JSON.parse(localStorage.getItem(1))
    for(let i = 0; i < a.length; i++) {
      if(a[i].shortLink === unique_id) {
        a[i].isRefreshed = true
        a[i].clicks = new_count
        localStorage.setItem(1,JSON.stringify(a))
      }
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
