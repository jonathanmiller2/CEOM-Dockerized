<?
##############################################
# Shiege Iseng Resize Class
# Modified: Pavel Dorovskoy
#	+text generation
# 11 March 2005
# shiegegeATyahoo.com
# http://shiege.com/scripts/thumbnail/
/*############################################
Sample :
$thumb=new thumbnail("./shiegege.jpg");			// generate image_file, set filename to resize/resample
$thumb->size_width(100);						// set width for thumbnail, or
$thumb->size_height(300);						// set height for thumbnail, or
$thumb->size_auto(200);							// set the biggest width or height for thumbnail
$thumb->jpeg_quality(75);						// [OPTIONAL] set quality for jpeg only (0 - 100) (worst - best), default = 75
$thumb->show();									// show your thumbnail
$thumb->save("./huhu.jpg");						// save your thumbnail to file
----------------------------------------------
Note :
- GD must Enabled
- Autodetect file extension (.jpg/jpeg, .png, .gif, .wbmp)
  but some server can't generate .gif / .wbmp file types
- If your GD not support 'ImageCreateTrueColor' function,
  change one line from 'ImageCreateTrueColor' to 'ImageCreate'
  (the position in 'show' and 'save' function)
- If your GD not support 'ImageCopyResampled' function,
  change 'ImageCopyResampled' to 'ImageCopyResize'
*/############################################


class thumbnail
{
	var $img;

	function thumbnail($imgfile)
	{
		//detect image format
		$this->img["format"]=ereg_replace(".*\.(.*)$","\\1",$imgfile);
		$this->img["format"]=strtoupper($this->img["format"]);
		if ($this->img["format"]=="JPG" || $this->img["format"]=="JPEG") {
			//JPEG
			$this->img["format"]="JPEG";
			$this->img["src"] = ImageCreateFromJPEG ($imgfile);
		} elseif ($this->img["format"]=="PNG") {
			//PNG
			$this->img["format"]="PNG";
			$this->img["src"] = ImageCreateFromPNG ($imgfile);
		} elseif ($this->img["format"]=="GIF") {
			//GIF
			$this->img["format"]="GIF";
			$this->img["src"] = ImageCreateFromGIF ($imgfile);
		} elseif ($this->img["format"]=="WBMP") {
			//WBMP
			$this->img["format"]="WBMP";
			$this->img["src"] = ImageCreateFromWBMP ($imgfile);
		} else {
			//DEFAULT
			echo "Not Supported File";
			exit();
		}
		@$this->img["lebar"] = imagesx($this->img["src"]);
		@$this->img["tinggi"] = imagesy($this->img["src"]);
		//default quality jpeg
		$this->img["quality"]=75;
	}

	function size_height($size=100)
	{
		//height
    	$this->img["tinggi_thumb"]=$size;
    	@$this->img["lebar_thumb"] = ($this->img["tinggi_thumb"]/$this->img["tinggi"])*$this->img["lebar"];
	}

	function size_width($size=100)
	{
		//width
		$this->img["lebar_thumb"]=$size;
    	@$this->img["tinggi_thumb"] = ($this->img["lebar_thumb"]/$this->img["lebar"])*$this->img["tinggi"];
	}

	function size_auto($size=100)
	{
		//size
		if ($this->img["lebar"]>=$this->img["tinggi"]) {
    		$this->img["lebar_thumb"]=$size;
    		@$this->img["tinggi_thumb"] = ($this->img["lebar_thumb"]/$this->img["lebar"])*$this->img["tinggi"];
		} else {
	    	$this->img["tinggi_thumb"]=$size;
    		@$this->img["lebar_thumb"] = ($this->img["tinggi_thumb"]/$this->img["tinggi"])*$this->img["lebar"];
 		}
	}

	function jpeg_quality($quality=75)
	{
		//jpeg quality
		$this->img["quality"]=$quality;
	}

