var cropDisplayControl = L.control();

cropDisplayControl.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'crop-display-control');
        this.update();
        return this._div;
};

cropDisplayControl.update = function (cropProps) {
    this._div.innerHTML = "<h4>" + (cropProps ? cropProps.name : "Click a crop to know more about it.") + "</h4><br />" +
    "<br />" +
    "<p>Lorem ipsum dolor sit amet</p>";

};
