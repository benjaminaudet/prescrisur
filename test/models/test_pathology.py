# coding=utf-8
import pytest
from freezegun import freeze_time

from api.models import Pathology, Substance, Speciality


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


def test_slugified_id(pathology):
	assert pathology._id == 'pathologie-testee'


@freeze_time("2015-01-01")
def test_refresh_update_date(pathology):
	patho_updated = pathology.refresh_update_date()
	assert isinstance(patho_updated, Pathology)
	assert patho_updated.updated_at == '2015-01-01T00:00:00'


def test_check_level(cleaned_pathology):
	assert 'levels' not in cleaned_pathology.levels[0]
	assert 'entries' not in cleaned_pathology.levels[1]['levels'][0]


def test_linkify_grade(pathology):
	assert pathology._linkify_grade('Bonjour (<a href="http://localhost:5000/#/pages/presentation">Grade A</a>)') == 'Bonjour (<a href="http://localhost:5000/#/pages/presentation">Grade A</a>)'
	assert pathology._linkify_grade('Bonjour (Grade B)') == 'Bonjour (<a class="grade" href="http://localhost:5000/#/pages/presentation">Grade B</a>)'
	assert pathology._linkify_grade('Bonjour <b>Grade C</b>') == 'Bonjour <b><a class="grade" href="http://localhost:5000/#/pages/presentation">Grade C</a></b>'


def test_serialize(cleaned_pathology):
	serialized_cleaned_pathology = cleaned_pathology.serialize()
	assert serialized_cleaned_pathology['_id'] == 'pathologie-testee'
	assert serialized_cleaned_pathology['levels'][1]['levels'][1]['entries'][0]['product']['name'] == 'lol'


class TestBleachedText:
	def test_text_clean(self, cleaned_pathology):
		assert cleaned_pathology.conclu == '<a href="http://www.google.com" target="_blank">juste un lien</a>'

	def test_text_unclean(self, cleaned_pathology):
		assert cleaned_pathology.intro == '&lt;script&gt;fumed()&lt;/script&gt;'

	def test_linkify_grade(self, cleaned_pathology):
		assert cleaned_pathology.levels[0]['text'] == 'Bonjour (<a class="grade" href="http://localhost:5000/#/pages/presentation">Grade A</a>)'


class TestCheckEntry:
	def test_raise_error_on_wrong_type(self, pathology):
		with pytest.raises(AssertionError):
			pathology._check_entry({'type': 'lol'})

	def test_raise_error_on_no_product(self, pathology):
		with pytest.raises(AssertionError):
			pathology._check_entry({'type': 'specialities'})

	def test_raise_error_on_uncompliant_product(self, pathology):
		with pytest.raises(AssertionError):
			pathology._check_entry({'type': 'specialities', 'product': {'_id': 'lol'}})

	def test_raise_error_on_substances_without_specialities(self, pathology):
		with pytest.raises(AssertionError):
			pathology._check_entry({'type': 'substances', 'product': {'_id': 'lol', 'name': 'ok'}})

	def test_substance_product(self, pathology):
		product = {'_id': 'lol', 'name': 'ok', 'specialities': [], 'displayOptions': True}
		checked_product = pathology._check_entry_product(product, 'substances')
		assert isinstance(checked_product, Substance)
		assert checked_product._id == 'lol'
		assert checked_product.name == 'ok'
		assert hasattr(checked_product, 'specialities')
		assert not hasattr(checked_product, 'displayOptions')

	def test_speciality_product(self, pathology):
		product = {'_id': 'lol', 'name': 'ok', 'displayOptions': True}
		checked_product = pathology._check_entry_product(product, 'specialities')
		assert isinstance(checked_product, Speciality)
		assert checked_product._id == 'lol'
		assert checked_product.name == 'ok'
		assert not hasattr(checked_product, 'displayOptions')

	def test_raise_error_on_wrong_reco(self, pathology):
		with pytest.raises(AssertionError):
			pathology._check_entry_reco({'_id': 'coucou'})

	def test_add_reco_label(self, pathology):
		checked_reco = pathology._check_entry_reco({'_id': 'ok'})
		assert checked_reco['name'] == 'Molécule Recommandée (voir RCP)'