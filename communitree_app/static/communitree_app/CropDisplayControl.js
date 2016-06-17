var cropDisplayControl = L.control();

cropDisplayControl.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'crop-display-control');
        this.update();
        return this._div;
};

cropDisplayControl.update = function (cf) {
    this.container.innerHTML = "<h4>" + (cf ? cf.name : "click a crop to know more about it") + "</h4>";
};
