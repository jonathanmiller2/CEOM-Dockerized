var map, select;
var gal_num = 12;
var selectedFeature = null;
function init(){

    //OpenLayers.Layer.Vector.prototype.renderers = ["SVG2", "VML", "Canvas"];

    var options = {
        projection: new OpenLayers.Projection("EPSG:3857"),
        displayProjection: new OpenLayers.Projection("EPSG:4326"),
        units: "m",
        maxResolution: 156543.0339,
        maxExtent: new OpenLayers.Bounds(-20037508.34, -20037508.34,
                                            20037508.34, 20037508.34),
        controls: [
            new OpenLayers.Control.Navigation(),
            new OpenLayers.Control.PanZoomBar(),
            new OpenLayers.Control.LayerSwitcher({'ascending':false}),
            //new OpenLayers.Control.Permalink(),
            //new OpenLayers.Control.ScaleLine(),
            //new OpenLayers.Control.Permalink('permalink'),
            new OpenLayers.Control.MousePosition(),
            //new OpenLayers.Control.OverviewMap(),
            new OpenLayers.Control.KeyboardDefaults()
        ],
        layers: [
            new OpenLayers.Layer.Google(
                "Google Hybrid",
                {type: google.maps.MapTypeId.HYBRID, numZoomLevels: 20}
            ),
            new OpenLayers.Layer.Google(
                "Google Satellite",
                {type: google.maps.MapTypeId.SATELLITE, numZoomLevels: 22}
            ),
            new OpenLayers.Layer.Google(
                "Google Physical",
                {type: google.maps.MapTypeId.TERRAIN}
            ),
            new OpenLayers.Layer.Google(
                "Google Streets", // the default
                {numZoomLevels: 20}
            )    
        ]
        // numZoomLevels: 6
    };

    map = new OpenLayers.Map( 'map', options );


    var style = new OpenLayers.Style({
        //label: "${name}",
        pointRadius: "${radius}",
        fillColor: "${color}",
        fillOpacity: 0.8,
        strokeColor: "${stroke}",
        strokeWidth: "${width}",
        strokeOpacity: 1
        }, {
        context: {
            color: function(feature) {
                var count = parseInt(feature.attributes.count.value, 10);
                if (count > gal_num)
                    return "#ffcc66";
                else if (count > 1)
                    return "#cc6633";
                else
                    return "#ff7777";

            },
            stroke: function(feature) {
                var count = parseInt(feature.attributes.count.value, 10);
                if (count > gal_num)
                    return "#cc6633";
                else if (count > 1)
                    return "#ff6622";
                else
                    return "#ff0000";
            },
            width: function(feature) {
                var count = parseInt(feature.attributes.count.value, 10);
                return (count > 1) ? 2 : 1;
            },
            radius: function(feature) {
                var count = parseInt(feature.attributes.count.value, 10);

                var pix = 4;
                    //pix = Math.min(feature.attributes.count, 6) + 2;
                    //pix = Math.max(Math.pow(feature.attributes.count,0.4), 3);
                pix = Math.max(Math.pow(count/3,0.4), 4);
                return pix;
            }
        }
    });

    var strategy = new OpenLayers.Strategy.Cluster({distance: 17, threshold: 3});

    var clusters = new OpenLayers.Layer.Vector("Clusters", {
        projection: new OpenLayers.Projection("EPSG:4326"),
        strategies: [
            new OpenLayers.Strategy.BBOX({resFactor: 1.1})
            //new OpenLayers.Strategy.Fixed(),
            //strategy
        ],
        protocol: new OpenLayers.Protocol.HTTP({
            url: "/photos/clusters.kml",
            format: new OpenLayers.Format.KML({
                //extractStyles: true,
                extractAttributes: true
            }),
            callback:erasePopUps
        }),
        styleMap: new OpenLayers.StyleMap({
            "default": style,
            "select": {
                fillColor: "#8aeeef",
                strokeColor: "#32a8a9"
            }
        })
    });

    clusters.events.on({
        "featureselected": onFeatureSelect,
        "featureunselected": onFeatureUnselect,
    });
    clusters.events.register("loadstart",clusters,function(){   
        erasePopUps();
        $("#gallery").empty();
        document.getElementById("total").innerHTML = "<h4 style=\"float:left\"> Loading</h4> <i class='icon-spinner icon-2x icon-spin icon-large'></i>";
    });
    clusters.events.register("loadend",clusters,function(){
        
        var count = 0;
        for (var i = 0; i < this.protocol.format.features.length; i++){
            count += parseInt(this.protocol.format.features[i].attributes.description, 10);
        }
        document.getElementById("total").innerHTML = "<h4 style=\"float:left\">"+count+" photos </h4>";
    });

    select = new OpenLayers.Control.SelectFeature(clusters);
    map.addControl(select);
    select.activate();

    map.addLayers([clusters]);

    if (init_bbox && init_bbox.length == 4){
        zoomToBBOX(init_bbox);
    }else{
        map.setCenter(new OpenLayers.LonLat(-1.0, 1.0).transform(
            "EPSG:4326",
            map.getProjectionObject()
        ), 3);
        // setTimeout( map.setCenter(new OpenLayers.LonLat(lon, lat).transform(map.displayProjection, map.projection), zoom), 200 );
        // map.setCenter(new OpenLayers.LonLat(lon, lat).transform(map.displayProjection, map.projection), zoom);
    }

    map.addControl(new OpenLayers.Control.LayerSwitcher());
    map.addControl(new OpenLayers.Control.MousePosition());

    // map.setBaseLayer(google);
    // map.setCenter(new OpenLayers.LonLat(0.0, 0.0), 5);
}
function erasePopUps(){
    var feature = selectedFeature;
    if(feature!= null && feature.popup) {
        map.removePopup(feature.popup);
        feature.popup.destroy();
        delete feature.popup;
    }
    else if(feature!= null && feature.cluster){
        if(feature.attributes.count == 1){
            feature = feature.cluster[0];
            if(feature.popup) {
                map.removePopup(feature.popup);
                feature.popup.destroy();
                delete feature.popup;
            }
        }
    }
}
function zoomToBBOX(bbox){
    var x1 = bbox[0],
        y1 = bbox[1],
        x2 = bbox[2],
        y2 = bbox[3];

    var bounds = new OpenLayers.Bounds();
    bounds.extend(new OpenLayers.LonLat(x1, y1).transform(map.displayProjection, map.projection));
    bounds.extend(new OpenLayers.LonLat(x2, y2).transform(map.displayProjection, map.projection));
    map.zoomToExtent(bounds);
}
function transformCoords(bbox){
    var x1 = bbox[0],
        y1 = bbox[1],
        x2 = bbox[2],
        y2 = bbox[3];

    var bounds = new OpenLayers.Bounds();
    bounds.extend(new OpenLayers.LonLat(x1, y1).transform(map.displayProjection, map.projection));
    bounds.extend(new OpenLayers.LonLat(x2, y2).transform(map.displayProjection, map.projection));
    return bounds
}
function onPopupClose(evt) {
    select.unselectAll();
}

