# coding=utf-8
from prescrisur.db import DB

collection = DB('Substance').collection


class Substance(object):
	def __init__(self, subst_id=None, name=None):
		self._id = subst_id
		self.name = name
		self.specialities = []

	def add_speciality(self, cis):
		return self.specialities.append(cis)

	def save(self):
		collection.save(vars(self))
