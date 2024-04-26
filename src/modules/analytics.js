import {draw} from "../utils/map.js"
import Toasts from "../utils/toasts.js";
//Create new element in domtree
const createDiv = document.createElement('div');
const createFormInputLink = document.createElement('input')
const createFormInputShortLink = document.createElement('input')
const createFormIsPreview = document.createElement('select')
const createFormInputSubmit = document.createElement('input')
const createFormClose = document.createElement('button')
const editLink = document.getElementById('edit-link');
const deleteLinkButton = document.getElementById('delete-link')
const toggleLink = document.getElementById("toggle-link")

const mapDiv = document.getElementById("map")
const insidediv = document.getElementById("inside-div")
const linkInfo = document.getElementById("link-info")

async function sendPutreq(data) {
    console.log(data)

    if (data.length == 0) {
        return {
            status: 403,
            details: "Empty Request sent"
        }
    } else {
        console.log(data)
        const path = window.location.pathname.split('/')
        data.push(["token", path[path.length - 2]], ["unique_id", path[path.length - 1]])
        const url = new URL(window.location.protocol + window.location.host + "/api/update/")
        const options = {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(Object.fromEntries(data))
        }
        const req = await fetch(url, options)

        if (req.status > 300) {
            return await {
                status: req.status,
                details: await req.json()
            }
        }

        return await {
            status: req.status
        }
    }
}

const toasts = new Toasts({
    width: 300,
    gap: 20,
    timing: 'ease',
    duration: '.5s',
    dimOld: true,
    position: 'top-right'// top-left | top-center | top-right | bottom-left | bottom-center | bottom-right
});

//Add toggle function
editLink.addEventListener("click", (e)=>{
    const optionObj = {
        1: {
            "": "Is Preview?",
            "true": "Yes",
            "false": "No [Default]"
        }
    }
    //Set Placehoders
    createFormInputLink.placeholder = "Paste New long link";
    createFormInputShortLink.placeholder = "Type new Short Code";

    //Create section
    for (let i = 0; i < Object.keys(optionObj[1]).length; i++) {
        const newOptionEl = document.createElement("option")
        if (i == 0) {
            newOptionEl.value = Object.keys(optionObj[1])[i]
            newOptionEl.text = Object.values(optionObj[1])[i]
            createFormIsPreview.add(newOptionEl)
        } else {
            newOptionEl.value = Object.keys(optionObj[1])[i]
            newOptionEl.text = Object.values(optionObj[1])[i]
            newOptionEl.classList.add("option")
            createFormIsPreview.add(newOptionEl)
        }
    }

    createFormInputSubmit.type = "submit"

    //Add classes to elements
    createFormIsPreview.classList.add("newSelectEl", "edit-div-input")
    createFormInputLink.classList.add("edit-div-input", "const-height")
    createFormInputShortLink.classList.add("edit-div-input", "const-height")
    createFormInputSubmit.classList.add("edit-div-input", "edit-input-submit", "hover")
    createFormClose.classList.add("edit-div-input", "hover")

    createFormClose.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="24" height="24" viewBox="0,0,256,256"><g fill="#ffffff" fill-rule="nonzero" stroke="none" stroke-width="1" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="10" stroke-dasharray="" stroke-dashoffset="0" font-family="none" font-weight="none" font-size="none" text-anchor="none" style="mix-blend-mode: normal"><g transform="scale(8.53333,8.53333)"><path d="M7,4c-0.25587,0 -0.51203,0.09747 -0.70703,0.29297l-2,2c-0.391,0.391 -0.391,1.02406 0,1.41406l7.29297,7.29297l-7.29297,7.29297c-0.391,0.391 -0.391,1.02406 0,1.41406l2,2c0.391,0.391 1.02406,0.391 1.41406,0l7.29297,-7.29297l7.29297,7.29297c0.39,0.391 1.02406,0.391 1.41406,0l2,-2c0.391,-0.391 0.391,-1.02406 0,-1.41406l-7.29297,-7.29297l7.29297,-7.29297c0.391,-0.39 0.391,-1.02406 0,-1.41406l-2,-2c-0.391,-0.391 -1.02406,-0.391 -1.41406,0l-7.29297,7.29297l-7.29297,-7.29297c-0.1955,-0.1955 -0.45116,-0.29297 -0.70703,-0.29297z"></path></g></g> </svg>'

    //Append element to creat div
    createDiv.append(createFormInputShortLink, createFormInputLink, createFormIsPreview, createFormInputSubmit, createFormClose)

    //Code for edit form

    createDiv.classList.add("edit-div")
    createDiv.style.display = "flex"
    insidediv.insertBefore(createDiv, mapDiv)
}
)

createFormClose.addEventListener('click', e=>{
    createDiv.style.display = 'none'
    createFormInputLink.value,
    createFormInputShortLink.value,
    createFormIsPreview.value = " ",
    " ",
    " "
    createDiv.remove(createFormInputShortLink, createFormInputLink, createFormIsPreview, createFormInputSubmit, createFormClose)
}
)

const path = window.location.pathname.split('/')

