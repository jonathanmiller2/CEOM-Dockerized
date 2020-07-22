<?
/**
 * UserEdit.php
 *
 * This page is for users to edit their account information
 * such as their password, email address, etc. Their
 * usernames can not be edited. When changing their
 * password, they must first confirm their current password.
 *
 * Written by: Jpmaster77 a.k.a. The Grandmaster of C++ (GMC)
 * Last Modified: Dec, 2007, Pavel Dorovskoy
 */
include_once("include/session.php");
include_once("include/func.php");

$req_user = trim($_GET['edit']);

/**
 * User has submitted form without errors and user's
 * account has been edited successfully.
 */
if(isset($_SESSION['useredit'])){
   unset($_SESSION['useredit']);

   echo "<h3 class=\"title\">User Account Edit Success!</h3>";
   echo "<p><b>$session->username</b>, the account has been successfully updated. "
       ."<a href=\"index.php\">Home</a>.</p>";
}
else{

/**
 * If user is not logged in, then do not display anything.
 * If user is logged in, then display the form to edit
 * account information, with the current email address
 * already in the field.
 */
 
if($session->logged_in){

    $names = array(
	    //array("Username", "username"),
	    array("Email","email",30),
	    array("Full Name",'name',30), 
	    array("Institute/Affiliation" ,'affiliation',30),
	    array("Telephone",'telephone',30),
	    array("Address" , 'address1',30),
	    array("", 'address2',30),
	    array("City", 'city',30),
	    array("State/Province", 'state',30),
	    array("Postal Code", 'postal',10),
	    array("Country", "country",30)
    );

?>

<h3 class="title">Edit Account: <? echo $req_user; ?></h3>
<?
if($form->num_errors > 0){
   echo "<td><font size=\"2\" color=\"#ff0000\">".$form->num_errors." error(s) found</font></td>";
}
?>
<p>Leave password blank to not change it.</p>
<form action="process.php" method="POST">
<table align="left" border="0" cellspacing="0" cellpadding="3">
<tr>
<td>Current Password:</td>
<td><input type="password" name="curpass" maxlength="30" value="
<? echo $form->value("curpass"); ?>"></td>
<td><? echo $form->error("curpass"); ?></td>
</tr>
<tr>
<td>New Password:</td>
<td><input type="password" name="newpass" maxlength="30" value="
<? echo $form->value("newpass"); ?>"></td>
<td><? echo $form->error("newpass"); ?></td>
</tr>
<? 
$req_user_info = $database->getUserInfo($req_user);
build_user_form($req_user_info, $names); ?>
<tr><td colspan="2" align="right">
<input type="hidden" name="subedit" value="1">
<input type="submit" value="Edit Account"></td></tr>
<tr><td colspan="2" align="left"></td></tr>
</table>
</form>

<?
}
else{
	echo "You must not be loged in";
}
}

?>
