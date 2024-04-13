import { getGeoJson } from "./send_req.js";
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
  const jso = await getGeoJson();
  for (let i = 0; i < analyticsAsList.length; i++) {
    var geojson = L.geoJson(
      jso.features[jso.hashmaps.indexOf(analyticsAsList[i][0])].geometry,
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
      layer.bindPopup(`<b>Country</b> - ${jso.features[jso.hashmaps.indexOf(analyticsAsList[i][0])].properties.name} <br> <b>Clicks</b> - ${analyticsAsList[i][1]}`);
    });
  }
  L.tileLayer(
    "https://{s}.basemaps.cartocdn.com/rastertiles/voyager_only_labels/{z}/{x}/{y}.png",
    { attribution: " ©CartoDB | shortCuts", pane: "labels" }
  ).addTo(map);
}
export { draw };
