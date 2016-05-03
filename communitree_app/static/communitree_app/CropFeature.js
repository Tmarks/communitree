function CropFeature(cf_json) {
     this.cf_json = cf_json;
     this.pk = this.cf_json.properties.pk;
     this.name = this.cf_json.properties.name;
     this.species = this.cf_json.properties.species;
     this.geo = L.geoJson(this.cf_json);

     this.mapMe = function (leaflet_map) {
         this.geo.addTo(leaflet_map);
         return this;
     }

     this.unmapMe = function (leaflet_map) {
        leaflet_map.removeLayer(this.geo);
     }
}

CropFeature.constructor = CropFeature;