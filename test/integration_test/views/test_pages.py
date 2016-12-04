import json
import pytest
from flask import url_for

from api.models import Page


@pytest.mark.parametrize('collection_name', ['Page'])
def test_get_page(mock_model, client):
	# Given
	obj = {"_id": "02039", "name": "Page", "text": "coucou"}
	mock_model.collection.insert(obj)

	# When
	res = client.get(url_for('api.page', page_id='02039'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == obj


@pytest.mark.parametrize('collection_name', ['Page'])
def test_get_page_no_page_404(mock_model, client, user):
	# When
	res = client.get(url_for('api.page', page_id='02039'))

	# Then
	assert res.status_code == 404


@pytest.mark.parametrize('collection_name', ['Page'])
def test_get_all_pages(mock_model, client):
	# Given
	objs = [
		{"_id": "02039", "name": "Page1", "text": "coucou1"},
		{"_id": "02040", "name": "Page2", "text": "coucou2"}
	]
	map(lambda o: mock_model.collection.insert(o), objs)

	# When
	res = client.get(url_for('api.page'))
	data = res.json

	# Then
	assert data['data'] == objs


@pytest.mark.parametrize('collection_name', ['Page'])
def test_create_page(mock_model, client, admin):
	# Given
	obj = {"name": "Page", "text": "<b>coucou</b>"}

	# When
	res = client.post(url_for('api.edit_page'), data=json.dumps(obj), content_type='application/json')
	data = res.json

	assert res.status_code == 201
	assert data['data']['name'] == 'Page'
	assert data['data']['_id'] == 'page'
	assert data['data']['text'] == '<b>coucou</b>'


@pytest.mark.parametrize('collection_name', ['Page'])
def test_update_page(mock_model, client, admin):
	# Given
	page = Page(name='Page', text='coucou')
	page.create()

	update_obj = {"_id": "page", "name": "Super Page", "text": "<b>coucou</b> <script>lol()</script>"}

	# When
	res = client.put(url_for('api.update_page', page_id='page'), data=json.dumps(update_obj), content_type='application/json')
	data = res.json

	assert res.status_code == 200
	assert data['data']['name'] == 'Super Page'
	assert data['data']['_id'] == 'page'
	assert data['data']['text'] == '<b>coucou</b> &lt;script&gt;lol()&lt;/script&gt;'


@pytest.mark.parametrize('collection_name', ['Page'])
def test_update_page_not_allowed(mock_model, client, user):
	# Given
	update_obj = {"_id": "page", "name": "Super Page", "text": "<b>coucou</b> <script>lol()</script>"}

	# When
	res = client.put(url_for('api.update_page', page_id='page'), data=json.dumps(update_obj), content_type='application/json')

	assert res.status_code == 403


@pytest.mark.parametrize('collection_name', ['Page'])
def test_update_page_not_logged_in(mock_model, client):
	# Given
	update_obj = {"_id": "page", "name": "Super Page", "text": "<b>coucou</b> <script>lol()</script>"}

	# When
	res = client.put(url_for('api.update_page', page_id='page'), data=json.dumps(update_obj), content_type='application/json')

	assert res.status_code == 401
