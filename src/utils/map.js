import {createList} from "../modules/analytics.js"


async function getGeoJson(cc) {

  const res = await fetch(
    `https://country.api.shrk.xyz/api?country=${cc}`
  );
  // console.log(await typeof(res.text()))
  return await res.text();
}

async function draw(as) {
  var map = L.map("map", {
    minZoom: 1.6,
    maxZoom: 3,
    worldCopyJump: !0,
    inertia: !0,
  }).setView([30, 30], 1);
  map.createPane("labels");
  L.tileLayer(
    "https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}.png",
    { attribution: "&copy; OpenStreetMap" }
  ).addTo(map);
  map.getPane("labels").style.zIndex = 650;
  map.getPane("labels").style.pointerEvents = "none";
  const analyticsAsList = Object.entries(as);
  const listObject = []
  for (let i = 0; i < analyticsAsList.length; i++) {
    const jso = JSON.parse(await getGeoJson(analyticsAsList[i][0]));
    listObject.push([jso.properties.name, analyticsAsList[i][1]])
    var geojson = L.geoJson(
      jso.geometry,
      {
        style: {
          fillColor: "#" + Math.floor(Math.random() * 16777215).toString(16),
          weight: 0,
          opacity: 1,
          color: "white",
          fillOpacity: 0.7,
        },
      }
    ).addTo(map);
    geojson.eachLayer(function (layer) {
      layer.bindPopup(`<b>Country</b> - ${jso.properties.name} <br> <b>Clicks</b> - ${analyticsAsList[i][1]}`);
    });
  }
  createList(listObject)
  L.tileLayer(
    "https://{s}.basemaps.cartocdn.com/rastertiles/voyager_only_labels/{z}/{x}/{y}.png",
    { attribution: " ©CartoDB | shortCuts", pane: "labels" }
  ).addTo(map);
}
export { draw };
