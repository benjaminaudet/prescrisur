import pytest

from api.db import DB


@pytest.fixture(autouse=True)
def db():
	return DB('Super')


def test_db(db):
	assert db.db.name == 'Prescrisur'
	assert db.collection.name == 'Super'

