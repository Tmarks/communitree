var Backbone = require('backbone');
var CropFeatureModel = require('CropFeatureModel').CropFeatureModel;
var L = require('leaflet');
var leaflet_draw = require('leaflet-draw');
var $ = require('jquery');
var _ = require('underscore');
var cropDisplayControl = require('CropDisplayControl');
var communitree_map = require('CommunitreeMap');
console.log("CropsInMapView -- communitree_map: " + communitree_map);

var cropClick = function (e) {
    layer=e.target;
    cf=layer.feature.properties;
    e.target.bindPopup(cf.name);
    cropDisplayControl.update(cf);
};

var CropsInMapView = Backbone.View.extend({

    //initialize: function() {
    //    this.listenTo(

    render: function() {
        console.log("call CropsInMapView.render");
    },

    mapFeature: function(cropFeature) {
        console.log("call mapFeature");
        /*var geo = L.geoJson(this.model.attributes, {
            onEachFeature: function (feature, layer) {
               layer.on({ click: cropClick });
            }
        });
        geo.addTo(communitree_map);
        */
    },

    unmapFeature: function (cropFeature) {
        console.log("call mapFeature");
        //communitree_map.removeLayer(this.geo);
    }
});

module.exports = CropsInMapView;