	function text($str){
		$this->img["text"] = $str;
	}

	function show()
	{
		//show thumb
		@Header("Content-Type: image/".$this->img["format"]);

		/* change ImageCreateTrueColor to ImageCreate if your GD not supported ImageCreateTrueColor function*/
		$this->img["des"] = ImageCreateTrueColor($this->img["lebar_thumb"],$this->img["tinggi_thumb"]);
    		@imagecopyresampled ($this->img["des"], $this->img["src"], 0, 0, 0, 0, $this->img["lebar_thumb"], $this->img["tinggi_thumb"], $this->img["lebar"], $this->img["tinggi"]);

		if ($this->img["format"]=="JPG" || $this->img["format"]=="JPEG") {
			//JPEG
			imageJPEG($this->img["des"],"",$this->img["quality"]);
		} elseif ($this->img["format"]=="PNG") {
			//PNG
			imagePNG($this->img["des"]);
		} elseif ($this->img["format"]=="GIF") {
			//GIF
			imageGIF($this->img["des"]);
		} elseif ($this->img["format"]=="WBMP") {
			//WBMP
			imageWBMP($this->img["des"]);
		}
	}

	function save($save="")
	{
		//save thumb
		if (empty($save)) $save=strtolower("./thumb.".$this->img["format"]);
		/* change ImageCreateTrueColor to ImageCreate if your GD not supported ImageCreateTrueColor function*/
		$this->img["des"] = ImageCreateTrueColor($this->img["lebar_thumb"],$this->img["tinggi_thumb"]);
    		@imagecopyresampled ($this->img["des"], $this->img["src"], 0, 0, 0, 0, $this->img["lebar_thumb"], $this->img["tinggi_thumb"], $this->img["lebar"], $this->img["tinggi"]);


		$white = imagecolorallocate($this->img["des"], 255, 255, 255);
		$grey = imagecolorallocate($this->img["des"], 255, 255, 255);
		$black = imagecolorallocate($this->img["des"], 0, 0, 0);
		//imagefilledrectangle($this->img["des"], 0, 0, 399, 29, $white);

		// The text to draw
		$text = $this->img["text"];
		// Replace path by your own font path
		//putenv('GDFONTPATH=' . realpath('.'));
		$font = '/include/verdana.ttf';

		// Add some shadow to the text
		//imagettftext($this->img["des"], 11, 0, 11, 21, $grey., $font, $text);
		//imagettftext($this->img["des"], 11, 0,  9, 21, $grey., $font, $text);
		// Add the text
		//imagettftext($this->img["des"], 11, 0, 10, 20, $black, $font, $text);
		$this->imagettfstroketext($this->img["des"], 11, 0, 10, 20, $black, $grey, $font, $text, 0.5);
		
		if ($this->img["format"]=="JPG" || $this->img["format"]=="JPEG") {
			//JPEG
			imageJPEG($this->img["des"],"$save",$this->img["quality"]);
		} elseif ($this->img["format"]=="PNG") {
			//PNG
			imagePNG($this->img["des"],"$save");
		} elseif ($this->img["format"]=="GIF") {
			//GIF
			imageGIF($this->img["des"],"$save");
		} elseif ($this->img["format"]=="WBMP") {
			//WBMP
			imageWBMP($this->img["des"],"$save");
		}
	}
	
	function imagettfstroketext(&$image, $size, $angle, $x, $y, &$textcolor, &$strokecolor, $fontfile, $text, $px) {

    	for($c1 = ($x-abs($px)); $c1 <= ($x+abs($px)); $c1++)
        	for($c2 = ($y-abs($px)); $c2 <= ($y+abs($px)); $c2++)
        		$bg = imagettftext($image, $size, $angle, $c1, $c2, $strokecolor, $fontfile, $text);

   		return imagettftext($image, $size, $angle, $x, $y, $textcolor, $fontfile, $text);
	}
}
?>
