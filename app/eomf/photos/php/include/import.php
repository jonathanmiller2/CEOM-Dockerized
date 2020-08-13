<?	/**
	* procUpload - Processes the user submitted upload form,
	* if errors are found, the user is redirected to correct the
	* information, if not, the users pictures are processed and
	* added to the database.
	*/
require_once ("config.inc");
require_once ("form.php");
require_once ("gallery.php");
require_once ("func.php");
require_once ('pclzip.lib.php');

class Import{
    $count = 0;
    $filelist = '';
    $filecount = 0;
    $imagecount = 0;
    $zipcount = 0;
    $workdir = '';
    $proc_upload = true;
    $move = true;

    function Import($workdir = '/tmp/php/import/', $upload = true, $move = true){
        $this->workdir = $workdir;
        $this->proc_upload = $upload;
        $this->move = $move;
    }

    /**
    * This function helps process the fractional dms value to
    * numerical value.
    * param: int array[$degree, $minute, $second]
    * return: float
    */
    function tf($str) {
	    $r = split('/', $str);
	    return $r[0] / $r[1];
    }

    function dms_to_float($arr) {
	    return tf($arr[0]) + tf($arr[1]) / 60 + tf($arr[2]) / 3600;
    }

    function getExifDate($exif){
	    $str = date("Y-m-d");
	    if (isset($exif['DateTime'])){
		    $str = $exif['DateTime'];
	    }else if(isset($exif['DateTimeDigitized'])){
		    $str = $exif['DateTimeDigitized'];
	    }else if(isset($exif['DateTimeOriginal'])){
		    $str = $exif['DateTimeOriginal'];
	    }
	    $takendate = (split(' ', $str));
			    $takendate = str_replace(':', '-', $takendate[0]);
	    return $takendate;
    }

    /**
    * This function takes location of an image, parses it
    * and inputs the relevant information into database.
    * param: string $location
    * return: void
    */
    function procImage($path) {
	    global $database;
	    $ext = substr(strrchr(basename($path), '.'), 1);

	    if (!((strcasecmp($ext, "jpg") == 0) || (strcasecmp($ext, "jpeg") == 0) ||
		     (strcasecmp($ext, "wbmp") == 0) || (strcasecmp($ext, "gif") == 0) ||
                (strcasecmp($ext, "png") == 0)))
		    return false;

	    $photoid = $database->getSequenceID('photos');
	    if($this->move){
	        $img = FILESYSTEM . INCOMING . '/' . $photoid . basename($path);
	        rename($path, $img);
	    }

	    //Set default values

	    if (($exif = exif_read_data($img)) != false) {
		    if (in_array('GPS', $exif)) {
			    $lat = $long = $alt = 0;
			    $datum = $takendate = '';
			    $long = dms_to_float($exif['GPSLongitude']);
			    $lat = dms_to_float($exif['GPSLatitude']);
			    $alt = isset ($exif['GPSAltitude']) ? $exif['GPSAltitude'] : 0;
			    if (strcasecmp('W', $exif['GPSLongitudeRef']) == 0)
				    $long *= -1;
			    if (strcasecmp('S', $exif['GPSLatitudeRef']) == 0)
				    $lat *= -1;
			    $takendate = getExifDate($exif);
			    $datum = trim($exif['GPSMapDatum']);

			    $userid = $session->userinfo['id'];

			    /*$q = "insert into photos (id,location,userid,long,lat,takendate,uploaddate,datum,alt,point) " .
			    "values (" . $photoid . ",'" . basename($img) . "'," . $userid . "," . $long . "," . $lat . ",'" .
			    $takendate . "','" . date("Y-m-d") . "','" . $datum . "'," . $alt .
			    ", GeometryFromText('POINT(" . $long . " " . $lat . ")',4326)" . "); ";*/

			    $q = "INSERT INTO PHOTOS (id,location,userid,long,lat,takendate,uploaddate,datum,alt) " .
								    "VALUES ($photoid ,'".basename($img)."', $userid, $long, $lat, '$takendate', '".date("Y-m-d")."', '$datum', $alt); ";

		    } else {
			    $takendate = getExifDate($exif);
			    $q = "INSERT INTO PHOTOS (id,location,userid,takendate,uploaddate) " .
			    "values (" . $photoid . ",'" . basename($img) . "'," . $session->userinfo['id'] . ",'" . $takendate . "', '" . date("Y-m-d") . "'); ";
		    }
	    } else {
		    $q = "insert into photos (id,location,userid,takendate,uploaddate) " .
		    "values (" . $photoid . ",'" . basename($img) . "'," . $session->userinfo['id'] . ",'" . date("Y-m-d") . "', '" . date("Y-m-d") . "'); ";
	    }
	    //echo $q;
	    //die();

	    $result = $database->query($q) or die('Query failed: ' . pg_last_error() . $q ."<br>Exif:<pre>". print_r($exif, true)."</pre>");
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
    * This function recusively processes all the directories and
    * images within
    */
    function procDir($dir) {
	    $list = scandir($dir);
	    if (sizeof($list) > 2) {
		    $list = array_slice($list, 2);
		    foreach ($list as $file) {
			    $tmp = $dir . '/' . $file;
			    if (is_file($tmp))
				    procImage($tmp);
			    if (is_dir($tmp));
			    procDir($tmp);
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

    function moveUploads($dest){
        global $form;
        $count = 0;
        while (list ($key, $value) = each($_FILES['userfile']['name'])) {
            $count++;
            if (!empty ($value)) {
	            $filename = $value;
	            $uploadfile = $dest . '/' . $filename;
            }
            if (move_uploaded_file($_FILES['userfile']['tmp_name'][$key], $uploadfile)) {
	            $this->filecount++;
	            chmod("$uploadfile", 0777);
	            $ext = substr(strrchr($uploadfile, '.'), 1);
	            if ((strcasecmp($ext, "jpg") == 0) || (strcasecmp($ext, "jpeg") == 0) ||
		            (strcasecmp($ext, "wbmp") == 0) || (strcasecmp($ext, "gif") == 0) ||
                    (strcasecmp($ext, "png")==0) ) {
		            $this->imagecount++;
	            } else {
		            if (strcasecmp($ext, "zip") == 0) {
			            if ($this->procZip($uploadfile, $dest, $count)){
				            $this->zipcount++;
				            unlink($uploadfile);
				            array_push($ziplist, $uploadfile);
			            }
		            } else {
			            $form->setError("userfile$count", 
				            "$filename: $ext of file is an unsupported format.");
			            unlink($uploadfile);
		            }
	            }
            }
        }
    }

    function process(){
        global $form;
        //For each userfile
        if (!is_dir($this->workdir)) {
	        mkdir($this->workdir);
        }

        ifmoveUploads($this->workdir);
        procDir($this->workdir);
        cleanup($this->workdir);

        $form->setValue("count", $this->filecount);
        $form->setValue("imagecount", $this->imagecount);
        $form->setValue("zipcount", $this->zipcount);

        $form->printErrors();
    }
}
?>
