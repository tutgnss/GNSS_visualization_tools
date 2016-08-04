__author__ = 'defrance'

import sys
sys.path.append('P:\\My Documents\\Desktop\\GitHub\\GNSS_visualization_tools\\data')
sys.path.append('P:\\My Documents\\Desktop\\GitHub\\GNSS_visualization_tools\\GNSSTools')

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
        P = position.position('P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\static_ublox.txt')
        Q = position.position('P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\static_spectracom.txt')
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




    print(index.html+str(form.getvalue("select"))+index.html2)
    print(index.html4+str(a)+index.html5+str(b)+index.html6)
