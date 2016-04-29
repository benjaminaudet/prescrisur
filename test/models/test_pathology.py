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
	def test_raise_error_on_wrong_type(self, wrong_type_pathology):
		with pytest.raises(AssertionError):
			wrong_type_pathology.check()

	def test_raise_error_on_no_product(self, no_product_pathology):
		with pytest.raises(AssertionError):
			no_product_pathology.check()

	def test_raise_error_on_uncompliant_product(self, uncompliant_product_pathology):
		with pytest.raises(AssertionError):
			uncompliant_product_pathology.check()

	def test_add_reco_label(self, cleaned_pathology):
		assert cleaned_pathology.levels[1]['levels'][1]['entries'][0]['reco']['name'] == 'Molécule Recommandée (voir RCP)'