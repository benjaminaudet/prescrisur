# coding=utf-8
from flask import *

from prescrisur import app
from prescrisur.update import SpecialityUpdater


@app.route('/')
def home():
	return render_template('index.html')


@app.route('/data')
@app.route('/data/<type>')
def data(type=None):
	if type:
		SpecialityUpdater().execute()
		flash('Specialites mises a jour !', 'success')
	return render_template('data.html')
