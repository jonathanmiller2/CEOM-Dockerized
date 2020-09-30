<?php
/*
require_once("include/h2o.php");
require_once("include/session.php");
require_once("include/gallery.php");
require_once("include/form.php");
require_once("include/func.php");
require_once("include/paginator.php");

global $database, $gallery, $session;

$debug = false;
$title = "Global Geo-Referenced Field Photo Library - Query";

ob_start();
//Add Map link
//echo "[<a href = \"map.php?".$_SERVER['QUERY_STRING']."\">Map Query</a>]";
echo "<br><br>\n";

//Build search query from any form input $_GET
$clause = query_process_form();

//Add sql for user and picture status
$clause2 = $clause . " AND ".$session->filterClause();

$items = "id, location, userid, photogroupid, description, long, lat, 
           regionid, takendate, uploaddate, datum, alt, categoryid, (SELECT name FROM categories WHERE id = categoryid) as categoryname, status, hash";

$query = "SELECT $items FROM photos WHERE  $clause2 ORDER BY id";

$_SESSION['query'] = $query;
$_SESSION['query_where_clause'] = $clause;

//Save origin url for edit page to return here
$_SESSION['url1'] = $_SERVER['REQUEST_URI'];

query_print_form();

//$pub = pg_fetch_row($database->query("SELECT COUNT(id) FROM photos WHERE $clause AND status = 1"));
//$del = pg_fetch_row($database->query("SELECT COUNT(id) FROM photos WHERE $clause AND status = 0"));
//$pri = pg_fetch_row($database->query("SELECT COUNT(id) FROM photos WHERE $clause AND status = 2"));
//$total = pg_fetch_row($database->query("SELECT COUNT(id) FROM photos WHERE $clause2"));
//$q = "select (SELECT COUNT(id) FROM photos WHERE $clause AND status = 1) as pub, 
//                                   (SELECT COUNT(id) FROM photos WHERE $clause AND status = 0) as del,
//                                   (SELECT COUNT(id) FROM photos WHERE $clause AND status = 2) as pri,
//                                   (SELECT COUNT(id) FROM photos WHERE $clause2) as total;";

$q2 = "select count(*) FROM photos WHERE $clause2;";
$arr = $database->queryFetch($q2);

//Start paginator
$pages = new Paginator();
$pages->items_total = intval($arr[0]['count']);
$pages->paginate();

$query = $query . " " . $pages->limit;

$photos = $database->queryFetch($query);

//echo "Public: (". $arr[1][0] . ")  Private: (" . $arr[0][0] . ")  Deleted: (" . $arr[2][0]. ")<br><br>";
//die();
if ($debug) {
	echo $query;
	$database->printTable("photos");

	echo '<pre>';
	print_r($arr);
	echo '</pre>';
}

echo "Photos found: {$arr[0]['count']}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" . $pages->display_pages()."&nbsp;&nbsp;&nbsp;" . $pages->display_jump_menu() . $pages->display_items_per_page(). "<br>&nbsp;";

$lim = $session->getDownloadLimit();
if ($session->userlevel == GUEST_LEVEL){
    $warning = "Your download limit of ($lim) has been reached. Register in order to download more.";
}else{
    $warning = "Your download limit of ($lim) has been reached. Upload more pictures in order to download more.";
}

?>
<script type="text/javascript"><!--
var formblock;
var forminputs;
var total = 0;

function prepare() {
    formblock = document.getElementById('form_id');
    forminputs = formblock.getElementsByTagName('input');
}

function select_all(name, value) {
    total = 0;
    if (value == 1){
        for (i = 0; (i < <? if ($lim) echo $lim; else echo "forminputs.length"; ?>) && ( i < forminputs.length ); i++) {
            // regex here to check name attribute
            var regex = new RegExp(name, "i");
            if (regex.test(forminputs[i].getAttribute('name'))) {
                forminputs[i].checked = true;
                total++;
            }
        }
    }
    else{
        for (i = 0; i < forminputs.length ; i++) {
            // regex here to check name attribute
            var regex = new RegExp(name, "i");
            if (regex.test(forminputs[i].getAttribute('name'))) {
                forminputs[i].checked = false;
            }
        }
    }
}

function check(e){
    var targ;
    if (!e) var e = window.event;
    if (e.target) targ = e.target;
    else if (e.srcElement) targ = e.srcElement;
    if (targ.nodeType == 3) // defeat Safari bug
        targ = targ.parentNode;

    if(targ.checked){
        total++;
        if (<? if ($lim) echo "total > $lim"; else echo "false"; ?>){
            warning();
            targ.checked = false;
            total--;
        }
    }else{
        total--;
    }

}

function warning(){
    alert("<?echo $warning;?>");
}

if (window.addEventListener) {
    window.addEventListener("load", prepare, false);
} else if (window.attachEvent) {
    window.attachEvent("onload", prepare)
} else if (document.getElementById) {
    window.onload = prepare;
}

//-->
</script>
<form id="form_id" name="download" action="process.php" method="post" >
<a href="#" onClick="select_all('list', '1'); return false;">Check All</a> | <a href="#" onClick="select_all('list', '0'); return false;">Uncheck All</a>
<br/><br/>
<?
$gallery->showResultArrayUnfiltered($photos, true);
?>
<br/>
<select name="get" >
    <option value="csv">CSV file and images.</option>
    <option value="kmz">KMZ: KML and images.</option>
    <option value="shp">ESRI Shapefile/DBF.</option>
</select>
<br/>
<select name="img" >
    <option value="big">Original images.</option>
    <option value="small">Downsized images.</option>
</select>
<br/>
<input type="hidden" name="subdownload" width="1">
<input type="submit" value="Download">
</form>
<br/>&nbsp;
<?
$content = ob_get_clean();

$menu = menu(true);
$h2o = new h2o(TEMPLATES_DIR."photos/main.html");
echo $h2o->render(compact("session","menu","title","content"));
*/
?>