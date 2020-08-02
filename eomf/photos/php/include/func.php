<?php


//---------------------------------------------------------
// Auxilarry Methods "Library"
//---------------------------------------------------------

function menu($ret = false) {
	global $session;
    
    $query = '';
	if (isset($_SESSION['query_string']))
	    $query = '?'.$_SESSION['query_string'];
    
    function menu_links($arr){
        $str = "";
        $last_item = end($arr);
        foreach ($arr as $a):
            //echo "\n<!-- regex:" . $a[0] . "  url:" . $_SERVER['REQUEST_URI'] . "-->\n";
            if (preg_match('/'.$a[0].'/', $_SERVER['REQUEST_URI'])):
                $str .= "\n<b><a style='color: darkgreen;' href='{$a[1]}'>{$a['2']}</a></b>";
            else:
                $str .= "\n<a href='{$a[1]}'>{$a['2']}</a>";
            endif;
            
            if ($a != $last_item):
                $str .= "&nbsp;&nbsp;|&nbsp;\n";
            endif;
        endforeach;
        return $str;
    }
    
	$items = array(
        array('(\/index.php$)|^\/photos\/$', 'index.php', 'Home'),
    );
	//echo "[<a href=\"index.php\">Main</a>] &nbsp;&nbsp;\n";
	if ($session->logged_in):
	    $items = array_merge($items, array(
	        array('a=user',"index.php?a=user&amp;info={$session->username}",ucwords($session->username)."'s Account"),
	        array('upload.php',"upload.php","Upload"),
	        array('a=login','process.php','Log out')
	    ));
	else:
	    $items = array_merge($items, array(
            array('a=login',"index.php?a=login", 'Log in'),
            array('a=register',"index.php?a=register", 'Register')
        ));
	endif;

	if ($session->isAdmin()):
	    $items = array_merge($items, array(
	        array('admin.php', 'admin/admin.php', 'Admin Center')
	    ));
	endif;

	$items = array_merge($items, array(
	    array('query.php',"query.php{$query}","Query"),
	    array('map.php',"map.php{$query}","Map Query"),
	    array('summary.php',"summary.php","Summary")
	));
	$out = menu_links($items);
	if ($ret):
	    return $out;
	else:
	    print $out;
	endif;
	//echo $session->userinfo['id'];
}


/**
 * Usage:
 * $result = $database->query("SELECT id,name FROM categories");
 *  build_checkbox_box($result, 'cat');
 */

function build_select_box($result, $name, $checked_val = "xzxz") {
	$rows = pg_numrows($result);
	echo '<select size = "' . $rows . '" name="' . $name . '">';
	for ($i = 0; $i < $rows; $i++) {
		echo '<option value ="' . pg_fetch_result($result, $i, 0) . '"';
		if (pg_fetch_result($result, $i, 0) == $checked_val) {
			echo ' selected';
		}
		echo '>' . pg_fetch_result($result, $i, 1) . '</option>' . "\n";
	}
	echo '</select>';
}

function build_select_box_small($arr, $name) {
    global $form;
    $checked_val = $form->value($name);
	$rows = count($arr);
	//print "<!---"; print_r($arr); print "-->";
	echo '<select class="small" size = "1" name="' . $name . '[]">';
	echo '<option value = "">All</option>';
	for ($i = 0; $i < $rows; $i++) {
	    $id = $arr[$i]['id'];
	    $name = $arr[$i]['name'];
		echo "<option value ='{$id}'";
		if ($id == $checked_val) {
			echo ' selected';
		}
		echo '>' . $name . '</option>' . "\n";
	}
	echo '</select>';
}

function build_select_box_array($arr, $name, $checked_val = "xzxz") {
	//print_r($arr);
	//echo $checked_val;
	//die();
	$rows = sizeof($arr);
	echo '<select size = "' . $rows . '" name="' . $name . '">';
	for ($i = 0; $i < $rows; $i++) {
	    if ( !empty($arr[$i][1]) ) {
            echo '<option value ="' . $arr[$i][0] . '"';
            if ($arr[$i][0] == $checked_val) {
                echo ' selected';
            }
            echo '>' . htmlspecialchars($arr[$i][1]) . '</option>' . "\n";
		}
	}
	echo '</select>';
}

