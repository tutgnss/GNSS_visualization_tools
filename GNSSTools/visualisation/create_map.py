# Tampere University of Technology
#
# DESCRIPTION
# Using folium, defines a function that can create a map and plot the estimated trajectory of the receiver
# and the true trajectory given by the generator
#
# AUTHOR
# Yannick DEFRANCE

# This Python file uses the following encoding: utf-8

import folium
import position


## Create a map ##
def create_map(P,Q):

# Initialisation of the first position
    map_1 = folium.Map(location=[P[0][1], P[0][2]])

# Creation of a list of the points
    a = []
    b = []
    for i in range(len(P)):
        a.append([P[i][1],P[i][2]])

    for i in range(len(Q)):
        b.append([Q[i][1],Q[i][2]])

# Ploting of the trajectory
    folium.PolyLine(a, color='red', popup='Ublox').add_to(map_1)
    folium.Marker([P[0][1],P[0][2]], popup='Start', icon=folium.Icon(color='red')).add_to(map_1)
    folium.Marker([P[len(P)-1][1],P[len(P)-1][2]], popup='End', icon=folium.Icon(color='red')).add_to(map_1)

    folium.PolyLine(b, popup='Spectracom').add_to(map_1)
    folium.Marker([Q[0][1],Q[0][2]], popup='Start').add_to(map_1)
    folium.Marker([Q[len(Q)-1][1],Q[len(Q)-1][2]], popup='End').add_to(map_1)
# Save map
    map_1.save('C:\Temp\Web page/map_1.html')

    map_2 = folium.Map(location=[P[0][1], P[0][2]])
    folium.Marker([46.8354, -121.7325], popup='Camp Muir').add_to(map_2)
    map_2.add_child(folium.ClickForMarker(popup="Waypoint"))
    map_2.save('C:\Temp\Web page/map_2.html')

