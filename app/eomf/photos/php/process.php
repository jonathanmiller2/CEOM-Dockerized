<?


/**
 * Process.php
 *
 * The Process class is meant to simplify the task of processing
 * user submitted forms, redirecting the user to the correct
 * pages if errors are found, or if form is successful, either
 * way. Also handles the logout procedure.
 *
 * Written by: Jpmaster77 a.k.a. The Grandmaster of C++ (GMC)
 * Last Modified: Dec, 2007, Pavel Dorovskoy
 */

include_once ("include/config.inc");
include_once ("include/session.php");
include_once ("include/gallery.php");
include_once ("include/func.php");
include_once ('include/pclzip.lib.php');

class Process {
	/* Class constructor */
	function Process() {
		global $session;
		/* User submitted login form */
		if (isset ($_POST['sublogin'])) {
			$this->procLogin();
		}
		/* User submitted registration form */
		else
			if (isset ($_POST['subjoin'])) {
				$this->procRegister();
			}
		/* User submitted forgot password form */
		else
			if (isset ($_POST['subforgot'])) {
				$this->procForgotPass();
			}
		/* User submitted edit account form */
		else
			if (isset ($_POST['subedit'])) {
				$this->procEditAccount();
			}
		/* User submitted picture upload form */
		else
			if (isset ($_POST['subupload'])) {
				$this->procUpload();
			}
		/* User submited picture edit form */
		else
			if (isset ($_POST['subeditphoto'])) {
				$this->procEditPhoto();
			}
		else
			if (isset ($_POST['subdownload'])) {
				$this->procDownload();
			}
		else
			if (isset ($_POST['subdeleteduplicates'])) {
				$this->procDeleteDuplicates();
			}
		/**
		* The only other reason user should be directed here
		* is if he wants to logout, which means user is
		* logged in currently.
		*/
		else
			if ($session->logged_in) {
				$this->procLogout();
			}
		/**
		* Should not get here, which means user is viewing this page
		* by mistake and therefore is redirected.
		*/
		else {
			header("Location: index.php");
		}
	}

	/**
	* procLogin - Processes the user submitted login form, if errors
	* are found, the user is redirected to correct the information,
	* if not, the user is effectively logged in to the system.
	*/
	function procLogin() {
		global $session, $form;
		/* Login attempt */
		$retval = $session->login($_POST['user'], $_POST['pass'], isset ($_POST['remember']));

		/* Login successful */
		if ($retval) {
			header("Location: " . $session->referrer);
		}
		/* Login failed */
		else {
			$_SESSION['value_array'] = $_POST;
			$_SESSION['error_array'] = $form->getErrorArray();
			header("Location: " . $session->referrer);
		}
	}

	/**
	* procLogout - Simply attempts to log the user out of the system
	* given that there is no logout form to process.
	*/
	function procLogout() {
		global $session;
		$retval = $session->logout();
		header("Location: index.php");
	}

	/**
	* procRegister - Processes the user submitted registration form,
	* if errors are found, the user is redirected to correct the
	* information, if not, the user is effectively registered with
	* the system and an email is (optionally) sent to the newly
	* created user.
	*/
	function procRegister() {
		global $session, $form;
		/* Convert username to all lowercase (by option) */
		if (ALL_LOWERCASE) {
			$_POST['user'] = strtolower($_POST['user']);
		}
		/* Registration attempt */
		$retval = $session->register($_POST['user'], $_POST['pass'], $_POST['email'], $_POST);

		/* Registration Successful */
		if ($retval == 0) {
			$_SESSION['reguname'] = $_POST['user'];
			$_SESSION['regsuccess'] = true;
			header("Location: " . $session->referrer);
		}
		/* Error found with form */
		else
			if ($retval == 1) {
				$_SESSION['value_array'] = $_POST;
				$_SESSION['error_array'] = $form->getErrorArray();
				header("Location: " . $session->referrer);
			}
		/* Registration attempt failed */
		else
			if ($retval == 2) {
				$_SESSION['reguname'] = $_POST['user'];
				$_SESSION['regsuccess'] = false;
				header("Location: " . $session->referrer);
			}
	}

