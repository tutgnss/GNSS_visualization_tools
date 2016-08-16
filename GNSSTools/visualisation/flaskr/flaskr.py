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

app = Flask(__name__)

@app.route('/main', methods=['GET','POST'])
def main():
    scenario = request.form.get("select")
    a = scenario
    return render_template('main.html', scenario=a)

@app.route('/scenario', methods=['GET','POST'])
def scenario():
    ubl = []
    spec=[]
    if request.form.get("select") == None:
        scenario = 'static'
    else:
        scenario = request.form.get("select")
    P = position.position('P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\s'+str(scenario)+'_ublox.txt')
    Q = position.position('P:\My Documents\Desktop\GitHub\GNSS_visualization_tools\data\database\s'+str(scenario)+'_spectracom.txt')
    for i in range(len(P)):
        ubl.append([P[i][1],P[i][2]])
    for i in range(len(Q)):
        spec.append([Q[i][1],Q[i][2]])
    return render_template('scenario.html', ubl=ubl, spec=spec, scenario=scenario)

if __name__ == '__main__':
    app.run(debug=True)