function CropFeature(cf_json) {
     this.cf_json = JSON.parse(cf_json).cropfeature
     console.log(typeof(this.cf_json))
     console.log(this.cf_json)
     this.name = this.cf_json.name
     console.log(this.name)
     this.species = this.cf_json.species
     console.log(this.species)
     console.log(this.cf_json.mpoly)
     console.log(typeof(this.cf_json.mpoly))
     this.geo = L.geoJson(this.cf_json.mpoly)

     this.map_me = function (leaflet_map) {
         this.geo.addTo(leaflet_map)
     }
}

CropFeature.constructor = CropFeature;