	/**
	* procForgotPass - Validates the given username then if
	* everything is fine, a new password is generated and
	* emailed to the address the user gave on sign up.
	*/
	function procForgotPass() {
		global $database, $session, $mailer, $form;
		/* Username error checking */
		$subuser = $_POST['user'];
		$field = "user"; //Use field name for username
		if (!$subuser || strlen($subuser = trim($subuser)) == 0) {
			$form->setError($field, "* Username not entered<br>");
		} else {
			/* Make sure username is in database */
			$subuser = stripslashes($subuser);
			if (strlen($subuser) < 5 || strlen($subuser) > 30 || !eregi("^([0-9a-z])+$", $subuser) || (!$database->usernameTaken($subuser))) {
				$form->setError($field, "* Username does not exist<br>");
			}
		}

		/* Errors exist, have user correct them */
		if ($form->num_errors > 0) {
			$_SESSION['value_array'] = $_POST;
			$_SESSION['error_array'] = $form->getErrorArray();
		}
		/* Generate new password and email it to user */
		else {
			/* Generate new password */
			$newpass = $session->generateRandStr(8);

			/* Get email of user */
			$usrinf = $database->getUserInfo($subuser);
			$email = $usrinf['email'];

			/* Attempt to send the email with new password */
			if ($mailer->sendNewPass($subuser, $email, $newpass)) {
				/* Email sent, update database */
				$database->updateUserField($subuser, "password", md5($newpass));
				$_SESSION['forgotpass'] = true;
			}
			/* Email failure, do not change password */
			else {
				$_SESSION['forgotpass'] = false;
			}
		}

		header("Location: " . $session->referrer);
	}

	/**
	* procEditAccount - Attempts to edit the user's account
	* information, including the password, which must be verified
	* before a change is made.
	*/
	function procEditAccount() {
		global $session, $form;
		/* Account edit attempt */
		$retval = $session->editAccount($_POST['curpass'], $_POST['newpass'], $_POST['email'], $_POST);

		/* Account edit successful */
		if ($retval) {
			$_SESSION['useredit'] = true;
			header("Location: " . $session->referrer);
		}
		/* Error found with form */
		else {
			$_SESSION['value_array'] = $_POST;
			$_SESSION['error_array'] = $form->getErrorArray();
			header("Location: " . $session->referrer);
		}
	}

