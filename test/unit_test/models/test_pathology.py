# coding=utf-8
import pytest
from freezegun import freeze_time

from api.models import Pathology, Substance, Speciality, Association


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
def therapeutic_class():
	return {
		'is_class': True,
		'name': 'class',
		'text': 'class text',
		'levels': [
			{
				'is_class': True,
				'name': 'class1',
				'text': 'class text1',
				'levels': [
					{
						'is_class': False,
						'name': 'class11',
						'text': 'class text11',
					},
					{
						'is_class': True,
						'name': 'class12',
						'entries': 'super'
					}
				]
			},
			{
				'is_class': False,
				'name': 'class2',
				'text': 'class text2',
			}
		]
	}


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


def test_serialize(cleaned_pathology):
	serialized_cleaned_pathology = cleaned_pathology.serialize()
	assert serialized_cleaned_pathology['_id'] == 'pathologie-testee'
	assert serialized_cleaned_pathology['levels'][1]['levels'][1]['entries'][0]['product']['name'] == 'lol'


def test_compute_class_level(pathology, therapeutic_class):
	computed_class = pathology.compute_therapeutic_class(therapeutic_class)
	assert computed_class == {
		'name': 'class',
		'text': 'class text',
		'levels': [
			{
				'name': 'class1',
				'text': 'class text1',
				'levels': [
					{
						'name': 'class12',
						'entries': 'super'
					}
				]
			}
		]
	}


class TestBleachedText:
	def test_text_clean(self, cleaned_pathology):
		assert cleaned_pathology.conclu == '<a href="http://www.google.com" target="_blank">juste un lien</a>'

	def test_text_unclean(self, cleaned_pathology):
		assert cleaned_pathology.intro == '&lt;script&gt;fumed()&lt;/script&gt;'


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

	def test_association_product(self, pathology):
		product = {'_id': 'lol', 'name': 'ok', 'specialities': [], 'substances': [], 'displayOptions': True}
		checked_product = pathology._check_entry_product(product, 'associations')
		assert isinstance(checked_product, Association)
		assert checked_product._id == 'lol'
		assert checked_product.name == 'ok'
		assert hasattr(checked_product, 'specialities')
		assert hasattr(checked_product, 'substances')
		assert not hasattr(checked_product, 'displayOptions')

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