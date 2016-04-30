# coding=utf-8
import pytest
from freezegun import freeze_time

from api.models import Pathology


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
	assert pathology._linkify_grade('Bonjour (Grade B)') == 'Bonjour (<a href="http://localhost:5000/#/pages/presentation">Grade B</a>)'
	assert pathology._linkify_grade('Bonjour <b>Grade C</b>') == 'Bonjour <b><a href="http://localhost:5000/#/pages/presentation">Grade C</a></b>'


class TestBleachedText:
	def test_text_clean(self, cleaned_pathology):
		assert cleaned_pathology.conclu == '<a href="http://www.google.com" target="_blank">juste un lien</a>'

	def test_text_unclean(self, cleaned_pathology):
		assert cleaned_pathology.intro == '&lt;script&gt;fumed()&lt;/script&gt;'

	def test_linkify_grade(self, cleaned_pathology):
		assert cleaned_pathology.levels[0]['text'] == 'Bonjour (<a href="http://localhost:5000/#/pages/presentation">Grade A</a>)'


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

	def test_remove_display_specialities_key_on_substances(self, pathology):
		product = {'_id': 'lol', 'name': 'ok', 'specialities': [], 'displaySpecialities': True}
		checked_product = pathology._check_entry_product(product, 'substances')
		assert 'displaySpecialities' not in checked_product

	def test_raise_error_on_wrong_reco(self, pathology):
		with pytest.raises(AssertionError):
			pathology._check_entry_reco({'_id': 'coucou'})

	def test_add_reco_label(self, pathology):
		checked_reco = pathology._check_entry_reco({'_id': 'ok'})
		assert checked_reco['name'] == 'Molécule Recommandée (voir RCP)'
