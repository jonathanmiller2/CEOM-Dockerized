<?php
include ("../photos/include/func.php");
ob_start();
?>
  <script src="http://api.maps.yahoo.com/ajaxymap?v=3.0&amp;appid=euzuro-openlayers" type="text/javascript"></script>
  <script src='http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAAmuvLtH3m9h8LpbkjVzUDhBQyRLBZZgMo3VuWp3Pab5JM-oPN4hRjhrpJr4lifELK29a1ma50wKiWHg'></script>
  <script src="http://www.openlayers.org/api/OpenLayers.js" type="text/javascript"></script>
  <script src="http://dev.openlayers.org/addins/scalebar/trunk/lib/OpenLayers/Control/ScaleBar.js"></script>
  <link rel="stylesheet" href="scalebar-thin.css" type="text/css" />
<script type="text/javascript">
        var maps = new Array();
        var control_map = 0;
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
                //map.panTo(map.getLonLatFromPixel(evt.xy));
                //map2.panTo(map.getLonLatFromPixel(evt.xy));
                for (var i = 0; i < maps.length; i++){
                    maps[i].panTo(maps[control_map].getLonLatFromPixel(evt.xy))
                }
                                
            }   

        });
        var click = new OpenLayers.Control.Click();
        
        function getLayers(){
            var jpl_wms = new OpenLayers.Layer.WMS("NASA Global Mosaic", 
                ["http://t1.hypercube.telascience.org/tiles?",
                 "http://t2.hypercube.telascience.org/tiles?",
                 "http://t3.hypercube.telascience.org/tiles?",
                 "http://t4.hypercube.telascience.org/tiles?"], 
                {layers: 'landsat7'}
            );
            
            var ghyb = new OpenLayers.Layer.Google(
                "Google Hybrid",
                {type: G_HYBRID_MAP, 'sphericalMercator': true}
            );
            var yahoosat = new OpenLayers.Layer.Yahoo(
                "Yahoo Satellite",
                {'type': YAHOO_MAP_SAT, 'sphericalMercator': true}
            );
            var yahoohyb = new OpenLayers.Layer.Yahoo(
                "Yahoo Hybrid",
                {'type': YAHOO_MAP_HYB, 'sphericalMercator': true}
            );
            
            var test = new OpenLayers.Layer.WMS( "TEST", "modis.php", {layers: "ncep", time:"2005-08-29"}});
            return [jpl_wms, ghyb, yahoosat, yahoohyb, test];
        }

        function addMap(divname){
            var options = {
                controls: [
                        new OpenLayers.Control.PanZoomBar(), 
                        new OpenLayers.Control.LayerSwitcher(), 
                        new OpenLayers.Control.LayerSwitcher(), 
                        new OpenLayers.Control.MouseToolbar() 
                        ],
                projection: new OpenLayers.Projection("EPSG:900913"),
                displayProjection: new OpenLayers.Projection("EPSG:4326"),
                units: "m",
                maxResolution: 156543.0339,
                maxExtent: new OpenLayers.Bounds(-20037508, -20037508,   20037508, 20037508.34)
            };
        
            var map = new OpenLayers.Map(divname, options);
            maps.push(map);
            map.tileSize = new OpenLayers.Size(600,600);
            
            var layer = new OpenLayers.Layer.WMS( "OpenLayers WMS", 
                "http://labs.metacarta.com/wms/vmap0", {layers: 'basic'} );
                

            var day = "361";
            var year = "2000";
            var variable = "evi";
            var url = rswms + "?prod="+variable+"&day="+day+"&"+"year="+year+"&";
            
            var modis = new OpenLayers.Layer.WMS( "MODIS WMS", url, {layers: "TOP,BOT,ocean_mask", isBaseLayer: true}, {'buffer':0});
            var mask = new OpenLayers.Layer.WMS( "Ocean Mask", url, {layers: "ocean_mask"}, {'buffer':0});
            
            map.addLayers([modis, layer, mask].concat(getLayers()));
            map.setCenter(new OpenLayers.LonLat(0, 4), 2);
            
            map.addControl(click);
            click.activate();

            var legendURL = url+"version=1.1.1&request=getlegendgraphic&format=image/PNG&layer=";
            var legendHTML = '<a style="text-decoration: none;color: black;" target="_blank">'+variable.toUpperCase()+'</a><br/><img src="'+legendURL+'TOP"/><br/>';
            $("#"+divname+" .legend").html(legendHTML);
        }
        
        function addMapDiv(){
            var num = maps.length+1;
            $("#content").append($('<div id="map'+num+'" class="map"><div id="legend'+num+'" class="legend"></div></div>'));
            $("#content").append($("#info1").clone().attr("id","info"+num));
            $("#info"+num+" input[name='map_num']").val(num);
            return "map"+num;
        }
        
        function init(){
            addMap("map1");
            addMapWindow();
        }

        function updateMap(form) {
            var map_tmp, modis_tmp;
            var map_num = form["map_num"].value;
            var variable = form["variable"].value;
            var day = form["day"].value;
            var year = form["year"].value;

            map_tmp = maps[parseInt(map_num)-1];
            modis_tmp = map_tmp.getLayersByName("MODIS WMS")[0];
            //modis_tmp = map_tmp.layers[0];
            var url = rswms + "?prod="+variable+"&day="+day+"&"+"year="+year+"&";

            map_tmp.removeLayer(modis_tmp);
            modis_tmp = new OpenLayers.Layer.WMS( "MODIS WMS", url, {layers: "TOP,BOT,ocean_mask", isBaseLayer: "true"});
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
            
            map_tmp = maps[parseInt(map_num)-1];
            modis_tmp = map_tmp.getLayersByName("MODIS WMS")[0];
            
            for (var i = 0; i < maps.length; i++){
                maps[i].zoomTo(map_tmp.zoom)
            }
        }
        function addMapWindow(){
            var id = addMapDiv();
            addMap(id);
            return true;
        }
        
