import json
import pytest
from flask import url_for

from api.models import Association, Substance


@pytest.mark.parametrize('collection_name', ['Association'])
def test_get_all_asso(mock_model, client, admin):
	# Given
	objs = [
		{"_id": "02032", "name": "SuperAsso", "substances": None, "specialities": None},
		{"_id": "02039", "name": "Asso", "substances": None, "specialities": None},
		{"_id": "02301", "name": "Super", "substances": None, "specialities": None}
	]
	map(lambda o: mock_model.collection.insert(o), objs)

	# When
	res = client.get(url_for('api.associations'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == objs


@pytest.mark.parametrize('collection_name', ['Association'])
def test_get_all_asso_no_asso_404(mock_model, client, admin):
	# When
	res = client.get(url_for('api.associations'))

	# Then
	assert res.status_code == 404


@pytest.mark.parametrize('collection_name', ['Association'])
def test_get_all_asso_not_authorized_403(mock_model, client, user):
	# Given
	objs = [
		{"_id": "02032", "name": "SuperAsso", "substances": None, "specialities": None},
		{"_id": "02039", "name": "Asso", "substances": None, "specialities": None},
		{"_id": "02301", "name": "Super", "substances": None, "specialities": None}
	]
	map(lambda o: mock_model.collection.insert(o), objs)

	# When
	res = client.get(url_for('api.associations'))

	# Then
	assert res.status_code == 403


@pytest.mark.parametrize('collection_name', ['Association'])
def test_get_all_asso_not_logged_in_401(mock_model, client):
	# Given
	objs = [
		{"_id": "02032", "name": "SuperAsso", "substances": None, "specialities": None},
		{"_id": "02039", "name": "Asso", "substances": None, "specialities": None},
		{"_id": "02301", "name": "Super", "substances": None, "specialities": None}
	]
	map(lambda o: mock_model.collection.insert(o), objs)

	# When
	res = client.get(url_for('api.associations'))

	# Then
	assert res.status_code == 401


@pytest.mark.parametrize('collection_name', ['Association'])
def test_search_asso(mock_model, client):
	# Given
	objs = [
		{"_id": "02032", "name": "SuperAsso", "substances": None, "specialities": None},
		{"_id": "02039", "name": "Asso", "substances": None, "specialities": None},
		{"_id": "02301", "name": "Super", "substances": None, "specialities": None}
	]
	map(lambda o: mock_model.collection.insert(o), objs)

	# When
	res = client.get(url_for('api.search_association'), query_string={'q': 'asso'})
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == [
		{"_id": "02039", "name": "Asso", "specialities": None}
	]


@pytest.mark.parametrize('collection_name', ['Association'])
@pytest.mark.parametrize('collection_name_bis', ['Substance'])
def test_create_asso(mock_model, mock_model_bis, client, admin):
	# Given
	obj = {"name": "SuperAsso", "substances": [{"_id": "1", "name": "Substance", "status": "G"}], "specialities": None}
	subst = {"_id": "1", "name": "Substance", "status": "G", "specialities": [{"_id": "1", "name": "Speciality"}]}
	mock_model_bis.collection.insert(subst)

	# When
	res = client.post(url_for('api.edit_association'), data=json.dumps(obj), content_type='application/json')
	data = res.json

	assert res.status_code == 201
	assert data['data']['name'] == 'SuperAsso'
	assert data['data']['_id'] == 'superasso'
	assert data['data']['status'] == 'G'
	assert data['data']['substances'] == [{"_id": "1", "name": "Substance", "specialities": [], "status": 'G', 'created_at': None, 'updated_at': None, 'deleted_at': None}]
	assert data['data']['specialities'] == [{'status': None, 'name': 'Speciality', 'short_name': None, 'enabled': True, 'treatment_type': None, 'spec_type': None, '_id': '1', 'dosage': None, 'created_at': None, 'updated_at': None, 'deleted_at': None}]


@pytest.mark.parametrize('collection_name', ['Association'])
def test_update_asso(mock_model, client, admin):
	# Given
	obj = {"_id": "1", "name": "SuperAsso", "substances": None, "specialities": None}

	# When
	res = client.put(url_for('api.update_association', asso_id='1'), data=json.dumps(obj), content_type='application/json')
	data = res.json

	assert res.status_code == 200
	assert data['data']['name'] == 'SuperAsso'
	assert data['data']['_id'] == '1'


@pytest.mark.parametrize('collection_name', ['Association'])
def test_update_asso_not_authorized_403(mock_model, client, user):
	# Given
	obj = {"_id": "1", "name": "SuperAsso", "substances": None, "specialities": None}

	# When
	res = client.put(url_for('api.update_association', asso_id='1'), data=json.dumps(obj), content_type='application/json')

	assert res.status_code == 403


@pytest.mark.parametrize('collection_name', ['Association'])
def test_update_asso_not_logged_in_401(mock_model, client):
	# Given
	obj = {"_id": "1", "name": "SuperAsso", "substances": None, "specialities": None}

	# When
	res = client.put(url_for('api.update_association', asso_id='1'), data=json.dumps(obj), content_type='application/json')

	assert res.status_code == 401


@pytest.mark.parametrize('collection_name', ['Association'])
def test_delete_asso(mock_model, client, admin):
	# Given
	obj = {"_id": "02032", "name": "SuperAsso", "substances": None, "specialities": None}
	mock_model.collection.insert(obj)

	# When
	res_del = client.delete(url_for('api.delete_association', asso_id='02032'))
	res_get = client.get(url_for('api.associations'))

	# Then
	assert res_del.status_code == 200
	assert res_get.status_code == 404


@pytest.mark.parametrize('collection_name', ['Association'])
def test_delete_asso_unauthorized_403(mock_model, client, user):
	# Given
	obj = {"_id": "02032", "name": "SuperAsso", "substances": None, "specialities": None}
	mock_model.collection.insert(obj)

	# When
	res_del = client.delete(url_for('api.delete_association', asso_id='02032'))

	# Then
	assert res_del.status_code == 403


@pytest.mark.parametrize('collection_name', ['Association'])
def test_delete_asso_not_logged_in_401(mock_model, client):
	# Given
	obj = {"_id": "02032", "name": "SuperAsso", "substances": None, "specialities": None}
	mock_model.collection.insert(obj)

	# When
	res_del = client.delete(url_for('api.delete_association', asso_id='02032'))

	# Then
	assert res_del.status_code == 401
