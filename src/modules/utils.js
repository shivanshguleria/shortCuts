import {renderUser, token} from "./storage.js"

async function delete_link(id) {
    let val = await token()

    const payload = {
        unique_id: id,
        token: val
    }
    // console.log(payload)
    await fetch('/api/delete/', {
        method: "DELETE",
        body: JSON.stringify(payload),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
          }
    })
remove_link_from_cache(id)
}


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


// function edit_link(short_link) {
//     let a = JSON.parse(localStorage.getItem(1))
//     for(let i = 0; i < a.length; i++) {
//         if(a[i].shortLink == shortUrl) {
            
//             localStorage.setItem(1,JSON.stringify(a))
//         } 
//     }
// }

// async function edit_link_path(unique_id) {
//  try {
    
//     await fetch("/api/update", {
//         method: "PUT",
//         body: JSON.stringify(payload),
//         headers: {
//           "Content-type": "application/json; charset=UTF-8"
//         }
//       })
//  } catch  {
    
//  }
// }
export {delete_link} 
