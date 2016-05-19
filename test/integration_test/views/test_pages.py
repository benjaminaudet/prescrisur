import json
from flask import url_for

from api.models import Page


def test_get_page(collection, client):
	# Given
	obj = {"_id": "02039", "name": "Page", "text": "coucou"}
	collection.insert(obj)
	Page.collection = collection

	# When
	res = client.get(url_for('api.page', page_id='02039'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == obj


def test_get_page_no_page_404(collection, client, user):
	# Given
	Page.collection = collection

	# When
	res = client.get(url_for('api.page', page_id='02039'))

	# Then
	assert res.status_code == 404


def test_get_all_pages(collection, client):
	# Given
	objs = [
		{"_id": "02039", "name": "Page1", "text": "coucou1"},
		{"_id": "02040", "name": "Page2", "text": "coucou2"}
	]
	map(lambda o: collection.insert(o), objs)
	Page.collection = collection

	# When
	res = client.get(url_for('api.page'))
	data = res.json

	# Then
	assert data['data'] == objs


def test_create_page(collection, client, admin):
	# Given
	obj = {"name": "Page", "text": "<b>coucou</b>"}
	Page.collection = collection

	# When
	res = client.post(url_for('api.edit_page'), data=json.dumps(obj), content_type='application/json')
	data = res.json

	assert res.status_code == 201
	assert data['data']['name'] == 'Page'
	assert data['data']['_id'] == 'page'
	assert data['data']['text'] == '<b>coucou</b>'


def test_update_page(collection, client, admin):
	# Given
	Page.collection = collection
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


def test_update_page_not_allowed(collection, client, user):
	# Given
	update_obj = {"_id": "page", "name": "Super Page", "text": "<b>coucou</b> <script>lol()</script>"}

	# When
	res = client.put(url_for('api.update_page', page_id='page'), data=json.dumps(update_obj), content_type='application/json')

	assert res.status_code == 403


def test_update_page_not_logged_in(collection, client):
	# Given
	update_obj = {"_id": "page", "name": "Super Page", "text": "<b>coucou</b> <script>lol()</script>"}

	# When
	res = client.put(url_for('api.update_page', page_id='page'), data=json.dumps(update_obj), content_type='application/json')

	assert res.status_code == 401
