import json
from flask import url_for
from freezegun import freeze_time

from api.models import Pathology


def test_get_patho(collection, client):
	# Given
	obj = {"_id": "patho", "name": "Patho", "levels": [], "intro": "intro", "conclu": "conclu", "updated_at": None}
	collection.insert(obj)
	Pathology.collection = collection

	# When
	res = client.get(url_for('api.pathology', patho_id='patho'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == obj


def test_get_patho_no_patho_404(collection, client):
	# Given
	Pathology.collection = collection

	# When
	res = client.get(url_for('api.pathology', patho_id='patho'))

	# Then
	assert res.status_code == 404


def test_get_all_patho(collection, client):
	# Given
	objs = [
		{"_id": "patho1", "name": "Patho1", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None},
		{"_id": "patho2", "name": "Patho2", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None},
		{"_id": "patho3", "name": "Patho3", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None}
	]
	map(lambda o: collection.insert(o), objs)
	Pathology.collection = collection

	# When
	res = client.get(url_for('api.pathologies'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == [
		{"_id": "patho1", "name": "Patho1", "updated_at": None},
		{"_id": "patho2", "name": "Patho2", "updated_at": None},
		{"_id": "patho3", "name": "Patho3", "updated_at": None}
	]


def test_get_all_patho_no_patho_404(collection, client):
	# Given
	Pathology.collection = collection

	# When
	res = client.get(url_for('api.pathologies'))

	# Then
	assert res.status_code == 404


def test_search_patho(collection, client):
	# Given
	objs = [
		{"_id": "patho1", "name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": "2015-12-12 00:00:00"},
		{"_id": "patho2", "name": "SuperPatho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": "2015-12-12 00:00:00"},
		{"_id": "super", "name": "Super", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": "2015-12-12 00:00:00"}
	]
	map(lambda o: collection.insert(o), objs)
	Pathology.collection = collection

	# When
	res = client.get(url_for('api.search_pathology'), query_string={'q': 'patho'})
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == [
		{"_id": "patho1", "name": "Patho", "updated_at": "2015-12-12 00:00:00"},
		{"_id": "patho2", "name": "SuperPatho", "updated_at": "2015-12-12 00:00:00"},
	]


@freeze_time("2015-01-01")
def test_create_patho(collection, client, admin):
	# Given
	obj = {"name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None}
	Pathology.collection = collection

	# When
	res = client.post(url_for('api.edit_pathology'), data=json.dumps(obj), content_type='application/json')
	data = res.json

	assert res.status_code == 201
	assert data['data']['name'] == 'Patho'
	assert data['data']['_id'] == 'patho'
	assert data['data']['intro'] == 'intro'
	assert data['data']['conclu'] == 'conclu'
	assert data['data']['updated_at'] == '2015-01-01T00:00:00'


@freeze_time("2015-01-01")
def test_update_patho(collection, client, admin):
	# Given
	obj = {"_id": "patho-id", "name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu",
	       "updated_at": '2014-01-01T00:00:00'}
	Pathology.collection = collection

	# When
	res = client.put(url_for('api.update_pathology', patho_id='patho-id'), data=json.dumps(obj),
	                 content_type='application/json')
	data = res.json

	assert res.status_code == 200
	assert data['data']['name'] == 'Patho'
	assert data['data']['_id'] == 'patho-id'
	assert data['data']['intro'] == 'intro'
	assert data['data']['conclu'] == 'conclu'
	assert data['data']['updated_at'] == '2015-01-01T00:00:00'


def test_update_path_unauthorized_403(collection, client, user):
	# Given
	obj = {"_id": "patho-id", "name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu",
	       "updated_at": '2014-01-01T00:00:00'}
	Pathology.collection = collection

	# When
	res = client.put(url_for('api.update_pathology', patho_id='patho-id'), data=json.dumps(obj),
	                 content_type='application/json')

	assert res.status_code == 403


def test_update_path_not_logged_in_401(collection, client):
	# Given
	obj = {"_id": "patho-id", "name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu",
	       "updated_at": '2014-01-01T00:00:00'}
	Pathology.collection = collection

	# When
	res = client.put(url_for('api.update_pathology', patho_id='patho-id'), data=json.dumps(obj),
	                 content_type='application/json')

	assert res.status_code == 401


def test_delete_patho(collection, client, admin):
	# Given
	obj = {"_id": "patho", "name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None}
	collection.insert(obj)
	Pathology.collection = collection

	# When
	res_del = client.delete(url_for('api.delete_pathology', patho_id='patho'))
	res_get = client.get(url_for('api.pathology', patho_id='patho'))

	# Then
	assert res_del.status_code == 200
	assert res_get.status_code == 404


def test_delete_patho_unauthorized_403(collection, client, user):
	# Given
	obj = {"_id": "patho", "name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None}
	collection.insert(obj)
	Pathology.collection = collection

	# When
	res_del = client.delete(url_for('api.delete_pathology', patho_id='patho'))
	res_get = client.get(url_for('api.pathology', patho_id='patho'))

	# Then
	assert res_del.status_code == 403
	assert res_get.status_code == 200


def test_delete_patho_not_logged_in_401(collection, client):
	# Given
	obj = {"_id": "patho", "name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None}
	collection.insert(obj)
	Pathology.collection = collection

	# When
	res_del = client.delete(url_for('api.delete_pathology', patho_id='patho'))

	# Then
	assert res_del.status_code == 401


def test_search_pathologies_from_substance(collection, client, user):
	subst = {"_id": "subst", "status": None, "name": "MAGNESIA", "specialities": []}
	collection.insert(subst)
	patho = {"_id": "patho", "name": "Patho", "intro": "intro",
	         "levels": [
		         {
			         "name": "level",
			         "entries": [
				         {
					         "type": "substances",
					         "reco": {"_id": "osef"},
					         "product": {
						         "_id": "subst"
					         }
				         }
			         ]
		         }
	         ],
	         "conclu": "conclu", "updated_at": None}
	collection.insert(patho)
	Pathology.collection = collection

	# When
	res = client.get(url_for('api.search_pathologies_from_substance', subst_id='subst'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert len(data['data']) == 1
	assert data['data'][0]['_id'] == 'patho'


def test_search_pathologies_from_substance_not_logged_in_401(collection, client):
	patho = {"_id": "patho", "name": "Patho", "intro": "intro", "levels": None, "conclu": "conclu", "updated_at": None}
	collection.insert(patho)
	Pathology.collection = collection

	# When
	res = client.get(url_for('api.search_pathologies_from_substance', subst_id='subst'))

	# Then
	assert res.status_code == 401
