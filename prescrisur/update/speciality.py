# coding=utf-8
import re
import urllib2

from prescrisur.models import Speciality

SPECIALITIES_URI = 'http://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_bdpm.txt'
REG_NAME = r"([a-zA-Z0-9.()'\"\- ]+)(\s([0-9,.\/-]+(\s[0-9])?\s?(bar|G|M|m|µ|n|g|I|%|U|u|POUR|pour|microgramme|gramme).*))"
REG_TYPE = r" et\s?"


class SpecialityUpdater(object):

	def execute(self):
		req = urllib2.urlopen(SPECIALITIES_URI)
		for line in req.readlines():
			line = line.decode('ISO-8859-1').encode('UTF8').split('\t')
			if not self.is_valid(line[4], line[6]):
				continue
			self.update_one(line)
		return

	def update_one(self, line):
		name, dosage = self.parse_name(line[1])
		spec_type = self.get_spec_type(line[2])
		return Speciality(
			_id=line[0],
			name=name,
			dosage=dosage,
			spec_type=spec_type,
			treatment_type=line[3],
			status=None
		).save()

	@staticmethod
	def is_valid(authorization, marketing):
		if authorization == 'Autorisation active' and marketing == 'Commercialisée':
			return True
		return False

	@staticmethod
	def parse_name(name):
		parsed_name = name.split(', ')[0]
		match = re.match(REG_NAME, parsed_name)
		if not match:
			return parsed_name, None
		return match.group(1), match.group(3)

	@staticmethod
	def get_spec_type(spec_type):
		parsed_spec_type = re.split(REG_TYPE, spec_type)
		return parsed_spec_type[0]
