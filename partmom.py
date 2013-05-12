#!/usr/bin/env python

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template
from werkzeug import secure_filename
import os

from settings import *
import xilinx

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/xilinx/spartan6', methods=['GET'])
def xilinx_spartan6():
    return render_template('grid.html', grid=xilinx.spartan6_grid)

@app.route('/xilinx/zynq7000', methods=['GET'])
def xilinx_zynq7000():
    return render_template('grid.html', grid=xilinx.zynq7000_grid)

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT, host=HOST)
