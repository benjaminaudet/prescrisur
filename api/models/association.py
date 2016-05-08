# coding=utf-8
from slugify import slugify

from base_model import BaseModel
from substance import Substance


class Association(BaseModel):
	def __init__(self, name, _id=None, substances=None):
		self._id = _id if _id else slugify(name)
		self.name = name
		self.substances = []
		if substances:
			self.add_substances(substances)

	def add_substances(self, substances):
		for s in substances:
			self.substances.append(Substance(**s))
