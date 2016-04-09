# coding=utf-8
import re

from prescrisur.db import DB

collection = DB('Speciality').collection


class Speciality(object):
	def __init__(self, _id=None, full_name=None, name=None, dosage=None, spec_type=None, treatment_type=None, status=None):
		self._id = _id
		self.full_name = full_name
		self.name = name
		self.dosage = dosage
		self.spec_type = spec_type
		self.treatment_type = treatment_type
		self.status = status

	def serialize(self):
		return vars(self)

	def save(self):
		collection.save(self.serialize())

	@staticmethod
	def get(spec_id):
		spec = collection.find_one({'_id': spec_id})
		if not spec:
			return None
		return Speciality(**spec)

	@staticmethod
	def search(query):
		regx = re.compile('^' +query, re.IGNORECASE)
		specs = collection.find({'name': regx})
		if not specs:
			return []
		return map(lambda s: Speciality(**s), specs)
