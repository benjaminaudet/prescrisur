import pytest
from flask import url_for

from api.models import Substance


@pytest.mark.parametrize('collection_name', ['Substance'])
def test_get_substance(mock_model, client, user):
	# Given
	obj = {"_id": "02039", "status": None, "name": "MAGNESIA", "specialities":  [], 'created_at': None, 'updated_at': None, 'deleted_at': None}
	mock_model.collection.insert(obj)

	# When
	res = client.get(url_for('api.substance', subst_id='02039'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == obj


@pytest.mark.parametrize('collection_name', ['Substance'])
def test_get_substance_no_subst_404(mock_model, client, user):
	# When
	res = client.get(url_for('api.substance', subst_id='02039'))

	# Then
	assert res.status_code == 404


@pytest.mark.parametrize('collection_name', ['Substance'])
def test_get_substance_not_logged_in_401(mock_model, client):
	# Given
	obj = {"_id": "02039", "status": None, "name": "MAGNESIA", "specialities":  []}
	mock_model.collection.insert(obj)

	# When
	res = client.get(url_for('api.substance', subst_id='02039'))

	# Then
	assert res.status_code == 401


@pytest.mark.parametrize('collection_name', ['Substance'])
def test_search_substance(mock_model, client):
	# Given
	objs = [
		{"_id": "02039", "status": None, "name": "SUBSTANCE", "specialities": []},
		{"_id": "02032", "status": None, "name": "SUPERSUBSTANCE", "specialities": []},
		{"_id": "02301", "status": None, "name": "SUPER"}
	]
	map(lambda o: mock_model.collection.insert(o), objs)

	# When
	res = client.get(url_for('api.search_substance'), query_string={'q': 'subst'})
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == [
		{"_id": "02039", "status": None, "name": "SUBSTANCE"},
		{"_id": "02032", "status": None, "name": "SUPERSUBSTANCE"}
	]


@pytest.mark.parametrize('collection_name', ['Substance'])
def test_search_substance_with_spec(mock_model, client):
	# Given
	objs = [
		{"_id": "02039", "status": None, "name": "SUBSTANCE", "specialities": []},
		{"_id": "02032", "status": None, "name": "SUPERSUBSTANCE", "specialities": []},
		{"_id": "02301", "status": None, "name": "SUPER"}
	]
	map(lambda o: mock_model.collection.insert(o), objs)

	# When
	res = client.get(url_for('api.search_substance'), query_string={'q': 'subst', 'specialities': True})
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == [objs[0], objs[1]]