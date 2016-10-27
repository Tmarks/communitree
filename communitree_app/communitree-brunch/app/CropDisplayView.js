var Backbone = require("backbone");
var _ = require("underscore");
var $ = require("jquery");

var CropDisplayView = Backbone.View.extend({
    
    el: $('#interact'),
    
    template: _.template($("#cdvtmpl").html()),
    
    v: 0,

    render: function() {
        this.$el.html("it's sorta working" + this.v); this.v++;
        //this.$el.html(this.template({model: this.model}));
        //
    }
});

module.exports = CropDisplayView;
