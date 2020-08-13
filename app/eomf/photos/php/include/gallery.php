<?
/**
 * Gallery.php
 *
 * The Database class is meant to simplify the task of accessing
 * information from the website's database.
 *
 * Written by: Pavel Dorovskoy
 */

require_once "session.php";
require_once "thumbnail.php";

class Gallery {

    var $maxcols = 4;
    var $thumbsize = 150;
    var $save = true;
    var $items;
    var $clause;
    var $photos;
    var $cats;
    var $status_clause = '';
    var $checkbox = false;
    var $modis_timeseries = true;

    function Gallery() {
        global $session;
        
	    $this->items = "id, location, userid, photogroupid, description, long, lat,
           regionid, takendate, uploaddate, datum, alt, categoryid, (SELECT name FROM categories WHERE id = categoryid) as categoryname ,dir, status, hash";

        $this->status_clause = $session->filterClause();
	
	//$cats = $database->queryFetch("SELECT id, name FROM categories");
	
	/* User submitted login form */
        if (isset ($_GET['view'])) {
            $this->viewPhoto();
        }
        if (isset ($_GET['edit'])) {
            $this->showEditPhoto();
        }
        /*else {
            header("Location: " . $session->referrer);
        }*/
    }

    function prepareFromSQL($clause, $items = "*"){
		$this->clause = $clause;
        $this->items = $items;
    }

    function showMapPopUp($id,$lon,$lat){
		?>

    	<script language="JavaScript">
		<!-- Begin
		function popUp(URL) {
		day = new Date();
		id = day.getTime();
		eval("page" + id + " = window.open(URL, '" + id + "', 'toolbar=0,scrollbars=0,location=0,statusbar=0,menubar=0,resizable=1,width=450,height=400');");
		}
		// End -->
		</script>

		<?
		echo "| <a href = \"javascript:popUp('popup.php?photo=$id&lon=$lon&lat=$lat')\">Map Photo</a>";
		echo "<br/><br/>\n";
		/*
		<form>
		<input type=button value="Show Map" onClick="javascript:popUp('')">
		</form>

		<?*/
    }

    function viewPhoto($id){
        global $database,$session;
        $result = $database->query("SELECT userid, location, long, lat, alt, name, takendate, dir, description " .
                "FROM photos LEFT OUTER JOIN categories " .
                "ON(photos.categoryid = categories.id) " .
                "WHERE photos.id = ".intval($id));
        $photo = pg_fetch_all($result);
        $photo = $photo[0];
        $user = $database->getUserInfoById($photo['userid']);
        $location = INCOMING . '/'. $photo['location'];
        $img_thumb = GAL_BIGTHUMBS . '/' . $photo['location'];
        
        $this->makeBigThumb($photo,FILESYSTEM.$img_thumb);
        //try to disable caching
        //header("Cache-Control: no-cache, must-revalidate"); // HTTP/1.1
        //header("Expires: Mon, 26 Jul 1997 05:00:00 GMT"); // Date in the pas

		if(isset($photo['long']) && isset($photo['lat']) && $photo['long'] != 0 && $photo['lat'] != 0)
			$this->showMapPopUp($id,$photo['long'],$photo['lat']);
        echo "<h3>View Photo</h3>";
        echo "<div id=\"bigthumb\" >";
        echo "<a href=\"".WEB.$location."\">";
        echo "<img src=\"".WEB.$img_thumb."\" alt=\"".basename($location)."\" border=\"0\"/>";
        echo "</a><table align=\"center\" width=\"500px\" cellpadding=\"0\">";
        echo "<tr><td>User: </td><td>" . $user['username']."</td></tr>";
        echo "<tr><td>Filename: </td><td>" . $photo['location']."</td></tr>";
        if ($photo['name'] != '')
        	echo "<tr><td>Category: </td><td>" . $photo['name'] ."</td></tr>";
        if ($photo['description'] != '')
        	echo "<tr><td>Field Notes: </td><td>" . $photo['description']. "</td></tr>";
        //echo $database->query("")
        echo "<tr><td></td><td><a target='_blank' href='index.php?a=view&exif=$id'>EXIF</a></td></tr>";
        echo "<tr><td></td><td>";
        if ($photo['userid'] == $session->userinfo['id'] || $session->userlevel == ADMIN_LEVEL){
                $_SESSION['url1'] = $_SERVER['REQUEST_URI'];
                echo "<a href=\"index.php?a=edit&photo=$id\">(Edit)</a><br/>";
        }
        echo "</td></tr></table> </div>";

        //FIXME: for some reason $photo['id'] doesn't work
    }

