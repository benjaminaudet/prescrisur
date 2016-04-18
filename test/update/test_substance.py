# coding=utf-8
import pytest

from api.update import Substance, SubstanceUpdater


@pytest.fixture(autouse=True)
def substance_updater():
	return SubstanceUpdater()


def test_create_substance(substance_updater):
	line = ['cis', 'pouet', 'subst_id', 'name']
	substance = substance_updater.create_substance(line)
	assert substance._id == 'subst_id'
	assert substance.name == 'name'
	assert substance.specialities == []