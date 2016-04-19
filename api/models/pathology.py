from slugify import slugify

from base_model import BaseModel


class Pathology(BaseModel):
	def __init__(self, name, _id=None, levels=None):
		self._id = _id if _id else slugify(name)
		self.name = name
		self.levels = levels if levels else []
