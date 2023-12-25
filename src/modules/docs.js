const sendPath = document.getElementById("path");
const renderLink = document.getElementById("route");
const textarea = document.getElementById("textarea");
const psudo = document.getElementById("psudo");
const psudo1 = document.getElementById("psudo1");
const submit = document.getElementById("submit");
// import obj from "./index.json";

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
let pointer = 0;
sendPath.addEventListener("click", () => {
    if(sendPath.value == 0) {
        alert("Select Method")
    } else {
  psudo.style.display = "block";
  renderLink.innerHTML = `<span id="method" style="color: #fee37d;">${
    obj[sendPath.value].method
  }</span><h2>${obj[sendPath.value].path}</h2>`;
}
  pointer = sendPath.value;
});

textarea.addEventListener("click", () => {
  console.log(typeof textarea.value);
});

submit.addEventListener("click", async () => {
  console.log(textarea.value, typeof textarea.value);
  if( obj[pointer].method == 'GET'){

  await fetch("https://shrk.xyz" + obj[pointer].path, {
    method: obj[pointer].method
  })
    .then((response) => response.json())

    .then((json) => {
      psudo1.style.display = "block";
      psudo1.innerHTML = `<pre id="route1"><code>${JSON.stringify(json, undefined, 2)}</code></pre>`;
    });

  console.log(typeof( textarea.value));
  }
  else {
    await fetch("https://shrk.xyz" + obj[pointer].path, {
    method: obj[pointer].method,
    body: textarea.value,
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    }
  })
    .then((response) => response.json())

    .then((json) => {
      psudo1.style.display = "block";
      psudo1.innerHTML = `<pre id="route1"><code>${JSON.stringify(json, undefined, 2)}</code></pre>`;
    });

  console.log(typeof( textarea.value));
  }
  
});