    function showEditPhoto($photoid){
        global $session,$database,$form;

        $session->referrer = $_SERVER['REQUEST_URI']; // For some reason doesn't do anything
        $_SESSION['url2'] = $_SERVER['REQUEST_URI'];  // which is why SESSION is used

        function fill_value($field,$photo){
            global $form;

            if($form->isValueSet($field))
                return $form->value($field);
            else
                return $photo[$field];
        }

        $status_r = array(array(DELETED_STATUS, "Deleted"),
                          array(PUBLIC_STATUS,  "Public"),
                          array(PRIVATE_STATUS, "Private"));

        if ($photoid != "" && $id = intval($photoid)){

            $result = $database->query("SELECT $this->items FROM photos WHERE id = $id");
            $photo  = pg_fetch_all($result);
            $photo = $photo[0];

            if($session->logged_in){
                echo "<div id=\"photo-edit\">";
                echo "<h2>Photo Edit: ";
                echo $photo['location'];
                echo "</h2>";

                $this->showThumb($photo);
                echo "<br/>Date taken: " . $photo['takendate'] . " <br/>";
                echo "<br/>";

                if($form->num_errors > 0){
                    echo "<td><font size=\"2\" color=\"#ff0000\">".
                        $form->num_errors." error(s) found</font></td>";
                }else{
                    if(isset($_SESSION['photoedit'])){
       		            unset($_SESSION['photoedit']);
       		            echo "<b>$session->username</b>, your photo has been successfully updated.<br>";
	                }                
                }
?>
<form action="process.php" method="post">
    <table border="0" cellspacing="0" cellpadding="3">
        <tr>
            <td>Longitude:</td>
            <td><input type="text" name="long" value="<?echo fill_value("long",$photo); ?>"/> Decimal degrees.</td>
            <td><? echo $form->error("long"); ?></td>
        </tr>
        <tr>
            <td>Latitude:</td>
            <td><input type="text" name="lat" value="<?echo fill_value("lat",$photo); ?>"/> Decimal degrees.</td>
            <td><? echo $form->error("lat"); ?></td>
        </tr>
        <tr>
            <td>Altitude:</td>
            <td><input type="text" name="alt" value="<?echo fill_value("alt",$photo); ?>"/> Meters.</td>
            <td><? echo $form->error("alt"); ?></td>
        </tr>
        <tr>
            <td>Direction:</td>
            <td><input type="text" name="dir" value="<?echo fill_value("dir",$photo); ?>"/> Cardinal direction. (i.e. NNE)</td>
            <td><? echo $form->error("dir"); ?></td>
        </tr>
<? if ($session->isOwner($photo) or $session->isAdmin()){ ?>
        <tr>
            <td>Status:</td>
            <td><? build_select_box_array($status_r,"status",fill_value("status",$photo)); ?> </td>
            <td><? echo $form->error("status"); ?></td>
        </tr>
<? } ?>
        <tr>
            <td>Category:</td>
            <td><? 
                $result = $database->query("SELECT id,name FROM categories");
                build_select_box($result, 'categoryid',fill_value("categoryid",$photo));?></td>
            <td><? echo $form->error("categoryid"); ?> </td>
        </tr>
        <tr>
            <td>Field Notes:</td>
            <td><textarea name="description" rows="5" cols="50"><? echo fill_value("description",$photo);?></textarea></td>
            <td><? echo $form->error("description"); ?></td>
        </tr>
        <tr>
            <td colspan="2" align="right">
            <input type="hidden" name="subeditphoto" value="<?
                    echo $photo['id']; $_SESSION['subeditphoto'] = $photo['id']; ?>"/>
            <input type="submit" value="Edit Photo"/></td></tr>
        <tr>
            <td colspan="2" align="left"></td></tr>
    </table>
</form></div>
<?
            }
        }
    }
    function showEditPhotoList($photo_r){
        global $session,$database,$form;

        $session->referrer = $_SERVER['REQUEST_URI']; // For some reason doesn't do anything
        $_SESSION['url2'] = $_SERVER['REQUEST_URI'];  // which is why SESSION is used

        function fill_value($field,$photo){
            global $form;

            if($form->isValueSet($field))
                return $form->value($field);
            else
                return $photo[$field];
        }

        $status_r = array(array(0,"Deleted"),array(1,"Public"),array(2,"Private"));

        $q = "SELECT $items FROM photos WHERE id in ( NULL ";
        foreach($photo_r as $pid):
            $q.= ', '.intval($pid);
        endforeach;
        $q .= ');';
        print "<br><pre>"+$q+"</pre><br>";
        
        if ($photoid != "" && $id = intval($photoid)){

            $result = $database->query("SELECT $this->items FROM photos WHERE id = $id");
            $photo  = pg_fetch_all($result);
            $photo = $photo[0];

            if($session->logged_in){
                echo "<div id=\"photo-edit\">";
                echo "<h2>Photo Edit: ";
                echo $photo['location'];
                echo "</h2>";

                $this->showThumb($photo);
                echo "<br/>Date taken: " . $photo['takendate'] . " <br/>";
                echo "<br/>";

                if($form->num_errors > 0){
                    echo "<td><font size=\"2\" color=\"#ff0000\">".
                        $form->num_errors." error(s) found</font></td>";
                }else{
                    if(isset($_SESSION['photoedit'])){
       		            unset($_SESSION['photoedit']);
       		            echo "<b>$session->username</b>, your photo has been successfully updated.<br>";
	                }                
                }
?>
<form action="process.php" method="post">
    <table border="0" cellspacing="0" cellpadding="3">
        <tr>
            <td>Longitude:</td>
            <td><input type="text" name="long" value="<?echo fill_value("long",$photo); ?>"/> Decimal degrees.</td>
            <td><? echo $form->error("long"); ?></td>
        </tr>
        <tr>
            <td>Latitude:</td>
            <td><input type="text" name="lat" value="<?echo fill_value("lat",$photo); ?>"/> Decimal degrees.</td>
            <td><? echo $form->error("lat"); ?></td>
        </tr>
        <tr>
            <td>Altitude:</td>
            <td><input type="text" name="alt" value="<?echo fill_value("alt",$photo); ?>"/> Meters.</td>
            <td><? echo $form->error("alt"); ?></td>
        </tr>
        <tr>
            <td>Direction:</td>
            <td><input type="text" name="dir" value="<?echo fill_value("dir",$photo); ?>"/> Cardinal direction. (i.e. NNE)</td>
            <td><? echo $form->error("dir"); ?></td>
        </tr>
        <tr>
            <td>Status:</td>
            <td><? build_select_box_array($status_r,"status",fill_value("status",$photo)); ?> </td>
            <td><? echo $form->error("status"); ?></td>
        </tr>
        <tr>
            <td>Category:</td>
            <td><? 
                $result = $database->query("SELECT id,name FROM categories");
                build_select_box($result, 'categoryid',fill_value("categoryid",$photo));?></td>
            <td><? echo $form->error("categoryid"); ?> </td>
        </tr>
        <tr>
            <td>Field Notes:</td>
            <td><textarea name="description" rows="5" cols="50"><? echo fill_value("description",$photo);?></textarea></td>
            <td><? echo $form->error("description"); ?></td>
        </tr>
        <tr>
            <td colspan="2" align="right">
            <input type="hidden" name="subeditphoto" value="<?
                    echo $photo['id']; $_SESSION['subeditphoto'] = $photo['id']; ?>"/>
            <input type="submit" value="Edit Photo"/></td></tr>
        <tr>
            <td colspan="2" align="left"></td></tr>
    </table>
</form></div>
<?
            }
        }
    }
    
