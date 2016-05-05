# coding=utf-8
import pytest

from api.models import Pathology, User


@pytest.fixture(autouse=True)
def pathology():
	return Pathology(
		name='Pathologie testée',
		intro='<script>fumed()</script>',
		conclu='<a href="http://www.google.com" target=_blank>juste un lien</a>',
		levels=[
			{
				'text': 'Bonjour (Grade A)',
				'name': 'coucou',
				'levels': []
			},
			{
				'name': 'super',
				'levels': [
					{
						'name': 'subsuper',
						'entries': []
					},
					{
						'name': 'subsuper',
						'entries': [{
							'product': {'_id': 'ok', 'name': 'lol'},
							'type': 'specialities',
							'reco': {'_id': 'ok'}
						}]
					},
				]
			}
		])


@pytest.fixture(autouse=True)
def cleaned_pathology(pathology):
	return pathology.check()


@pytest.fixture(autouse=True)
def user():
	return User(_id="pbo", password="password", name="PBO")
