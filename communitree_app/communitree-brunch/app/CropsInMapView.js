var Backbone = require('backbone');
var CropFeatureModel = require('CropFeatureModel').CropFeatureModel;
var L = require('leaflet');
var leaflet_draw = require('leaflet-draw');
var $ = require('jquery');
var _ = require('underscore');
var cropDisplayControl = require('CropDisplayControl');
var map = require('communitree').map;
console.log("oh");
console.log(map);

var cropClick = function (e) {
    layer=e.target;
    cf=layer.feature.properties;
    e.target.bindPopup(cf.name);
    cropDisplayControl.update(cf);
};

var CropsInMapView = Backbone.View.extend({

    initialize: function() {
        this.listenTo(

    render: function() {
         var geo = L.geoJson(this.model.attributes, {
             onEachFeature: function (feature, layer) {
                layer.on({ click: cropClick });
             }
         });
         console.log(map);
         geo.addTo(map);
    }

    mapFeature: function(cropFeature) {
        console.log("call mapFeature");
    }

    unmapFeature: function (cropFeature) {
        leaflet_map.removeLayer(this.geo);
    }
});

module.exports = CropsInMapView;
