var Backbone = require("backbone");
var _ = require("underscore");
var $ = require("jquery");

var CropDisplayView = Backbone.View.extend({
    
    el: $('#interact'),
    
    template: _.template($("#cdvtmpl").html()),
    
    initialize: function() {
        this.on("cropClick", this.cropClickEvent);
    },
    
    cropClickEvent: function(newModel, ready) {
        this.model = newModel;
        this.render(ready);
    },
    
    render: function(ready) {
        this.$el.html(this.template({data: {crop: this.model, ready: ready}}));
        //
    },

    /*
    events: {
        "cropClick" : "render"
    }
    */

    
});

module.exports = CropDisplayView;
