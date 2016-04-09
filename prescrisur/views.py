# coding=utf-8
from flask import *

from prescrisur import app
from prescrisur.models import Speciality, Substance

ANSM_SPEC_URI = 'http://base-donnees-publique.medicaments.gouv.fr/extrait.php?specid='


@app.route('/')
def home():
	return render_template('index.html')


@app.route('/speciality/<cis>')
def speciality(cis):
	return redirect(ANSM_SPEC_URI+cis)


@app.route('/api/search/speciality')
def search_speciality():
	q = request.args.get('q')
	return jsonify(data=Speciality.search(q))


@app.route('/substance/<subst_id>')
def substance(subst_id):
	subst = Substance.get(subst_id)
	if not subst:
		abort(404)
	return render_template('substance.html', substance=subst)
