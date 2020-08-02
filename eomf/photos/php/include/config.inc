<?php
//This sets the number of files that can e
//uploaded at once

$dev = false;
// Report all errors except E_NOTICE
// This is the default value set in php.ini
error_reporting(E_ALL ^ E_NOTICE);

define("MAX_FILES", 5);
define("LOG","/outgoing/log.txt"); //log
define("TMP_D" ,"tmp");
define("INCOMING","incoming");
if ($dev){
	define("WEB","");
	define("FILESYSTEM","");
}else{
	//Attention: slash at end.
	define("WEB","/data/pb/");
	define("FILESYSTEM","/data/health/data1/web/data/pb/");
}

define("TEMPLATES_DIR", dirname(__FILE__)."/../../templates/");

/**
 * Mapping variables
 */
 
define("MAP_GOOGLEKEY","AIzaSyBo98LuzUr-aVpxRZPFHkBl2m4ogHeROGQ");

/**
 * Database Table Constants - these constants
 * hold the names of all the database tables used
 * in the script.
 */

define("DB_LOCAL", "true");
define("DB_SERVER", "localhost");
define("DB_USER", "eomf");
define("DB_PASS", "30mfadmin");
if($dev)
	define("DB_NAME", "devremotesensing");
else
	define("DB_NAME", "eomf");

/**
 * Database Table Constants - these constants
 * hold the names of all the database tables used
 * in the script.
 */
define("TBL_USERS", "users");
define("TBL_ACTIVE_USERS",  "active_users");
define("TBL_ACTIVE_GUESTS", "active_guests");
define("TBL_BANNED_USERS",  "banned_users");

/**
 * Special Names and Level Constants - the admin
 * page will only be accessible to the user with
 * the admin name and also to those users at the
 * admin user level. Feel free to change the names
 * and level constants as you see fit, you may
 * also add additional level specifications.
 * Levels must be digits between 0-9.
 */
define("ADMIN_NAME", "admin");
define("GUEST_NAME", "Guest");
define("ADMIN_LEVEL", 9);
define("EDITOR_LEVEL", 5);
define("TRUSTED_LEVEL",  3);
define("USER_LEVEL",  1);
define("GUEST_LEVEL", 0);

/**
* Photo status levels
*/

define("PUBLIC_STATUS", 1);
define("PRIVATE_STATUS", 2);
define("DELETED_STATUS", 0);

/**
 * This boolean constant controls whether or
 * not the script keeps track of active users
 * and active guests who are visiting the site.
 */
define("TRACK_VISITORS", false);

/**
 * Timeout Constants - these constants refer to
 * the maximum amount of time (in minutes) after
 * their last page fresh that a user and guest
 * are still considered active visitors.
 */
define("USER_TIMEOUT", 10);
define("GUEST_TIMEOUT", 5);

/**
 * Email Constants - these specify what goes in
 * the from field in the emails that the script
 * sends to users, and whether to send a
 * welcome email to newly registered users.
 */
define("EMAIL_FROM_NAME", "EOMF Photos");
define("EMAIL_FROM_ADDR", "eomf@rccc.ou.edu");
define("EMAIL_WELCOME", false);

/**
 * This constant forces all users to have
 * lowercase usernames, capital letters are
 * converted automatically.
 */
define("ALL_LOWERCASE", false);

/**
 * Gallery Constants defines variables such as
 * the location of the generated thumbnails.
 */
define("GAL_THUMBS","thumb");
define("GAL_BIGTHUMBS","thumb/big");

/**
 * Download constants based on user level
 */
define("LIMIT_BASE", 50);
define("LIMIT_MULT", 5);

define("LIMIT_ADMIN", 99999); // multiplier
define("LIMIT_EDITOR", 99999);
define("LIMIT_USER", 5); // multiplier
define("LIMIT_GUEST", 1); // multiplier

?>
