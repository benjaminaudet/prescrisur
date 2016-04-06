# coding=utf-8
from flask import *

from prescrisur import app
from prescrisur.update import SpecialityUpdater


@app.route('/')
def home():
	return render_template('index.html')
