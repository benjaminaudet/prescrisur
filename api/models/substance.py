# coding=utf-8
from base_model import BaseModel
from speciality import Speciality


class Substance(BaseModel):
	def __init__(self, _id, name, status=None, specialities=None):
		self._id = _id
		self.name = name
		self.status = None
		self.specialities = []
		if specialities:
			self.add_specialities(specialities)

	def add_specialities(self, specs):
		for s in specs:
			self.specialities.append(Speciality(**s))

	def add_speciality_from_cis(self, cis):
		spec = Speciality.get(cis)
		if spec:
			self.specialities.append(spec)