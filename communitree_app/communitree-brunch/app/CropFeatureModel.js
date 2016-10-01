var Backbone = require("backbone");
//cropDisplayControl = require("CropDisplayControl");

var CropFeatureModel = Backbone.Model.extend({
    defaults: {
        geometry: null,
        id: -1,
        type: '',
        properties: {}
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

exports.CropFeatureModel = CropFeatureModel;
