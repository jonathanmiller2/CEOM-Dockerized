<?php
include_once "include/session.php";
include_once "include/config.inc";
include_once "include/gallery.php";
include_once "include/func.php";

$cols = "id, long, lat, alt, takendate, description, status, location, userid, dir, dir_deg, ".
        "(select name from categories where categories.id = photos.categoryid) as category";

$clause = " long != 0 AND lat != 0 AND ".$session->filterClause();

if (isset ($_SESSION['query_where_clause'])):
	$clause .= " AND ".$_SESSION['query_where_clause'];
else:
    $clause .= " AND ".query_process_form(true);
endif;

if (isset($_GET['bbox'])):
    $bb = split(',',$_GET['bbox'],4);
    $bb = array_map(floatval, $bb);
    $clause .= " AND point && 
    st_geometryfromtext('Polygon(({$bb[0]} {$bb[1]}, 
                                  {$bb[2]} {$bb[1]}, 
                                  {$bb[2]} {$bb[3]}, 
                                  {$bb[0]} {$bb[3]}, 
                                  {$bb[0]} {$bb[1]}))',4326)";
endif;

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

echo '<?xml version="1.0" encoding="UTF-8"?>';
//http://maps.google.com/mapfiles/kml/pal4/icon28.png
//<href>http://www.iconarchive.com/icons/newformula.org/canon-digital-camera/32/Ixus-430-icon.png</href>

?>

<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <name>EOMF Photos</name>
    <open>1</open>
    <Style id="style">
        <IconStyle>
            <color>ffffffff</color>
            <scale>0.8</scale>
            <Icon>
            <href>http://www.iconarchive.com/icons/newformula.org/canon-digital-camera/32/Ixus-430-icon.png</href>
            </Icon>
        </IconStyle>
        <LabelStyle>
            <scale>0</scale>
        </LabelStyle>
    </Style>
    <Folder>
        <name>Unique Point Placemarks</name>
<?
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
            
        echo "<Placemark id=\"{$id}\"> \n".
                "<styleUrl>#style</styleUrl>\n".
                "<name>Photo: {$fname}</name>\n".
                "<description> <![CDATA[{$description}]]> </description>\n".
                "<Point><coordinates>{$line['long']},{$line['lat']},{$line['alt']}</coordinates></Point>\n".
           "</Placemark>\n";
    endif;
endforeach;
?>
    </Folder>
</Document>
</kml>
