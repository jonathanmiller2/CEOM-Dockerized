<?php
include_once "include/session.php";
include_once "include/config.inc";
include_once "include/gallery.php";
include_once "include/func.php";


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
	$x_size = abs(($bb[2] - $bb[0]))/30;						  	
	$y_size = $x_size / 2; // abs(($bb[3] - $bb[1]))/60;
	error_log($x_size.",".$y_size);
	error_log($_GET['bbox']);
else:
	$x_size = 22.25;						  	
	$y_size = 11.125;
endif;

$limit = isset($_GET['limit']) ? intval($_GET['limit']) : 'ALL';
$offset = isset($_GET['offset']) ? intval($_GET['offset']) : 0;
//$clause .= " LIMIT $limit OFFSET $offset ";

//ST_Area(ST_ConvexHull(ST_Collect(point))) as area
$query = 
"SELECT kmeans, count(*), 
array_to_string(array_agg(id), ',') as ids, 
ST_AsKML(ST_Centroid(ST_Collect(point))) as point,
ST_Area(ST_ConvexHull(ST_Collect(point))) as area
FROM (
  SELECT kmeans(ARRAY[ST_X(ST_Transform(point, 900913)), ST_Y(ST_Transform(point, 900913))], 200) OVER (), point, id
  FROM photos WHERE point is not NULL AND $clause
) AS ksub
GROUP BY kmeans
ORDER BY kmeans";


//ST_AsKML(ST_Centroid(ST_Collect(ST_SnapToGrid( point, $x_size, $y_size)))) as point
$query =
" SELECT
      array_to_string(array_agg(id), ',') as ids,
      COUNT( point ) AS count,
      ST_SnapToGrid( point, $x_size, $y_size) as cluster,
	  ST_AsKML(ST_Centroid(ST_Collect(point))) as point
  FROM photos WHERE point is not NULL AND $clause
  GROUP BY cluster
  ORDER BY count DESC
";

$result = $database->query($query);

$gmapclusters = pg_fetch_all($result);
//header("Content-Type: application/vnd.google-earth.kml+xml");

echo '<?xml version="1.0" encoding="UTF-8"?>';

?>

<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <name>EOMF Photo gmapclusters</name>
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
foreach($gmapclusters as $line):
	if (isset($line['kmeans']))
    	$id = $line['kmeans'];
	else{
		$id = isset($id) ? $id++ : 0 ;
	}
	
    $description =  "{$line['count']} photos in cluster.";
    echo "<Placemark id=\"{$id}\"> \n".
            "<styleUrl>#style</styleUrl>\n".
            "<name>Cluster: {$id}</name>\n".
            "<description> <![CDATA[{$description}]]> </description>\n".
			"<ExtendedData>\n".              
			"  <Data name=\"ids\">\n".     
			"    <displayName>ids</displayName>\n".     
			"    <value>{$line['ids']}</value>\n".
			"  </Data>\n".
			"  <Data name=\"count\">\n".     
			"    <displayName>count</displayName>\n".     
			"    <value>{$line['count']}</value>\n".
			"  </Data>\n".
			"  <Data name=\"area\">\n".     
			"    <displayName>area</displayName>\n".     
			"    <value>{$line['area']}</value>\n".
			"  </Data>\n".
			"</ExtendedData>\n".
            "{$line['point']}".
       "</Placemark>\n";
endforeach;
?>
    </Folder>
</Document>
</kml>
