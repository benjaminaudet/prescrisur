# coding=utf-8
import pytest

from api.models import User


@pytest.fixture(autouse=True)
def user():
	return User(_id="pbo", password="password", name="PBO")


def test_verify_password(user):
	assert user.verify_password("password")


def test_add_role(user):
	# When
	user.add_role('admin')

	# Then
	assert len(user.roles) == 1
	assert 'admin' in user.roles


def test_add_role_already_exists(user):
	# Given
	user.add_role('admin')

	# When
	user.add_role('admin')

	# Then
	assert len(user.roles) == 1
	assert 'admin' in user.roles


def test_remove_role(user):
	# Given
	user.add_role('admin')

	# When
	user.remove_role('admin')

	# Then
	assert len(user.roles) == 0


def test_remove_role_does_not_exist(user):
	# Given
	user.add_role('admin')
	user.add_role('subscriber')

	# When
	user.remove_role('coucou')

	# Then
	assert len(user.roles) == 2
