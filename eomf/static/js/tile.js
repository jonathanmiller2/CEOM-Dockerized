//
//	UNH IDS page javascript functions
//		Dr. A. Prusevich
//		january, 2005
//

var win = 0; 
function Load_Page() {
//  var message = "Tile indices = ("+Tile_col+","+Tile_row+")";
//  alert(message);
  windowName = "tile_inventory";
  params = "toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=1,resizable=1,width=700,height=700";
  url = "tile_inventory.cgi?tile_x="+Tile_col+"&tile_y="+Tile_row;
  if ((win) && (!win.closed)) {
    win.focus();
  }
  setTimeout("win = window.open(url, windowName , params);",200);
  return false;
}

/////////////////////////////////////////////////////////////////

var Agent = navigator.userAgent.toLowerCase();
var Aname = navigator.appName.toLowerCase();
var Os = navigator.platform.toLowerCase();
var isWin = (Os.indexOf("win")!=-1);
var isMac = (Os.indexOf("mac")!=-1);
var isGec = (Agent.indexOf("gecko")!=-1);
var Win = (isWin && !isGec) ? [1,1] : [0,0];
var SmaLL = (isWin && isGec) ? [2,0] : [2,-5];
var Mac = (isMac && Aname.indexOf("explorer")!=-1) ? [9,14] : [0,0];
var NS4 = document.layers;

function init() {
  _dom=document.all?3:(document.getElementById?1:(document.layers?2:0));

  if(_dom==2){                         // for NN4
    div_3 = document.layers.square_red;
  }
  else if(document.getElementById){    // for IE5, Mozilla
    div_3 = document.getElementById('square_red');
  }
  else {                               // for IE4
    div_3 = document.all('square_red');
  }

  Set_Menue();
}

var Resizing = false;

function Page_Resize() {
  Resizing = true;
  Set_Menue();
  Resizing = false;
}

/////////////////////////////////////////////////////////////////

function find_xy(Img) {
  var Img_coord = new Array(2);
  if (NS4) {
    Img_coord = [Img.x, Img.y];
  }
  else {
    Img_coord = [Img.offsetLeft+Mac[0]+Win[0], Img.offsetTop+Mac[1]+Win[1]];
    var tempElm = Img.offsetParent;
    while (tempElm != null) {
      Img_coord[0] += tempElm.offsetLeft;
      Img_coord[1] += tempElm.offsetTop;
      tempElm = tempElm.offsetParent;
    }
  }
  return Img_coord;
}

////////////////////  Menue Functions  //////////////////

var Tile_col=0; var Tile_row=0;
var Menue_Loaded = false;
var Chooser_coord;

function Set_Menue(coord) {
  Chooser_coord = find_xy(document.images["chooser"]);
  Menue_Loaded = true;
}

function Show_Square(mx,my,col,row) {
  if (Menue_Loaded) {
    Tile_col = col;
    Tile_row = row;
    if (NS4)
    {
      div_3.moveTo(Chooser_coord[0]+mx,Chooser_coord[1]+my);
      div_3.visibility="show";
    }
    else
    {
      div_3.style.left = Chooser_coord[0]+mx;
      div_3.style.top  = Chooser_coord[1]+my;
      div_3.style.visibility="visible";
    }
    document.tile.col.value=Tile_col;
    document.tile.row.value=Tile_row;
    document.tile.lon_min.value=Tile_Coords[Tile_row][Tile_col][2];
    document.tile.lon_max.value=Tile_Coords[Tile_row][Tile_col][3];
    document.tile.lat_min.value=Tile_Coords[Tile_row][Tile_col][4];
    document.tile.lat_max.value=Tile_Coords[Tile_row][Tile_col][5];
    document.tile.region.value=Tile_Coords[Tile_row][Tile_col][6];
  }
}

function Hide_Square() {
  if (Menue_Loaded) {
    if (NS4)
    {
      div_3.visibility="hide";
    }
    else
    {
      div_3.style.visibility="hidden";
    }
    document.tile.col.value="";
    document.tile.row.value="";
    document.tile.lon_min.value="";
    document.tile.lon_max.value="";
    document.tile.lat_min.value="";
    document.tile.lat_max.value="";
    document.tile.region.value="";
  }
}

function Check_Square(ev) {
  if(document.all && !(Aname.indexOf("konqueror")!=-1)) ev=window.event; // for IE
  if (typeof ev.layerX == 'number') {
    ev_X = ev.layerX;
    ev_Y = ev.layerY;
  }
  else if (typeof ev.offsetX == 'number') {
    ev_X = ev.offsetX+((isMac)?document.body.scrollLeft:0);
    ev_Y = ev.offsetY+((isMac)?document.body.scrollTop:0);
  }
  else {
    ev_X = ev.clientX+((isMac)?document.body.scrollLeft:0);
    ev_Y = ev.clientY+((isMac)?document.body.scrollTop:0);
  }
  xx = ev_X;
  yy = ev_Y;

  if (xx < Chooser_coord[0]+Chooser_grid[0] || xx > Chooser_coord[0]+610) {Hide_Square();}
//  if (yy < Chooser_coord[1]+Chooser_grid[1] || yy > Chooser_coord[1]+340) {Hide_Square();}
  
  return false;
}

function change_map() {

  var regions = (document.tile.regions.checked)?"_regions":"";

  var Index = 0; var product = "";
  if (document.tile.prod[Index]) {
    while (document.tile.prod[Index].checked == false) {Index++}
    product = document.tile.prod[Index].value;
  }
  else {product = document.tile.prod.value;}
  
  Index = 0;
  while (document.tile.year[Index].checked == false) {Index++}
  var year = document.tile.year[Index].value;
  if(product == "phenology"){
	//alert("this is phenology");
	document.images.chooser.src="/modis_vp/inventory_images/sinusoidal"+regions+"_phe_"+product+"_"+year+"_phe.png";
  }
else{
  document.images.chooser.src="inventory_images/sinusoidal"+regions+"_"+product+"_"+year+".png";
}
  return false;
}

function change_r_map() {
  var img_URL = document.images.chooser.src;
  var regExpr_1 = "_regions";
  var regExpr_2 = "sinusoidal";
  if (document.tile.regions.checked) {
    if (!img_URL.match(regExpr_1)) img_URL = img_URL.replace(regExpr_2,regExpr_2+regExpr_1);
  }
  else {
    if (img_URL.match(regExpr_1)) img_URL = img_URL.replace(regExpr_1,"");
  }

  document.images.chooser.src = img_URL;
}
