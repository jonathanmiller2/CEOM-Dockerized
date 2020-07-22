/********************************************************************
 * openWYSIWYG settings file Copyright (c) 2006 openWebWare.com
 * Contact us at devs@openwebware.com
 * This copyright notice MUST stay intact for use.
 *
 * $Id: wysiwyg-settings.js,v 1.4 2007/01/22 23:05:57 xhaggi Exp $
 ********************************************************************/

/*
 * Full featured setup used the openImageLibrary addon
 */
var full = new WYSIWYG.Settings();
full.ImagesDir = "/media/ow/images/";
full.PopupsDir = "/media/ow/popups/";
full.CSSFile = "/media/ow/styles/wysiwyg.css";
full.Width = "94%"; 
full.Height = "800px";
// customize toolbar buttons
full.addToolbarElement("font", 3, 1); 
full.addToolbarElement("fontsize", 3, 2);
full.addToolbarElement("headings", 3, 3);
// openImageLibrary addon implementation
full.ImagePopupFile = "/media/ow/addons/imagelibrary/insert_image.php";
full.ImagePopupWidth = 600;
full.ImagePopupHeight = 245;

/*
 * Small Setup Example
 */
var small = new WYSIWYG.Settings();
small.Width = "350px";
small.Height = "100px";
small.DefaultStyle = "font-family: Arial; font-size: 12px; background-color: #AA99AA";
small.Toolbar[0] = new Array("font", "fontsize", "bold", "italic", "underline"); // small setup for toolbar 1
small.Toolbar[1] = ""; // disable toolbar 2
small.StatusBarEnabled = false;
