Backbone = require("backbone");
CropFeature = require("CropFeature").CropFeature;

CropFeatures = Backbone.Collection.extend({
    url: 'communitree/crops',
    model: CropFeature

});

exports.CropFeatures = CropFeatures;
