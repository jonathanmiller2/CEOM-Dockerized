<?
if(!defined('TBL_ACTIVE_USERS')) {
  die("Error processing page");
}

$q = "SELECT username FROM ".TBL_ACTIVE_USERS
    ." ORDER BY timestamp DESC,username";
$result = $database->query($q);
/* Error occurred, return given name by default */
$num_rows = pg_num_rows($result);
if(!$result || ($num_rows < 0)){
   echo "Error displaying info";
}
else if($num_rows > 0){
   /* Display active users, with link to their info */
   echo "<table align=\"left\" border=\"1\" cellspacing=\"0\" cellpadding=\"3\">\n";
   echo "<tr><td><font size=\"2\">\n";
   for($i=0; $i<$num_rows; $i++){
      $uname = pg_fetch_result($result,$i,"username");

      echo "<a href=\"userinfo.php?user=$uname\">$uname</a> / ";
   }
   echo "</font></td></tr></table><br>\n";
}
?>
