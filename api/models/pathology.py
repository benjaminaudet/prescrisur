from base_model import BaseModel


class Pathology(BaseModel):
	def __init__(self, name, levels=None):
		self.name = name
		self.levels = levels if levels else []
