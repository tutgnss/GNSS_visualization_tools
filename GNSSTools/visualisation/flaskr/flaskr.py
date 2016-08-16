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
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('layout.html',)

if __name__ == '__main__':
    app.run(debug=True)