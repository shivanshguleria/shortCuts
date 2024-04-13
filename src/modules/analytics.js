async function getGeoJson() {
  const res = await fetch('https://files.shivanshguleria.ml/src/json/alpha-2-cc.json');
  return await res.json();

}

async function draw(e){var t=L.map("map",{minZoom:1.6,maxZoom:3,worldCopyJump:!0,inertia:!0}).setView([30,30],1);t.createPane("labels"),L.tileLayer("https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}.png",{attribution:"&copy; OpenStreetMap"}).addTo(t),t.getPane("labels").style.zIndex=650,t.getPane("labels").style.pointerEvents="none";const a=Object.entries(e),o=await getGeoJson();for(let e=0;e<a.length;e++){L.geoJson(o.features[o.hashmaps.indexOf(a[e][0])].geometry,{style:{fillColor:"#"+Math.floor(16777215*Math.random()).toString(16),weight:0,opacity:1,color:"white",fillOpacity:.7}}).addTo(t).eachLayer((function(t){t.bindPopup(`<b>Country</b> - ${o.features[o.hashmaps.indexOf(a[e][0])].properties.name} <br> <b>Clicks</b> - ${a[e][1]}`)}))}L.tileLayer("https://{s}.basemaps.cartocdn.com/rastertiles/voyager_only_labels/{z}/{x}/{y}.png",{attribution:" ©CartoDB | shortCuts",pane:"labels"}).addTo(t)}export{draw};