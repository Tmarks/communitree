var cropDisplayControl = L.control();



cropDisplayControl.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'crop-display-control');


        this.drawPolyHandler = new L.Draw.Polygon(map);
        var dph = this.drawPolyHandler;
        console.log("it works fine here");
        this.addCropLink = L.DomUtil.create('a', null);
        $(this.addCropLink).click(function(e) {
            dph.enable();
        })
        this.update();

        map.on('draw:created', function (e) {
            var type = e.layerType,
                layer = e.layer;
            console.log(layer);

            // Do whatever else you need to. (save to db, add to map etc)
            map.addLayer(layer);
        });

        return this._div;
};

cropDisplayControl.update = function (cropProps) {
    this._div.innerHTML = "<h4>" + (cropProps ? cropProps.name : "Click a crop to know more about it.") + "</h4><br />" +
    "<br />";

    this.addCropLink.innerHTML = "Map out a new crop...";
    this._div.appendChild(this.addCropLink);

};