    function editPhoto($id, $lat, $long, $alt, $dir, $status, $categoryid, $description){
        global $database, $form;
        $latval = $longval = $altval = $dirval = $statusval = $categoryidval = $descriptionval = 0;

        if(isset($lat)){
            $field = "lat";

            $latval = floatval($lat);
            if(! is_numeric($latval)){
                $form->setError($field, "* Enter a numerical value.");
            }
            else{
                if($latval < -180 || $latval > 180){
                    $form->setError($field, "* Enter value between -180 and 180");
                }
            }
        }
        else unset($latval);

        if(isset($long)){
            $field = "long";

            $longval = floatval($long);
            if(!is_numeric($longval)){
                $form->setError($field, "* Enter a numerical value.");
            }
            else{
                if($longval < -180 || $longval > 180){
                    $form->setError($field, "* Enter value between -90 and 90");
                }
            }
        }
        else unset($longval);

        if(isset($alt)){
            $field = "alt";

            $altval = floatval($alt);
            if(!is_numeric($altval)){
                $form->setError($field, "* Enter a numerical value.");
            }
        }
        else unset($altval);

        if(isset($categoryid)){
            $field = "categoryid";

            $categoryidval = intval($categoryid);
            if($categoryidval != 0 && !$categoryidval){
                $form->setError($field, "* Error parsing form, try again.");
            }
        }
        else unset($categoryidval);

        if(isset($status)){
            $statusval = intval($status);
            if(!($statusval != 0 || $statusval != 1 || $statusval != 2))
                $form->setError("status", "* Error with the status given.");
        }
        else unset($statusval);

        if($dir && strlen($dir)>0){
            $field = "dir";
            $dirval = trim($dir);
            if ( strlen($dirval) > 4){
                $form->setError($field, "* Value is too long.");
            }else{
                if ( eregi('^[NSEW]{1,4}$', $dirval) )
                    $dirval = trim($dir);
                else
                    $form->setError($field, "* Enter a cardinal value.");
            }
        }
        else unset($dirval);

        if($description){
            $descriptionval = pg_escape_string($description);
        }
        else unset($descriptionval);

        /* Errors exist, have user correct them */
        if($form->num_errors > 0){
            return false;  //Errors with form
        }

        //$p = Photo::find($id);
        /* Update fields */
        //if(isset($latval)){
        //    $p->lat = $latval;
        //}
        //if(isset($longval)){
        //    $p->long = $longval;
        //}
        //if(isset($altval)){
        //    $p->alt = $altval);
        //}
        
        /* Update fields */
        if(isset($latval)){
            $database->updatePhotoField($id,"lat",$latval);
        }
        if(isset($longval)){
            $database->updatePhotoField($id,"long",$longval);
        }
        if(isset($altval)){
            $database->updatePhotoField($id,"alt",$altval);
        }
        //if(isset($longval) and isset($latval)){
        //    $database->updatePhotoField($id,"point", "geomfromtext('POINT($longval $latval)',4326)");
        //}
        if(isset($statusval)){
            $database->updatePhotoField($id,"status",$statusval);
        }
        if(isset($dirval)){
            $database->updatePhotoField($id,"dir",$dirval);
        }
        if(isset($categoryidval)){
            $database->updatePhotoField($id,"categoryid",$categoryidval);
        }
        if(isset($descriptionval)){
            $database->updatePhotoField($id,"description",$descriptionval);
        }
        if (isset($categoryidval) || isset($descriptionval)){
        	$database->query("update photos set idxfti = " .
        			"to_tsvector('default', coalesce((" .
        			"select categories.name from photos p1 left outer join categories " .
        			"on (p1.categoryid = categories.id) where photos.id = p1.id),' ') ||' '|| " .
        			"coalesce(description,'')) where id = $id;");
        }

        $result = $database->query("SELECT location FROM photos WHERE id = $id");
        $photo  = pg_fetch_all($result);
        $photo = $photo[0];

        $target = FILESYSTEM.GAL_BIGTHUMBS."/".$photo['location'];
        unlink($target);

        /* Success! */
        return true;
    }

