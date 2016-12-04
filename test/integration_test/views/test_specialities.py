import pytest
from flask import url_for

from api.models import Speciality


@pytest.mark.parametrize('collection_name', ['Speciality'])
def test_search_speciality(mock_model, client):
	# Given
	objs = [
		{"_id": "02039", "status": None, "name": "SPECIALITY", "dosage": "100mg"},
		{"_id": "02032", "status": None, "name": "SUPERSPECIALITY", "dosage": "100mg"},
		{"_id": "02301", "status": None, "name": "SUPER", "dosage": "100mg"}
	]
	map(lambda o: mock_model.collection.insert(o), objs)

	# When
	res = client.get(url_for('api.search_speciality'), query_string={'q': 'spec'})
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == [
		{"_id": "02039", "status": None, "name": "SPECIALITY"},
		{"_id": "02032", "status": None, "name": "SUPERSPECIALITY"}
	]
