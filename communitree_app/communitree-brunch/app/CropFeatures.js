var Backbone = require("backbone");
var CropFeatureModel = require("CropFeatureModel").CropFeatureModel;

var CropFeatures = Backbone.Collection.extend({
    url: 'communitree/crops',
    model: CropFeatureModel

});

exports.CropFeatures = CropFeatures;