	/**
	* procUpload - Processes the user submitted upload form,
	* if errors are found, the user is redirected to correct the
	* information, if not, the users pictures are processed and
	* added to the database.
	*/
	function procUpload() {
		global $session, $form, $database, $status;
		//$session->lock(true); //Make any asynchonouse procedure wait to finish here
		$filelist = '';
		$filecount = 0;
		$imagecount = 0;
		$zipcount = 0;
		//$workdir = FILESYSTEM . INCOMING . '/' . $session->sessid;
        $workdir = $session->getWorkdir();
        $status = PUBLIC_STATUS; // Default status is Public
        
		/**
		* This function helps process the fractional dms value to
		* numerical value.
		* param: int array[$degree, $minute, $second]
		* return: float
		*/
		function tf($str) {
		    if($p = strpos($str,'/')){
				$remainder =  floatval(substr($str,$p+1));
				if ($remainder == 0) return 0;
			    return floatval(substr($str,0,$p)) / $remainder ;
			}else{
			    return floatval($str);
			}
		}

		function dms_to_float($arr) {
			return tf($arr[0]) + tf($arr[1]) / 60 + tf($arr[2]) / 3600;
		}
        
        function degCar($type, $val){
            $vals = Array('N','NNE','NE','ENE',
                          'E','ESE','SE','SSE',
                          'S','SSW','SW','WSW',
                          'W','WNW','NW','NNW');
            return $vals[intval((((tf($val) + 11.25) / 22.5) % 16))];
            //Ignored True North
        }
        
		function getExifDate($exif){
			$str = date("Y-m-d");
			if (isset($exif['DateTimeOriginal'])){
				$str = $exif['DateTimeOriginal'];
			}else if(isset($exif['DateTimeDigitized'])){
				$str = $exif['DateTimeDigitized'];
			}else if(isset($exif['DateTime'])){
				$str = $exif['DateTime'];
			}
			$takendate = (split(' ', $str));
			$takendate = str_replace(':', '-', $takendate[0]);
			if ($takendate == "NOW()"){
			    return 'NULL';
			}
			return $takendate;
		}

		/**
		* This function takes location of an image, parses it
		* and inputs the relevant information into database.
		* param: string $location
		* return: void
		*/
		function procImage($path) {
			global $session, $database, $form, $status;
			
			$ext = substr(strrchr(basename($path), '.'), 1);

			if (!((strcasecmp($ext, "jpg") == 0) || (strcasecmp($ext, "jpeg") == 0) ||
				 (strcasecmp($ext, "wbmp") == 0) || (strcasecmp($ext, "gif") == 0) ||
                 (strcasecmp($ext, "png") == 0)))
				return false;

			$photoid = $database->getSequenceID('photos');
			$img = FILESYSTEM . INCOMING . '/' . $photoid . basename($path);
			rename($path, $img);

			//Set default values

			if (($exif = exif_read_data($img)) != false) {
				if (array_key_exists('GPSLatitude', $exif)) {
					$lat = $long = $alt = 0;
					$datum = $takendate = '';
					$long = dms_to_float($exif['GPSLongitude']);
					$lat = dms_to_float($exif['GPSLatitude']);
					$alt = !empty($exif['GPSAltitude']) ? tf($exif['GPSAltitude']) : 0;
					$dir_deg = !empty($exif['GPSImgDirection']) ? tf($exif['GPSImgDirection']) : 'NULL';
                    $dir_car = !empty($exif['GPSImgDirection']) ? "'".degCar($exif['GPSImgDirectionRef'],$exif['GPSImgDirection'])."'" : 'NULL';
					if (strcasecmp('W', $exif['GPSLongitudeRef']) == 0)
						$long *= -1;
					if (strcasecmp('S', $exif['GPSLatitudeRef']) == 0)
						$lat *= -1;
					$takendate = getExifDate($exif);
					$datum = trim($exif['GPSMapDatum']);
					$userid = $session->userinfo['id'];
                    $location = basename($img);
                    $uploadd = date("Y-m-d");
                    //$pnt = "geomfromtext('POINT($long $lat)',4326)";
                    $pnt = 'NULL';
					$q = "INSERT INTO PHOTOS (id,location,userid,long,lat,takendate,uploaddate,datum,alt,point,status,dir,dir_deg) " .
						 "VALUES ($photoid ,'$location', $userid, $long, $lat, '$takendate', '$uploadd', '$datum', $alt, $pnt, $status, $dir_car, $dir_deg); ";

				} else {
					$takendate = getExifDate($exif);
					$q = "INSERT INTO PHOTOS (id,location,userid,takendate,uploaddate,status) " .
					"values (" . $photoid . ",'" . basename($img) . "'," . $session->userinfo['id'] . ",'" . $takendate . "', '" . date("Y-m-d") . "',$status); ";
				}
			} else {
				$q = "insert into photos (id,location,userid,takendate,uploaddate,status) " .
				"values (" . $photoid . ",'" . basename($img) . "'," . $session->userinfo['id'] . ",'" . date("Y-m-d") . "', '" . date("Y-m-d") . "',$status); ";
			}
			//echo $q;
			//die();

			$result = $database->query($q) or die('Query failed: ' . pg_last_error() . $q .
				"<br>Exif:<pre>". print_r($exif, true)."</pre>".
				"</br>You may report the problem to: pavel@unh.edu");
		}

		/**
		* This function takes location of a zip archive and extracts
		* the files into specified location
		* param: string $zip, string $destination
		* return: string array[]
		*/
		function procZip($file, $destination, $num) {
			$list = '';
			$archive = new PclZip($file);
			if ($archive->extract(PCLZIP_OPT_PATH, $destination) == 0) {
				//die("Error : " . $archive->errorInfo(true));
				$form->setError("userfile$num", "Error unzipping: ".$archive->errorInfo(true) );
				return false;
			}else{
				return true;
			}
		}
		
		/**
		* This function takes location of a zip archive and extracts
		* the files into specified location
		* param: string $zip, string $destination
		* return: string array[]
		*/
		function procRar($file, $destination, $num) {
		    //error_log("procRar($file, $destination, $num)");
			$list = '';
			$archive = rar_open(realpath($file));
			if ($archive === FALSE){
				$form->setError("userfile$num", "Error opening RAR:".basename($file));
				return false;
			}
			
            $list = rar_list($archive);
            if ($list === FALSE){
				$form->setError("userfile$num", "Error getting entries for RAR:".basename($file));
				return false;
			}
            foreach($list as $entry) {
               $entry->extract($destination); // extract to the current dir
            }
            rar_close($archive);
			return true;
		}
		
		/**
		* This function recusively processes all the directories and
		* images within
		*/
		function procDir($dir) {
		    //error_log($dir);
			$list = scandir($dir);
			if (sizeof($list) > 2) {
				$list = array_slice($list, 2);
				foreach ($list as $file) {
					$tmp = $dir . '/' . $file;
					//error_log($tmp);
					if (is_file($tmp) and is_image($tmp) 
					    //and 0 != strpos($file, "._")
					   )
					{
						procImage($tmp);
					}
					if (is_dir($tmp) and $file != "__MACOSX" and $file != "thumbnails")
					{
					    procDir($tmp);
					}
				}
			}
		}

		/**
		* deletes the temporary directory for the session with all files in it
		*/
		function cleanup($dirname) {
			if (is_dir($dirname))
				$dir_handle = opendir($dirname);
			if (!$dir_handle)
				return false;
			while ($file = readdir($dir_handle)) {
				if ($file != "." && $file != "..") {
					if (!is_dir($dirname . "/" . $file))
						unlink($dirname .
						"/" . $file);
					else
						cleanup($dirname .
						'/' . $file);
				}
			}
			closedir($dir_handle);
			rmdir($dirname);
			return true;
		}
		
		if (isset($_POST['private']) and $_POST['private'] == 'Yes'){
		    $status = PRIVATE_STATUS;
        }

		//For each userfile
		if (!is_dir($workdir)) {
			mkdir($workdir);
		}
		$count = 0;
		$ziplist = array();
		while (list ($key, $value) = each($_FILES['userfile']['name'])) {
			$count++;
			if (!empty ($value)) {
				$filename = $value;
				$uploadfile = $workdir . '/' . $filename;
			}
			if (move_uploaded_file($_FILES['userfile']['tmp_name'][$key], $uploadfile)) {
				$filecount++;
				chmod("$uploadfile", 0777);
				$ext = strtolower(substr(strrchr($uploadfile, '.'), 1));
				if (in_array($ext, array( "jpg", "jpeg", "bmp", "gif", "png"))) {
					$imagecount++;
				} else {
					if (strcasecmp($ext, "zip") == 0) {
						if (procZip($uploadfile, $workdir, $count)){
							$zipcount++;
							unlink($uploadfile);
							array_push($ziplist, $uploadfile);
						}
					} else if (strcasecmp($ext, "rar") == 0) {
						if (procRar($uploadfile, $workdir, $count)){
							$zipcount++;
							unlink($uploadfile);
							array_push($ziplist, $uploadfile);
						}
					} else {
						$form->setError("userfile$count", 
							"\"$ext\" is an unsupported format.");
						unlink($uploadfile);
					}
				}
			}
		}

		procDir($workdir);
		cleanup($workdir);

		if ($zipcount > 0) $_SESSION['ziplist'] = $ziplist;

		$form->setValue("count", $filecount);
		$form->setValue("imagecount", $imagecount);
		$form->setValue("zipcount", $zipcount);

		$session->lock(false);
		$form->setValue("postback", true);

		if ($count) {
			//sucess
			$_SESSION['value_array'] = $form->getValueArray(); //$_POST; post was assigned here before
			$_SESSION['error_array'] = $form->getErrorArray();
			header("Location: upload.php");
		} else {
			//errors
			$form->setError("userfile", "*Failed to upload any files");
			$_SESSION['value_array'] = $_POST;
			$_SESSION['error_array'] = $form->getErrorArray();
			header("Location: upload.php");
		}
	}

