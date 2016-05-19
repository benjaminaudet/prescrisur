import pytest

from api.models import Page


@pytest.fixture(autouse=True)
def page():
	return Page(name='Super Page', text='<p>Youpi !</p>')


@pytest.fixture(autouse=True)
def dirty_page():
	return Page(name='<script>niark()</script> Super Page', text='<p>Youpi !</p> <abc>super</abc>')


def test_check(page):
	# When
	cleaned_page = page.check()

	# Then
	assert isinstance(cleaned_page, Page)
	assert cleaned_page == page
	assert page._id == 'super-page'
	assert page.name == 'Super Page'
	assert page.text == '<p>Youpi !</p>'


def test_check_not_clean(dirty_page):
	# When
	dirty_page.check()

	# Then
	assert dirty_page.name == '&lt;script&gt;niark()&lt;/script&gt; Super Page'
	assert dirty_page.text == '<p>Youpi !</p> &lt;abc&gt;super&lt;/abc&gt;'
