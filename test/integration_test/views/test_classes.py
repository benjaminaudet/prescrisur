import pytest
from flask import url_for

from api.models import TherapeuticClass


@pytest.mark.parametrize('collection_name', ['TherapeuticClass'])
def test_get_class(mock_model, client, user):
	# Given
	obj = {"_id": "02039", "name": "Classe", "pathology": "Patho", "text": None, "levels": None, "entries": None}
	mock_model.collection.insert(obj)

	# When
	res = client.get(url_for('api.therapeutic_class', class_id='02039'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == obj


@pytest.mark.parametrize('collection_name', ['TherapeuticClass'])
def test_get_class_no_class_404(mock_model, client, user):
	# When
	res = client.get(url_for('api.therapeutic_class', class_id='02039'))

	# Then
	assert res.status_code == 404


@pytest.mark.parametrize('collection_name', ['TherapeuticClass'])
def test_get_class_not_logged_in_401(mock_model, client):
	# Given
	obj = {"_id": "02039", "name": "Classe", "pathology": "Patho", "text": None, "levels": None, "entries": None}
	mock_model.collection.insert(obj)

	# When
	res = client.get(url_for('api.therapeutic_class', class_id='02039'))

	# Then
	assert res.status_code == 401


@pytest.mark.parametrize('collection_name', ['TherapeuticClass'])
def test_search_class(mock_model, client):
	# Given
	objs = [
		{"_id": "02039", "name": "Class", "pathology": "Patho", "text": None, "levels": None, "entries": None},
		{"_id": "02032", "name": "Superclass", "pathology": "Patho", "text": None, "levels": None, "entries": None},
		{"_id": "02301", "name": "Super", "pathology": "Patho", "text": None, "levels": None, "entries": None}
	]
	map(lambda o: mock_model.collection.insert(o), objs)

	# When
	res = client.get(url_for('api.search_therapeutic_class'), query_string={'q': 'class'})
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == [
		{"_id": "02039", "name": "Class", "pathology": "Patho"}
	]


@pytest.mark.parametrize('collection_name', ['TherapeuticClass'])
def test_delete_class(mock_model, client, admin):
	# Given
	obj = {"_id": "02039", "name": "Classe", "pathology": "Patho", "text": None, "levels": None, "entries": None}
	mock_model.collection.insert(obj)

	# When
	res_del = client.delete(url_for('api.delete_therapeutic_class', class_id='02039'))
	res_get = client.get(url_for('api.therapeutic_class', class_id='02039'))

	# Then
	assert res_del.status_code == 200
	assert res_get.status_code == 404


@pytest.mark.parametrize('collection_name', ['TherapeuticClass'])
def test_delete_class_unauthorized_403(mock_model, client, user):
	# Given
	obj = {"_id": "02039", "name": "Classe", "pathology": "Patho", "text": None, "levels": None, "entries": None}
	mock_model.collection.insert(obj)

	# When
	res_del = client.delete(url_for('api.delete_therapeutic_class', class_id='02039'))
	res_get = client.get(url_for('api.therapeutic_class', class_id='02039'))

	# Then
	assert res_del.status_code == 403
	assert res_get.status_code == 200


@pytest.mark.parametrize('collection_name', ['TherapeuticClass'])
def test_delete_class_not_logged_in_401(mock_model, client):
	# Given
	obj = {"_id": "02039", "name": "Classe", "pathology": "Patho", "text": None, "levels": None, "entries": None}
	mock_model.collection.insert(obj)

	# When
	res_del = client.delete(url_for('api.delete_therapeutic_class', class_id='02039'))

	# Then
	assert res_del.status_code == 401
