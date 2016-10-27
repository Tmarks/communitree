var Backbone = require("backbone");
var CropFeatureModel = require("CropFeatureModel").CropFeatureModel;

var CropFeatures = Backbone.Collection.extend({
    url: 'crops',
    model: CropFeatureModel

});

exports.CropFeatures = CropFeatures;
