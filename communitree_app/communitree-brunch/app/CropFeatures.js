Backbone = require("backbone");
CropFeature = require("CropFeature");

CropFeatures = Backbone.Collection.extend({
    url: '/crops',
    model: CropFeature,

    parse: function(data) {
        return data.cropfeatures;
    }
});

exports.CropFeatures = CropFeatures;
