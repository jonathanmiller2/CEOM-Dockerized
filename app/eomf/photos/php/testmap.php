<?php
require_once("include/h2o.php");
require_once("include/func.php");
require_once("include/session.php");
require_once("include/config.inc");

global $database;

$clause = query_process_form();
$clause2 = $clause . " AND long != 0 AND lat != 0 AND ".$session->filterClause() ;
//               id, long, lat, alt, location, description, userid, status
//$query = "SELECT DISTINCT ON (lat, long) id, long, lat, alt, description, status, location, userid  FROM photos WHERE " . $clause2 ;//. " LIMIT 4100";

//echo $query;

$_SESSION['query'] = $query;
$_SESSION['query_where_clause'] = $clause;

//Save origin url for edit page to return here
$_SESSION['url1'] = $_SERVER['REQUEST_URI'];

$title = "Global Geo-Referenced Field Photo Library";
$menu = menu(true);
$qform = query_print_form(true);

$h2o = new h2o(TEMPLATES_DIR."photos/testmap.html");
echo $h2o->render(compact("session","menu","title","qform"));
?>
