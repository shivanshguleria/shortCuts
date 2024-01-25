const sendPath = document.getElementById("path");
const renderLink = document.getElementById("route");
const textarea = document.getElementById("textarea");
const psudo = document.getElementById("psudo");
const psudo1 = document.getElementById("psudo1");
const psudo2 = document.getElementById("psudo2");
const submit = document.getElementById("submit");
const inputToken = document.getElementById("input-token")
const inputId = document.getElementById("input-id")

// import obj from "./index.json";
const path = window.location.origin
const obj = {
    "1": {
      "method": "GET",
      "path": "/api/token"
    },
    "2": {
      "method": "POST",
      "path": "/api/link"
    },
    "3": {
      "method": "GET",
      "path": "/api/count/{token}/{id}"
    },
    "4": {
      "method": "PUT",
      "path": "/api/update/"
    },
    "5": {
      "method": "DELETE",
      "path": "/api/delete/"
    }
  }
  
psudo.style.display = "none";
psudo1.style.display = "none";
psudo2.style.display = "none";
let pointer = 0;
sendPath.addEventListener("click", () => {
  let  sendPathInnerHtml = `<span id="method" style="color: #fee37d;">${
    obj[sendPath.value].method
  }</span><h2>${obj[sendPath.value].path}</h2>`
  if(localStorage.getItem(0)){
    sendPathInnerHtml += `<p style="font-size: 1.50em;" >Saved Token: ${localStorage.getItem(0)}</p>`
  }
  if(sendPath.value == 0) {
    psudo.style.display = "none";
} else if(sendPath.value == 3) {
      textarea.style.display = "none"
      psudo.style.display = "block";
      psudo2.style.display = "block"
  renderLink.innerHTML = sendPathInnerHtml

}
    else {
      textarea.style.display = "block"
      psudo2.style.display = "none"
  psudo.style.display = "block";
  renderLink.innerHTML = sendPathInnerHtml
}
  pointer = sendPath.value;
});

textarea.addEventListener("click", () => {
  console.log(typeof textarea.value);
});

submit.addEventListener("click", async () => {
  console.log(textarea.value, typeof textarea.value);
  if(sendPath.value == 0) {
    alert("Select Method")
} 
else if(sendPath.value == 1 && localStorage.getItem(0)) {
  alert("Token exists. Clear local storage for new token")
}

 else if(obj[pointer].method == 'GET' && sendPath.value == 3){
    
    console.log(inputId, inputToken)
    console.log("https://shrk.xyz" + "/api/count/" + inputToken.value + inputId.value)
        await fetch(path + "/api/count/" + inputToken.value + "/" + inputId.value, {
          method: obj[pointer].method
        })
          .then(async(response) =>  {
            let cat = await response.json()
            psudo1.style.display = "block";
            psudo1.innerHTML = `<pre id="route1"><code>${JSON.stringify(cat, undefined, 2)}</code><p class="fief">Status Code - ${JSON.stringify(response.status)}</p></pre>`;
          });


  } else if(obj[pointer].method == 'GET') {


    await fetch(path + obj[pointer].path, {
      method: obj[pointer].method
    })
      .then(async(response) => {
        let cat = await response.json()
        psudo1.style.display = "block";
        if(pointer == 1){
          localStorage.setItem(0, JSON.stringify(cat.token))
          console.log(cat)
        }
        psudo1.innerHTML = `<pre id="route1"><code>${JSON.stringify(cat, undefined, 2)}</code><p class="fief">Status Code - ${JSON.stringify(response.status)}</p></pre>`;
      });
  
    console.log(typeof( textarea.value));
  }
  else {
    await fetch(path + obj[pointer].path, {
    method: obj[pointer].method,
    body: textarea.value,
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    }
  })
    .then(async (response) =>  {
      let cat = await response.json()
      psudo1.style.display = "block";
      psudo1.innerHTML = `<pre id="route1"><code>${JSON.stringify(cat, undefined, 2)}</code><p class="fief">Status Code - ${JSON.stringify(response.status)}</p></pre>`;
    });

  console.log(typeof( textarea.value));
  }
  
});
