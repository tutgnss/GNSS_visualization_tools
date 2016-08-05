# Tampere University of Technology
#
# DESCRIPTION
# Calls the html script. Processing functions are added.
# This file is launched on the browser
#
# AUTHOR
# Yannick DEFRANCE

#!/usr/bin/python3
# -*- coding: utf-8 -*



from GNSSTools import tools

import cgi
from visualisation import create_map
from visualisation import position
from visualisation import index
from data import database

if __name__ == '__main__':
    form = cgi.FieldStorage()

    print("Content-type: text/html; charset=utf-8\n")

    if form.getvalue("select") == None :
        P = position.position('P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\sstatic_ublox.txt')
        Q = position.position('P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\sstatic_spectracom.txt')
    else :
        P = position.position('P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\s'+str(form.getvalue("select"))+'_ublox.txt')
        Q = position.position('P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\s'+str(form.getvalue("select"))+'_spectracom.txt')

    a = []
    b = []
    for i in range(len(P)):
        a.append([P[i][1],P[i][2]])

    for i in range(len(Q)):
        b.append([Q[i][1],Q[i][2]])

    create_map.create_map(P,Q)


    print(index.init+str(form.getvalue("select"))+index.tileLayer)
    print(index.varUblox+str(a)+index.varSpectracom+str(b)+index.popup+index.test+index.end)
