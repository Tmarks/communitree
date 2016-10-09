var Backbone = require('backbone');
var CropFeatureModel = require('CropFeatureModel').CropFeatureModel;
var L = require('leaflet');
var leaflet_draw = require('leaflet-draw');
var $ = require('jquery');
var _ = require('underscore');
var cropDisplayControl = require('CropDisplayControl');
var communitree_map = require('CommunitreeMap');
var CropDisplayView = require("CropDisplayView");

var cropDisplayView = new CropDisplayView();


var MappedCropView = Backbone.View.extend({
    cropClick: function (e) {
        layer=e.target;
        cf=layer.feature.properties;
        cropDisplayControl.update(cf);

        cropDisplayView.model = this.model;
        cropDisplayView.render();

        
    },

    initialize: function() {
        var myCropClick = this.cropClick;
        var thisView=this;
        this.geoJson = L.geoJson(this.model.attributes, {
            onEachFeature: function (feature, layer) {
               layer.on("click", thisView.cropClick, thisView);
            }
        });
        this.geoJson.addTo(communitree_map);
    }
});


var CropsInMapView = Backbone.View.extend({

    initialize: function() {
        //Key: crop feature ID. Value: corresponding MappedCropView.
        this.mappedCropViews = new Map();
    },
        

    render: function() {
        console.log("call CropsInMapView.render");
    },

    mapFeature: function(model) {
        console.log("call mapFeature");
        this.mappedCropViews.set(model.id, new MappedCropView({ model: model }));
    },

    unmapFeature: function (model) {
        console.log("call unmapFeature");
        view = this.mappedCropViews.get(model.id);
        communitree_map.removeLayer(view.geoJson);
        this.mappedCropViews.delete(model.id);
    }
});

    
module.exports = CropsInMapView;
