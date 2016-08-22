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
from GNSSTools.visualisation import create_map
from GNSSTools.visualisation import position
from GNSSTools.visualisation import index
from data import database
from GNSSTools.tools import data

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
    P = data('P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\s'+str(scenario)+'_ublox.txt')
    Q = data('P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\s'+str(scenario)+'_spectracom.txt')
    matrix(P,Q)
    return render_template('scenario.html', ubl=matrix(P,Q)[0], spec=matrix(P,Q)[1], scenario=scenario)

@app.route('/test', methods=['GET','POST'])
def test():
    P = data('P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\scircle_ublox.txt')
    Q = data('P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\scircle_spectracom.txt')
    matrix(P,Q)
    return render_template('test.html', ubl=matrix(P,Q)[0], spec=matrix(P,Q)[1], scenario=scenario)

if __name__ == '__main__':
    app.run(debug=True)