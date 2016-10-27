var Backbone = require("backbone");
//cropDisplayControl = require("CropDisplayControl");

var CropFeatureModel = Backbone.Model.extend({
    defaults: {
        geometry: null,
        id: -1,
        type: '',
        properties: {},
    }
});

exports.CropFeatureModel = CropFeatureModel;
