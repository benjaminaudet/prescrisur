# coding=utf-8
from flask import *
from flask.ext.login import login_required, login_user, logout_user, current_user

from api import login_manager
from api.models import *
from api.decorators import required_role
from api.services import mail as mail_service

api = Blueprint('api', __name__)


@api.route('/')
def index():
	return app.send_static_file('index.html')


@api.route('/api/specialities/search')
def search_speciality():
	q = request.args.get('q')
	return jsonify(data=Speciality.search_by_name(q))


@api.route('/api/substances/<subst_id>')
@login_required
def substance(subst_id):
	subst = Substance.get(subst_id)
	if not subst:
		abort(404)
	return jsonify(data=subst)


@api.route('/api/substances/search')
def search_substance():
	q = request.args.get('q')
	with_spec = request.args.get('specialities')
	if not with_spec or with_spec == 'false':
		return jsonify(data=Substance.search_by_name(q))
	else:
		return jsonify(data=Substance.search_by_name(q, {'name': 1, 'status': 1, 'specialities': 1}))


@api.route('/api/pathologies/substances/<subst_id>')
@login_required
def search_pathologies_from_substance(subst_id):
	return jsonify(data=Pathology.search_by_substance(subst_id))


@api.route('/api/pathologies', methods=['POST'])
@api.route('/api/pathologies/<patho_id>', methods=['PUT'])
@required_role('admin')
def edit_pathology(patho_id=None):
	data = json.loads(request.data)
	patho = Pathology(**data).check().refresh_update_date()
	patho.save_therapeutic_classes()
	patho.save()
	return jsonify(data=patho)


@api.route('/api/pathologies/<patho_id>', methods=['DELETE'])
@required_role('admin')
def delete_pathology(patho_id):
	success = False
	remove = Pathology.delete(patho_id)
	if remove.acknowledged:
		success = True
	return jsonify({'success': success})


@api.route('/api/pathologies', methods=['GET'])
@api.route('/api/pathologies/<patho_id>', methods=['GET'])
def pathology(patho_id=None):
	patho = Pathology.get(patho_id)
	if not patho:
		abort(404)
	return jsonify(data=patho)


@api.route('/api/pathologies/search')
def search_pathology():
	q = request.args.get('q')
	return jsonify(data=Pathology.search_by_name(q))


@api.route('/api/classes/<class_id>', methods=['GET'])
@login_required
def therapeutic_class(class_id=None):
	t_class = TherapeuticClass.get(class_id)
	if not t_class:
		abort(404)
	return jsonify(data=t_class)


@api.route('/api/classes/search')
def search_therapeutic_class():
	q = request.args.get('q')
	return jsonify(data=TherapeuticClass.search_by_name(q))


@api.route('/api/pages', methods=['POST'])
@api.route('/api/pages/<page_id>', methods=['PUT'])
@required_role('admin')
def edit_page(page_id=None):
	data = json.loads(request.data)
	p = Page(**data).check()
	p.save()
	return jsonify(data=p)


@api.route('/api/pages', methods=['GET'])
@api.route('/api/pages/<page_id>', methods=['GET'])
def page(page_id=None):
	p = Page.get(page_id)
	if not p:
		abort(404)
	return jsonify(data=p)


@api.route('/api/news', methods=['POST'])
@api.route('/api/news/<news_id>', methods=['PUT'])
@required_role('admin')
def edit_news(news_id=None):
	data = json.loads(request.data)
	n = News(**data).check().refresh_update_date().set_author(current_user)
	n.save()
	return jsonify(data=n)


@api.route('/api/news/<news_id>', methods=['DELETE'])
@required_role('admin')
def delete_news(news_id):
	success = False
	remove = News.delete(news_id)
	if remove.acknowledged:
		success = True
	return jsonify({'success': success})


@api.route('/api/news', methods=['GET'])
@api.route('/api/news/<news_id>', methods=['GET'])
def news(news_id=None):
	n = News.get(news_id)
	if not n:
		abort(404)
	return jsonify(data=n)


@api.route('/api/associations', methods=['POST'])
@api.route('/api/associations/<asso_id>', methods=['PUT'])
@required_role('admin')
def edit_association(asso_id=None):
	data = json.loads(request.data)
	asso = Association(**data)
	asso.save()
	return jsonify(data=asso)


@api.route('/api/associations/<asso_id>', methods=['DELETE'])
@required_role('admin')
def delete_association(asso_id):
	success = False
	remove = Association.delete(asso_id)
	if remove.acknowledged:
		success = True
	return jsonify({'success': success})


@api.route('/api/associations', methods=['GET'])
def association():
	asso = Association.get()
	if not asso:
		abort(404)
	return jsonify(data=asso)


@api.route('/api/associations/search')
def search_association():
	q = request.args.get('q')
	return jsonify(data=Association.search_by_name(q, proj=None))


@api.route('/api/users', methods=['GET'])
@required_role('admin')
def users():
	return jsonify(data=User.all())


@api.route('/api/users/<user_id>/subscription', methods=['PUT', 'DELETE'])
def subscribe(user_id):
	u = User.get(user_id)
	if not u:
		abort(404)
	if request.method == 'PUT':
		u.add_role('subscriber').save()
	elif request.method == 'DELETE':
		u.remove_role('subscriber').save()
	return jsonify({'success': True})


@api.route('/api/mail', methods=['POST'])
def send_mail():
	data = json.loads(request.data)
	mail_service.send(data)
	return jsonify({'success': True})


###############
# Login
###############


@login_manager.user_loader
def user_loader(email):
	return User.get(email)


@login_manager.unauthorized_handler
def unauthorized_handler():
	return jsonify({'need_login': True}), 401


@api.route('/api/register', methods=['POST'])
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


@api.route('/api/login', methods=['POST'])
def login():
	data = json.loads(request.data)
	user = User.get(data['email'])
	if not user:
		abort(401)
	if user.verify_password(data['passwd']):
		login_user(user)
		return jsonify(data=user)
	return jsonify({'error': 'error'})


@api.route('/api/logout')
@login_required
def logout():
	logout_user()
	return jsonify({'success': True})


@api.route('/api/me')
def get_user_status():
	if not current_user.is_authenticated:
		return jsonify(user=False)
	delattr(current_user, 'password_hash')
	return jsonify(user=current_user)
