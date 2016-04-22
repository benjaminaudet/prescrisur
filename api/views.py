# coding=utf-8
from flask import *
from flask.ext.login import login_required, login_user, logout_user, current_user

from api import app, login_manager
from api.models import Pathology, Speciality, Substance, User


@app.route('/')
def index():
	return app.send_static_file('index.html')


# TODO: virer ce truc
@app.route('/lol')
def index2():
	return app.send_static_file('index_old.html')


@app.route('/api/specialities/search')
def search_speciality():
	q = request.args.get('q')
	return jsonify(data=Speciality.search(q))


@app.route('/api/substances/<subst_id>')
def substance(subst_id):
	subst = Substance.get(subst_id)
	if not subst:
		abort(404)
	return jsonify(data=subst)


@app.route('/api/substances/search')
def search_substance():
	q = request.args.get('q')
	return jsonify(data=Substance.search(q))


@app.route('/api/pathologies', methods=['POST'])
@app.route('/api/pathologies/<patho_id>', methods=['PUT'])
def edit_pathology(patho_id=None):
	data = json.loads(request.data)
	patho = Pathology(**data)
	if patho_id:
		patho.save()
	else:
		patho.create()
	return jsonify(data=patho)


@app.route('/api/pathologies/<patho_id>')
def pathology(patho_id):
	patho = Pathology.get(patho_id)
	if not patho:
		abort(404)
	return jsonify(data=patho)


@app.route('/api/pathologies/search')
def search_pathology():
	q = request.args.get('q')
	return jsonify(data=Pathology.search(q))


###############
# Login
###############


@login_manager.user_loader
def user_loader(email):
	return User.get(email)


@login_manager.unauthorized_handler
def unauthorized_handler():
	return 'Unauthorized'


@app.route('/api/login', methods=['POST'])
def login():
	data = json.loads(request.data)
	user = User.get(data['email'])
	if not user:
		abort(401)
	if data['passwd'] == user.password_hash:
		login_user(user)
		return jsonify(data=user)
	return jsonify({'error': 'error'})


@app.route('/api/logout')
@login_required
def logout():
	logout_user()
	return jsonify({'success': True})


@app.route('/api/me')
@login_required
def get_user_status():
	if not current_user:
		abort(401)
	return jsonify(user=current_user)
