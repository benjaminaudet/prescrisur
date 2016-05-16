from flask import url_for

from api.models import Substance


def test_get_substance(collection, client, user):
	# Given
	obj = {"_id": "02039", "status": None, "name": "MAGNESIA", "specialities":  []}
	collection.insert(obj)
	Substance.collection = collection

	# When
	res = client.get(url_for('api.substance', subst_id='02039'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == obj


def test_get_substance_no_subst_404(collection, client, user):
	# Given
	Substance.collection = collection

	# When
	res = client.get(url_for('api.substance', subst_id='02039'))

	# Then
	assert res.status_code == 404


def test_get_substance_not_logged_in_401(collection, client):
	# Given
	obj = {"_id": "02039", "status": None, "name": "MAGNESIA", "specialities":  []}
	collection.insert(obj)
	Substance.collection = collection

	# When
	res = client.get(url_for('api.substance', subst_id='02039'))

	# Then
	assert res.status_code == 401


def test_search_substance(collection, client):
	# Given
	objs = [
		{"_id": "02039", "status": None, "name": "SUBSTANCE", "specialities": []},
		{"_id": "02032", "status": None, "name": "SUPERSUBSTANCE", "specialities": []},
		{"_id": "02301", "status": None, "name": "SUPER"}
	]
	map(lambda o: collection.insert(o), objs)
	Substance.collection = collection

	# When
	res = client.get(url_for('api.search_substance'), query_string={'q': 'subst'})
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == [
		{"_id": "02039", "status": None, "name": "SUBSTANCE"},
		{"_id": "02032", "status": None, "name": "SUPERSUBSTANCE"}
	]


def test_search_substance_with_spec(collection, client):
	# Given
	objs = [
		{"_id": "02039", "status": None, "name": "SUBSTANCE", "specialities": []},
		{"_id": "02032", "status": None, "name": "SUPERSUBSTANCE", "specialities": []},
		{"_id": "02301", "status": None, "name": "SUPER"}
	]
	map(lambda o: collection.insert(o), objs)
	Substance.collection = collection

	# When
	res = client.get(url_for('api.search_substance'), query_string={'q': 'subst', 'specialities': True})
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == [objs[0], objs[1]]