	function deleteDuplicates($date, $uid = null){
		global $database, $session;
        if($uid == null){
            $uid = $session->userinfo['id'];
        }
		if (ereg ("([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})", $date)){
			//make sure all md5 hashes for files are set
			$photos = $database->queryFetch("SELECT DISTINCT {$this->items} FROM photos WHERE uploaddate = '$date' AND hash is NULL AND userid = $uid ORDER BY id");

            foreach ($photos as $photo){
            	$hash = md5_file(FILESYSTEM.INCOMING.'/'.$photo['location']);
            	$database->updatePhotoField($photo['id'],"hash",$hash);
            }

			$query = "select t1.id as id from " .
            		"photos t1, (select distinct on (hash) hash, id from (select * from photos order by id) as t3) as t2 " .
            		"where t1.hash = t2.hash and t1.id != t2.id and t1.uploaddate = '$date' and t1.userid = $uid";

            $photos = $database->queryFetch($query);

            foreach ($photos as $photo){
            	$database->updatePhotoField($photo['id'],"status",0);
            }

            return true;
		}
		else
			return false;
	}
    
    function undelete($date, $uid = null){
		global $database, $session;
        if($uid == null){
            $uid = $session->userinfo['id'];
        }
		if (ereg ("([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})", $date)){
			$query = "select id from photos where uploaddate = '$date' and userid = $uid and status = 0";

            $photos = $database->queryFetch($query);

            foreach ($photos as $photo){
            	$database->updatePhotoField($photo['id'],"status",1);
            }

            return true;
		}
		else
			return false;
    }

