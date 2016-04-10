# coding=utf-8
from base_model import BaseModel


class Speciality(BaseModel):
	def __init__(self, _id=None, full_name=None, name=None, dosage=None, spec_type=None, treatment_type=None, status=None):
		self._id = _id
		self.full_name = full_name
		self.name = name
		self.dosage = dosage
		self.spec_type = spec_type
		self.treatment_type = treatment_type
		self.status = status