function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (err) {
        return false;
    }
}
createFormInputSubmit.addEventListener('click', async(e)=>{

    let entries = Object.entries({
        short_link: createFormInputShortLink.value,
        is_preview: createFormIsPreview.value,
        link: createFormInputLink.value
    })

    for (let i = 0; i < entries.length; i++) {
        if (entries[i][1] == '') {
            entries[i] = 0
        }
    }
    const newArr = []
    for (let i = 0; i < entries.length; i++) {
        if (entries[i] != 0) {
            newArr.push(entries[i])

        } else {
            continue
        }
    }

    const putRes = await sendPutreq(newArr)
    if (putRes.status > 299) {

        toasts.push({
            title: 'Error',
            content: JSON.stringify(putRes.details.detail),
            style: 'error',
            closeButton: true,
            dismissAfter: "3s",
            onOpen: toast=>{
                console.log(toast);
            }
            ,
            onClose: toast=>{
                console.log(toast);
            }
        });
    } else {

        createFormInputShortLink.value = ""
        createFormIsPreview.value = ""
        createFormInputLink.value = ""

        toasts.push({
            title: 'Updation Successfull',
            style: 'success',
            closeButton: true,
            dismissAfter: "3s",
            onOpen: toast=>{
                console.log(toast);
            }
            ,
            onClose: toast=>{
                console.log(toast);
            }
        });

    }
}
)

//Special count function 
async function count() {

    const response = await fetch(`/api/count/${path[path.length - 2] + "/" + path[path.length - 1]}`);
    if (response.status < 300) {
        const count1 = await response.json();
        const res = count1
        return res
    } else {
        return -1
    }
}

deleteLinkButton.addEventListener("click", async()=>{
    if (confirm("Delete link Confirmation")) {
        const del = await delete_link()

        if (del.status < 299) {
            toasts.push({
                title: 'Link Deletion Successfull',
                style: 'success',
                closeButton: true,
                dismissAfter: "3s",
                onOpen: toast=>{
                    console.log(toast);
                }
                ,
                onClose: toast=>{
                    console.log(toast);
                }
            });
        } else {
            toasts.push({
                title: `Error - ${del.status}`,
                content: JSON.stringify(del.details),
                style: 'error',
                closeButton: true,
                dismissAfter: "3s",
                onOpen: toast=>{
                    console.log(toast);
                }
                ,
                onClose: toast=>{
                    console.log(toast);
                }
            });
        }

    }
}
)
async function delete_link() {

    const payload = {
        unique_id: path[path.length - 1],
        token: path[path.length - 2]
    }
    const req = await fetch('/api/delete/', {
        method: "DELETE",
        body: JSON.stringify(payload),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    if (req.status < 299) {
        return {
            "status": req.status
        }
    } else {
        return {
            "status": req.status,
            "details": await req.json()
        }
    }
}

//send draw req

toggleLink.addEventListener("click", async(e)=>{
    const options = {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            unique_id: path[path.length - 1],
            token: path[path.length - 2]
        })
    }
    const req = await fetch('/api/toggle', options)

    if (req.status < 299) {
        if (toggleLink.getAttribute('value') == 1) {
            toggleLink.classList.remove("toggle-link-green")
            toggleLink.classList.add("toggle-link")
            toggleLink.textContent = "Disable Link"
            toggleLink.setAttribute('value', 0)

        } else {
            toggleLink.classList.remove("toggle-link")
            toggleLink.classList.add("toggle-link-green")
            toggleLink.textContent = "Enable Link"
            toggleLink.setAttribute('value', 1)
        }

        toasts.push({
            title: 'Link Toggled Successfully',
            style: 'success',
            closeButton: true,
            dismissAfter: "3s",
            onOpen: toast=>{
                console.log(toast);
            }
            ,
            onClose: toast=>{
                console.log(toast);
            }
        });
    } else {
        toasts.push({
            title: `Error - ${req.status}`,
            content: JSON.stringify(req.json().detail),
            style: 'error',
            closeButton: true,
            dismissAfter: "3s",
            onOpen: toast=>{
                console.log(toast);
            }
            ,
            onClose: toast=>{
                console.log(toast);
            }
        });
    }
}
)

function createList(listObj) {
    const newTable = document.createElement('table');
    const newH3 = document.createElement("h3")
    createDiv.classList.add("tab")
    newH3.textContent = "Traffic Countries/Regions"
    const newTableRow = document.createElement('tr')
    const newTableHeader1 = document.createElement('th')
    const newTableHeader2 = document.createElement('th')
    newTableHeader1.textContent = "Country/Region"
    newTableHeader2.textContent = "Traffic"
    newTableHeader1.classList.add("l")
    newTableHeader1.classList.add("same")
    newTableHeader2.classList.add("same")
    newTableHeader2.classList.add("r")
    newTableRow.append(newTableHeader1, newTableHeader2)
    newTable.append(newTableRow)
    for (let i = 0; i < listObj.length; i++) {
        const newTableRow = document.createElement('tr')
        const newTableData1 = document.createElement('td')
        const newTableData2 = document.createElement('td')
        newTableData1.textContent = listObj[i][0]
        newTableData1.classList.add("l")
        newTableData1.classList.add("same")
        newTableData2.classList.add("same")
        newTableData2.textContent = listObj[i][1]
        newTableData2.classList.add("r")
        newTableRow.append(newTableData1, newTableData2)
        newTable.append(newTableRow)
    }
    createDiv.append(newH3, newTable)
    insidediv.append(createDiv)
}
const countObj = await count()
linkInfo.innerHTML += `<p><strong>Total Count</strong>- ${countObj.count}</p>`
draw(countObj.analytics)

export {createList}
