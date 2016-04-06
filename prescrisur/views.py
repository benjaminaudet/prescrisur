from prescrisur import app

from flask import *


@app.route('/')
def home():
	return render_template('index.html')


@app.route('/data')
def data():
	return render_template('data.html')
