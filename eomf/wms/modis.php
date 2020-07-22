<?php
error_reporting (E_ALL);
//dl('php_mapscript.so');

// Configuration

$map_path = "/data1/web/data/mapfiles/";
if(isset($_GET['year']) and intval($_GET['year'])<=2005)
    $data_path = "/data/vol02/modis/products/mod09a1/geotiff/";
else if (isset($_GET['year']) and intval($_GET['year'])<=2012)
    $data_path = "/data/vol05/modis/products/mod09a1/geotiff/";
else
    $data_path = "/data/vol16/modis/products/mod09a1/geotiff/";
$img_path = "/data1/web/data/tmp/";

//error_log("TEST");

//$mask_path = "/data1/web/rs/prod/htdocs/wms/esri/WORLD-Ocean-Mask";
//$mask_path = "/data1/web/data/country_boundary/world_cntry_fao_shoreline_new.shp";
//$mask_path = "/data1/web/rs/dev/code/eomf/wms/new/world_cntry_fao_shoreline_new.shp";
//$mask_path = "/web/rs/dev/code/eomf/wms/shoreline/world_outline.shp";
$mask_path = "/data1/web/data/shapes/50m_ocean";
//Variables

$EPSG_MODIS = "+proj=sinu +R=6371007.181 +nadgrids=@null +wktext";

$prod;
$day;
$year;
$date;


//-----------------------------------------------------------------
//Functions

function addOceanMask($map){
    global $mask_path;
    $shape = $mask_path;
    $mask_layer = ms_newLayerObj($map);
    //$mask_layer = $map->getLayer(2);
    //error_log($mask_layer->type);
    $mask_layer->set("name", "ocean_mask");
    $mask_layer->set("data", $shape);
    $mask_layer->set("status", "ON");
    $mask_layer->set("type", 2);
    //$mask_layer->set("transparency",20);
    
    $class = ms_newClassObj($mask_layer);
    //$class->color->setRGB(-1,-1,-1);
    //$class->outlinecolor->setRGB(176,226,225);
    //$class->setExpression("ocean-mask");
    $style = ms_newStyleObj($class);
    //$style = $class->getStyle(0);
    
    //$style->imagecolor->setRGB(80,100,155);
    $style->color->setRGB(80,100,155);
    $style->outlinecolor->setRGB(80,100,155);
    //$style->symbol = 0;

    //$mask_layer->setMetaData("wms_extent", "-180.0 -90.0 180.0 90.0");
    //$mask_layer->setMetaData("wms_srs", "EPSG:4326 EPSG:900913 EPSG:510501");
    //$mask_layer->setMetaData("wms_title", "ocean-mask");
    //$mask_layer->setMetaData("wms_group_title", "vector");
}

function setFromArray($arr, $layer){
    $len = sizeof($arr);
    $op1 = '>=';
    $op2 = '<';
    
    foreach( $arr as $cv){
        if($len-- == 1) 
            $op2 = '<=';
        //error_log($op2);
        $class = ms_newClassObj($layer);
        $class->set('name', sprintf("%01.2f - %01.2f" , $cv[0], $cv[1]) );
        $class->setExpression("([pixel] >= {$cv[0]} AND [pixel] {$op2} {$cv[1]})");
        $style = ms_newStyleObj($class);
        $style->color->setRGB($cv[2],$cv[3],$cv[4]);
    }
}

function setGeneric($layer){
    $op1 = '>=';
    $op2 = '<';
    
    $min = -1;
    $max = 1;
    $num = 18;
    for($val = $min; $val < $max; $val = $val + ($max-$min)/$num){
        $val2 = $val + ($max-$min)/$num;
        $i = ($val - $min)/($max - $min);

        if($val > $min) {
            $op1 = '>';
        }
        if($val2 == $max) {
            $op2 = '<=';
        }
        
        //error_log($i.":". 255*$i);
        $class = ms_newClassObj($layer);
        $class->set('name', sprintf("%01.2f - %01.2f" , $val, $val2) );
        $class->setExpression("([pixel] $op1 $val AND [pixel] $op2 $val2)");
        //error_log("([pixel] $op1 $val AND [pixel] $op2 $val2)");
        $style = ms_newStyleObj($class);
        $style->color->setRGB(255*$i ,255*$i,255*$i);
    }
}

