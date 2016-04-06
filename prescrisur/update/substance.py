# coding=utf-8
import urllib2

from prescrisur.models import Substance

SUBSTANCE_URI = 'http://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_COMPO_bdpm.txt'


class SubstanceUpdater(object):

	def update(self):
		substances = {}
		req = urllib2.urlopen(SUBSTANCE_URI)
		for line in req.readlines():
			line = line.decode('ISO-8859-1').encode('UTF8').split('\t')
			subst_id = line[2]
			if subst_id not in substances:
				substances[subst_id] = self.create_substance(line)
			substances[subst_id].add_speciality(line[0])
		map(lambda x: substances[x].save(), substances)

	@staticmethod
	def create_substance(line):
		return Substance(
			subst_id=line[2],
			name=line[3]
		)
