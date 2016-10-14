var Backbone = require("backbone");
var _ = require("underscore");
var $ = require("jquery");

var CropDisplayView = Backbone.View.extend({
    
    el: $('#interact'),

    template: _.template("<p>Hello <%= model.attributes.properties.name %></p>"),

    render: function() {
        this.$el.html(this.template({model: this.model}));
        return this;
    }
});

module.exports = CropDisplayView;
