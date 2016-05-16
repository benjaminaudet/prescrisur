from flask import url_for

from api.models import TherapeuticClass


def test_get_class(collection, client, user):
	# Given
	obj = {"_id": "02039", "name": "Classe", "pathology": "Patho", "text": None, "levels": None, "entries": None}
	collection.insert(obj)
	TherapeuticClass.collection = collection

	# When
	res = client.get(url_for('api.therapeutic_class', class_id='02039'))
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == obj


def test_get_class_no_class_404(collection, client, user):
	# Given
	TherapeuticClass.collection = collection

	# When
	res = client.get(url_for('api.therapeutic_class', class_id='02039'))

	# Then
	assert res.status_code == 404


def test_get_class_not_logged_in_401(collection, client):
	# Given
	obj = {"_id": "02039", "name": "Classe", "pathology": "Patho", "text": None, "levels": None, "entries": None}
	collection.insert(obj)
	TherapeuticClass.collection = collection

	# When
	res = client.get(url_for('api.therapeutic_class', class_id='02039'))

	# Then
	assert res.status_code == 401


def test_search_class(collection, client):
	# Given
	objs = [
		{"_id": "02039", "name": "Class", "pathology": "Patho", "text": None, "levels": None, "entries": None},
		{"_id": "02032", "name": "Superclass", "pathology": "Patho", "text": None, "levels": None, "entries": None},
		{"_id": "02301", "name": "Super", "pathology": "Patho", "text": None, "levels": None, "entries": None}
	]
	map(lambda o: collection.insert(o), objs)
	TherapeuticClass.collection = collection

	# When
	res = client.get(url_for('api.search_therapeutic_class'), query_string={'q': 'class'})
	data = res.json

	# Then
	assert res.status_code == 200
	assert data['data'] == [
		{"_id": "02039", "name": "Class"},
		{"_id": "02032", "name": "Superclass"}
	]