//A certain feature was clicked
function onFeatureSelect(event) {

    var feature = event.feature;
    var count = parseInt(feature.attributes.description, 10);
    if(count >= 1){
        var text;

         if (!map.isValidZoomLevel(map.zoom + 1)){ 
            displayGallery(feature,1,24);
            text ="<h2>Cluster<\/h2> <p>Maximum zoom level reached.<br/>"+
                  "<a href='#gallery'>View "+count+" contained features below</a>.";
         }else{
            text = "<h2>Cluster<\/h2> <p>Zoom in to see " +count+" features.";
            text += "<br/><a href='#gallery'>Or view the features below</a>.";
            displayGallery(feature,1,24);
            
        } 

        var popup = new OpenLayers.Popup.FramedCloud("chicken",
            feature.geometry.getBounds().getCenterLonLat(),
            new OpenLayers.Size(100,100),
            text,
            null,
            true,
            onPopupClose
        );
        //The following line is necesary to solve the bug where popup will not close
        feature.popup = popup;
        selectedFeature = feature;
        select.handlers.feature.lastFeature = selectedFeature;
        
        map.addPopup(popup);
    } 
/*     else{
        displayPopup(feature);
        selectedFeature = feature;
        select.handlers.feature.lastFeature = selectedFeature;
    } */
}

function onFeatureUnselect(event) {
    erasePopUps();
}

function getFeatureLoc(feature){
    var ll = feature.geometry.getBounds().getCenterLonLat();
    ll.transform(new OpenLayers.Projection("EPSG:3857"), new OpenLayers.Projection("EPSG:4326"));
    var geo = {"lat": ll.lat, "lon": ll.lon};
    ll.transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:3857"));
    return geo;
}

function osm_getTileURL(bounds) {
    var res = this.map.getResolution();
    var x = Math.round((bounds.left - this.maxExtent.left) / (res * this.tileSize.w));
    var y = Math.round((this.maxExtent.top - bounds.top) / (res * this.tileSize.h));
    var z = this.map.getZoom();
    var limit = Math.pow(2, z);

    if (y < 0 || y >= limit) {
        return OpenLayers.Util.getImagesLocation() + "404.png";
    } else {
        x = ((x % limit) + limit) % limit;
        return this.url + z + "/" + x + "/" + y + "." + this.type;
    }
}

function displayPopup(feature){
 $.getJSON("/photos/photos.json", {ids:feature.attributes.ids.value}, function(data){
        var popup = new OpenLayers.Popup.FramedCloud("featurePopup",
            feature.geometry.getBounds().getCenterLonLat(),
            new OpenLayers.Size(300,100),
            "<h2>"+data[0].name + "<\/h2>" +
            "<div class='description'>"+ data[0].description +
            "<a class='btn btn-small' href='#' onclick='timeSeries("+data[0].lon+","+data[0].lat+"); return false;'>MODIS</a>"+
            "</div>",
            null,
            true,
            onPopupClose
        );
        //popup.autoSize = true;
        //popup.panMapIfOutOfView = true;
        //popup.updateSize();
        //alert(popup.getSafeContentSize());
        feature.popup = popup;
        popup.feature = feature;
        map.addPopup(popup);
    });
}

function displayGallery(feature,desired_page,desired_ppp){
    $("#gallery").html("<div class=\"span12 text-center\"><i class='icon-spinner icon-2x icon-spin icon-large'></i></div>").fadeIn();
    $.get("/photos/photos.html", {ids:feature.attributes.ids.value,x_size:feature.attributes.x_size.value,y_size:feature.attributes.y_size.value,page:desired_page,ppp:desired_ppp}, function(html){
        $("#gallery").html(html).fadeIn();
    });
}

