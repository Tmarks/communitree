Backbone = require("backbone");
//cropDisplayControl = require("CropDisplayControl");

CropFeature = Backbone.Model.extend({
    defaults: {
        cf_json: null,
        pk: -1,
        name: '',
        species: ''
    }
});



/*

function CropFeature(cf_json) {
     this.cf_json = cf_json;
     this.pk = this.cf_json.properties.pk;
     this.name = this.cf_json.properties.name;
     this.species = this.cf_json.properties.species;

     this.mapMe = function (leaflet_map, cropDisplayControl) {
         this.geo = L.geoJson(this.cf_json, {
             onEachFeature: function (feature, layer) {
                layer.on({ click: cropClick });
             }
         });
         this.geo.addTo(leaflet_map);
         this.geo.cropFeature = this;
         return this;
     }

     this.unmapMe = function (leaflet_map) {
        leaflet_map.removeLayer(this.geo);
     }
     console.log("made a cropfeature");
}

var cropClick = function (e) {
    layer=e.target;
    cf=layer.feature.properties;
    e.target.bindPopup(cf.name);
    cropDisplayControl.update(cf);
};

CropFeature.constructor = CropFeature;
*/

exports.CropFeature = CropFeature;
