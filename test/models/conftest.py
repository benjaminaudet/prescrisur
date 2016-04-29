# coding=utf-8
import pytest

from api.models import Pathology


@pytest.fixture(autouse=True)
def pathology():
	return Pathology(
		name='Pathologie testée',
		intro='<script>fumed()</script>',
		conclu='<a href="http://www.google.com" target=_blank>juste un lien</a>',
		levels=[
			{
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
							'type': 'substances',
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
def wrong_type_pathology():
	return Pathology(
		name='Pathologie testée',
		intro='<script>fumed()</script>',
		conclu='<a href="http://www.google.com" target=_blank>juste un lien</a>',
		levels=[
			{
				'name': 'coucou',
				'entries': [{
					'type': 'lol'
				}]
			}
		])


@pytest.fixture(autouse=True)
def no_product_pathology():
	return Pathology(
		name='Pathologie testée',
		intro='<script>fumed()</script>',
		conclu='<a href="http://www.google.com" target=_blank>juste un lien</a>',
		levels=[
			{
				'name': 'coucou',
				'entries': [{
					'type': 'substances'
				}]
			}
		])


@pytest.fixture(autouse=True)
def uncompliant_product_pathology():
	return Pathology(
		name='Pathologie testée',
		intro='<script>fumed()</script>',
		conclu='<a href="http://www.google.com" target=_blank>juste un lien</a>',
		levels=[
			{
				'name': 'coucou',
				'entries': [{
					'type': 'substances',
					'product': {
						'_id': 'ok'
					}
				}]
			}
		])