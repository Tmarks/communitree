
function CropFeature(cf_json) {
     this.cf_json = cf_json;
     this.pk = this.cf_json.properties.pk;
     this.name = this.cf_json.properties.name;
     this.species = this.cf_json.properties.species;

     this.mapMe = function (leaflet_map, cropDisplayControl) {
         this.geo = L.geoJson(this.cf_json, {
             onEachFeature: function (feature, layer) {
                layer.on({
                          click: cropDisplayControl.update
                         })
             }
         });
         this.geo.addTo(leaflet_map);
         return this;
     }

     this.unmapMe = function (leaflet_map) {
        leaflet_map.removeLayer(this.geo);
     }
     console.log("made a cropfeature");
}

CropFeature.constructor = CropFeature;