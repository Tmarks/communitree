var CropDisplayControl = L.Control.extend({
    onAdd : function (map) {
        this.container = L.DomUtil.create('div', 'crop-display-control');
        this.update();
        return this.container;
    }
});

CropDisplayControl.update = function (cf) {
    this.container.innerHTML = "<h4>" + (cf ? cf.name : "click a crop to know more about it") + "</h4>";
}