</script>
<style type="text/css">
.map  {position: relative; width: 658px; height: 350px; top: 25px; left: 0px; border: solid #999999 1px;}
.legend {position: absolute; top: 10px; left: 670px; text-align: left; z-index: 999999;}
.info  {position: relative; width: 648px; height: 25px; top: 20px; left: 0px; padding: 5px; background-color: #EEE; border: solid 1px #999999; text-align: left; overflow: auto;}
#control {  position: absolute; top: 480px; left: 10px; z-index: 999999; }
</style>
<?
$output_string=ob_get_contents();
ob_end_clean();

$body = "<body bgcolor=\"#FFFFFF\" onload=\"init()\">";

head("EOMF - Two Pane Visualization", false, "normal", $output_string, $body)

?>
        <div id="top"><a href='#' onClick='addMapWindow()'>Add Map</a></div>
        <div id="map1" class="map"> <div id="legend1" class="legend"></div></div>
        <div id="info1" class="info">
            <form>
                <select name="variable">
                    <option value="evi">EVI</option>
                    <option value="lswi">LSWI</option>
                    <option value="ndsi">NDSI</option>
                    <option value="ndvi">NDVI</option>
                    <option value="ndwi">NDWI</option>
                    <option value="cloudmask ">cloudmask </option>
                    <option value="snow">snow</option>
                    <option value="oceanmask">oceanmask</option>
                </select>
                <select name="day">
<? for ($i = '1'; $i != '361'; $i += 8){
                    echo "\t\t\t<option value=\"".sprintf("%0" . 3 . "d", $i)."\" >".sprintf("%0" . 3 . "d", $i)."</option>\n";
           }
?>
                    <option value="361" selected>361</option>
                </select>
                <select name="year">
                    <option value="2000" selected>2000</option>
                    <option value="2001">2001</option>
                    <option value="2002">2002</option>
                    <option value="2003">2003</option>
                    <option value="2004">2004</option>
                    <option value="2005">2005</option>
                    <option value="2006">2006</option>
                    <option value="2007">2007</option>
                    <option value="2008">2008</option>
                    <option value="2009">2009</option>
                    <option value="2009">2010</option>
                </select>
                <input type="hidden" name="map_num" value="1" />
                <input type="button" value="Update Modis Map" onclick="javascript:updateMap(this.form);return false;"/>
                <input type="button" value="Synch Zoom" onclick="javascript:synchZoom(this.form);return false;"/>
            </form>
        </div>
        <!--<div id="map2" class="map"><div id="legend2" class="legend"></div></div>
        <div id="info2" class="info">
            <form>
                <select name="variable">
                    <option value="evi">EVI</option>
                    <option value="lswi">LSWI</option>
                    <option value="ndsi">NDSI</option>
                    <option value="ndvi">NDVI</option>
                    <option value="ndwi">NDWI</option>
                </select>
                <select name="day">
        <? for ($i = '1'; $i != '361'; $i += 8){
                    echo "\t\t\t<option value=\"".sprintf("%0" . 3 . "d", $i)."\" >".sprintf("%0" . 3 . "d", $i)."</option>\n";
           }
        ?>
                    <option value="361" selected>361</option>
                </select>
                <select name="year">
                    <option value="2000" selected>2000</option>
                    <option value="2001">2001</option>
                    <option value="2002">2002</option>
                    <option value="2003">2003</option>
                    <option value="2004">2004</option>
                    <option value="2005">2005</option>
                    <option value="2006">2006</option>
                    <option value="2007">2007</option>
                    <option value="2008">2008</option>
                    <option value="2009">2009</option>
                    <option value="2009">2010</option>
                </select>
                <input type="hidden" name="map_num" value="2" />
                <input type="button" value="Update Modis Map" onclick="javascript:updateMap(this.form);return false;"/>
                <input type="button" value="Synch Zoom" onclick="javascript:synchZoom(this.form);return false;"/>
            </form>
        </div>-->
    <?php tail(); ?>
