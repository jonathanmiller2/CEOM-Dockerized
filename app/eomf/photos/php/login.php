<?
/**
 * User has already logged in, so display relavent links, including
 * a link to the admin center if the user is an administrator.
 */
if($session->logged_in){
	echo "<h1>Logged In</h1>";
}
else{
?>
<br/>
<br/>
<h1>Login</h1>
<?
/**
 * User not logged in, display the login form.
 * If user has already tried to login, but errors were
 * found, display the total number of errors.
 * If errors occurred, they will be displayed.
 */
if($form->num_errors > 0){
   echo "<font size=\"2\" color=\"#ff0000\">".$form->num_errors." error(s) found</font>";
}
?>
<form action="process.php" method="POST">
<table align="left" border="0" cellspacing="0" cellpadding="3">
<tr>
	<td>Username or Email:</td><td><input type="text" name="user" maxlength="30" value="<? echo $form->value("user"); ?>"></td><td><? echo $form->error("user"); ?></td>
</tr>
<tr>
	<td>Password:</td><td><input type="password" name="pass" maxlength="30" value="<? echo $form->value("pass"); ?>"></td><td><? echo $form->error("pass"); ?></td>
</tr>
<tr>
	<td colspan="2" align="left"><input type="checkbox" name="remember" <? if($form->value("remember") != ""){ echo "checked"; } ?>>
	<font size="2">Remember me next time &nbsp;&nbsp;&nbsp;&nbsp;</font>
	<input type="hidden" name="sublogin" value="1">
	<input type="submit" value="Login"></td>
</tr>
<tr>
	<td colspan="2" align="left"><br><font size="2">[<a href="forgotpass.php">Forgot Password?</a>]</font></td><td align="right"></td>
</tr>
<tr>
	<td colspan="2" align="left"><br>Not registered? <a href="index.php?a=register">Sign-Up!</a></td>
</tr>
</table>
</form>

<?
}

/**
 * Just a little page footer, tells how many registered members
 * there are, how many users currently logged in and viewing site,
 * and how many guests viewing site. Active users are displayed,
 * with link to their user information.
 */

echo "<div style='clear:both;'><br/>";
echo "<b>Member Total:</b> ".$database->getNumMembers()."<br/></div>";
//echo "There are $database->num_active_users registered members and ";
//echo "$database->num_active_guests guests viewing the site.<br><br>";

//include("include/view_active.php");

?>
