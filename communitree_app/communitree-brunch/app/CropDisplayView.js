var Backbone = require("backbone");
var _ = require("underscore");
var $ = require("jquery");

var CropDisplayView = Backbone.View.extend({
    
    el: $('#interact'),

    template: _.template("Hello <%= model.attributes.properties.name %>"),

    render: function() {
        console.log(this.el.innerHTML);
        console.log(this.model);
        this.$el.html(this.template({model: this.model}));
        return this;
    }
});

module.exports = CropDisplayView;
