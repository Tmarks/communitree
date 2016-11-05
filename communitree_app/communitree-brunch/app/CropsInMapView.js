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
        this.model.fetch({
                           success: function(model, response, options) {
                                        cropDisplayView.trigger("cropClick", model, true);
                                    }
                         });
        cropDisplayView.trigger("cropClick", this.model, false);
    },

    initialize: function() {
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
        

    /*
    //Everything is handled by the Leaflet event system here for now. I wanted 
    //Backbone and Leaflet to play together, but then suddenly I had everything 
    //working with just Leaflet.
    //I think it's very much worth revisiting later.
    render: function() {
        //console.log("call CropsInMapView.render");
    },
    */

    mapFeature: function(model) {
        this.mappedCropViews.set(model.id, new MappedCropView({ model: model }));
    },

    unmapFeature: function (model) {
        view = this.mappedCropViews.get(model.id);
        communitree_map.removeLayer(view.geoJson);
        this.mappedCropViews.delete(model.id);
    }
});

    
module.exports = CropsInMapView;
