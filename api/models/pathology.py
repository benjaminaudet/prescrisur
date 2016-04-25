from slugify import slugify
from datetime import datetime

from base_model import BaseModel


class Pathology(BaseModel):
	def __init__(self, name, _id=None, levels=None, intro=None, conclu=None, updated_at=None):
		self._id = _id if _id else slugify(name)
		self.name = name
		self.levels = levels if levels else []
		self.intro = intro
		self.conclu = conclu
		self.updated_at = updated_at

	def refresh_update_date(self, update_date=None):
		if update_date:
			upd = update_date
		else:
			upd = datetime.now().isoformat()
		self.updated_at = upd
		return self
