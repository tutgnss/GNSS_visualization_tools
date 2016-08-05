# Tampere University of Technology
#
# DESCRIPTION
# Defines the html script of the web page
#
# AUTHOR
# Yannick DEFRANCE

#!/usr/bin/python3
# -*- coding: utf-8 -*


init = """<!DOCTYPE html>
<nav></nav>
<head>
	<meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet/v0.7.7/leaflet.css" />
<style>
header
{
text-align: center;

}

img
{

}

body
{
background-color: #BDBDBD;
line-height: 1.65em;
font-size: 16px;
text-align: center;
margin: 0 auto;
margin-bottom: 100px;
height:100%
}


a:link
{
color: #696;
text-decoration: none;
background-color: transparent
}

a:visited
{
color: #699;
text-decoration: none;
background-color: transparent
}

a:hover
{
color: #c93;
text-decoration: underline;
background-color: transparent
}

a:active
{
color: #900;
text-decoration: underline;
background-color: transparent
}

fieldset
{
min-height: 20em;
border-radius: 12px;
margin-top: 50px;
margin-right: 200px;
margin-left: 200px;

}

#mapid
{
height: 400px;
}


#choices
{
width:100%;
height:150px;
border-top: 2px solid;
border-bottom: 2px solid;
}


#choices #run
{
float: left;
width:471px;


}


#choices #create
{
float: left;
width:978px;


}


#choices #change
{
float: left;

}

#myLines
{
color: red;
}
</style>
</head>

<body>
<header>
    <img src="http://www.tibco.com/blog/wp-content/uploads/2014/10/TIBCO-Spotfire-4-Ways-Data-Visualization-Will-Help-Your-Organization1.jpg" />
    <h1>Visualization Tool</h1>
</header>

<section id="choices">
    <article id="run">
        <h2>Run current scenario</h2>
        <p>Visualize the chosen scenario</p>
    </article>
    <article id="create">
        <h2>Create scenario</h2>
        <p>Select the parameters to create your own route</p>
    </article>
    <article id="change">
        <h2>Change scenario</h2>
        <p>Select the scenario you want to play</p>
        <form method="post" action="/main_vis.py" enctype=multipqrt/form-data">
            <select name="select">
                <optgroup label="Scenario">
                    <option value="circle">Circle</option>
                    <option value="square">Square</option>
                    <option value="acceleration">Acceleration</option>
                    <option value="static">Static</option>
                    <option value="cno">CN0</option>
                    <option value="freetourban">Free to Urban</option>
                </optgroup>
            </select>
            <input type="submit" name="change" value="Change scenario">
        </form>
    </article>
</section>

<fieldset>
    <legend>Visualisation of the
"""

tileLayer = """
    scenario</legend>
    <div id="mapid">
    <script src="sample-geojson.js" type="text/javascript"></script>
	<script src="https://npmcdn.com/leaflet@1.0.0-rc.2/dist/leaflet.js"></script>
	<script>

		var mymap = L.map('mapid').setView([51.505, -0.09], 13);

		L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpandmbXliNDBjZWd2M2x6bDk3c2ZtOTkifQ._QA7i5Mpkd_m30IGElHziw', {
			attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
				'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
				'Imagery <a href="http://mapbox.com">Mapbox</a>',
			id: 'mapbox.streets'
		}).addTo(mymap);
"""

varUblox = """

        var ublox = L.polyline("""

varSpectracom = """
        , {color: 'red'}).addTo(mymap);

        mymap.fitBounds(ublox.getBounds());

        var spectracom = L.polyline("""

popup = """
        , {color: 'blue'}).addTo(mymap);

        function onEachFeature(feature, layer) {
		        	var popupContent = "<p>I started out as a GeoJSON " +
				        	feature.geometry.type + ", but now I'm a Leaflet vector!</p>";

        			if (feature.properties && feature.properties.popupContent) {
		        		popupContent += feature.properties.popupContent;
			        }

			        layer.bindPopup(popupContent);
                }

        L.geoJson(ublox, {

			filter: function (feature, layer) {
				if (feature.properties) {
					// If the property "underConstruction" exists and is true, return false (don't render features under construction)
					return feature.properties.underConstruction !== undefined ? !feature.properties.underConstruction : true;
				}
				return false;
			},

			onEachFeature: onEachFeature
		}).addTo(mymap);

    </script>
	</div>
</fieldset>
"""

test = """

<fieldset>
<legend>Test</legend>
    <p>test</p>
</fieldset>

"""

end = """

</body>
</html>
"""




