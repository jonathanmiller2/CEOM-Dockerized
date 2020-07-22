<?php
require_once 'include/h2o.php';
require_once 'include/session.php';
require_once 'include/gallery.php';

$_SESSION['query_where_clause'] = "photos.id = ".intval($_GET['photo']);
$_SESSION['query'] = "SELECT {$gallery->items} FROM photos WHERE ".$_SESSION['query_where_clause'];

$h2o = new h2o(TEMPLATES_DIR."photos/popup.html");
$lon = $_GET['lon'];
$lat = $_GET['lat'];
echo $h2o->render(compact("lon","lat"));
?>