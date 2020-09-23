function DataQuery(element_id){
    var self = this;

    self.out_id = "#data-output";
    self.form_id = "#latlon";
    self.parent_id = element_id;
    self.selector_id = "#data-selection";

    self.formoutput = '<div id="data-output" class="span12 style="margin-left:auto;margin-rigt:auto;"><div id="output_title"><h3>Data</h3></div>';

    self.formstring =
        '<div class="span6 offset3" id="data-selector">'+
        ''+
        '<h4 style="text-align:center;">Select location, product and year</h5>'+
        '<form id="latlong" name="latlong" >'+
        '   <div class="row-fluid">'+
        '   <div class="span12">'+
        '       <div class="span6">'+
        '           <label>Latitude</label>'+
        '           <input class="span12" name="LAT" type="text" size="20">'+
        '       </div>'+
        '      <div class="span6">'+
        '           <label>Longitude</label>'+
        '           <input class="span12" name = "LONG" type = "text" size="20">'+
        '      </div>'+
        '   </div>'+
        '   <div class="span12" style="margin-left: 0;">'+
        '       <div class="span6">'+
        '           <label>Dataset</label>'+
        '           <select class="span12" name="dataset" size="4">'+
        '               <option value ="mod09a1" selected>MOD09A1</option>'+
        '               <option value ="mcd43a4">MCD43A4</option>'+
        '               <option value ="mod09q1">MOD09Q1</option>'+
        '               <option value ="mod11a2">MOD11A2</option>'+
        '               <option value ="mod11c3">MOD11C3</option>'+
        '               <option value ="mod12q1">MOD12Q1</option>'+
        '               <option value ="mod13c2">MOD13C2</option>'+
        '               <option value ="mod14a2">MOD14A2</option>'+
        '               <option value ="mod17a2">MOD17A2</option>'+
        '               <option value ="myd11a2">MYD11A2</option>'+
        '               <option value ="myd11c3">MYD11C3</option>'+
        '               <option value ="myd14a2">MYD14A2</option>'+
        '           </select>'+
        '       </div>'+
        '       <div class="span6">'+
        '           <label>Year</label>'+
        '           <select class="span12" name="years" multiple="multiple">'+
        '               <option value="2000">2000</option>'+
        '               <option value="2001">2001</option>'+
        '               <option value="2002">2002</option>'+
        '               <option value="2003">2003</option>'+
        '               <option value="2004">2004</option>'+
        '               <option value="2005">2005</option>'+
        '               <option value="2006">2006</option>'+
        '               <option value="2007">2007</option>'+
        '               <option value="2008">2008</option>'+
        '               <option value="2009">2009</option>'+
        '               <option value="2010">2010</option>'+
        '               <option value="2011">2011</option>'+
        '               <option value="2012">2012</option>'+
        '               <option value="2013">2013</option>'+
        '               <option value="2014" selected>2014</option>'+ 
        '           </select>'+
        '       </div>'+
        '       <button class="btn" type = "submit" value = "Submit">Submit</button>'+
        '       <button class="btn" type = "reset">Reset</button>'+
        '    </div>'+
        '    </div>'+
        '</form>'+
        '</div>';

    if($(self.selector_id).length<=0){
        self.selector = $(self.formstring);
        self.selector.hide().appendTo(self.parent_id).fadeIn();
    }else{

    }

    $("#latlong").submit(function(){
        self.showData(this.LONG.value,
                      this.LAT.value,
                      self.l2s(this.years),
                      this.dataset.value);
        return false;
    });

    self.l2s = function (listBox) {
        if (typeof listBox === "string") {
            listBox = document.getElementById(listBox);
        }
        if (!(listBox || listBox.options)) {
            throw Error("No options");
        }
        var options=[],opt;
        for (var i=0, l=listBox.options.length; i < l; ++i) {
            opt = listBox.options[i];
            if ( opt.selected ) {
                options.push(opt.value);
            }
        }
        return options.join(",");
    };

    self.timeSeries = function(lon, lat){
        //alert(lon+"|"+lat);
        document.latlong.LAT.value = lat;
        document.latlong.LONG.value = lon;
    };

    self.setCoords = function(lon, lat){
        //alert(lon+"|"+lat);
        document.latlong.LAT.value = lat;
        document.latlong.LONG.value = lon;
    };

    self.showData = function(lon, lat, year, prod){
        if(lat.length == 0 || lon.length == 0){
            alert('Please pick a point');
        }else{
            var str = "<p>";
            str += "<br /> Latitude: " + lat;
            str += "<br /> Longitude: " + lon;
            //query(lat, lon);

            var filename = prod+"_"+year+"_"+jQuery.trim(lat)+"_"+jQuery.trim(lon);

            str += "<br /> Download raw data as an ASCII Table: <a href=\"/visualization/ascii_"+filename+".txt\">ascii_"+filename+".txt</a>";
            str += "<br /> Download raw data as an CSV Table: <a href=\"/visualization/csv_"+filename+".csv\">csv_"+filename+".csv</a>";
            if (prod == 'mod09a1' || prod == 'mod09q1'){
                str += "<br /> Download products as CSV Table: <a href=\"/visualization/csv_products_"+filename+".csv\">csv_products_"+filename+".csv</a>";
            }
            str += "<br /> View raw data as a series of graphs: <a href=\"/visualization/graph-"+filename+"\">Graph Data</a>";
             str += "<br /> View products in graphs <a href=\"/visualization/graphjs2-"+filename+"\">Graph Data</a>";
            str += "<p>";

            if($(self.out_id).length <= 0){
                self.selector.after(self.formoutput);
            }

            $(self.out_id).append(str);

            $(self.out_id+" a").click(function(){
                window.open(this.href);
                return false;
            });
        }
    };

    self.query = function(lon, lat){
        //alert('Viewing: '+form_id);
        //$("#ge_output").append(form_id);
        var out = "test";
        $.get("/visualization/ascii", {lat: latV, lon: lonV},
            function(data) {
                $(self.out_id).html(data);
            },
            "html"
        );
        return out;
    };

    return self;
}

function timeSeries(lon, lat){
    var ds = DataQuery("#content");
    ds.timeSeries(lon, lat);
}

var dms2dd = function (d, m, s){
    var total = 0.0;
    var latsign = 1;

    if(d < 0)
        latsign = -1;
    absd = Math.abs(d);
    if (absd > 0)
        total += absd;
    if (m > 0)
        total += m/60;
    if (s > 0)
        total += s/3600;

    return total * latsign;
};
