import json
from flask import url_for

from api.models import User


def test_get_me(client, user):
	# When
	res = client.get(url_for('api.get_user_status'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['user'] == user.serialize()


def test_get_me_not_logged_in(client):
	# When
	res = client.get(url_for('api.get_user_status'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert not data['user']


def test_logout(client, user):
	# When
	res_out = client.get(url_for('api.logout'))
	res_in = client.get(url_for('api.get_user_status'))
	data = res_in.json

	# Then
	assert res_out.status_code == 200
	assert res_in.status_code == 200
	assert not data['user']


def test_logout_not_logged_in(client):
	# When
	res_out = client.get(url_for('api.logout'))

	# Then
	assert res_out.status_code == 401


def test_login(user_collection, client):
	# Given
	test_user = User(_id="test", email='test@test', password='default', name='Test', confirmed=True)
	User.collection = user_collection

	# When
	res_in = client.post(url_for('api.login'), data=json.dumps(dict(email='test@test', passwd='default')), content_type='application/json')
	data = res_in.json
	res = client.get(url_for('api.get_user_status'))
	user = res.json

	# Then
	assert res_in.status_code == 200
	assert data['data'] == test_user.clean().serialize()
	assert res.status_code == 200
	assert data['data'] == user['user']


def test_login_no_user_401(user_collection, client):
	# Given
	User.collection = user_collection

	# When
	res = client.post(url_for('api.login'), data=json.dumps(dict(email='nouser@test', passwd='default')), content_type='application/json')

	# Then
	assert res.status_code == 401


def test_login_bad_password_400(user_collection, client):
	# Given
	User.collection = user_collection

	# When
	res = client.post(url_for('api.login'), data=json.dumps(dict(email='test@test', passwd='badpass')), content_type='application/json')
	data = res.json

	# Then
	assert res.status_code == 400
	assert data['bad_password']


def test_login_not_confirmed_400(user_collection, client):
	# Given
	test_user = User(_id="notconfirmed", email='notconfirmed@test', password='default', name='Test', confirmed=False)
	User.collection = user_collection
	test_user.save()

	# When
	res = client.post(url_for('api.login'), data=json.dumps(dict(email='notconfirmed@test', passwd='default')), content_type='application/json')
	data = res.json

	# Then
	assert res.status_code == 400
	assert data['not_confirmed']
