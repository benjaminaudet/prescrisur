import json
import pytest
from flask import url_for
from freezegun import freeze_time

from api.models import Pathology, PathologyDraft


@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_get_patho(mock_model, client, user):
	# Given
	obj = {"_id": "patho", "name": "Patho", "levels": [], "intro": "intro", "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(obj)

	# When
	res = client.get(url_for('api.pathology', patho_id='patho'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == obj
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_get_patho_not_logged_in_401(mock_model, client):
	# Given
	obj = {"_id": "patho", "name": "Patho", "levels": [], "intro": "intro", "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(obj)

	# When
	res = client.get(url_for('api.pathology', patho_id='patho'))

	# Then
	assert res.status_code == 401
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_get_patho_no_patho_404(mock_model, client, user):
	# When
	res = client.get(url_for('api.pathology', patho_id='patho'))

	# Then
	assert res.status_code == 404
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_get_patho_draft(mock_model, client, admin):
	# Given
	obj = {"_id": "patho", "name": "Patho", "levels": [], "intro": "intro", "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(obj)

	# When
	res = client.get(url_for('api.pathology_draft', patho_id='patho'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == obj
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_get_patho_draft_no_patho_404(mock_model, client, admin):
	# When
	res = client.get(url_for('api.pathology_draft', patho_id='patho'))

	# Then
	assert res.status_code == 404
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_patho_has_draft(mock_model, client, admin):
	# Given
	obj = {"_id": "patho", "name": "Patho", "levels": [], "intro": "intro", "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(obj)

	# When
	res_ok = client.get(url_for('api.pathology_has_draft', patho_id="patho"))
	res_nok = client.get(url_for('api.pathology_has_draft', patho_id="no-patho"))
	data_ok = res_ok.json
	data_nok = res_nok.json

	# Then
	assert res_ok.status_code == 200
	assert data_ok['exists']
	assert res_nok.status_code == 200
	assert not data_nok['exists']
	
	
def test_patho_has_draft_unauthorized_403(client, user):
	# When
	res = client.get(url_for('api.pathology_has_draft', patho_id="patho"))

	# Then
	assert res.status_code == 403
	
	
def test_patho_has_draft_not_logged_in_401(client):
	# When
	res = client.get(url_for('api.pathology_has_draft', patho_id="patho"))

	# Then
	assert res.status_code == 401
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_get_patho_draft_unauthorized_403(mock_model, client, user):
	# Given
	obj = {"_id": "patho", "name": "Patho", "levels": [], "intro": "intro", "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(obj)

	# When
	res = client.get(url_for('api.pathology_draft', patho_id='patho'))

	# Then
	assert res.status_code == 403
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_get_patho_draft_not_logged_in_401(mock_model, client):
	# Given
	obj = {"_id": "patho", "name": "Patho", "levels": [], "intro": "intro", "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(obj)

	# When
	res = client.get(url_for('api.pathology_draft', patho_id='patho'))

	# Then
	assert res.status_code == 401
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_get_all_patho(mock_model, client, user):
	# Given
	objs = [
		{"_id": "patho1", "name": "Patho1", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None},
		{"_id": "patho2", "name": "Patho2", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None},
		{"_id": "patho3", "name": "Patho3", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None}
	]
	map(lambda o: mock_model.collection.insert(o), objs)

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
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_get_all_patho_no_patho_404(mock_model, client, user):
	# When
	res = client.get(url_for('api.pathologies'))

	# Then
	assert res.status_code == 404
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_get_all_patho_draft(mock_model, client, admin):
	# Given
	objs = [
		{"_id": "patho1", "name": "Patho1", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None},
		{"_id": "patho2", "name": "Patho2", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None},
		{"_id": "patho3", "name": "Patho3", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None}
	]
	map(lambda o: mock_model.collection.insert(o), objs)

	# When
	res = client.get(url_for('api.pathologies_drafts'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == [
		{"_id": "patho1", "name": "Patho1", "updated_at": None},
		{"_id": "patho2", "name": "Patho2", "updated_at": None},
		{"_id": "patho3", "name": "Patho3", "updated_at": None}
	]
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_get_all_patho_draft_no_patho_404(mock_model, client, admin):
	# When
	res = client.get(url_for('api.pathologies_drafts'))

	# Then
	assert res.status_code == 404
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_search_patho(mock_model, client):
	# Given
	objs = [
		{"_id": "patho1", "name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": "2015-12-12 00:00:00"},
		{"_id": "patho2", "name": "SuperPatho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": "2015-12-12 00:00:00"},
		{"_id": "super", "name": "Super", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": "2015-12-12 00:00:00"}
	]
	map(lambda o: mock_model.collection.insert(o), objs)

	# When
	res = client.get(url_for('api.search_pathology'), query_string={'q': 'patho'})
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == [
		{"_id": "patho1", "name": "Patho", "updated_at": "2015-12-12 00:00:00"},
		{"_id": "patho2", "name": "SuperPatho", "updated_at": "2015-12-12 00:00:00"},
	]



@pytest.mark.parametrize('collection_name', ['Pathology'])
@freeze_time("2015-01-01")
def test_create_patho_draft(mock_model, client, admin):
	# Given
	obj = {"name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None}

	# When
	res = client.post(url_for('api.edit_pathology_draft'), data=json.dumps(obj), content_type='application/json')
	data = res.json

	assert res.status_code == 201
	assert data['data']['name'] == 'Patho'
	assert data['data']['_id'] == 'patho'
	assert data['data']['intro'] == 'intro'
	assert data['data']['conclu'] == 'conclu'
	assert data['data']['updated_at'] == '2015-01-01T00:00:00'



@pytest.mark.parametrize('collection_name', ['Pathology'])
@freeze_time("2015-01-01")
def test_update_patho_draft(mock_model, client, admin):
	# Given
	obj = {"_id": "patho-id", "name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": '2014-01-01T00:00:00'}

	# When
	res = client.put(url_for('api.update_pathology_draft', patho_id='patho-id'), data=json.dumps(obj), content_type='application/json')
	data = res.json

	assert res.status_code == 200
	assert data['data']['name'] == 'Patho'
	assert data['data']['_id'] == 'patho-id'
	assert data['data']['intro'] == 'intro'
	assert data['data']['conclu'] == 'conclu'
	assert data['data']['updated_at'] == '2015-01-01T00:00:00'
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_update_patho_draft_unauthorized_403(mock_model, client, user):
	# Given
	obj = {"_id": "patho-id", "name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": '2014-01-01T00:00:00'}

	# When
	res = client.put(url_for('api.update_pathology_draft', patho_id='patho-id'), data=json.dumps(obj), content_type='application/json')

	assert res.status_code == 403
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_update_patho_draft_not_logged_in_401(mock_model, client):
	# Given
	obj = {"_id": "patho-id", "name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": '2014-01-01T00:00:00'}

	# When
	res = client.put(url_for('api.update_pathology_draft', patho_id='patho-id'), data=json.dumps(obj), content_type='application/json')

	assert res.status_code == 401
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_delete_patho(mock_model, client, admin):
	# Given
	obj = {"_id": "patho", "name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(obj)

	# When
	res_del = client.delete(url_for('api.delete_pathology', patho_id='patho'))
	res_get = client.get(url_for('api.pathology', patho_id='patho'))

	# Then
	assert res_del.status_code == 200
	assert res_get.status_code == 404
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_delete_patho_unauthorized_403(mock_model, client, user):
	# Given
	obj = {"_id": "patho", "name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(obj)

	# When
	res_del = client.delete(url_for('api.delete_pathology', patho_id='patho'))
	res_get = client.get(url_for('api.pathology', patho_id='patho'))

	# Then
	assert res_del.status_code == 403
	assert res_get.status_code == 200
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_delete_patho_not_logged_in_401(mock_model, client):
	# Given
	obj = {"_id": "patho", "name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(obj)

	# When
	res_del = client.delete(url_for('api.delete_pathology', patho_id='patho'))

	# Then
	assert res_del.status_code == 401
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_delete_patho_draft(mock_model, client, admin):
	# Given
	obj = {"_id": "patho", "name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(obj)

	# When
	res_del = client.delete(url_for('api.delete_pathology_draft', patho_id='patho'))
	res_get = client.get(url_for('api.pathology_draft', patho_id='patho'))

	# Then
	assert res_del.status_code == 200
	assert res_get.status_code == 404
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_delete_patho_draft_unauthorized_403(mock_model, client, user):
	# Given
	obj = {"_id": "patho", "name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(obj)

	# When
	res_del = client.delete(url_for('api.delete_pathology_draft', patho_id='patho'))

	# Then
	assert res_del.status_code == 403
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_delete_patho_draft_not_logged_in_401(mock_model, client):
	# Given
	obj = {"_id": "patho", "name": "Patho", "levels": None, "intro": "intro", "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(obj)

	# When
	res_del = client.delete(url_for('api.delete_pathology_draft', patho_id='patho'))

	# Then
	assert res_del.status_code == 401
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_search_pathologies_from_substance(mock_model, client, user):
	subst = {"_id": "subst", "status": None, "name": "MAGNESIA", "specialities": []}
	mock_model.collection.insert(subst)
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
	mock_model.collection.insert(patho)

	# When
	res = client.get(url_for('api.search_pathologies_from_substance', subst_id='subst'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert len(data['data']) == 1
	assert data['data'][0]['_id'] == 'patho'
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
def test_search_pathologies_from_substance_not_logged_in_401(mock_model, client):
	patho = {"_id": "patho", "name": "Patho", "intro": "intro", "levels": None, "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(patho)

	# When
	res = client.get(url_for('api.search_pathologies_from_substance', subst_id='subst'))

	# Then
	assert res.status_code == 401


@pytest.mark.parametrize('collection_name', ['PathologyDraft'])
@pytest.mark.parametrize('collection_name_bis', ['Pathology'])
@freeze_time("2015-01-01")
def test_validate_pathology(mock_model, mock_model_bis, client, admin):
	# Given
	patho = {"_id": "patho", "name": "Patho", "intro": "intro", "levels": [], "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(patho)

	# When
	res_no_patho = client.get(url_for('api.pathology', patho_id='patho'))
	res_validate_patho = client.put(url_for('api.validate_pathology', patho_id='patho'))
	res_ok_patho = client.get(url_for('api.pathology', patho_id='patho'))
	res_no_draft = client.get(url_for('api.pathology_draft', patho_id='patho'))
	data_validate_patho = res_validate_patho.json
	data_ok_patho = res_ok_patho.json

	# Then
	assert res_no_patho.status_code == 404
	assert res_validate_patho.status_code == 200
	assert res_ok_patho.status_code == 200
	assert res_no_patho.status_code == 404
	assert data_validate_patho['data']['name'] == patho['name']
	assert data_validate_patho['data']['updated_at'] == '2015-01-01T00:00:00'


@pytest.mark.parametrize('collection_name', ['PathologyDraft'])
@pytest.mark.parametrize('collection_name_bis', ['Pathology'])
def test_validate_pathology_unauthorized_403(mock_model, mock_model_bis, client, user):
	# Given
	patho = {"_id": "patho", "name": "Patho", "intro": "intro", "levels": [], "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(patho)

	# When
	res_validate_patho = client.put(url_for('api.validate_pathology', patho_id='patho'))

	# Then
	assert res_validate_patho.status_code == 403


@pytest.mark.parametrize('collection_name', ['PathologyDraft'])
@pytest.mark.parametrize('collection_name_bis', ['Pathology'])
def test_validate_pathology_not_logged_in_401(mock_model, mock_model_bis, client):
	# Given
	patho = {"_id": "patho", "name": "Patho", "intro": "intro", "levels": [], "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(patho)

	# When
	res_validate_patho = client.put(url_for('api.validate_pathology', patho_id='patho'))

	# Then
	assert res_validate_patho.status_code == 401
	
	
@pytest.mark.parametrize('collection_name', ['Pathology'])
@pytest.mark.parametrize('collection_name_bis', ['PathologyDraft'])
def test_unvalidate_pathology(mock_model, mock_model_bis, client, admin):
	# Given
	patho = {"_id": "patho", "name": "Patho", "intro": "intro", "levels": [], "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(patho)

	# When
	res_no_draft = client.get(url_for('api.pathology_draft', patho_id='patho'))
	res_unvalidate_patho = client.put(url_for('api.unvalidate_pathology', patho_id='patho'))
	res_ok_draft = client.get(url_for('api.pathology_draft', patho_id='patho'))
	res_no_patho = client.get(url_for('api.pathology', patho_id='patho'))
	data_unvalidate_patho = res_unvalidate_patho.json
	data_ok_draft = res_ok_draft.json

	# Then
	assert res_no_draft.status_code == 404
	assert res_unvalidate_patho.status_code == 200
	assert res_ok_draft.status_code == 200
	assert res_no_patho.status_code == 404
	assert data_unvalidate_patho['data'] == data_ok_draft['data'] == patho


@pytest.mark.parametrize('collection_name', ['Pathology'])
@pytest.mark.parametrize('collection_name_bis', ['PathologyDraft'])
def test_unvalidate_pathology_unauthorized_404(mock_model, mock_model_bis, client, user):
	# Given
	patho = {"_id": "patho", "name": "Patho", "intro": "intro", "levels": [], "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(patho)

	# When
	res_unvalidate_patho = client.put(url_for('api.unvalidate_pathology', patho_id='patho'))

	# Then
	assert res_unvalidate_patho.status_code == 403


@pytest.mark.parametrize('collection_name', ['Pathology'])
@pytest.mark.parametrize('collection_name_bis', ['PathologyDraft'])
def test_unvalidate_pathology_not_logged_in_401(mock_model, mock_model_bis, client):
	# Given
	patho = {"_id": "patho", "name": "Patho", "intro": "intro", "levels": [], "conclu": "conclu", "updated_at": None}
	mock_model.collection.insert(patho)

	# When
	res_unvalidate_patho = client.put(url_for('api.unvalidate_pathology', patho_id='patho'))

	# Then
	assert res_unvalidate_patho.status_code == 401
