import json
import pytest
import mongomock
from flask import url_for
import flask_login as flask_login

from api import create_app, db
from api.models import *


@pytest.fixture(scope='function')
def app():
	app_ = create_app('api.config.EnvConfig')
	return app_


@pytest.fixture(scope='function')
def mock_model(request, collection_name):
	mock_collection = mongomock.MongoClient().db[collection_name]
	model = eval(collection_name)
	model.collection = mock_collection
	return model


@pytest.fixture(scope='function')
def mock_model_bis(request, collection_name_bis):
	mock_collection = mongomock.MongoClient().db[collection_name_bis]
	model = eval(collection_name_bis)
	model.collection = mock_collection
	return model


@pytest.fixture(scope='session')
def user_collection(request):
	return mongomock.MongoClient().db.User


# TODO: Factorize user creation ?
@pytest.fixture(scope='function')
def user(client, user_collection, request):
	test_user = User(_id="test", email='test@test', password='default', name='Test', confirmed=True)
	User.collection = user_collection
	test_user.save()
	client.post(url_for('api.login'), data=json.dumps(dict(email='test@test', passwd='default')))

	def logout():
		return client.get(url_for('api.logout'))

	request.addfinalizer(logout)
	return flask_login.current_user


@pytest.fixture(scope='function')
def admin(client, user_collection, request):
	test_user = User(_id="test", email='test@test', password='default', name='Test', roles=['admin'], confirmed=True)
	User.collection = user_collection
	test_user.save()
	client.post(url_for('api.login'), data=json.dumps(dict(email='test@test', passwd='default')))

	def logout():
		return client.get(url_for('api.logout'))

	request.addfinalizer(logout)
	return flask_login.current_user


# Specialities
@pytest.fixture(scope='function')
@pytest.mark.parametrize('collection_name', ['Speciality'])
def spec1(mock_model):
	spec = Speciality(_id='61266250', name='Spec1')
	spec.save()
	return spec


@pytest.fixture(scope='function')
@pytest.mark.parametrize('collection_name', ['Speciality'])
def spec2(mock_model):
	spec = Speciality(_id='64332894', name='Spec2')
	spec.save()
	return spec


# Substances
@pytest.fixture(scope='function')
@pytest.mark.parametrize('collection_name_bis', ['Substance'])
def subst1(mock_model_bis):
	subst = Substance(_id='42215', name='Subst1')
	subst.save()
	return subst


@pytest.fixture(scope='function')
@pytest.mark.parametrize('collection_name_bis', ['Substance'])
def subst2(mock_model_bis):
	subst = Substance(_id='86571', name='Subst2')
	subst.save()
	return subst


@pytest.fixture(scope='function')
@pytest.mark.parametrize('collection_name_bis', ['Substance'])
def deleted_subst(mock_model_bis):
	subst = Substance(_id='33333', name='Deleted Subst', deleted_at='2015-10-10')
	subst.save()
	return subst