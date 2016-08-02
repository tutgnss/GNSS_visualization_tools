# Tampere University of Technology
#
# DESCRIPTION
# Defines the html script of the web page
#
# AUTHOR
# Yannick DEFRANCE

#!/usr/bin/python3
# -*- coding: utf-8 -*


import cgi
import project2.create_map
import project2.position

form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")



html = """<!DOCTYPE html>
<nav></nav>
<head>
	<meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet/v0.7.7/leaflet.css" />
    <link rel="stylesheet" type="text/css" href="http://localhost:63342/Web page/css/style.css" />
</head>
<body>
<header>
    <img src="http://www.tibco.com/blog/wp-content/uploads/2014/10/TIBCO-Spotfire-4-Ways-Data-Visualization-Will-Help-Your-Organization1.jpg" />
    <h1>Visualization Tool</h1>
</header>

<section id="choices">
    <article id="run">
        <h2>Run current scenario</h2>
        <a href="http://localhost:63342/Web%20page/map_1.html"><p>Visualize the chosen scenario</p></a>

"""
print(html)
print('Current scenario : '+str(form.getvalue("select")))
html2="""
    </article>
    <article id="create">
        <h2>Create scenario</h2>
        <a href="http://localhost:63342/Web%20page/map_2.html"><p>Place yourself the markers to create your own route</p></a>
    </article>
    <article id="change">
        <h2>Change scenario</h2>
        <p>Select the scenario you want to play</p>
        <form method="post" action="/index.py" enctype=multipqrt/form-data">
            <select name="select">
                <optgroup label="Scenario">
                    <option value="Circle">Circle</option>
                    <option value="Square">Square</option>
                    <option value="Line">Line</option>
                </optgroup>
            </select>
            <input type="submit" name="change" value="Change scenario">
        </form>
    </article>
</section>


"""

print(html2)

html3 ="""

<fieldset>
    <legend>Title</legend>
    <div id="mapid"></div>
    <script src="http://cdn.leafletjs.com/leaflet/v0.7.7/leaflet.js"></script>
	<script>

		var mymap = L.map('mapid').setView([51.505, -0.09], 13);

        L.marker([51.5, -0.09]).addTo(mymap)
			.bindPopup("<b>Hello world!</b><br />I am a popup.").openPopup();

		L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpandmbXliNDBjZWd2M2x6bDk3c2ZtOTkifQ._QA7i5Mpkd_m30IGElHziw', {
			maxZoom: 18,
			attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
				'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
				'Imagery <a href="http://mapbox.com">Mapbox</a>',
			id: 'mapbox.streets'
		}).addTo(mymap);

    	L.marker([51.5, -0.09]).addTo(mymap)
			.bindPopup("<b>Hello world!</b><br />I am a popup.").openPopup();

		L.circle([51.508, -0.11], 500, {
			color: 'red',
			fillColor: '#f03',
			fillOpacity: 0.5
		}).addTo(mymap).bindPopup("I am a circle.");

		L.polygon([
			[51.509, -0.08],
			[51.503, -0.06],
			[51.51, -0.047]
		]).addTo(mymap).bindPopup("I am a polygon.");


		var popup = L.popup();

		function onMapClick(e) {
			popup
				.setLatLng(e.latlng)
				.setContent("You clicked the map at " + e.latlng.toString())
				.openOn(mymap);
		}

        mymap.on('click', onMapClick);

	</script>
</fieldset>


</body>
</html>
"""

print(html3)

P = project2.position.data('project2/ublox_data_'+str(form.getvalue("select"))+'.txt')
Q = project2.position.data2('project2/ublox_data_'+str(form.getvalue("select"))+'.txt')


project2.create_map.create_map(P,Q)
