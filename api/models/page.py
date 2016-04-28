# coding=utf-8
from slugify import slugify

from base_model import BaseModel


class Page(BaseModel):
	def __init__(self, _id=None, name=None, text=None):
		self._id = _id if _id else slugify(name)
		self.name = name
		self.text = text
