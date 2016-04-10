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


class TestGetFullName:
	def test_full_name(self, speciality_updater):
		assert speciality_updater.get_full_name('A', 'B', ['C']) == 'A, B (C)'

	def test_no_spec_type(self, speciality_updater):
		assert speciality_updater.get_full_name('A', 'B', None) == 'A, B'

	def test_no_dosage(self, speciality_updater):
		assert speciality_updater.get_full_name('A', None, ['C']) == 'A (C)'

	def test_only_name(self, speciality_updater):
		assert speciality_updater.get_full_name('A', None, None) == 'A'

	def test_multiple_spec_types(self, speciality_updater):
		assert speciality_updater.get_full_name('A', 'B', ['C', 'D']) == 'A, B (C/D)'


class TestGetSpecType:
	def test_simple_string(self, speciality_updater):
		assert speciality_updater.get_spec_type('simple string') == ['simple string']

	def test_half_string(self, speciality_updater):
		assert speciality_updater.get_spec_type('half string et') == ['half string']

	def test_full_string(self, speciality_updater):
		assert speciality_updater.get_spec_type('full et string') == ['full', 'string']

	def test_needs_trimming(self, speciality_updater):
		assert speciality_updater.get_spec_type(' full et string ') == ['full', 'string']

	def test_duplicates(self, speciality_updater):
		assert speciality_updater.get_spec_type('full et full') == ['full']

	def test_full_example(self, speciality_updater):
		assert speciality_updater.get_spec_type(' full et  full et string et ') == ['full', 'string']


class TestGetTreatmentType:
	def test_simple_string(self, speciality_updater):
		assert speciality_updater.get_treatment_type('orale') == ['orale']

	def test_multiple_strings(self, speciality_updater):
		assert speciality_updater.get_treatment_type('orale;sublinguale;cutanée') == ['orale', 'sublinguale', 'cutanée']


class TestParseName:
	def test_common_name(self, speciality_updater):
		assert speciality_updater.parse_name('ABILIFY 10 mg, comprimé') == ('ABILIFY', '10 mg')

	def test_simple_name(self, speciality_updater):
		assert speciality_updater.parse_name('ABROTANUM WELEDA, 2CH et 30CH') == ('ABROTANUM WELEDA', None)

	def test_complex_name(self, speciality_updater):
		assert speciality_updater.parse_name('ACT-HIB 10 microgrammes/0,5 ml') == ('ACT-HIB', '10 microgrammes/0,5 ml')

	def test_slashes_in_name(self, speciality_updater):
		name = 'DOLI ETAT GRIPPAL PARACETAMOL/VITAMINE C/PHENIRAMINE'
		dosage = '500 mg/200 mg/25 mg'
		assert speciality_updater.parse_name(' '.join([name, dosage])) == (name, dosage)


def test_valid_line(speciality_updater):
	def check_save(s):
		assert s._id == '64743867'
		assert s.full_name == 'ACICLOVIR RPG, 5 % (poudre/crème)'
		assert s.name == 'ACICLOVIR RPG'
		assert s.dosage == '5 %'
		assert s.spec_type == ['poudre', 'crème']
		assert s.treatment_type == ['cutanée']
		assert not s.status

	Speciality.save = check_save

	speciality_updater.update_one([
		'64743867',
		'ACICLOVIR RPG 5 %, cr\xc3\xa8me',
		'cr\xc3\xa8me et poudre', 'cutan\xc3\xa9e',
		'Autorisation active',
		'Proc\xc3\xa9dure nationale',
		'Commercialis\xc3\xa9e'])
