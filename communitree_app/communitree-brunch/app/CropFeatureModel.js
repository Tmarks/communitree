var Backbone = require("backbone");
//cropDisplayControl = require("CropDisplayControl");

var CropFeatureModel = Backbone.Model.extend({
    defaults: {
        geometry: null,
        id: -1,
        type: '',
        properties: {},
        recent_prunings: [],
        pruning_event: false,
        species: ''
    }
});

exports.CropFeatureModel = CropFeatureModel;
