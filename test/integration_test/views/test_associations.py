import json
from flask import url_for

from api.models import Association, Substance


def test_get_all_asso(collection, client, admin):
	# Given
	objs = [
		{"_id": "02032", "name": "SuperAsso", "substances": None, "specialities": None},
		{"_id": "02039", "name": "Asso", "substances": None, "specialities": None},
		{"_id": "02301", "name": "Super", "substances": None, "specialities": None}
	]
	map(lambda o: collection.insert(o), objs)
	Association.collection = collection

	# When
	res = client.get(url_for('api.associations'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == objs


def test_get_all_asso_no_asso_404(collection, client, admin):
	# Given
	Association.collection = collection

	# When
	res = client.get(url_for('api.associations'))

	# Then
	assert res.status_code == 404


def test_get_all_asso_not_authorized_403(collection, client, user):
	# Given
	objs = [
		{"_id": "02032", "name": "SuperAsso", "substances": None, "specialities": None},
		{"_id": "02039", "name": "Asso", "substances": None, "specialities": None},
		{"_id": "02301", "name": "Super", "substances": None, "specialities": None}
	]
	map(lambda o: collection.insert(o), objs)
	Association.collection = collection

	# When
	res = client.get(url_for('api.associations'))

	# Then
	assert res.status_code == 403


def test_get_all_asso_not_logged_in_401(collection, client):
	# Given
	objs = [
		{"_id": "02032", "name": "SuperAsso", "substances": None, "specialities": None},
		{"_id": "02039", "name": "Asso", "substances": None, "specialities": None},
		{"_id": "02301", "name": "Super", "substances": None, "specialities": None}
	]
	map(lambda o: collection.insert(o), objs)
	Association.collection = collection

	# When
	res = client.get(url_for('api.associations'))

	# Then
	assert res.status_code == 401


def test_search_asso(collection, client):
	# Given
	objs = [
		{"_id": "02032", "name": "SuperAsso", "substances": None, "specialities": None},
		{"_id": "02039", "name": "Asso", "substances": None, "specialities": None},
		{"_id": "02301", "name": "Super", "substances": None, "specialities": None}
	]
	map(lambda o: collection.insert(o), objs)
	Association.collection = collection

	# When
	res = client.get(url_for('api.search_association'), query_string={'q': 'asso'})
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == [
		{"_id": "02032", "name": "SuperAsso", "specialities": None},
		{"_id": "02039", "name": "Asso", "specialities": None}
	]


def test_create_asso(collection, client, admin):
	# Given
	obj = {"name": "SuperAsso", "substances": [{"_id": "1", "name": "Substance"}], "specialities": None}
	subst = {"_id": "1", "name": "Substance", "specialities": [{"_id": "1", "name": "Speciality"}]}
	collection.insert(subst)
	Association.collection = collection
	Substance.collection = collection

	# When
	res = client.post(url_for('api.edit_association'), data=json.dumps(obj), content_type='application/json')
	data = res.json

	assert res.status_code == 201
	assert data['data']['name'] == 'SuperAsso'
	assert data['data']['_id'] == 'superasso'
	assert data['data']['substances'] == [{"_id": "1", "name": "Substance", "specialities": [], "status": None}]
	assert data['data']['specialities'] == [{'status': None, 'name': 'Speciality', 'short_name': None, 'enabled': True, 'treatment_type': None, 'spec_type': None, '_id': '1', 'dosage': None}]


def test_update_asso(collection, client, admin):
	# Given
	obj = {"_id": "1", "name": "SuperAsso", "substances": None, "specialities": None}
	Association.collection = collection

	# When
	res = client.put(url_for('api.update_association', asso_id='1'), data=json.dumps(obj), content_type='application/json')
	data = res.json

	assert res.status_code == 200
	assert data['data']['name'] == 'SuperAsso'
	assert data['data']['_id'] == '1'


def test_update_asso_not_authorized_403(collection, client, user):
	# Given
	obj = {"_id": "1", "name": "SuperAsso", "substances": None, "specialities": None}
	Association.collection = collection

	# When
	res = client.put(url_for('api.update_association', asso_id='1'), data=json.dumps(obj), content_type='application/json')

	assert res.status_code == 403


def test_update_asso_not_logged_in_401(collection, client):
	# Given
	obj = {"_id": "1", "name": "SuperAsso", "substances": None, "specialities": None}
	Association.collection = collection

	# When
	res = client.put(url_for('api.update_association', asso_id='1'), data=json.dumps(obj), content_type='application/json')

	assert res.status_code == 401


def test_delete_asso(collection, client, admin):
	# Given
	obj = {"_id": "02032", "name": "SuperAsso", "substances": None, "specialities": None}
	collection.insert(obj)
	Association.collection = collection

	# When
	res_del = client.delete(url_for('api.delete_association', asso_id='02032'))
	res_get = client.get(url_for('api.associations'))

	# Then
	assert res_del.status_code == 200
	assert res_get.status_code == 404


def test_delete_asso_unauthorized_403(collection, client, user):
	# Given
	obj = {"_id": "02032", "name": "SuperAsso", "substances": None, "specialities": None}
	collection.insert(obj)
	Association.collection = collection

	# When
	res_del = client.delete(url_for('api.delete_association', asso_id='02032'))

	# Then
	assert res_del.status_code == 403


def test_delete_asso_not_logged_in_401(collection, client):
	# Given
	obj = {"_id": "02032", "name": "SuperAsso", "substances": None, "specialities": None}
	collection.insert(obj)
	Association.collection = collection

	# When
	res_del = client.delete(url_for('api.delete_association', asso_id='02032'))

	# Then
	assert res_del.status_code == 401
