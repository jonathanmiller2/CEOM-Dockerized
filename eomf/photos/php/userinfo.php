<?

/**
 * UserInfo.php
 *
 * This page is for users to view their account information
 * with a link added for them to edit the information.
 *
 * Written by: Jpmaster77 a.k.a. The Grandmaster of C++ (GMC)
 * Last Modified: Dec, 2007, Pavel Dorovskoy
 */
include_once 'include/session.php';
include_once 'include/gallery.php';

/* Requested Username error checking */
$req_user = trim($_GET['info']);

if (!$req_user || strlen($req_user) == 0 || !preg_match("/^\w+$/", $req_user) || !$database->usernameTaken($req_user)) {
	die("Username not registered");
}

/* Logged in user viewing own account */
if (strcmp($session->username, $req_user) == 0) {
	echo "<h3>My Account</h3>";
}
/* Visitor not viewing own account */
else {
	echo "<h3>User Info</h3>";
}

$req_user_info = $database->getUserInfo($req_user);
$_SESSION['cur_uid'] = $req_user_info['id'];

function build_user_table($arr, $names, $skip=true){
	global $database,$session;

	echo "\n<table>";
	foreach($names as $n){
		if (!empty($arr[$n[1]]))
			echo "<tr><td align=\"right\"><b>". $n[0] . '</b> </td><td>' . $arr[$n[1]] . "</tr>\n";
	}
	/* Role */
	echo "<tr><td align=\"right\"><b>User type:</b></td><td>".$session->getRole($arr['level'])."</td></tr></table>";
}

$names = array(
	array("Username:", "username"),
	array("Email:","email"),
	array("Full Name:",'name'), 
	array("Affiliation:" ,'affiliation'),
	array("Telephone:",'telephone'),
	array("Address:" , 'address1'),
	array(" ", 'address2'),
	array("City:", 'city'),
	array("State/Province:", 'state'),
	array("Postal Code:", 'postal'),
	array("Country:", "country")
);

build_user_table($req_user_info,$names);
/**
 * Note: when you add your own fields to the users table
 * to hold more information, like homepage, location, etc.
 * they can be easily accessed by the user info array.
 *
 * $session->user_info['location']; (for logged in users)
 *
 * ..and for this page,
 *
 * $req_user_info['location']; (for any user)
 */

echo "<br>";

/* If logged in user viewing own account, give link to edit */
if (strcmp($session->username, $req_user) == 0 or $session->isAdmin()) {
	echo "<p><a href=\"index.php?a=user&edit=$req_user\">Edit Account Information</a></p>";

	if(isset($_SESSION['photoedit'])){
   		unset($_SESSION['photoedit']);

   		echo "<b>$session->username</b>, the photo has been successfully updated.<br/>";
	}

	echo "<br/><h3>Uploaded pictures by date of upload</h3>";

	if (! ($gallery->showFoldersByDate($req_user,false))){
		echo "No pictures uploaded<br>";
	}else{
		echo "<br>";
	}

	if(isset($_GET['uploaddate'])){
        ?>
        <script type="text/javascript"><!--
        var formblock;
        var forminputs;
        var total = 0;

        function select_all(name, value) {
            flag = value == 1 ? true : false;
            for (i = 0; i < forminputs.length ; i++) {
                // regex here to check name attribute
                var regex = new RegExp(name, "i");
                if (regex.test(forminputs[i].getAttribute('name'))) {
                    forminputs[i].checked = flag;
                }
            }
        }

        function check(e){
            return;
        }
        $(document).ready(function(){
            formblock = document.getElementById('form_id');
            forminputs = formblock.getElementsByTagName('input');
        });
        //--></script>
        <a href="#" onClick="select_all('list', '1'); return false;">Check All</a> | <a href="#" onClick="select_all('list', '0'); return false;">Uncheck All</a>
        <br/><br/>
        <?
        echo "<form id='form_id' method='GET' action='index.php'>";
	    echo "<input type='hidden' name='a' value='edit'>";
	    //$gallery->checkbox = true;
		$gallery->showPhotosByDate($_GET['uploaddate'], $req_user_info['id']);
        //echo "<input type='submit' value='Edit Selected'></form><br/>";
        
		echo "<form action=\"process.php\" method=\"post\"><input type=\"hidden\" name=\"subdeleteduplicates\" value=\"1\">" .
				"<input type=\"hidden\" name=\"subdel_date\" value=\"".$_GET['uploaddate']."\">" .
				"<input type=\"submit\" value=\"Delete Duplicates\"></form>";
                
        echo "<form action=\"process.php\" method=\"post\"><input type=\"hidden\" name=\"subdeleteduplicates\" value=\"1\">" .
				"<input type=\"hidden\" name=\"subdel_date\" value=\"".$_GET['uploaddate']."\">" .
                "<input type=\"hidden\" name=\"undo\" value=\"1\">" .
				"<input type=\"submit\" value=\"Undelete\"></form><br/>&nbsp;";
	}
}
?>
