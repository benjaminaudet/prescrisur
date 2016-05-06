# coding=utf-8
from flask import *
from flask.ext.login import login_required, login_user, logout_user, current_user

from api import app, login_manager
from api.models import *
from api.decorators import required_role


@app.route('/')
def index():
	return app.send_static_file('index.html')


@app.route('/api/specialities/search')
def search_speciality():
	q = request.args.get('q')
	return jsonify(data=Speciality.search_by_name(q))


@app.route('/api/substances/<subst_id>')
@login_required
def substance(subst_id):
	subst = Substance.get(subst_id)
	if not subst:
		abort(404)
	return jsonify(data=subst)


@app.route('/api/substances/search')
def search_substance():
	q = request.args.get('q')
	return jsonify(data=Substance.search_by_name(q))


@app.route('/api/substances/pathologies/<subst_id>')
@login_required
def search_pathologies_from_substance(subst_id):
	return jsonify(data=Pathology.search_by_substance(subst_id))


@app.route('/api/pathologies', methods=['POST'])
@app.route('/api/pathologies/<patho_id>', methods=['PUT'])
@required_role('admin')
def edit_pathology(patho_id=None):
	data = json.loads(request.data)
	patho = Pathology(**data).check().refresh_update_date()
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
	return jsonify(data=Pathology.search_by_name(q))


@app.route('/api/pages', methods=['POST'])
@app.route('/api/pages/<page_id>', methods=['PUT'])
@required_role('admin')
def edit_page(page_id=None):
	data = json.loads(request.data)
	p = Page(**data).check()
	if page_id:
		p.save()
	else:
		p.create()
	return jsonify(data=p)


@app.route('/api/pages/<page_id>')
def page(page_id):
	p = Page.get(page_id)
	if not p:
		abort(404)
	return jsonify(data=p)


@app.route('/api/news', methods=['POST'])
@app.route('/api/news/<news_id>', methods=['PUT'])
@required_role('admin')
def edit_news(news_id=None):
	data = json.loads(request.data)
	n = News(**data).check().refresh_update_date().set_author(current_user)
	if news_id:
		n.save()
	else:
		n.create()
	return jsonify(data=n)


@app.route('/api/news', methods=['GET'])
@app.route('/api/news/<news_id>', methods=['GET'])
def news(news_id=None):
	n = News.get(news_id)
	if not n:
		abort(404)
	return jsonify(data=n)


###############
# Login
###############


@login_manager.user_loader
def user_loader(email):
	return User.get(email)


@login_manager.unauthorized_handler
def unauthorized_handler():
	return jsonify({'need_login': True}), 401


@app.route('/api/register', methods=['POST'])
def register():
	data = json.loads(request.data)
	user = User(**data)
	res = {'success': False}
	try:
		user.create()
		res['success'] = True
	except Exception as e:
		res['error'] = repr(e)
	return jsonify(res)


@app.route('/api/login', methods=['POST'])
def login():
	data = json.loads(request.data)
	user = User.get(data['email'])
	if not user:
		abort(401)
	if user.verify_password(data['passwd']):
		login_user(user)
		return jsonify(data=user)
	return jsonify({'error': 'error'})


@app.route('/api/logout')
@login_required
def logout():
	logout_user()
	return jsonify({'success': True})


@app.route('/api/me')
def get_user_status():
	if not current_user.is_authenticated:
		return jsonify(user=False)
	delattr(current_user, 'password_hash')
	return jsonify(user=current_user)