function build_checkbox_box($result, $name, $checked_val = "xzxz") {
	$rows = pg_numrows($result);
	for ($i = 0; $i < $rows; $i++) {
		echo '<input type=checkbox name="' . $name . '[]" value="' . pg_fetch_result($result, $i, 0) . '"';
		if (pg_fetch_result($result, $i, 0) == $checked_val) {
			echo ' selected';
		}
		echo '>' . pg_fetch_result($result, $i, 1) . '<br/>' . "\n";
	}
}

// This function takes an array of arrays, each of which has two elements
//    of which the first is used as a value and the second concatonated to first
//    as a name for each option
function build_select_box_count($arr, $name, $checked_val = "xzxz", $style, $default='All') {
        $options = "<option value=''>$default</option>";
        foreach  ($arr as $item):
            if (!empty($item[$name])):
                $value = htmlentities($item[$name]);
                $options .= "<option value ='{$value}'";
                if ($item[$name] == $checked_val):
                        $options .= ' selected';
                endif;
                $options .= ">{$item[$name]} ";
            if(!empty($item['count'])):
                $options .= "({$item['count']})";
            endif;
            $options .= "</option>\n";
        endif;
        endforeach;
        $select = "<select size = '1' name='$name' $style>\n$options\n</select>";
    echo $select;
}

function build_user_form($arr, $names){
	global $form;
	foreach($names as $n){
			//echo "<tr><td align=\"right\"><b>". $n[0] . ':</b> </td><td>' . $arr[$n[1]] . "</tr>";
		?><tr>
		<td><?echo empty($n[0])?'':$n[0].':';?> </td>
		<td><input type="text" name="<?echo $n[1];?>" size="<? echo $n[2];?>" maxlength="70" value="<?
		if($form->value($n['1']) == ""){
		    if(array_key_exists($n[1], $arr))
		        echo $arr[$n[1]];
		}else{
		   echo $form->value($n[1]);
		}
		?>">
		</td>
		<td><? echo $form->error($n[1]); ?></td>
		</tr><?
	}
}

/**
  * Return human readable sizes
  *
  * @author      Aidan Lister <aidan@php.net>
  * @version     1.1.0
  * @link        http://aidanlister.com/repos/v/function.size_readable.php
  * @param       int    $size        Size
  * @param       int    $unit        The maximum unit
  * @param       int    $retstring   The return string format
  * @param       int    $si          Whether to use SI prefixes
 */
function size_readable($size, $unit = null, $retstring = null, $si = true) {
	// Units
	if ($si === true) {
		$sizes = array (
			'B',
			'kB',
			'MB',
			'GB',
			'TB',
			'PB'
		);
		$mod = 1000;
	} else {
		$sizes = array (
			'B',
			'KiB',
			'MiB',
			'GiB',
			'TiB',
			'PiB'
		);
		$mod = 1024;
	}
	$ii = count($sizes) - 1;

	// Max unit
	$unit = array_search((string) $unit, $sizes);
	if ($unit === null || $unit === false) {
		$unit = $ii;
	}

	// Return string
	if ($retstring === null) {
		$retstring = '%01.2f %s';
	}

	// Loop
	$i = 0;
	while ($unit != $i && $size >= 1024 && $i < $ii) {
		$size /= $mod;
		$i++;
	}

	return sprintf($retstring, $size, $sizes[$i]);
}

function query_coordinate_box() {
	global $form;
?>
<b>Search by coordinates:</b><br/>

<table>
<tr>
	<td>Longitude min:<br/><input type="text" name="longmin" size="10" value="<? echo $form->value("longmin"); ?>"></td><? echo $form->error("longmin"); ?>
	<td>Longitude max:<br/><input type="text" name="longmax" size="10" value="<? echo $form->value("longmax"); ?>"></td><? echo $form->error("longmax"); ?>
</tr>
<tr>
	<td>Latitude min:<br/><input type="text" name="latmin" size="10" value="<? echo $form->value("latmin"); ?>"></td><? echo $form->error("latmin"); ?>
	<td>Latitude max:<br/><input type="text" name="latmax" size="10" value="<? echo $form->value("latmax"); ?>"></td><? echo $form->error("latmax"); ?>
</tr>
</table>
<?

}

