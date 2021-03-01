<?
/**
 * Admin.php
 *
 * This is the Admin Center page. Only administrators
 * are allowed to view this page. This page displays the
 * database table of users and banned users. Admins can
 * choose to delete specific users, delete inactive users,
 * ban users, update user levels, etc.
 *
 * Written by: Jpmaster77 a.k.a. The Grandmaster of C++ (GMC)
 * Last Updated: August 26, 2004
 */
include("../include/session.php");
include("../include/func.php");
include("../include/h2o.php");
//head("Remote Sensing - Admin Center");

/**
 * displayUsers - Displays the users database table in
 * a nicely formatted html table.
 */
function displayUsers(){
   global $database;
   $q = "SELECT username,level,email,timestamp, 
            (select count(*) from photos where userid = users.id) as photos "
       ."FROM ".TBL_USERS." ORDER BY level DESC,username";
   $result = $database->query($q);
   /* Error occurred, return given name by default */
   $num_rows = pg_num_rows($result);
   if(!$result || ($num_rows < 0)){
      echo "Error displaying info";
      return;
   }
   if($num_rows == 0){
      echo "Database table empty";
      return;
   }
   /* Display table contents */
   echo "<table id='users' cellpadding='0' cellspacing='0' border='0' class='display'>\n";
   echo "<thead>
        <tr><th>Username</th><th>Photos</th><th>Level</th><th>Email</th><th>Last Active</th></tr>
   </thead>
   <tbody>";
   for($i=0; $i<$num_rows; $i++){
      $uname  = pg_fetch_result($result,$i,"username");
      $photos = pg_fetch_result($result,$i,"photos");
      $ulevel = pg_fetch_result($result,$i,"level");
      $email  = pg_fetch_result($result,$i,"email");
      $time   = date("F j, Y, g:i a",pg_fetch_result($result,$i,"timestamp"));
      $url = htmlspecialchars("/photos/index.php?a=user&info=$uname");
      echo "<tr><td><a href='$url'>$uname</a></td><td>$photos</td><td>$ulevel</td><td>$email</td><td>$time</td></tr>\n";
   }
   echo "</tbody></table><br/>\n";
}

/**
 * displayBannedUsers - Displays the banned users
 * database table in a nicely formatted html table.
 */
function displayBannedUsers(){
   global $database;
   $q = "SELECT username,timestamp "
       ."FROM ".TBL_BANNED_USERS." ORDER BY username";
   $result = $database->query($q);
   /* Error occurred, return given name by default */
   $num_rows = pg_num_rows($result);
   if(!$result || ($num_rows < 0)){
      echo "Error displaying info";
      return;
   }
   if($num_rows == 0){
      echo "Database table empty";
      return;
   }
   /* Display table contents */
   echo "<table align='left' border=\"1\" cellspacing=\"0\" cellpadding=\"3\">\n";
   echo "<tr><td><b>Username</b></td><td><b>Time Banned</b></td></tr>\n";
   for($i=0; $i<$num_rows; $i++){
      $uname = pg_fetch_result($result,$i,"username");
      $time  = pg_fetch_result($result,$i,"timestamp");

      echo "<tr><td>$uname</td><td>$time</td></tr>\n";
   }
   echo "</table>
   <br/>\n";
}
ob_start();
/**
 * User not an administrator, redirect to main page
 * automatically.
 */
if(!$session->isAdmin() and false){
   header("Location: ../index.php");
}
else{
/**
 * Administrator is viewing page, so display all
 * forms.
 */
?>
<h1>Admin Center</h1>
<font size="4">Logged in as <b><? echo $session->username; ?></b></font><br/><br/>
Back to [<a href="../index.php">Main Page</a>]<br/><br/>
<?
if($form->num_errors > 0){
   echo "<font size=\"4\" color=\"#ff0000\">"
       ."!*** Error with request, please fix</font><br/><br/>";
}

echo "<br/>";

/**
 * Display Users Table
 */
?>
<h3>Users Table Contents:</h3>
<p>
<?
displayUsers();

echo "</p>";

/**
 * Update User Level
 */
?>
<h3>Update User Level</h3>
<? echo $form->error("upduser"); ?>

<form action="adminprocess.php" method="post">

Username:<br/>
<input type="text" name="upduser" maxlength="30" value="<? echo $form->value("upduser"); ?>"/>
<br/>
Level:<br/>
<select name="updlevel">
<option value="1">1 (Regular User)</option>
<option value="3">3 (Trusted User)</option>
<option value="5">5 (CEOM Group User)</option>
<option value="9">9 (Administrator)</option>
</select>
<br/>
<br/>
<input type="hidden" name="subupdlevel" value="1"/>
<input type="submit" value="Update Level"/>
<br/>
</form>
<br/>
<hr/>
<br/>
<?
/**
 * Delete User
 */
?>
<h3>Delete User</h3>
<? echo $form->error("deluser"); ?>
<form action="adminprocess.php" method="post">
Username:<br/>
<input type="text" name="deluser" maxlength="30" value="<? echo $form->value("deluser"); ?>"/>
<input type="hidden" name="subdeluser" value="1"/>
<input type="submit" value="Delete User"/>
</form>
<br/><hr/><br/>
<br/>
<?
/**
 * Delete Inactive Users
 */
?>
<h3>Delete Inactive Users</h3>
This will delete all users (not administrators), who have not logged in to the site<br/>
within a certain time period. You specify the days spent inactive.<br/><br/>
<br/>
<form action="adminprocess.php" method="post">
<br/>
Days:<br/>
<select name="inactdays">
<option value="3">3</option>
<option value="7">7</option>
<option value="14">14</option>
<option value="30">30</option>
<option value="100">100</option>
<option value="365">365</option>
</select>
<br/>
<br/>
<input type="hidden" name="subdelinact" value="1"/>
<input type="submit" value="Delete All Inactive"/>
<br/>
</form>
<br/><hr/><br/>
<?
/**
 * Ban User
 */
?>
<h3>Ban User</h3>
<? echo $form->error("banuser"); ?>
<form action="adminprocess.php" method="post">
Username:<br/>
<input type="text" name="banuser" maxlength="30" value="<? echo $form->value("banuser"); ?>"/>
<input type="hidden" name="subbanuser" value="1"/>
<input type="submit" value="Ban User"/>
</form>
<br/><hr/><br/>
<?
/**
 * Display Banned Users Table
 */
?>
<h3>Banned Users Table Contents:</h3>
<?
displayBannedUsers();
?>
<br/><hr/>
<?
/**
 * Delete Banned User
 */
?>
<h3>Delete Banned User</h3>
<? echo $form->error("delbanuser"); ?>
<form action="adminprocess.php" method="post">
Username:<br/>
<input type="text" name="delbanuser" maxlength="30" value="<? echo $form->value("delbanuser"); ?>"/>
<input type="hidden" name="subdelbanned" value="1"/>
<input type="submit" value="Delete Banned User"/>
</form>
<br/>
<?
}

$content = ob_get_clean();
//$menu = menu(true);
$title = "Photo-Browser Admin Center";
$head_extra = '
		<link rel="stylesheet" href="/media/css/demo_page.css" />
		<link rel="stylesheet" href="/media/css/demo_table.css" />
		<script type="text/javascript" language="javascript" src="/media/js/jquery.dataTables.js"></script>
		<script type="text/javascript" charset="utf-8">
			$(document).ready(function() {
				$("#users").dataTable();
			} );
		</script>
';
//error_log("----".TEMPLATES_DIR."-----");
$h2o = new h2o(TEMPLATES_DIR."photos/main.html");
echo $h2o->render(compact("head_extra","session","title","content"));
?>

