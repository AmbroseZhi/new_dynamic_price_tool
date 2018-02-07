#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dynamic_pricing_tool
from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)


pt = dynamic_pricing_tool.UseRateCalc()


@app.route('/action_page.html', methods=['POST'])
def calc_rent():
	#if request.method == 'POST':
		#if request.form['truck_size'] != current_app.config['USERNAME']:
		#request.form['hours']

	calc_rent = {
		'start_date': request.form['dini']+" "+request.form['hini'],
		'end_date': request.form['dend']+" "+request.form['hend'],
		'mileage': request.form['mileage'],
		'result': pt.total_cost(request.form['dini']+" "+request.form['hini'], request.form['dend']+" "+request.form['hend'], request.form['mileage'])
	}

	return render_template("action_page.html", rent=calc_rent)

@app.route('/')
def index():
	return render_template("t2.html")
	#return \"We're walking out of the store\"

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)


