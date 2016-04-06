# coding=utf-8
from prescrisur.db import DB

collection = DB('Speciality').collection


class Speciality(object):
	def __init__(self, cis=None, name=None, dosage=None, spec_type=None, treatment_type=None, status=None):
		self._id = cis
		self.dosage = dosage
		self.name = name
		self.spec_type = spec_type
		self.treatment_type = treatment_type
		self.status = status

	def save(self):
		collection.save(vars(self))