    function makeThumb($loc){
        $location = INCOMING . '/'.$loc;
        $img_thumb = GAL_THUMBS . '/' . $loc;

        if (!file_exists(FILESYSTEM.$img_thumb)) {
            $thumb = new thumbnail(FILESYSTEM.$location);
            $thumb->size_auto($this->thumbsize);
            $thumb->save(FILESYSTEM.$img_thumb);
        }
        return WEB.$img_thumb;
    }

    function showThumb($photo){
        echo "<a href='index.php?a=view&amp;photo={$photo['id']}'>";
        echo "<img class='thumb' align='top' src='".$this->makeThumb($photo['location'])."' alt='".basename($photo['location'])."'/>";
        echo "</a>";
    }

    function showInfo($photo){
        global $session,$database;

        echo "<br/>Date taken: " . $photo['takendate'];
        if ($photo['long'] != 0 and $photo['lat'] != 0){
            echo "<br/>";
            echo loc2str($photo['long'], $photo['lat']);
            //echo $photo['alt']."m altidude.";
        }
        
		//$r = $database->query("SELECT username FROM users WHERE id = ".$photo['userid']);
		//echo "<br/>User: " . pg_fetch_result($r,0,0);

        if ( $photo['categoryid']!= null ){
			//$r = $database->query("SELECT name FROM categories WHERE id = ".$photo['categoryid']);
			//echo "<br/>Category: " . pg_fetch_result($r,0,0);
			echo "<br/>Category: {$photo['categoryname']}";
		}else{
			echo "<br/>Category: Not Set";
		}
		
		if ($this->modis_timeseries)
		    echo "<br/>MODIS time series data: <a href='#' onclick='timeSeries({$photo['long']},{$photo['lat']}); return false'>View</a>";
        if ($session->isEditor($photo)){
                echo "<br/><a href=\"index.php?a=edit&photo=".$photo['id']."\">(Edit)</a>";
        }
    }

    /** showFoldersByDate - Takes userid as an argument as well
     * as a boolean identifying whether to display thumbnails.
     * Outputs html with links to galleries containing the images.
     */
    function showFoldersByDate($user, $displaythumbs) {
        global $database;

        $_SESSION['url1'] = $_SERVER['REQUEST_URI'];

        $query = "SELECT uploaddate, count(id) FROM photos 
                    WHERE userid = (select id from users where username = '{$user}') 
                    AND {$this->status_clause}
                    GROUP BY uploaddate ORDER BY uploaddate DESC";
                    
        $result = $database->query($query);

        $r = pg_fetch_all($result);

        if (sizeof($r) == 0)
            return false;
        //print_r($r);
        echo "<ul>";
        foreach ($r as $row) {
            if ($row['uploaddate'] == "")
                $row['uploaddate'] = "Undefined";
            
            $link = "<a href='index.php?a=user&info={$user}&uploaddate={$row['uploaddate']}'>View</a>";
            if(isset($_GET['uploaddate']) and $_GET['uploaddate'] == $row['uploaddate'] ){
                $link= '('.$link.')';
            }else{
                $link= '&nbsp;'.$link.'&nbsp;';
            }
            echo "<li>{$link} {$row['count']} pictures uploaded on {$row['uploaddate']} </li>\n";
        }
        echo "</ul>";
        return true;
    }