function query_date_box() {
	global $form;
?>

<b>Search by date:</b><br/>
<table>
<tr><td>
From:<br/>
<div class="padless">
<script type="text/javascript">
//<![CDATA[
    DateInput('datemin', true, 'YYYY-MM-DD', "<? echo $form->isValueSet('datemin') ? $form->value('datemin') : '1990-01-01'; ?>");
//]]>
</script>
</div>
</td></tr>
<tr><td>
To:<br/>
<div class="padless">
<script type="text/javascript">
//<![CDATA[
    DateInput('datemax', true, 'YYYY-MM-DD' <? echo $form->isValueSet("datemax") ? ", '".$form->value("datemax")."'" : "";?>);
//]]>
</script>
</div>
</td></tr>
</table>
<?

}

function query_description_box() {
	global $form;
?>
 <input size = "80" type="text" name="searchwords" value="<? echo $form->value("searchwords"); ?>"><?echo $form->error("searchwords");?><br/>
<?

}

function query_print_form($noecho = false) {
	global $database,$form;
//    $result = $database->query("SELECT id, username FROM users where users.id in (select userid from photos) ORDER BY username");

    if ($noecho) ob_start();
	echo "<form id='search' action=\"" . $_SERVER['PHP_SELF'] . "\" method=\"get\" >";
	echo "<table width = '100%' ><tr><td>"; //bgcolor=#DCDCDC
	//echo "<table align = \"center\" width = 90% ><tr><td>";

	query_coordinate_box();

	echo "</td><td>";

	query_date_box();

	echo "</td><td>";
	
    echo "<table><tr><td>";
  	
  	echo "<b>Search by metadata:</b><br>";
	
	echo "Categories:<br>";
	
	$result = $database->queryFetch("SELECT id,name FROM categories");
	$result[] = array('id'=>"notset",'name'=>"Not Set");
	$result[] = array('id'=>"set",'name'=>"Is Set");
	build_select_box_small($result, 'cat');

	echo "</td><td>";
	echo "<b>Search by region:</b><br>";
	$result = $database->queryFetch("SELECT gid as id, cntry_name as name FROM country_buffered ORDER BY cntry_name");
	echo "Countries:<br/>";
	build_select_box_small($result, 'country');
	
	echo "</td></tr><tr><td>";

    $count = "(select count(photos.id) from photos where userid = users.id  and status = ".PUBLIC_STATUS.")";
    $ucq= "SELECT id as id, username || '  (' || $count || ')' as name FROM users where users.id in (select userid from photos) ORDER BY username";
    $uq= "SELECT id as id, username as name FROM users where users.id in (select userid from photos) ORDER BY username";
    $result = $database->queryFetch($uq);
	echo "Users:<br>";
	build_select_box_small($result, 'users');
	
	echo "</td><td>";
	
	$result = $database->queryFetch("SELECT gid as id, continent as name FROM continent_buffered ORDER BY continent");
	echo "Geographical:<br/>";
	build_select_box_small($result, 'region');
	
    echo "</td></tr></table>";
    echo "</td></tr></table>";
    
	echo "<br/><b>Search by keywords:</b>&nbsp;";

	query_description_box();

	echo "<br/>";

	echo "<input name=\"submit\" type=\"submit\" value=\"Submit\"/></form><br/>";
	
	if($noecho) return ob_get_clean();
}

function query_spatial_single($table, $id){
    //$p1 = 'TFFTFF212';
    //$p2 = 'T**T*****';
    //$p3 = 'T********';
    //$sql = "ST_RELATE(point, (select geometry from $table where gid = $id), '$p3')";
    //$sql = "id in ( SELECT p.id FROM photos p, $table m WHERE m.gid = $id AND ST_Intersects(p.point,m.geometry)) ";
    $sql = "ST_Intersects(point, (select geometry from $table where gid = $id))";
    return $sql;
}

