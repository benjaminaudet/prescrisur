from flask import url_for

from api.models import Speciality


def test_search_speciality(collection, client):
	# Given
	objs = [
		{"_id": "02039", "status": None, "name": "SPECIALITY", "dosage": "100mg"},
		{"_id": "02032", "status": None, "name": "SUPERSPECIALITY", "dosage": "100mg"},
		{"_id": "02301", "status": None, "name": "SUPER", "dosage": "100mg"}
	]
	map(lambda o: collection.insert(o), objs)
	Speciality.collection = collection

	# When
	res = client.get(url_for('api.search_speciality'), query_string={'q': 'spec'})
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == [
		{"_id": "02039", "status": None, "name": "SPECIALITY"},
		{"_id": "02032", "status": None, "name": "SUPERSPECIALITY"}
	]
