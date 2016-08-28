import pytest

from api.models import Substance, Association


@pytest.fixture(autouse=True)
def substance():
	return Substance(name='Substance', _id=1)


@pytest.fixture(autouse=True)
def substance_g():
	return Substance(name='SubstanceG', _id=2, status='G')


def test_get_status_no_g(substance):
	# Given
	substances = [substance]

	# Then
	assert not Association.get_status(substances)


def test_get_status_g(substance, substance_g):
	# Given
	substances = [substance, substance_g]

	# Then
	assert Association.get_status(substances) == 'G'
