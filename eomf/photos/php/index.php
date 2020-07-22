<?php
require_once 'include/h2o.php';
require_once 'include/config.inc'; //include configuring variables
require_once 'include/func.php'; //Include auxillary functions
require_once 'include/session.php';
require_once 'include/gallery.php';

global $gallery, $session, $database;

$title = "Global Geo-Referenced Field Photo Library";
ob_start();
//---------------------------------------------------------
// Navigation logic
//---------------------------------------------------------
switch ($_GET['a']){
	case "login":
		$title .= " - Main";
		include('login.php');
		break;
		
    case "register":
        $title .= " - Register";
        include('register.php');
        break;

	case "query":
		header("Location: query.php?".$_SESSION['query_string']." ");
		exit(1);
		break;

	case "upload":
		header("Location: upload.php ");
		break;

	case "user":
		if( isset( $_GET['edit'])){
			$title .=" - Edit User";
			include('useredit.php');
		}else{
            $title .=" - User";
            include('userinfo.php');
		}
		break;

	case "edit":
		if ( isset($_GET['photo'])){
			$title .= " - Edit Photo";
			$gallery->showEditPhoto($_GET['photo']);
		}else if (isset($_GET['list[]'])){
		    //die();
			$title .=" - Edit Photos";
			$gallery->showEditPhotoList($_GET['list[]']);
		}
		break;

	case "view":
		if ( isset($_GET['photo'])){
			$title .= " - View Photo";
			//$h2o = new h2o(TEMPLATES_DIR."photos/main.html");
			
			$gallery->viewPhoto($_GET['photo']);
		} 
		else if (isset($_GET['exif'])) {
            $gallery->viewExif($_GET['exif']);
		}
		break;
	default:
		//head("Global Geo-Referenced Field Photo Library");
}

$content = ob_get_clean();
$menu = menu(true);
$h2o = new h2o(TEMPLATES_DIR."photos/main.html");
echo $h2o->render(compact("session","menu","title","content"));
?>
