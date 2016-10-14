module='communitree'

var CropFeatures = require('CropFeatures').CropFeatures;
var CropFeatureModel = require('CropFeatureModel').CropFeatureModel;
var L = require('leaflet');
var leaflet_draw = require('leaflet-draw');
var $ = require('jquery');
var _ = require('underscore');
var cropDisplayControl = require('CropDisplayControl');
var CropsInMapView = require('CropsInMapView');
var communitree_map = require('CommunitreeMap');


function init() {
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'trianos.cigr0cuxo01y8thknjt8q30xd',
        accessToken: 'pk.eyJ1IjoidHJpYW5vcyIsImEiOiJjaWdyMGN3M3EwMXdyc3hrbjI4MHU5d21pIn0.uFMuGs921SdH6mzg6BtN1w'
    }).addTo(communitree_map);

    //collectionInView is an instance of the CropFeatures collection. It holds cropfeatures currently in the view.
    //It's updated after every call of getCrops() by calling Collection.set(models).
    var collectionInView = new CropFeatures();
    collectionInView.on("add", function(m){console.log("Adding " + m.id); cropsInMapView.mapFeature(m);});
    collectionInView.on("remove", function(m){console.log("something got removed..." + m); cropsInMapView.unmapFeature(m)});
    //collectionInView.on("update", function(c){console.log("We am the update.");});

    var cropsInMapView = new CropsInMapView();

    function getCrops() {
        var aj = $.ajax({
            url: "/communitree/cropsbybounds",
            data:
            {
                bounds: communitree_map.getBounds().toBBoxString()
            }
        }).done(function( json ) {
            modelsInView = _.map(json, function(cf) { return new CropFeatureModel(cf); });
            console.log('modelsInView: ' + modelsInView);
            _.each(modelsInView, function(m) {
                                                 m.on("add", function(){console.log("modelInView added, " + this.id);})
                                             }
            );
            collectionInView.set(modelsInView);
        });
    }
    //communitree_map.on('load', getCrops);
    communitree_map.on('moveend', getCrops);

    cropDisplayControl.addTo(communitree_map);

    function onMapClick(e) {
        //var poppy = L.popup()
            //.setLatLng(e.latlng)
            //.setContent("You clicked the map at " + e.latlng)
            //.openOn(communitree_map);
        cropDisplayControl.update();
    }
    communitree_map.on('click', onMapClick);

    var drawnItems = new L.FeatureGroup();
    communitree_map.addLayer(drawnItems);
    var drawControl = new L.Control.Draw({
        edit: {
            featureGroup: drawnItems
        },
        draw: {
            polyline: false,
            marker: false
        }
    });
    //communitree_map.addControl(drawControl);

    communitree_map.setView([42.407956, -71.238515], 13);
};
exports.init = init;
