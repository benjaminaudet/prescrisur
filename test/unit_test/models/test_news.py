import pytest
from freezegun import freeze_time

from api.models import News, User


@pytest.fixture(autouse=True)
@freeze_time("2015-01-01")
def news():
	return News(name='Super News', text='<p>Youpi !</p>')


@pytest.fixture(autouse=True)
def user():
	return User(name='User', email='test@test', password_hash='coucou', token='token')


def test_set_author(news, user):
	# When
	news.set_author(user)

	# Then
	assert isinstance(news.author, User)
	assert news.author.name == 'User'
	assert not hasattr(news.author, 'password_hash')
	assert not hasattr(news.author, 'token')


def test_news_created_at(news):
	assert news.created_at == '2015-01-01T00:00:00'


@freeze_time("2016-01-01")
def test_news_refresh_update_date(news):
	# When
	news.refresh_update_date()

	# Then
	assert news.created_at == '2015-01-01T00:00:00'
	assert news.updated_at == '2016-01-01T00:00:00'
