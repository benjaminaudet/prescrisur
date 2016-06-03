# coding=utf-8
import urllib2

from api.models import Substance

SUBSTANCE_URI = 'http://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_COMPO_bdpm.txt'


class SubstanceUpdater(object):

	def execute(self):
		substances = {}
		req = urllib2.urlopen(SUBSTANCE_URI)
		for line in req.readlines():
			line = line.decode('ISO-8859-1').encode('UTF8').split('\t')
			subst_id = line[2]
			if subst_id not in substances:
				substances[subst_id] = self.create_substance(line)
			substances[subst_id].add_speciality_from_cis(line[0])
		map(lambda x: self.save_if_has_specialities(substances[x]), substances)

	@staticmethod
	def save_if_has_specialities(subst):
		if len(subst.specialities) > 0:
			return subst.sort_specialities().save()
		return False

	@staticmethod
	def create_substance(line):
		return Substance(
			_id=line[2],
			name=line[3],
			status=None
		)
