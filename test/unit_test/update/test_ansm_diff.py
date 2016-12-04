# -*- coding: utf8 -*-
import pytest
import requests_mock
from freezegun import freeze_time

from api.models import Speciality, Substance
from api.update import SpecialityUpdater, SubstanceUpdater


SPEC_STREAM = u"""
61266250	A 313 200 000 UI POUR CENT, pommade	pommade	cutanee	Autorisation active	Procedure nationale	Commercialis�e	12/03/1998			 PHARMA DEVELOPPEMENT	Non
66513085	ABASAGLAR 100 unites/ml, solution injectable en cartouche	solution injectable	sous-cutanee	Autorisation active	Procedure centralisee	Commercialis�e	09/09/2014		EU/1/14/944	 ELI LILLY REGIONAL OPERATIONS (AUTRICHE)	Oui
"""

SUBST_STREAM = u"""
61266250	comprim	42215	ANASTROZOLE	1,00 mg	un comprim	SA	1
64332894	granules	42215	ACTAEA RACEMOSA	2CH ? 30CH et 4DH ? 60DH	un comprime	SA	7
66513085	comprim	25783	RANITIDINE (CHLORHYDRATE DE)	168 mg	un comprim	SA	1
61266250	comprim	49632	RANITIDINE BASE	150 mg	un comprim	FT	1
"""


@pytest.mark.parametrize('collection_name', ['Speciality'])
@freeze_time("2016-12-12")
def test_update_spec(spec1, spec2):
	with requests_mock.mock() as mock:
		# Given
		mock.get(
			requests_mock.ANY,
			text=SPEC_STREAM,
			headers={
				'Content-Type': 'text/html',
				'Charset': 'ISO-8859-1'
			}
		)
		spec_updater = SpecialityUpdater()

		# When
		spec_updater.execute()
		spec_list = Speciality.all()

		# Then
		assert len(spec_list) == 3
		assert not spec_list[0]['deleted_at']
		assert not spec_list[1]['deleted_at']
		assert spec_list[0]['_id'] == '61266250'
		assert spec_list[1]['_id'] == '66513085'
		assert spec_list[2]['_id'] == '64332894'
		assert spec_list[1]['created_at'] == '2016-12-12T00:00:00'
		assert spec_list[2]['deleted_at'] == '2016-12-12T00:00:00'


@pytest.mark.parametrize('collection_name', ['Speciality'])
@pytest.mark.parametrize('collection_name_bis', ['Substance'])
@freeze_time("2016-12-15")
def test_update_subst(subst1, subst2, spec1, spec2):
	with requests_mock.mock() as mock:
		# Given
		mock.get(
			requests_mock.ANY,
			text=SUBST_STREAM,
			headers={
				'Content-Type': 'text/html',
				'Charset': 'ISO-8859-1'
			}
		)
		subst_updater = SubstanceUpdater()

		# When
		subst_updater.execute()
		subst_list = Substance.all()

		# Then
		assert len(subst_list) == 3
		assert not subst_list[0]['deleted_at']
		assert not subst_list[1]['deleted_at']
		assert subst_list[0]['_id'] == '42215'
		assert subst_list[1]['_id'] == '49632'
		assert subst_list[2]['_id'] == '86571'
		assert subst_list[1]['created_at'] == '2016-12-15T00:00:00'
		assert subst_list[2]['deleted_at'] == '2016-12-15T00:00:00'
