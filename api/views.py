# coding=utf-8
from flask import *

from api import app
from api.models import Speciality, Substance


@app.route('/')
def index():
	return app.send_static_file('index.html')


@app.route('/api/speciality/search')
def search_speciality():
	q = request.args.get('q')
	return jsonify(data=Speciality.search(q))


@app.route('/api/substances/<subst_id>')
def substance(subst_id):
	subst = Substance.get(subst_id)
	if not subst:
		abort(404)
	return jsonify(data=subst)