function query_process_form($submit = false) {
	global $form;
	if (isset ($_GET["submit"]) or $submit) {
	
	    $_SESSION['query_string'] = $_SERVER['QUERY_STRING']; 
	    
		$string1 = "";
		$string2 = "";
		$string3 = "";
		$string4 = "";
		$string5 = "";
		$string6 = "";
		$string7 = "";

		if ($_GET["users"] != "") {
			$users = $_GET["users"];
			$string1 .= "(";
			//$userId = explode(" ", $users);
			for ($i = 0; $i < sizeof($users); $i++) {
				if ($users[$i] != "" && $tmp = intval($users[$i])) {
					$string1 .= "photos.userid = " . $tmp;
					$form->setValue("users", $tmp);
					if ($i +1 == sizeof($users))
						$string1 .= " AND ";
					else
						$string1 .= " OR ";
				}
			}
			$i = 0;

			$string1 .= " 1=1 ) AND ";
		}

		if ($_GET["cat"] != "") {
			$cat = $_GET["cat"];
						
			if ($cat[0] == "notset"){
			    $string2 .= "( photos.categoryid is null ) AND ";
			    $form->setValue("cat", "notset");
			}else if ($cat[0] == "set"){
			    $string2 .= "( photos.categoryid is not null) AND ";
			    $form->setValue("cat", "set");
			}else{
                $string2 .= "(";
                for ($i = 0; $i < sizeof($cat); $i++) {
                    if ($cat[$i] != "" && (($tmp = intval($cat[$i])) || $tmp == 0)) {
                        $string2 .= "photos.categoryid = " . $tmp;
                        $form->setValue("cat", $tmp);
                        if ($i+1 == sizeof($cat))
                            $string2 .= " AND ";
                        else
                            $string2 .= " OR ";
                    }
                }
                $i = 0;
    
                $string2 .= " 1=1 ) AND ";
			}
		}

		if ($_GET["latmin"] != ""  || $_GET["latmax"] != "" || 
		    $_GET["longmin"] != "" || $_GET["longmax"] != "" ) {
			
			$latmin = $_GET["latmin"];
			$latmax = $_GET["latmax"];
			$longmin = $_GET["longmin"];
			$longmax = $_GET["longmax"];

			$form->setValue("latmin", $latmin);
			$form->setValue("latmax", $latmax);
			$form->setValue("longmin", $longmin);
			$form->setValue("longmax", $longmax);

			$string3 .= "(";

            if(isset($latmin) and $latmin != ""){
                $latmin = floatval($latmin);
                if ($latmin >= -90) {
                    $string3 .= " photos.lat >= " . $latmin . " AND ";
                } else {
                    $form->setError("latmin", "*Enter minimal latitude greater than -90");
                    $string3 . " 1=1 AND ";
                }
            }
            
            if(isset($latmax) and $latmax != ""){
                $latmax = floatval($latmax);
                
                if ($latmax <= 90) {
                    $string3 .= " photos.lat <= " . $latmax . " AND ";
                } else {
                    $form->setError("latmin", "*Enter maximum latitude less than 90");
                    $string3 . " 1=1 AND ";
                }
            }
            
            if(isset($longmin) and $longmin != ""){
                $longmin = floatval($longmin);
                if ($longmin >= -180) {
                    $string3 .= " photos.long >= " . $longmin . " AND ";
                } else {
                    $form->setError("latmin", "*Enter minimal longitude greater than -180");
                    $string3 .= " 1=1 AND ";
                }
            }
            
            if(isset($longmax) and $longmax != ""){
                $longmax = floatval($longmax);
                if ($longmax <= 180) {
                    $string3 .= " photos.long <= " . $longmax . " AND";
                } else {
                    $form->setError("latmin", "*Enter maximum longitude less than 180");
                    $string3 .= " 1=1 AND ";
                }
            }
            
			$string3 .= " 1=1 ) AND ";
		}

		if ($_GET["datemin"] != "" || $_GET["datemax"] != "") {
			$datemin = $_GET["datemin"];
			$datemax = $_GET["datemax"];

			$form->setValue("datemin", $datemin);
			$form->setValue("datemax", $datemax);

			$string4 .= "(";

			if (ereg("([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})", $datemin)) {
				$string4 .= " photos.takendate >= '$datemin' AND ";
			} else {
				$string4 .= "1=1 "; //echo "Invalid date format: $datemin";
			}
			if (ereg("([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})", $datemax)) {
				$string4 .= " photos.takendate <= '$datemax' AND ";
			} else {
				$string4 .= "1=1 "; //echo "Invalid date format: $datemin";
			}

			$string4 .= " 1=1 ) AND ";
		}

		if ($_GET["searchwords"] != "") {
			$str = pg_escape_string($_GET["searchwords"]);
			$string5 .= "( idxfti @@ to_tsquery('default', '$str') ) AND ";
			$form->setValue("searchwords", $_GET["searchwords"]);
		}
        if ($_GET["country"] != "") {
            $reg = $_GET["country"];
            $string6 .= "(";
            for ($i = 0; $i < sizeof($reg); $i++) {
                if ($reg[$i] != "" && (($tmp = intval($reg[$i])) || $tmp == 0)) {
                    $string6 .= query_spatial_single('country_buffered', $tmp);
    
                    $form->setValue("country", $tmp);
                    if ($i + 1 == sizeof($reg))
                        $string6 .= " AND ";
                    else
                        $string6 .= " OR ";
                }
            }
            $i = 0;
    
            $string6 .= " 1=1 ) AND ";
        }
    
        if ($_GET["region"] != "") {
            $reg = $_GET["region"];
            $string7 .= "(";
            for ($i = 0; $i < sizeof($reg); $i++) {
                if ($reg[$i] != "" && (($tmp = intval($reg[$i])) || $tmp == 0)) {
                    $string7 .= query_spatial_single('continent_buffered', $tmp);
    
                    $form->setValue("region", $tmp);
                    if ($i + 1 == sizeof($reg))
                        $string7 .= " AND ";
                    else
                        $string7 .= " OR ";
                }
            }
            $i = 0;
    
            $string7 .= " 1=1 ) AND ";
        }
        
		return $string1 . $string2 . $string3 . $string4 . $string5 . $string6 . $string7. " 1=1 ";
	} else {
		return " 1=1 ";
	}
}


