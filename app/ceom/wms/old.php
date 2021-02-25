<?php
include ("../photos/include/func.php");
ob_start();
?>
  <script src="http://api.maps.yahoo.com/ajaxymap?v=3.0&amp;appid=euzuro-openlayers" type="text/javascript"></script>
  <script src="http://www.openlayers.org/api/OpenLayers.js" type="text/javascript"></script>
  <script src="http://dev.openlayers.org/addins/scalebar/trunk/lib/OpenLayers/Control/ScaleBar.js"></script>
  <link rel="stylesheet" href="scalebar-thin.css" type="text/css" />
<script type="text/javascript">
        var map,map2,layer, modis,modis2, running = false;
        var rswms = "modis.php";

        OpenLayers.Control.Click = OpenLayers.Class(OpenLayers.Control, {                
            defaultHandlerOptions: {
                'single': true,
                'delay': 0
            },

            initialize: function(options) {
                this.handlerOptions = OpenLayers.Util.extend(
                    {}, this.defaultHandlerOptions
                );
                OpenLayers.Control.prototype.initialize.apply(
                    this, arguments
                ); 
                this.handler = new OpenLayers.Handler.Click(
                    this, {
                        'click': this.onClick 
                    }, this.handlerOptions
                );
            }, 

            onClick: function(evt) {
            	//to add : get LonLat from map which caused event
                map.panTo(map.getLonLatFromPixel(evt.xy));
                map2.panTo(map.getLonLatFromPixel(evt.xy));
            }   

        });

        function init(){
            /*var options = {
                controls: [],
                projection: new OpenLayers.Projection("EPSG:900913"),
                displayProjection: new OpenLayers.Projection("EPSG:4326"),
                units: "m",
                maxResolution: 156543.0339,
                maxExtent: new OpenLayers.Bounds(-20037508, -20037508,   20037508, 20037508.34)
            };*/
        
            map = new OpenLayers.Map('map', { controls: [] });
            map.tileSize = new OpenLayers.Size(600,600);
            layer = new OpenLayers.Layer.WMS( "OpenLayers WMS", 
                "http://labs.metacarta.com/wms/vmap0", {layers: 'basic'} );
            var shade = new OpenLayers.Layer.WMS("Shaded Relief",
                "http://gisdata.usgs.gov/wmsconnector/com.esri.wms.Esrimap?ServiceName=USGS_EDC_Elev_NED_3",
                {layers: "HR-NED.IMAGE", reaspect: "false", transparent: 'true'},
                {isBaseLayer: false, opacity: 0.3});
                
            //var gmap = new OpenLayers.Layer.Google( "Google Hybrid" , 	{type: G_HYBRID_MAP} );
            
           var jpl_wms = new OpenLayers.Layer.WMS("Imagery", 
                        ["http://t1.hypercube.telascience.org/tiles?",
                         "http://t2.hypercube.telascience.org/tiles?",
                         "http://t3.hypercube.telascience.org/tiles?",
                         "http://t4.hypercube.telascience.org/tiles?"], 
                        {layers: 'landsat7'}
                    );

            var jpl_wms2 = new OpenLayers.Layer.WMS("Imagery", 
                        ["http://t1.hypercube.telascience.org/tiles?",
                         "http://t2.hypercube.telascience.org/tiles?",
                         "http://t3.hypercube.telascience.org/tiles?",
                         "http://t4.hypercube.telascience.org/tiles?"], 
                        {layers: 'landsat7'}
                    );
            
            var day = "361";
            var year = "2000";
            var variable = "evi";
            var url = rswms + "?prod="+variable+"&day="+day+"&"+"year="+year+"&";
            
            modis = new OpenLayers.Layer.WMS( "MODIS WMS", url, {layers: "TOP,BOT,WORLD-Ocean-Mask", isBaseLayer: true}, {'buffer':0});
            
            shade.setVisibility(false);
            map.addLayers([modis, layer, jpl_wms, shade]);
            map.setCenter(new OpenLayers.LonLat(0, 4), 2);
            
            addControls(map);
            
            var click = new OpenLayers.Control.Click();
            map.addControl(click);
            click.activate();

            map2 = new OpenLayers.Map('map2', { controls: [] });
            map2.tileSize = new OpenLayers.Size(600,600);
            layer = new OpenLayers.Layer.WMS( "OpenLayers WMS", 
                "http://labs.metacarta.com/wms/vmap0", {layers: 'basic'} );
            modis2 = new OpenLayers.Layer.WMS( "MODIS WMS", url, {layers: "TOP,BOT,WORLD-Ocean-Mask", isBaseLayer: true}, {'buffer':0});
            
            map2.addLayers([modis2, layer, jpl_wms2]);
            map2.setCenter(new OpenLayers.LonLat(0, 4), 2);
            addControls(map2);
            //click = new OpenLayers.Control.Click();
            map2.addControl(click);
            //click.activate();

            var legendURL = url+"version=1.1.1&request=getlegendgraphic&format=image/PNG&layer=";
            var legendHTML = '<a style="text-decoration: none;color: black;" target="_blank">'+variable.toUpperCase()+'</a><br/><img src="'+legendURL+'TOP"/><br/>';
            var legendDiv = document.getElementById('legend1');
            legendDiv.innerHTML = legendHTML;
            legendDiv = document.getElementById('legend2');
            legendDiv.innerHTML = legendHTML;

        }
        
        function addControls(m){
        	m.addControl( new OpenLayers.Control.PanZoomBar() );
            m.addControl( new OpenLayers.Control.LayerSwitcher() );
            m.addControl( new OpenLayers.Control.MousePosition() );
            m.addControl( new OpenLayers.Control.OverviewMap() );
            m.addControl( new OpenLayers.Control.MouseToolbar() );
            m.addControl( new OpenLayers.Control.ScaleBar() );
        }

        function updateMap(form) {
            var map_tmp, modis_tmp;
            var map_num = form["map_num"].value;
            var variable = form["variable"].value;
            var day = form["day"].value;
            var year = form["year"].value;
            
            if(map_num == "1"){
                map_tmp = map;
                modis_tmp = modis;
            }else if (map_num == "2"){
                map_tmp = map2;
                modis_tmp = modis2;
            }

            var url = rswms + "?prod="+variable+"&day="+day+"&"+"year="+year+"&";

            map_tmp.removeLayer(modis_tmp);
            modis_tmp = new OpenLayers.Layer.WMS( "MODIS WMS", url, {layers: "TOP,BOT,WORLD-Ocean-Mask", isBaseLayer: "true"});
            if (map_num == "1") { 
                modis = modis_tmp;
            } else if (map_num == "2") { 
                modis2 = modis_tmp;
            }
            map_tmp.addLayer(modis_tmp);
            map_tmp.setBaseLayer(modis_tmp);
            
            var legendURL = url+"version=1.1.1&request=getlegendgraphic&format=image/PNG&layer=";
            var legendHTML = '<a style="text-decoration: none;color: black;" target="_blank">'+variable.toUpperCase()+'</a><br/><img src="'+legendURL+'TOP"/><br/>';
            var legendDiv = document.getElementById('legend'+map_num);
            legendDiv.innerHTML = legendHTML;
        }
        
        function synchZoom(form) {
            var map_tmp, modis_tmp;
            var map_num = form["map_num"].value;
            
            if(map_num == "1"){
                map_tmp = map;
                map2_tmp = map2;
            }else if (map_num == "2"){
                map_tmp = map2;
                map2_tmp = map;
            }
            
            map_tmp.zoomTo(map2_tmp.zoom);
        }
