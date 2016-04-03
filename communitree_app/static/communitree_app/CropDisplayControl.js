var CropDisplayControl = L.Control.extend({
    onAdd : function (map) {
        var container = L.DomUtil.create('div', 'crop-display-control');
        container.innerHTML = "<h2>schween</h2>"
        return container;
    }
});
