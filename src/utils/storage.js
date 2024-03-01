import { count } from "./send_req.js"
import { renderUser } from "./helper.js"

function remove_link_from_cache(id) {
    let a = JSON.parse(localStorage.getItem(1))
    for(let i = 0; i < a.length; i++) {
        if(a[i].unique_id == id) {
            a.splice(i,1)
            localStorage.setItem(1,JSON.stringify(a))
        } 
    }
    setTimeout(renderUser(), 2000)
    // renderUser()

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
        let updatedClicks =  await count(links[j]['unique_id'])
        links[j]['clicks'] = updatedClicks
      }
    }
    localStorage.setItem(1, JSON.stringify(links))
  }




function storage(link, shortLink, unique_id) {
    if(localStorage.getItem(1) == null) {
      localStorage.setItem(1, JSON.stringify([{link: link, shortLink: shortLink, clicks: 0, isRefreshed: false, unique_id: unique_id }])) 
    } else  {
      let a = JSON.parse(localStorage.getItem(1))
      a.push({link: link, shortLink: shortLink, clicks: 0, isRefreshed: false, unique_id: unique_id })
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
  

function getUniqueId(short_link){
let a = JSON.parse(localStorage.getItem(1))
for(let i = 0 ; i < a.length; i++) {
if(a[i].shortLink == short_link) {
    return a[i].unique_id
    }
}
return false
}


export {storage, count_routine, getUniqueId, remove_link_from_cache}