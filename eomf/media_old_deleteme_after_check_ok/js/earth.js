google.load("earth", "1");

var ge;
var gex ;
var networkLink;
var opacityObject;
var currentKmlObjects = {};
var kml_extension = ".kml";

function init() {

    google.earth.createInstance('map3d', initCB, failureCB);
    
    for(var i = 0; i<kmlobjects.length; i++){
        currentKmlObjects[kmlobjects] = null;
    }
    
    for (var entry = 0;entry < kmlobjects.length;entry++) {
        var tmp = 'slider_'+kmlobjects[entry];
        var tmp2 = kmlobjects[entry];
        $("#"+tmp).html("<div class='tmp2' id='"+tmp2+"'></div>");
        $("#"+tmp).slider({
                 animate: false,
                 step: 1,
                 min: 1,
                 orientation: 'horizontal',
                 max: 255,
                 value: 0,
                 slide:function(event,ui){
                         var id = $(this).children(".tmp2").attr("id");
                         currentKmlObjects[id].setOpacity(ui.value);
                 }
           });
    }

}

function dlog(text){
    console.log(text);
}

function initCB(instance) {
    ge = instance;
    gex = new GEarthExtensions(ge);
    ge.getWindow().setVisibility(true);
    ge.getOptions().setStatusBarVisibility(true);
    
    // add a navigation control
    ge.getNavigationControl().setVisibility(ge.VISIBILITY_AUTO);
    
    // add some layers
    ge.getLayerRoot().enableLayerById(ge.LAYER_BORDERS, true);
    ge.getLayerRoot().enableLayerById(ge.LAYER_ROADS, true);
    
    
    // create network link
    //  createNetworkLink();
    
    // fly to UNH
    /*var la = ge.createLookAt('');
    la.set(43.1347, -70.9356,
      0, // altitude
      ge.ALTITUDE_RELATIVE_TO_GROUND,
      0, // heading
      0, // straight-down tilt
      10000000 // range (inverse of zoom)
      );*/
      
    //Fly to China
    var la = ge.createLookAt('');
    la.set(35, 86,
      0, // altitude
      ge.ALTITUDE_RELATIVE_TO_GROUND,
      0, // heading
      0, // straight-down tilt
      9000000 // range (inverse of zoom)
      );
    ge.getView().setAbstractView(la);

}

/**/
function setVis(sel) {
    if (!clouds[sel].kml) {
        clouds[sel].kml = addOverlay(sel);
    } else {
        clouds[sel].kml.setVisibility(true);
        clouds[sel].kml.getColor().setA(alpha);
    }
    if (clouds[1-sel].kml)
        clouds[1-sel].kml.setVisibility(false);
    current = sel;
}
/**/

function createNetworkLink() {
    networkLink = ge.createNetworkLink("");
    networkLink.setDescription("NetworkLink open to fetched content");
    networkLink.setName("Open NetworkLink");
    networkLink.setFlyToView(false);

    // create a Link object
    var link = ge.createLink("");
    link.setHref("http://nsidc.org/data/google_earth/noaa/NSIDC_permafrost.kml");

    // attach the Link to the NetworkLink
    networkLink.setLink(link);

    // add the Network Link feature to Earth
    ge.getFeatures().appendChild(networkLink);
}
  
function failureCB(errorCode) {
    
}
  
//
//function addOverlay(sel) {
//    var icon = ge.createIcon('');
//    icon.setHref('
//}
//

  function toggleKml(file) {
    // remove the old KML object if it exists
    dlog("toggle");
    if (currentKmlObjects[file]) {
        ge.getFeatures().removeChild(currentKmlObjects[file]);
        currentKmlObject = null;
    }
    
    // if the checkbox is checked, fetch the KML and show it on Earth
    var kmlCheckbox = document.getElementById('kml-' + file);
	if (kmlCheckbox.checked)
      loadKml(file,false);
  }
  
  function loadKml(file,traverse) {
    dlog("loadKml");
	var kmlUrl = host_url + kml_path + file + kml_extension;

    // fetch the KML
    google.earth.fetchKml(ge, kmlUrl, function(kmlObject) {
      // NOTE: we still have access to the 'file' variable (via JS closures)
      dlog(kmlUrl);
      if (kmlObject) {
        // show it on Earth
        currentKmlObjects[file] = kmlObject;

		ge.getFeatures().appendChild(kmlObject);	
      } else {
        // bad KML
        currentKmlObjects[file] = null;
  
        // wrap alerts in API callbacks and event handlers
        // in a setTimeout to prevent deadlock in some browsers
        setTimeout(function() {
          alert(kmlUrl + ': Bad or null KML.');
        }, 0);
        
        // uncheck the box
        document.getElementById('kml-' + file).checked = '';
      }
    });
  }
  
  function traverseKml(node) {
		
	if (node.getFeatures().hasChildNodes()) {
      var subNodes = node.getFeatures().getChildNodes();
      var length = subNodes.getLength();
      var eachSubNode;
      var nodeType;
      var nodeName;
      var nodeID;
      var nodeDescription;
        
      for (var i = 0; i < length; i++) {
          eachSubNode = subNodes.item(i);
          nodeType = eachSubNode.getType();
          nodeName = eachSubNode.getName();
          nodeID = eachSubNode.getId();
          nodeDescription = eachSubNode.getDescription();
          //var nodeStyle = eachSubNode.getStyleUrl();
		  switch (nodeType) {
              case 'KmlNetworkLink' :
                  google.earth.fetchKml(ge, eachSubNode.getLink().getHref(), function(object) {
                    if(!object) {
                        alert('bad or Null kml');
                        return;
                    }
                    traverseKml(object);
                    ge.getFeatures().removeChild(eachSubNode);
                    ge.getFeatures().appendChild(object)
                  });
                  break;

              case 'KmlPlacemark':
                   google.earth.addEventListener(eachSubNode, 'click', function(event) {
                      event.preventDefault();
					  ge_handle_placemark(event);
					  event.stopPropagation();
                  });

                  break;
					  
              case 'KmlFolder':
                  traverseKml(eachSubNode);
                  break;
            }
        }
    }
}
  
function ge_handle_placemark(event){
//	var form_id = event.getTarget().getName();
  	var balloon = ge.createHtmlStringBalloon('');
	balloon.setContentString(event.getTarget().getDescription());
	balloon.setFeature(event.getTarget());
	balloon.setMinWidth(300);
	balloon.setMaxWidth(700);
	ge.setBalloon(balloon); //set the ballon to ge plugin
}

// Fly to the study area 
function area(name,latitude,longitude){
	gex.dom.clearFeatures();

	var folder = gex.dom.addFolder([
	  gex.dom.buildPointPlacemark([parseInt(latitude), parseInt(longitude)])  // Used parseInt because the point should be in numerical not in decimal points
	]);

	var bounds = gex.dom.computeBounds(folder);
	gex.view.setToBoundsView(bounds, { aspectRatio: 1.0 });
		
}




