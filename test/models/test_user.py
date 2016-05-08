# coding=utf-8
import pytest

from api.models import User


@pytest.fixture(autouse=True)
def user():
	return User(_id="pbo", password="password", name="PBO")


def test_verify_password(user):
	assert user.verify_password("password")
