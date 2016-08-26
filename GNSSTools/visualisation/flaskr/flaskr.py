# Tampere University of Technology
#
# DESCRIPTION
# Calls the html script. Processing functions are added.
# This file is launched on the browser
#
# AUTHOR
# Yannick DEFRANCE

#! /usr/bin/python
# -*- coding:utf-8 -*-

# Imports
from flask import Flask, render_template, request
from GNSSTools.visualisation import index
from data import database
from GNSSTools.tools import data
from GNSSTools.tools import computation
from GNSSTools.devices import device

app = Flask(__name__)

def matrix(P,Q):
    ubl = []
    spec= []
    for i in range(len(P)):
        ubl.append([P[i][2],P[i][1],P[i][0]])
    for i in range(len(Q)):
        spec.append([Q[i][2],Q[i][1]])
    return [ubl,spec]


@app.route('/main', methods=['GET','POST'])
def main():
    scenario = request.form.get("select")
    a = scenario
    return render_template('main.html', scenario=a)



@app.route('/scenario', methods=['GET','POST'])
def scenario():
    if request.form.get("select") == None:
        scenario = 'static'
    else:
        scenario = request.form.get("select")
    U = 'P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\s'+str(scenario)+'_ublox.txt'
    S = 'P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\s'+str(scenario)+'_spectracom.txt'
    P = data(U)
    Q = data(S)
    matrix(P,Q)
    computation(file1=U, file2=S)
    return render_template('scenario.html', ubl=matrix(P,Q)[0], spec=matrix(P,Q)[1], scenario=scenario, computation=computation(file1=U, file2=S))



@app.route('/test', methods=['GET','POST'])
def test():
    P = data('P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\scircle_ublox.txt')
    Q = data('P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\scircle_spectracom.txt')
    matrix(P,Q)
    return render_template('test.html', ubl=matrix(P,Q)[0], spec=matrix(P,Q)[1], scenario=scenario)



@app.route('/point', methods=['GET','POST'])
def point():
    if request.form.get("select") == None:
        scenario = 'static'
    else:
        scenario = request.form.get("select")
    U = 'P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\s'+str(scenario)+'_ublox.txt'
    S = 'P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\s'+str(scenario)+'_spectracom.txt'
    P = data(U)
    Q = data(S)
    matrix(P,Q)
    computation(file1=U, file2=S)

    return render_template('point.html', ubl=matrix(P,Q)[0], spec=matrix(P,Q)[1], scenario=scenario, computation=computation(file1=U, file2=S))



if __name__ == '__main__':
    app.run(debug=True)