	/**
	* procEditPhoto - processes the user submitted photo information form,
	* if errors are found, the user is redirected to correct the
	* information, if not, the users pictures are processed and
	* added to the database.
	*/
	function procEditPhoto() {
			global $session, $form, $gallery;
			/* Photo edit attempt */
			if ($_POST['subeditphoto'] == $_SESSION['subeditphoto'])
				$retval = $gallery->editPhoto($_POST['subeditphoto'], 
                                            $_POST['lat'], 
                                            $_POST['long'], 
                                            $_POST['alt'], 
                                            $_POST['dir'], 
                                            $_POST['status'], 
                                            $_POST['categoryid'], 
                                            $_POST['description']);
			else
				$retval = false;
			/* Photo edit successful */
			if ($retval) {
				$_SESSION['photoedit'] = true;
				header("Location: " . $_SESSION['url1']);
			}
			/* Error found with form */
			else {
				$_SESSION['value_array'] = $_POST;
				$_SESSION['error_array'] = $form->getErrorArray();
				header("Location: " . $_SESSION['url2']);
			}
	}

	function procDownload() {
		global $database, $gallery, $session;
		$workdir = FILESYSTEM . INCOMING . '/' . $session->sessid;

		$query = "SELECT DISTINCT photos.id, ".
								"(SELECT email FROM users WHERE photos.userid = users.id) as email, ".
						"photos.location, photos.description, " .
						"photos.long, photos.lat, photos.takendate, " .
						"photos.alt,  photos.dir, (SELECT name FROM categories WHERE photos.categoryid".
						" = categories.id) as category FROM photos ";

		if (!empty ($_POST['list'])) {
			$query .= " WHERE ";

			$n = sizeof($_POST['list']);

			$lim = $session->getDownloadLimit();

			if($lim && $n > $lim){
				$n = $lim;
			}

			for ($i = 0; $i < $n; $i++) {
				$query .= " photos.id = ". intval($_POST['list'][$i]);
				if ($i < $n - 1)
					$query .= " OR";
			}
		} else {
			//if (!empty($_SESSION['query_where_clause']))
			//	$query.= " WHERE (".$_SESSION['query_where_clause']." )";
			//else
			$query .= " WHERE 1=0 ";
		}

		error_log($query);

		$result = $database->query($query);

		$photos = '';
		$str = '';
		$output = '';
		$archive = '';

		//If the requested data with pictures is CSV, assign the text data to string
		if (strcmp($_POST['get'], "csv") == 0) {
			$str = "id,\tfilename,\temail,\tlongitude,\tlatitude,\taltitude,\tdirection,\tdate,\tcategory,\tdescription\n";
			while ($line = pg_fetch_array($result, null, PGSQL_ASSOC)) {
				$photos .= $line['location'] . ",";
				$str .= $line['id'] .
				",\t" . $line['location'] .
				",\t" . $line['email'] .
				",\t" . $line['long'] .
				",\t" . $line['lat'] .
				",\t" . $line['dir'] .
				",\t" . $line['takendate'] .
				",\t" . $line['category'] .
				",\t\"" . $line['description'] . "\"\n";
			}
			$output = "data.csv";
			$archive = "data.zip";
		}
		else if (strcmp($_POST['get'], "kmz") == 0) {
			$str = '<kml xmlns="http://www.opengis.net/kml/2.2">
                    <Document>
                        <name>EOMF Photos</name>
                        <open>1</open>
                        <Style id="photo_style">
                            <IconStyle>
                                <color>ffffffff</color>
                                <scale>0.8</scale>
                                <Icon>
                                <href>http://www.iconarchive.com/icons/newformula.org/canon-digital-camera/32/Ixus-430-icon.png</href>
                                </Icon>
                            </IconStyle>
                            <LabelStyle>
                                <scale>0</scale>
                            </LabelStyle>
                        </Style>
                        <Folder>
                            <name>Photos</name>';

			while ($line = pg_fetch_array($result, null, PGSQL_ASSOC)) {				
                if (!empty ($line['long']) && !empty ($line['lat'])):
                    $photos .= $line['location'] . ',';
                    if(empty($line['dir_deg']))
                        if(empty($line['dir']))
                            $dir = 'N';
                        else $dir = trim($line['dir']);
                    else
                        $dir = floatval($line['dir_deg']);
                        
                    if(empty($line['alt']))
                        $line['alt'] = '0';
                    $fname = str_shorten($line['location']);
                    //$fname = $line['location'];
                    $id = $line['id'];
                    $description =  "<img  width=\"300\" height=\"224\" class='thumb' src=\"".basename($line['location'])."\"/> <br/>";
                    $description .= "Date: ".$line['takendate']."<br/>";
                    $description .= "Location: ".loc2str($line['long'],$line['lat'])."<br/>";
                    if (!empty($line['dir']))
                        $description .= "Aspect: $dir <br/>";
                    if (!empty($line['category']))
                        $description .= "Category: {$line['category']}<br/>";
                    if (!empty($line['description']))
                        $description .= wordwrap("Field Notes: ".$line['description'], 45, "<br />\n");
                        
                    $str .= "
                        <Placemark id=\"{$id}\">
                            <styleUrl>#photo_style</styleUrl>
                            <name>Photo: {$fname}</name>
                            <description> <![CDATA[{$description}]]> </description>
                            <Point><coordinates>{$line['long']},{$line['lat']},{$line['alt']}</coordinates></Point>
                       </Placemark>\n";
                endif;
			}

			$str .= " </Folder> </Document> </kml>";

			$output = "doc.kml";
			$archive = "data.kmz";
		}
		else if (strcmp($_POST['get'], "shp") == 0) {
			$def = array(
			  array("id",		 "N", 3, 0),
			  array("DATUM",	 "C", 50),
			  array("LON",		 "N", 13, 8),
			  array("LAT",		 "N", 12, 8),
			  array("ALTITUDE",  "N", 8, 2),
			  array("PICTURE",	 "C", 100),
			  array("DATE",		 "C", 10),
			  array("LOCALTIME", "C", 30),
			  array("CATEGORY",  "C", 30),
			  array("EMAIL",	 "C", 50),
			  array("SERIALNUM", "N", 9, 2)
			);

			unlink(FILESYSTEM.INCOMING."/shapefile.shp");
			unlink(FILESYSTEM.INCOMING."/shapefile.shx");
			unlink(FILESYSTEM.INCOMING."/shapefile.dbf");

			if((dbase_create(FILESYSTEM.INCOMING."/shapefile.dbf", $def)) && ($shph = shp_create(FILESYSTEM.INCOMING."/shapefile.shp", SHPT_POINT))){
				$db = dbase_open(FILESYSTEM.INCOMING.'/shapefile.dbf',2);
				$id = 0;
				while ($line = pg_fetch_array($result, null, PGSQL_ASSOC)){
					$photos .= $line['location'] . ",";
					dbase_add_record($db, array($line['id'],'WGS 84',$line['long'],$line['lat'],$line['alt'],$line['location'],$line['takendate'],date(DATE_RFC822),$line['category'],$line['email'],3101076));
					$shpobj = shp_create_object(SHPT_POINT,$id,1,array(0, 1),array(),1,array($line['long']),array($line['lat']),array($line['alt']), array());
					$res = shp_write_object($shph, -1, $shpobj);
					$id++;
				}
				dbase_close($db);
				$res = shp_close($shph);
				$output = "shapefile.shp,".
						  FILESYSTEM.INCOMING."/shapefile.shx,".
						  FILESYSTEM.INCOMING."/shapefile.dbf,".
						  "readme.txt,".
						  "shapefile.prj";
				$archive = "data.zip";
			}
		}
		else echo "error";

		//echo "<pre>".$str."</pre>";  print_r($_POST);  die();

		if (!empty($str)){
			$fh = fopen(FILESYSTEM . INCOMING . "/" . $output, 'w') or die("can't open file");
			fwrite($fh, $str);
			fclose($fh);
		}

		//Include smaller versions of original files
		if (strcmp($_POST['img'], "small") == 0) {
			$r = explode(",", $photos);
			$p = pg_fetch_all($result);
			//-1 because there is always a trailing comma
			for ($i = 0; $i < sizeof($r) - 1; $i++) {
				$tmp = $r[$i];
				$r[$i] = FILESYSTEM . GAL_BIGTHUMBS . "/" . $tmp;
				$gallery->makeBigThumb($p[$i], $r[$i]);
			}
			$files = implode(",", $r);
		} else {
			//still need to set location for photos
			$r = explode(",", $photos);
			for ($i = 0; $i < sizeof($r) - 1; $i++) {
				$r[$i] = FILESYSTEM . INCOMING . '/' . $r[$i];
			}
			$files = implode(",", $r);
		}

		//Here are appended any additional files to be archived
		$files .= FILESYSTEM . INCOMING . "/" . $output;

		$zip = new PclZip(FILESYSTEM . INCOMING . '/archive.zip');
		$v_list = $zip->create($files, PCLZIP_OPT_REMOVE_ALL_PATH);
		if ($v_list == 0) {
			die("Error : " . $zip->errorInfo(true));
		}

		force_download(file_get_contents(FILESYSTEM.INCOMING.'/archive.zip'), $archive);
	}

	/**
	* procDeleteDuplicates - processes the user submitted criteria for deleting duplicate photos
	* search for duplicates is done within the specified criteria, whic his date of upload by default
	*/
	function procDeleteDuplicates() {
		global $session, $form, $gallery;
			/* Photo edit attempt */
        if(!isset($_POST['undo'])){
            $retval = $gallery->deleteDuplicates($_POST['subdel_date'], $_SESSION['cur_uid']);
        }else{
            $retval = $gallery->undelete($_POST['subdel_date'], $_SESSION['cur_uid']);
        }
		/* Photo edit successful */

		if ($retval) {
			header("Location: " . $session->referrer);
		}
		else {
			$_SESSION['value_array'] = $_POST;
			$_SESSION['error_array'] = $form->getErrorArray();
			header("Location: " . $session->referrer);
		}

	}
};

/* Initialize process */
$process = new Process;
?>
