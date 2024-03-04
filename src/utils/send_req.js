import {remove_link_from_cache, getUniqueIds} from "./storage.js"

async function count(id) {
    const response = await fetch(`/api/count/${await token()}/${id}`);
    const count1 = await response.json();
    const res = count1.count
    if(res == 0 | res) {
        return res
    }
  }

async function getAllCount() {
    var data
    let payload = {
        "links": getUniqueIds()
    }
    await fetch(`/api/count/all/${await token()}`, {
        method: "POST",
        body: JSON.stringify(payload),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
        .then((response) => response.json())
        
        .then((json) => {
            data = json
        })

        return data
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


// async function send_link_gen_req() {

// }

export {token, count, delete_link, getAllCount}