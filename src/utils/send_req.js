import {remove_link_from_cache, getUniqueIds} from "./storage.js"

async function count(id) {
    const response = await fetch(`/api/count/${await token()}/${id}`);
    if(response.status < 300) {
    const count1 = await response.json();
    const res = count1
    return res
    } else {
        return -1
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

async function getGeoJson() {
    const res = await fetch('https://files.shivanshguleria.ml/src/json/alpha-2-cc.json');
    return await res.json();
  
  }
// async function send_link_gen_req() {

// }


async function sendPutreq(data) {
console.log(data)
    
    if (data.length == 0){
        return {status: 403, details: "Empty Request sent"}
    }
    else {
        console.log(data)
        const path = window.location.pathname.split('/')
        data.push(["token", path[path.length - 2]], ["unique_id", path[path.length - 1]])
        const url = new URL(window.location.protocol+ window.location.host + "/api/update/")
    const options = {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(Object.fromEntries(data))
    }
    const req = await fetch(url, options)

    if (req.status > 300) {
    return await {status: req.status, details: await req.json()}
    } 

    return await {status: req.status}
    }
}

export {token, count, delete_link, getAllCount, getGeoJson, sendPutreq}