    /**
     * showPhotosByDate
     * Stuff
     */
    function showPhotosByDate($date, $uid = null){
        global $session;
        if($uid == null){
            $uid = $session->userinfo['id'];
        }
        if (preg_match ('/([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})/', $date)){
            $query = "SELECT {$this->items} FROM photos WHERE uploaddate = '$date' AND userid = $uid ORDER BY id"; 
            $this->showPhotosQuery($query);
        }
        else return false;
    }

    /**
     * showPhotosQuery - Takes SQL query and displays the gallery
     * view from the result.
     */
    function showPhotosQuery($query = "SELECT * FROM photos"){
        global $database;
        $result  = $database->query($query);

        $this->photos = pg_fetch_all($result);

        $this->showResultArray($this->photos, false);
    }

	/**
	 * showFilteredArray - Takes an array of arrays containing photo
	 * information, filters it using a function and forwards it to show
     * in gallery format
	 */
	function showResultArray($a, $checkbox = true){
		global $session;
		$photos = $session->filterPhotos($a);
		$this->showResultArrayUnfiltered($photos, $checkbox);
	}

    /** showResultArrayUnfiltered - Takes an array of arrays conaining photo
     * information and diplays it in gallery format, with optional
     * form components for maping in openLayers
     * **UNSECURED**
     */
    function showResultArrayUnfiltered($a, $checkbox = false) {
        global $session, $database;
		$photos = $a;

        $n = 4;
        $i = 0;
        $size = sizeof($photos);

        //border=0 cellspacing=0 cellpadding=10
        echo "\n<table width = '100%' border='0' cellspacing='0'>\n\t<tr valign=top bgcolor=#FFFFFF>\n";

        foreach ($photos as $photo) {
            if (file_exists(FILESYSTEM.INCOMING.'/'.$photo['location'])) {
                echo "\t\t<td>\n\t\t\t";

                echo "<div class=\"photo-thumb\" style=\"width: 193px; float:left; font-size: 13px;\">";
		        $this->showThumb($photo);
		        if ($checkbox or $this->checkbox)
                	echo "<input type=\"checkbox\" name=\"list[]\" value=\"".$photo['id']."\" onClick=\"check(event)\">";
		        $this->showInfo($photo);
		        echo "<br/> &nbsp;";
		        echo "</div>";

                $i++;
                echo "\n\t\t</td>\n";
                if ($i%$n == 0){
                    echo "\t</tr>\n\t<tr valign=top bgcolor=#FFFFFF>\n";
                }
            }
        }
        for ($j=0; $j<($n-$i%$n); $j++) {
            echo "\t<td>&nbsp</td>";
        }
        echo "\t</tr>\n</table>";
    }

    /** makeBigThumb - takes source image location, destination image
     *  location and outputs a thumb image with embedded information
     *  at a specified size, as an optional argument.
     */
    function makeBigThumb($photo, $img_thumb, $size=800 ){
        //rmdir(dirname($img_thumb));
        if (!is_dir(dirname($img_thumb))){
            mkdir(dirname($img_thumb));
        }
        $str = $photo['takendate'] . "\n";
        
        if (!empty($photo['long']) and !empty($photo['lat'])){
            if ($photo['long']<0)
                $str .= round($photo['long'],4) * -1 . " ºW\n";
            else $str .= round($photo['long'],4) . " ºE\n";
    
            if ($photo['lat']<0)
                $str .= round($photo['lat'],4) * -1 . " ºS\n";
            else $str .= round($photo['lat'],4) . " ºN\n";
            
            if (strlen($photo['dir'])>0)
                $str .= "View: ".$photo['dir']."\n";
            if (!empty($photo['alt']))
                $str .= $photo['alt']."m altitude.";
        }
        
        if (!file_exists($img_thumb)) {
            $thumb = new thumbnail(FILESYSTEM.INCOMING.'/'.$photo['location']);
            $thumb->size_auto($size);
            $thumb->text($str);
            $thumb->jpeg_quality(85);
            $thumb->save($img_thumb);
        }
    }
    
    function viewExif($pid){
        global $database;
        $id = intval($pid);
        $res = $database->query("SELECT * FROM photos WHERE id=$id");
        $photo = pg_fetch_assoc($res);
        //print_r($photo);
        $img = FILESYSTEM.INCOMING.'/'.$photo['location'];
        echo "<pre>";
	    print_r(exif_read_data($img));
	    echo "</pre>";
    }
};

$gallery = new Gallery;
?>
