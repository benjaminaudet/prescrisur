# coding=utf-8
from pymongo import ASCENDING

from base_model import BaseModel


class Speciality(BaseModel):
	ORDER_BY = [('name', ASCENDING)]

	def __init__(self, _id=None, short_name=None, name=None, dosage=None, spec_type=None, treatment_type=None, status=None, enabled=True, **kwargs):
		self._id = _id
		self.short_name = short_name
		self.name = name
		self.dosage = dosage
		self.spec_type = spec_type
		self.treatment_type = treatment_type
		self.status = status
		self.enabled = enabled
