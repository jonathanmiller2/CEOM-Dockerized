<?php
include_once "include/session.php";
include_once "include/config.inc";
include_once "include/gallery.php";
include_once "include/func.php";

$cols = "id, long, lat, alt, takendate, description, status, location, userid, dir, dir_deg, ".
        "(select name from categories where categories.id = photos.categoryid) as category";

$clause = " long != 0 AND lat != 0 AND ".$session->filterClause();

$ids = $_GET['ids'];

$clause .= " AND id in ($ids) ";


$limit = isset($_GET['limit']) ? intval($_GET['limit']) : 'ALL';
$offset = isset($_GET['offset']) ? intval($_GET['offset']) : 0;
$clause .= " LIMIT $limit OFFSET $offset ";

//$query = "SELECT DISTINCT ON (lat, long) $cols FROM photos WHERE $clause ";
$query = "SELECT $cols FROM photos WHERE $clause ";

$result = $database->query($query);
#error_log("SQL:{$query}\n");

//error_log(curPageURL());

$photos = pg_fetch_all($result);
//$photos = $session->filterPhotos($photos);

$directions = array('N'=>0,'NNE'=>22.5,'NE'=>45,'ENE'=>67.5,'E'=>90,'ESE'=>112.5,'SE'=>135,'SSE'=>157.5,'S'=>180,'SSW'=>202.5,'SW'=>225,'WSW'=>247.5,'W'=>270,'WNW'=>292.5,'NW'=>315,'NNW'=>337.5);

//header("Content-Type: application/vnd.google-earth.kml+xml");
$json_data = array();

foreach($photos as $line):
    if (!empty ($line['long']) && !empty ($line['lat'])):
        if(empty($line['dir_deg']))
            if(empty($line['dir']))
                $dir = 'N';
            else $dir = trim($line['dir']);
        else
            $dir = floatval($line['dir_deg']);
            
        if(empty($line['alt']))
            $line['alt'] = '0';
        $fname = str_shorten($line['location']);
        //$fname = $line['location'];
        $id = $line['id'];
        $description =  "<a href='http://{$_SERVER['HTTP_HOST']}/photos/index.php?a=view&photo={$line['id']}' target='_blank'>\n".
                            "<img class='thumb' src=\"http://".$_SERVER['HTTP_HOST'].WEB.GAL_THUMBS."/".basename($line['location'])."\"/>\n".
                         //"<br/>";
                         "</a><br/>";
        $description .= "Date: ".$line['takendate']."<br/>";
        //$description .= "Location: ".loc2str($line['long'],$line['lat'])."<br/>";
        $description .= loc2str($line['long'],$line['lat'])."<br/>";
        if (!empty($line['dir']))
            $description .= "Aspect: $dir <br/>";
        if (!empty($line['category']))
            $description .= "Category: {$line['category']}<br/>";
        if (!empty($line['description']))
            $description .= wordwrap("Field Notes: ".$line['description'], 45, "<br/>\n");
            
        $json_data[] = array(
			"id"=>$id,
			"name"=>"Photo: {$fname}",
            "description"=>$description,
            "lon"=>$line['long'],
			"lat"=>$line['lat'],
			"alt"=>$line['alt']);
    endif;
endforeach;

print json_encode($json_data);
?>