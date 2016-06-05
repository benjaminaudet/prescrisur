# coding=utf-8
from pymongo import ASCENDING

from base_model import BaseModel
from speciality import Speciality


class Substance(BaseModel):
	ORDER_BY = [('name', ASCENDING)]

	def __init__(self, _id, name, status=None, specialities=None, **kwargs):
		self._id = _id
		self.name = name
		self.status = status
		self.specialities = []
		if specialities:
			self.add_specialities(specialities)

	def add_specialities(self, specs):
		for s in specs:
			self.specialities.append(Speciality(**s))

	def add_speciality_from_cis(self, cis):
		spec = Speciality.get(cis)
		if spec:
			if spec.status == 'R':
				self.status = 'G'
			return self.specialities.append(spec)

	def sort_specialities(self):
		self.specialities.sort(key=lambda s: s.name)
		return self
