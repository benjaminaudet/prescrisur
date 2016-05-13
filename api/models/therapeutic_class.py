# coding=utf-8
from slugify import slugify

from base_model import BaseModel


class TherapeuticClass(BaseModel):
	def __init__(self, pathology_id, name, text=None, levels=None, entries=None, _id=None):
		self._id = _id if _id else slugify(name)
		self.pathology_id = pathology_id
		self.name = name
		self.text = text
		self.levels = levels
		self.entries = entries
