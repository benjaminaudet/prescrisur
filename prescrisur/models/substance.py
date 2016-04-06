# coding=utf-8
import jsonpickle

from prescrisur.db import DB
from prescrisur.models import Speciality

collection = DB('Substance').collection


class Substance(object):
	def __init__(self, _id, name, specialities=None):
		self._id = _id
		self.name = name
		self.specialities = []
		if specialities:
			self.add_specialities(specialities)

	def _serialize(self):
		to_string = jsonpickle.encode(self, unpicklable=False)
		return jsonpickle.decode(to_string)

	def add_specialities(self, specs):
		for s in specs:
			self.specialities.append(Speciality(**s))

	def add_speciality_from_cis(self, cis):
		spec = Speciality.get(cis)
		if spec:
			return self.specialities.append(spec)

	def save(self):
		collection.save(self._serialize())

	@staticmethod
	def get(subst_id):
		raw_subst = collection.find_one({'_id': subst_id})
		return Substance(**raw_subst)