function setGenericColor($layer,$c1, $c2, $mid, $min=-1, $max=1, $num=16){
    $op1 = '>=';
    $op2 = '<';
    
    if ( $min > -1){
        $class = ms_newClassObj($layer);
        $class->set('name', sprintf("%01.2f - %01.2f" , -1, $min) );
        $class->setExpression("([pixel] $op1 -1 AND [pixel] $op2 $min)");
        $style = ms_newStyleObj($class);
        $style->color->setRGB(32,32,32);
    }
    
    for($val = $min; $val < $max; $val = $val + ($max-$min)/$num){
        $val2 = $val + ($max-$min)/$num;
        $i = ($val - $min)/($max - $min);

        if($val > $min) {
            $op1 = '>';
        }
        if($val2 == $max) {
            $op2 = '<=';
        }
        
        $class = ms_newClassObj($layer);
        $class->set('name', sprintf("%01.2f - %01.2f" , $val, $val2) );
        $class->setExpression("([pixel] $op1 $val AND [pixel] $op2 $val2)");

        $style = ms_newStyleObj($class);
        if($val < $mid){
            $style->color->setRGB(abs($c1[0]-(255*$i)) ,abs($c1[1]-(255*$i)),abs($c1[2]-(255*$i)));
        }
        else{
            $style->color->setRGB(abs($c2[0]-(255*$i)) ,abs($c2[1]-(255*$i)),abs($c2[2]-(255*$i)));
        }
    }
}

function setThreeColor($layer,$cm, $c1, $c2, $mid, $min=-1, $max=1, $num=16){
    
    $class = ms_newClassObj($layer);
    $class->set('name', "No Data");
    $class->setExpression("([pixel] > $max OR [pixel] < $min)");
    $style = ms_newStyleObj($class);
    $style->color->setRGB(40,5,0);
    
    if ( $min > -1){
        $class = ms_newClassObj($layer);
        $class->set('name', sprintf("%01.2f - %01.2f" , -1, $min) );
        $class->setExpression("([pixel] >= -1 AND [pixel] < $min)");
        //error_log("([pixel] >= -1 AND [pixel] < $min)");
        $style = ms_newStyleObj($class);
        $style->color->setRGB(32,32,32);
    }
    
    $i = 0;
    $mid1 = ($mid - $min)/(($max - $min)/$num);
    $mid2 = ($max - $mid)/(($max - $min)/$num);
    for($val = $min; $val < $max; $val = $val + ($max-$min)/$num){
        $val2 = $val + ($max-$min)/$num;

        if($val == $min) {
            $op1 = '>=';
        }else{
            $op1 = '>';
        }
        $op2 = '<=';

        
        $class = ms_newClassObj($layer);
        $class->set('name', sprintf("%01.2f - %01.2f" , $val, $val2) );
        $class->setExpression("([pixel] $op1 $val AND [pixel] $op2 $val2)");
        //error_log("([pixel] $op1 $val AND [pixel] $op2 $val2)");

        $style = ms_newStyleObj($class);
        if($val2 < $mid){
            $style->color->setRGB($c1[0]+($cm[0]-$c1[0])*($i/$mid1),$c1[1]+($cm[1]-$c1[1])*($i/$mid1),$c1[2]+($cm[2]-$c1[2])*($i/$mid1) );
        }
        else if (($val <= $mid) && ($val2 >= $mid)){
            $style->color->setRGB($cm[0] ,$cm[1], $cm[2]);
            $i = 0;
        }
        else if ($val > $mid) {
            $style->color->setRGB($cm[0]+($c2[0]-$cm[0])*($i/$mid2),$cm[1]+($c2[1]-$cm[1])*($i/$mid2),$cm[2]+($c2[2]-$cm[2])*($i/$mid2) );
        }
        $i++;
    }
}



function setColorScale($layer, $prod){
    switch($prod){
        case 'evi':
            setThreeColor($layer, array(250,250,150),array(130,10,10),array(0,140,0),0.3,-0,1, 17);
            break;
        case 'ndsi':
            setThreeColor($layer, array(255,250,250),array(130,0,0),array(140,140,140),0,-1,1, 17);
            break;
        case 'ndvi':
            setThreeColor($layer, array(250,250,150),array(130,10,10),array(0,140,0),0.3,-0,1, 17);
            break;
        case 'ndwi':
            setThreeColor($layer, array(250,250,250),array(130,130,130),array(0,140,0),0,-1,1, 17);
            break;
        case 'lswi':
            setThreeColor($layer, array(250,250,250),array(130,130,130),array(0,140,0),0,-1,1, 17);
            break;
        case 'snow':
        case 'cloudmask':
        case 'oceanmask':
        case 'phenology':
            setGeneric($layer);
    }
}