</script>
<style type="text/css">
#map  {position: relative; width: 658px; height: 350px; top: 15px; left: 0px; border: solid #999999 1px;}
#map2 {position: relative; width: 658px; height: 350px; top: 25px; left: 0px; border: solid #999999 1px;}
#legend1 {position: absolute; top: 10px; left: 670px; text-align: left; z-index: 999999;}
#legend2 {position: absolute; top: 10px; left: 670px; text-align: left; z-index: 999999;}
#info  {position: relative; width: 648px; height: 25px; top: 20px; left: 0px; padding: 5px; background-color: #EEE; border: solid 1px #999999; text-align: left; overflow: auto;}
#info2 {position: relative; width: 648px; height: 25px; top: 30px; left: 0px; padding: 5px; background-color: #EEE; border: solid 1px #999999; text-align: left; overflow: auto;}
#control {	position: absolute; top: 480px; left: 10px; z-index: 999999; }
</style>
<?
$output_string=ob_get_contents();
ob_end_clean();

$body = "<body bgcolor=\"#FFFFFF\" onload=\"init()\">";

head("CEOM - Two Pane Visualization", false, "normal", $output_string, $body)

?>
        <div id="top"></div>
        <div id="map"> <div id="legend1"></div></div>
        <div id="info">
            <form>
                <select name="variable">
                    <option value="evi"/>EVI
                    <option value="lswi"/>LSWI
                    <option value="ndsi"/>NDSI
                    <option value="ndvi"/>NDVI
                    <option value="ndwi"/>NDWI
                </select>
                <select name="day">
<? for ($i = '1'; $i != '361'; $i += 8){
                    echo "\t\t\t<option value=\"".sprintf("%0" . 3 . "d", $i)."\" />".sprintf("%0" . 3 . "d", $i)."\n";
           }
?>
                    <option value="361" selected/>361
                </select>
                <select name="year">
                    <option value="2000" selected/>2000
                    <option value="2001"/>2001
                    <option value="2002"/>2002
                    <option value="2003"/>2003
                    <option value="2004"/>2004
                    <option value="2005"/>2005
                    <option value="2006"/>2006
                </select>
                <input type="hidden" name="map_num" value="1" />
                <input type="button" value="Update Modis Map" onclick="javascript:updateMap(this.form);return false;"/>
                <input type="button" value="Synch Zoom" onclick="javascript:synchZoom(this.form);return false;"/>
            </form>
        </div>
        <div id="map2"><div id="legend2"></div></div>
        <div id="info2">
            <form>
                <select name="variable">
                    <option value="evi"/>EVI
                    <option value="lswi"/>LSWI
                    <option value="ndsi"/>NDSI
                    <option value="ndvi"/>NDVI
                    <option value="ndwi"/>NDWI
                </select>
                <select name="day">
        <? for ($i = '1'; $i != '361'; $i += 8){
                    echo "\t\t\t<option value=\"".sprintf("%0" . 3 . "d", $i)."\" />".sprintf("%0" . 3 . "d", $i)."\n";
           }
        ?>
                    <option value="361" selected/>361
                </select>
                <select name="year">
                    <option value="2000" selected/>2000
                    <option value="2001"/>2001
                    <option value="2002"/>2002
                    <option value="2003"/>2003
                    <option value="2004"/>2004
                    <option value="2005"/>2005
                    <option value="2006"/>2006
                </select>
                <input type="hidden" name="map_num" value="2" />
                <input type="button" value="Update Modis Map" onclick="javascript:updateMap(this.form);return false;"/>
                <input type="button" value="Synch Zoom" onclick="javascript:synchZoom(this.form);return false;"/>
            </form>
        </div>
	<?php tail(); ?>
