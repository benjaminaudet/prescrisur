import json
import pytest
import mongomock
from flask import url_for
import flask.ext.login as flask_login

from api import create_app
from api.models import User


@pytest.fixture(scope='function')
def app():
	app_ = create_app('api.config.EnvConfig')
	return app_


@pytest.fixture(scope='function')
def collection(request):
	return mongomock.MongoClient().db.collection


@pytest.fixture(scope='session')
def user_collection(request):
	return mongomock.MongoClient().db.User


@pytest.fixture(scope='function')
def user(client, user_collection, request):
	test_user = User(_id="test", email='test@test', password='default', name='Test')
	User.collection = user_collection
	test_user.save()
	client.post(url_for('api.login'), data=json.dumps(dict(email='test@test', passwd='default')))

	def logout():
		return client.get(url_for('api.logout'))

	request.addfinalizer(logout)
	return flask_login.current_user


@pytest.fixture(scope='function')
def admin(client, user_collection, request):
	test_user = User(_id="test", email='test@test', password='default', name='Test', roles=['admin'])
	User.collection = user_collection
	test_user.save()
	client.post(url_for('api.login'), data=json.dumps(dict(email='test@test', passwd='default')))

	def logout():
		return client.get(url_for('api.logout'))

	request.addfinalizer(logout)
	return flask_login.current_user