function saveLegend($oMap, $prod){
	$oImg=$oMap->drawLegend();
   	$oImg->saveImage($szImg.'_legend',$oMap);
   	copy($szImg.'_legend', $szImg.'_legend.png');
   	$legendW = $oImg->width;
   	$legendH = $oImg->height;
	$oImg->free();
}

function addDataSources($map){
    global $data_path, $map_path, $prod, $date;
    
    processModisParams();
    
    $day = sprintf("%03d",$date['jday']);
    
    $top_layer = $map->getLayer(0);
    $top_layer->set("data", "{$data_path}{$prod}/{$date['year']}/globe/{$prod}_{$date['year']}{$day}_10km_mosaic.tif");

    setColorScale($top_layer, $prod);

    $bot_layer = $map->getLayer(1);
    $bot_layer->set("tileindex", "{$data_path}{$prod}/{$date['year']}/globe/{$prod}_{$date['year']}{$day}.shp");
    $bot_layer->set("tileitem", "LOCATION");
    
    setColorScale($bot_layer, $prod);
}

function ncep_layer(){
    //$date = new DateTime($_GET['time']);
    global $date;
    //$date = date_parse($_GET['time']);
    return "/data/vol04/gis_data/world/precipitation/trmm/TRMMV6/Daily/3B42V6.{$date['year']}{$date['month']}{$date['day']}.txt";
}

function addTimeLayer($map){
    $layer = ms_newLayerObj($map);
    $layer->set("name","ncep");
    $layer->set("type",MS_LAYER_RASTER);
    
    $ht = $layer->metadata;
    $ht->set("wms_title", "NCEP Temperature");
    $ht->set("wms_timeextent", $_GET['time'].'/'.$_GET['time']);
    $layer->set("data",ncep_layer());
    //$ncep_layer->set("data","/data/vol04/gis_data/world/precipitation/trmm/TRMMV6/Daily/3B42V6.20081231.txt");
    
    setThreeColor($layer, array(30,30,250),array(250,250,250),array(250,30,30),0,-10,25, 30);
}

function runWMS($map){
    
    //Begin WMS request handling
    $req = ms_newowsrequestobj();
    //$req->loadparams(); // Does not work  ->
    foreach ($_GET as $k=>$v) {
        $req->setParameter($k, $v);
    }
    
    ms_ioinstallstdouttobuffer();
    
    $map->owsdispatch( $req );
    $contenttype = ms_iostripstdoutbuffercontenttype();
    
    if ($contenttype == 'image/png')
       header('Content-type: image/png');
    if ($contenttype == 'image/jpeg')
       header('Content-type: image/jpeg');

    //error_log($contenttype);

    ms_iogetStdoutBufferBytes();
    ms_ioresethandlers();
}

// Handle url parameters
function processModisParams(){
    global $date, $prod;
    //error_log($_SERVER['SERVER_NAME']."/".$_SERVER['REQUEST_URI']);
    if(!eregi("^([0-9a-z])*$", $_GET['prod'])){
        $prod = 'evi';
    }else{
        $prod = $_GET['prod'];
    }

    if (true or isset($_GET['time'])){
    
        if(!isset($_GET['year']) and !eregi("^\d*$", $_GET['year'])){
            $date['year'] = 2000;
        }else{
            $date['year'] = intval($_GET['year']);
        }
        
        if(isset($_GET['month']) and !eregi("^\d+$", $_GET['month'])){
            if(!eregi("^\d*$", $_GET['day'])){
                $date['day'] = 1;
            }else{
                $date['day'] = intval($_GET['day']);
            }
            $date['month'] = intval($_GET['month']);
            $date['jday'] = gregoriantojd($date['month'],$date['day'],$date['year']);
            if(!eregi("^\d+$", $_GET['day'])){
                $date['month'] = 1;
            }else{
                $date['month'] = sprintf("%02d",intval($_GET['day']));
            }

        }else{
            if(!isset($_GET['day']) and !eregi("^\d*$", $_GET['day'])){
                $date['jday'] = 1;
                //$date['day'] = 
            }else{
                $date['jday'] = intval($_GET['day']);
            }
        }
    }else{
        $date = date_parse($_GET['time']);
        $date['jday'] = gregoriantojd($date['month'],$date['day'],$date['year']);
    }
}

//-----------------------------------------------------------------
//Main

$map = ms_newMapObj($map_path."new.map");

addOceanMask($map);
addDataSources($map);

//error_log(print_r($map->getlayersdrawingorder(),true));

//$map->setlayersdrawingorder(array(2,0,1));

runWMS($map);

//saveLegend($map,$prod)

?>
