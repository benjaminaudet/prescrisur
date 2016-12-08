import pytest
from freezegun import freeze_time

from api.models import Substance


@freeze_time("2016-12-12")
@pytest.mark.parametrize('collection_name_bis', ['Substance'])
def test_flag_all_as_deleted(subst1, deleted_subst):
	# When
	Substance.flag_all_as_deleted()
	substances = Substance.all()

	# Then
	assert substances[0]['name'] == 'Deleted Subst'
	assert substances[0]['deleted_at'] == '2015-10-10'
	assert substances[1]['name'] == 'Subst1'
	assert substances[1]['deleted_at'] == '2016-12-12T00:00:00'
