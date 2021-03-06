import json
import pytest
import dateutil.parser
from flask import url_for
from freezegun import freeze_time

from api.models import News


@pytest.mark.parametrize('collection_name', ['News'])
def test_get_news(mock_model, client):
	# Given
	obj = {"_id": "02039", "name": "News", "text": "coucou", "author": None, "created_at": "blabla", "updated_at": None}
	mock_model.collection.insert(obj)

	# When
	res = client.get(url_for('api.news', news_id='02039'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == obj


@pytest.mark.parametrize('collection_name', ['News'])
def test_get_news_no_news_404(mock_model, client, user):
	# When
	res = client.get(url_for('api.news', news_id='02039'))

	# Then
	assert res.status_code == 404


@pytest.mark.parametrize('collection_name', ['News'])
def test_get_all_news(mock_model, client):
	# Given
	objs = [
		{"_id": "02039", "name": "News1", "text": "coucou1"},
		{"_id": "02040", "name": "News2", "text": "coucou2"}
	]
	map(lambda o: mock_model.collection.insert(o), objs)

	# When
	res = client.get(url_for('api.news'))
	data = res.json

	# Then
	assert data['data'] == objs



@pytest.mark.parametrize('collection_name', ['News'])
@freeze_time("2015-01-01")
def test_create_news(mock_model, client, admin):
	# Given
	obj = {"name": "Super News", "text": "<b>coucou</b>"}

	# When
	res = client.post(url_for('api.edit_news'), data=json.dumps(obj), content_type='application/json')
	data = res.json

	assert res.status_code == 201
	assert data['data']['name'] == 'Super News'
	assert data['data']['_id'] == 'super-news'
	assert data['data']['text'] == '<b>coucou</b>'
	assert data['data']['author']['name'] == 'Test'
	assert data['data']['created_at'] == '2015-01-01T00:00:00'
	assert data['data']['created_at'] == data['data']['updated_at']


@pytest.mark.parametrize('collection_name', ['News'])
def test_update_news(mock_model, client, admin):
	# Given
	news = News(name='News', text='coucou')
	news.create()

	update_obj = {"_id": "news", "name": "Super News", "text": "<b>coucou</b> <script>lol()</script>"}

	# When
	res = client.put(url_for('api.update_news', news_id='news'), data=json.dumps(update_obj), content_type='application/json')
	data = res.json

	assert res.status_code == 200
	assert data['data']['name'] == 'Super News'
	assert data['data']['_id'] == 'news'
	assert data['data']['text'] == '<b>coucou</b> &lt;script&gt;lol()&lt;/script&gt;'
	assert dateutil.parser.parse(data['data']['created_at']) < dateutil.parser.parse(data['data']['updated_at'])


@pytest.mark.parametrize('collection_name', ['News'])
def test_update_news_not_allowed(mock_model, client, user):
	# Given
	update_obj = {"_id": "news", "name": "Super News", "text": "<b>coucou</b> <script>lol()</script>"}

	# When
	res = client.put(url_for('api.update_news', news_id='news'), data=json.dumps(update_obj), content_type='application/json')

	assert res.status_code == 403


@pytest.mark.parametrize('collection_name', ['News'])
def test_update_news_not_logged_in(mock_model, client):
	# Given
	update_obj = {"_id": "news", "name": "Super News", "text": "<b>coucou</b> <script>lol()</script>"}

	# When
	res = client.put(url_for('api.update_news', news_id='news'), data=json.dumps(update_obj), content_type='application/json')

	assert res.status_code == 401


@pytest.mark.parametrize('collection_name', ['News'])
def test_delete_news(mock_model, client, admin):
	# Given
	obj = {"_id": "02039", "name": "News", "text": "coucou", "author": None, "created_at": "blabla", "updated_at": None}
	mock_model.collection.insert(obj)

	# When
	res_del = client.delete(url_for('api.delete_news', news_id='02039'))
	res_get = client.get(url_for('api.news', news_id='02039'))

	# Then
	assert res_del.status_code == 200
	assert res_get.status_code == 404


@pytest.mark.parametrize('collection_name', ['News'])
def test_delete_news_unauthorized_403(mock_model, client, user):
	# Given
	obj = {"_id": "02039", "name": "News", "text": "coucou", "author": None, "created_at": "blabla", "updated_at": None}
	mock_model.collection.insert(obj)

	# When
	res_del = client.delete(url_for('api.delete_news', news_id='02039'))
	res_get = client.get(url_for('api.news', news_id='02039'))

	# Then
	assert res_del.status_code == 403
	assert res_get.status_code == 200


@pytest.mark.parametrize('collection_name', ['News'])
def test_delete_news_not_logged_in_401(mock_model, client):
	# Given
	obj = {"_id": "02039", "name": "News", "text": "coucou", "author": None, "created_at": "blabla", "updated_at": None}
	mock_model.collection.insert(obj)

	# When
	res_del = client.delete(url_for('api.delete_news', news_id='02039'))

	# Then
	assert res_del.status_code == 401


