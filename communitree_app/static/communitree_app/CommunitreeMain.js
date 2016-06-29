// Used to store the currently displayed crops so that we can get more info
// about them if a user clicks one.
var currentCropFeatures = new Map();

var map = L.map('map').on('load', getCrops);
map.setView([42.407956, -71.238515], 13);
map.on('moveend', getCrops);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'trianos.cigr0cuxo01y8thknjt8q30xd',
    accessToken: 'pk.eyJ1IjoidHJpYW5vcyIsImEiOiJjaWdyMGN3M3EwMXdyc3hrbjI4MHU5d21pIn0.uFMuGs921SdH6mzg6BtN1w'
}).addTo(map);

cropDisplayControl.addTo(map);

function onMapClick(e) {
  //alert("You clicked the map at " + e.latlng);
  var popup = L.popup();
  popup
    .setLatLng(e.latlng)
    .setContent("You clicked the map at " + e.latlng.toString())
    .openOn(map);
    cropDisplayControl.update();
}

map.on('click', onMapClick);

function getCrops() {
    var aj = $.ajax({
        url: "/communitree/querydb",
        data:
        {
            bounds: map.getBounds().toBBoxString()
        }
    })
    .done(function( json ) {
        // This will eventually contain the keys of CropFeatures no longer in view.
        // They will be subsequently deleted.
        // TODO: I might've been tired when I decided to add existing things I might not want to delete to a Set marking them for deletion, and removing the ones I want to keep later on. I think I should change how this works.
        cfKeysForDeletion = new Set(currentCropFeatures.keys());
        for (i = 0; i < json.cropfeatures.length; i++)
        {
            //L.geoJson(json.cropfeatures[i]).addTo(map);
            cf = new CropFeature(json.cropfeatures[i]);
            if (!currentCropFeatures.has(cf.pk))
            {
                currentCropFeatures.set(cf.pk, cf);
                cf.mapMe(map, cropDisplayControl);
            }
            else {
                // The CropFeature is already in the Map of current features displayed.
                // So remove it from our Set.
                // By the end of the loop, this will contain the PKs of CropFeatures
                // that were displayed and are now out of view.
                cfKeysForDeletion.delete(cf.pk)
            }
        }
        console.log("currentCropFeatures");
        console.log(currentCropFeatures);
        console.log("end currentCropFeatures");
        console.log("cfKeysForDeletion");
        console.log(cfKeysForDeletion);
        console.log("end cfKeysForDeletion");

        cfKeysForDeletion.forEach(function (val, a2, a3) {
            currentCropFeatures.get(val).unmapMe(map);
            currentCropFeatures.delete(val);
        })
    });
}
