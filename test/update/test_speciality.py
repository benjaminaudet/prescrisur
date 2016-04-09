# coding=utf-8
import pytest

from prescrisur.update import Speciality, SpecialityUpdater


@pytest.fixture(autouse=True)
def speciality_updater():
	return SpecialityUpdater()


class TestIsValid:
	def test_empty_line(self, speciality_updater):
		assert not speciality_updater.is_valid(None, None)

	def test_invalid_line(self, speciality_updater):
		assert not speciality_updater.is_valid('NOK', 'NOK')

	def test_valid_line(self, speciality_updater):
		assert speciality_updater.is_valid('Autorisation active', 'Commercialisée')


class TestGetSpecType:
	def test_simple_string(self, speciality_updater):
		assert speciality_updater.get_spec_type('simple string') == 'simple string'

	def test_half_string(self, speciality_updater):
		assert speciality_updater.get_spec_type('half string et') == 'half string'

	def test_full_string(self, speciality_updater):
		assert speciality_updater.get_spec_type('full et string') == 'full'


class TestGetTreatmentType:
	def test_simple_string(self, speciality_updater):
		assert speciality_updater.get_treatment_type('orale') == ['orale']

	def test_simple_string(self, speciality_updater):
		assert speciality_updater.get_treatment_type('orale;sublinguale;cutanée') == ['orale', 'sublinguale', 'cutanée']


class TestParseName:
	def test_common_name(self, speciality_updater):
		assert speciality_updater.parse_name('ABILIFY 10 mg, comprimé') == ('ABILIFY', '10 mg')

	def test_simple_name(self, speciality_updater):
		assert speciality_updater.parse_name('ABROTANUM WELEDA, 2CH et 30CH') == ('ABROTANUM WELEDA', None)

	def test_complex_name(self, speciality_updater):
		assert speciality_updater.parse_name('ACT-HIB 10 microgrammes/0,5 ml') == ('ACT-HIB', '10 microgrammes/0,5 ml')


def test_valid_line(speciality_updater):
	def check_save(s):
		assert s._id == '64743867'
		assert s.name == 'ACICLOVIR RPG'
		assert s.dosage == '5 %'
		assert s.spec_type == 'crème'
		assert s.treatment_type == ['cutanée']
		assert not s.status

	Speciality.save = check_save

	speciality_updater.update_one([
		'64743867',
		'ACICLOVIR RPG 5 %, cr\xc3\xa8me',
		'cr\xc3\xa8me', 'cutan\xc3\xa9e',
		'Autorisation active',
		'Proc\xc3\xa9dure nationale',
		'Commercialis\xc3\xa9e'])
