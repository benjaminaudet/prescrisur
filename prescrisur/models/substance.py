# coding=utf-8
from prescrisur.db import DB

collection = DB('Substance').collection


class Substance(object):
	def __init__(self, _id, name, specialities=None):
		self._id = _id
		self.name = name
		self.specialities = specialities if specialities else []

	def add_speciality(self, cis):
		return self.specialities.append(cis)

	def save(self):
		collection.save(vars(self))

	@staticmethod
	def get(subst_id):
		s = collection.find_one({'_id': subst_id})
		return Substance(**s)
