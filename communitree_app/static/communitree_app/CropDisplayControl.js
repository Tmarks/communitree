var CropDisplayControl = L.Control.extend({
    onAdd : function (map) {
        var container = L.DomUtil.create('div', 'crop-display-control');
        container.innerHTML = "<h2>schween</h2>"
        return container;
    }
});

CropDisplayControl.update = function (cf) {
    this.container.innerHTML = "<h4>" + cf.name + "</h4">
}
