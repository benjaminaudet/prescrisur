# coding=utf-8
import pytest
from mock import MagicMock

from api.update import Speciality, Substance, SubstanceUpdater


@pytest.fixture(autouse=True)
def substance_updater():
	return SubstanceUpdater()


@pytest.fixture(autouse=True)
def substance():
	s = Substance(_id='1', name='subst')
	s.save = MagicMock()
	return s


def test_create_substance(substance_updater):
	line = ['cis', 'pouet', 'subst_id', 'name']
	substance = substance_updater.create_substance(line)
	assert substance._id == 'subst_id'
	assert substance.name == 'name'
	assert substance.specialities == []


def test_save_if_has_specialities_ok(substance_updater, substance):
	# Given
	substance.specialities = [Speciality(_id='1', name='spec')]

	# When
	substance_updater.save_if_has_specialities(substance)

	# Then
	assert substance.save.assert_called_once()


def test_save_if_has_specialities_nok(substance_updater, substance):
	# When
	res = substance_updater.save_if_has_specialities(substance)

	# Then
	assert not res