//This functions forces a download of the $data
function force_download($data, $name, $mimetype = '', $filesize = false) {
	// File size not set?
	if ($filesize == false OR !is_numeric($filesize)) {
		$filesize = strlen($data);
	}

	// Mimetype not set?
	if (empty ($mimetype)) {
		$mimetype = 'application/octet-stream';
	}

	// Make sure there's not anything else left
	ob_clean_all();

	// Start sending headers
	header("Pragma: public"); // required
	header("Expires: 0");
	header("Cache-Control: must-revalidate, post-check=0, pre-check=0");
	header("Cache-Control: private", false); // required for certain browsers
	header("Content-Transfer-Encoding: binary");
	header("Content-Type: " . $mimetype);
	header("Content-Length: " . $filesize);
	header("Content-Disposition: attachment; filename=\"" . $name . "\";");

	// Send data
	echo $data;
	die();
}

function ob_clean_all() {
	$ob_active = ob_get_length() !== false;
	while ($ob_active) {
		ob_end_clean();
		$ob_active = ob_get_length() !== false;
	}

	return true;
}

function str_shorten($str, $len = 20){
    if (strlen($str)>$len)
        return substr($str, 0, $len)."...";
    else
        return $str;
}

/* text to a space then adds ellipses if desired
 * @param string $input text to trim
 * @param int $length in characters to trim to
 * @param bool $ellipses if ellipses (...) are to be added
 * @param bool $strip_html if html tags are to be stripped
 * @return string
 */
function trim_text($input, $length, $ellipses = true, $strip_html = true) {
    //strip tags, if desired
    if ($strip_html) {
        $input = strip_tags($input);
    }

    //no need to trim, already shorter than trim length
    if (strlen($input) <= $length) {
        return $input;
    }

    //find last space within length
    $last_space = strrpos(substr($input, 0, $length), ' ');
    $trimmed_text = substr($input, 0, $last_space);

    //add ellipses (...)
    if ($ellipses) {
        $trimmed_text .= '...';
    }

    return $trimmed_text;
}

function curPageURL() {
 $pageURL = 'http';
 if (isset($_SERVER["HTTPS"]) and $_SERVER["HTTPS"] == "on") {$pageURL .= "s";}
 $pageURL .= "://";
 if ($_SERVER["SERVER_PORT"] != "80") {
  $pageURL .= $_SERVER["SERVER_NAME"].":".$_SERVER["SERVER_PORT"].$_SERVER["REQUEST_URI"];
 } else {
  $pageURL .= $_SERVER["SERVER_NAME"].$_SERVER["REQUEST_URI"];
 }
 return $pageURL;
}

function is_image($path){
    $file_info = getimagesize($path);
    if(empty($file_info))
        return false;
    else
        return true;
}

function loc2str($lon, $lat){
    $lon = round($lon,4);
    $lat = round($lat,4);
    
    if ($lon<0)
        $str = $lon * -1 . ' &deg;W, ';
    else 
        $str = $lon.' &deg;E, ';

    if ($lat<0)
        return $str . $lat * -1 . ' &deg;S';
    else 
        return $str . $lat . ' &deg;N';
    
    return $str;            
}
?>
