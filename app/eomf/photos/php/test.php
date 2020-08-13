<?php

$s = "pgsql:host=localhost;port=5432;dbname=remotesensing;user=rsadmin;password=b1u3b1rd";
$s = "pgsql:dbname=remotesensing;host=localhost";
$s = "pgsql:host=localhost port=5432 dbname=remotesensing user=rsadmin password=b1u3b1rd";
//$dbh = new PDO($s, 'rsadmin', 'b1u3b1rd');
//$dbh = new PDO($s);

include 'include/database.php';

echo "<pre>";
//print_r(Photo::last(array('order'=>'id asc'))->attributes());
echo "</pre>";

echo Photo::query("SELECT 1+1");
?>
