# Tampere University of Technology
#
# DESCRIPTION
# Defines the Flask application. Launches the server where the application is hosted.
# All the pages paths are defined here.
#
# AUTHOR
# Yannick DEFRANCE

#! /usr/bin/python
# -*- coding:utf-8 -*-

# Imports
from flask import Flask, render_template, request
from data import database
from GNSSTools.tools import data
from GNSSTools.tools import computation
from GNSSTools.devices import device

app = Flask(__name__)

def matrix(P,Q,R,T):
    ubl = []
    spec= []
    for i in range(len(P)):
        ubl.append([P[i+250]['long'],P[i+250]['lat'],P[i+250]['time'],R[i]['Speed Over Ground']])
    for i in range(len(Q)):
        spec.append([Q[i]['long'],Q[i]['lat'],Q[i]['time'],T[i]['Speed Over Ground']])
    return [ubl,spec]

def gsv_data(P,Q):
    ubl = []
    spec = []
    for i in range(len(P)):
        a = []
        b = []
        for j in range(len(P[i])):
            a.append([P[i][j]['elevation'],P[i][j]['C/N0'],P[i][j]['azimuth'],P[i][j]['Sat ID']])
        ubl.append(a)
        for k in range(len(Q[i])):
            b.append([Q[i][j]['elevation'],Q[i][j]['C/N0'],Q[i][j]['azimuth'],Q[i][j]['Sat ID']])
        spec.append(b)
    return [ubl,spec]



@app.route('/home', methods=['GET','POST'])
def main():
    scenario = request.form.get("select")
    a = scenario
    return render_template('home.html', scenario=a)



@app.route('/scenario', methods=['GET','POST'])
def scenario():
    if request.form.get("select") == None:
        scenario = 'static'
    else:
        scenario = request.form.get("select")
    U = 'P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\s'+str(scenario)+'_ublox.txt'
    S = 'P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\s'+str(scenario)+'_spectracom.txt'
    DU = device.Device(U)
    DS = device.Device(S)
    P = DU.nmea_gga_store(U)
    Q = DS.nmea_gga_store(S)
    R = DU.nmea_rmc_store(U)
    T = DS.nmea_rmc_store(S)
    V = DU.nmea_gsv_store(U)
    W = DS.nmea_gsv_store(S)
    a = gsv_data(V,W)
    b = matrix(P,Q,R,T)
    computation(file1=U, file2=S)
    return render_template('scenario.html', ubl=b[0], spec=b[1],
                           gsvUbl=a[0], gsvSpec=a[1], scenario=scenario, computation=computation(file1=U, file2=S))



if __name__ == '__main__':
    app.run(debug=True)