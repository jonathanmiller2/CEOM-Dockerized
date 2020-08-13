<?php
require_once 'include/h2o.php';
require_once 'include/func.php'; //Include auxillary functions
require_once 'include/session.php';

global $session, $database;

$title = "Global Geo-Referenced Field Photo Library";

//$photos = Photo::find('all', array('limit'=>20));
$pri = "(select count(*) from photos where userid = users.id and status = ".PRIVATE_STATUS.")";
$pub = "(select count(*) from photos where userid = users.id and status = ".PUBLIC_STATUS.")";
$userq = "SELECT id, username, $pri as private, $pub as public 
          FROM users 
          WHERE id in (select userid from photos)
          ORDER BY username";
$users = $database->queryFetch($userq);
if(!$users) error_log($userq);

$cc = "ST_Intersects(point, geometry)";
$pri = "(select count(*) from photos where {$cc} and status = ".PRIVATE_STATUS.")";
$pub = "(select count(*) from photos where {$cc} and status = ".PUBLIC_STATUS.")";
$countryq = "SELECT gid as id, cntry_name as name, $pri as private, $pub as public
             FROM country_buffered 
             ORDER BY cntry_name";
$countries = $database->queryFetch($countryq);
if(!$countries) error_log($countryq);

$contq = "SELECT gid as id, continent as name, $pri as private, $pub as public
             FROM continent_buffered
             ORDER BY continent";
//$regions = $database->queryFetch($contq);
if(!$regions) error_log($contq);

$menu = menu(true);

$h2o = new h2o(TEMPLATES_DIR."photos/summary.html");
echo $h2o->render(compact("session",
                          "menu",
                          "title",
                          "users",
                          "countries",
                          "regions"));
?>
