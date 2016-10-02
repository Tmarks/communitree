module='communitree'
var communitree_map;
function init() {
    var CropFeatures = require('CropFeatures').CropFeatures;
    var CropFeatureModel = require('CropFeatureModel').CropFeatureModel;
    var L = require('leaflet');
    var leaflet_draw = require('leaflet-draw');
    var $ = require('jquery');
    var _ = require('underscore');
    var cropDisplayControl = require('CropDisplayControl');
    var CropsInMapView = require('CropsInMapView');

    // Used to store the currently displayed crops so that we can get more info
    // about them if a user clicks one.
    var currentCropFeatures = new Map(); //this is a javascript key-value map, not a leaflet map. i was confused for
                                         //a second because i'm tired

    communitree_map = L.map('map').on('load', getCrops);
    communitree_map.setView([42.407956, -71.238515], 13);
    communitree_map.on('moveend', getCrops);


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



    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'trianos.cigr0cuxo01y8thknjt8q30xd',
        accessToken: 'pk.eyJ1IjoidHJpYW5vcyIsImEiOiJjaWdyMGN3M3EwMXdyc3hrbjI4MHU5d21pIn0.uFMuGs921SdH6mzg6BtN1w'
    }).addTo(communitree_map);

    cropDisplayControl.addTo(communitree_map);

    function onMapClick(e) {
        //var poppy = L.popup()
            //.setLatLng(e.latlng)
            //.setContent("You clicked the map at " + e.latlng)
            //.openOn(communitree_map);
        cropDisplayControl.update();
    }

    communitree_map.on('click', onMapClick);

    //collectionInView is an instance of the CropFeatures collection. It holds cropfeatures currently in the view.
    //It's updated after every call of getCrops() by calling Collection.set(models).
    var collectionInView = new CropFeatures();
    collectionInView.on("add", function(m){console.log("A model was added to collectionInView:" + m)});
    collectionInView.on("remove", function(m){console.log("something got removed..." + m);});
    /*collectionInView = new CropFeatures(null, {
        events: {
            "add": function() {
                       console.log("A model was added to collectionInView");
            }
        }
    });
    */

    function getCrops() {
        var aj = $.ajax({
            url: "/communitree/crops",
            data:
            {
                bounds: communitree_map.getBounds().toBBoxString()
            }
        })
        .done(function( json ) {
            modelsInView = _.map(json, function(cf) { return new CropFeatureModel(cf); });
            console.log(modelsInView);
            _.each(modelsInView, function(m) {
                                                 m.on("add", function(){new CropsInMapView({model: this}).render();console.log("This didn't work");})
                                                 m.on("remove", function(){console.log("i got removed...");});
                                             }
            );
            collectionInView.set(modelsInView);
        });
    }
};
exports.init = init;
exports.communitree_map = communitree_map;
