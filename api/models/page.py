# coding=utf-8
import bleach
from slugify import slugify

from base_model import BaseModel

bleach.ALLOWED_TAGS += ['p', 'br', 'span', 'div', 'img', 'i', 'u']
bleach.ALLOWED_ATTRIBUTES.update({
	'a': ['href', 'title', 'target'],
	'img': ['src', 'alt', 'title']
})


class Page(BaseModel):
	def __init__(self, name, text, _id=None):
		self._id = _id if _id else slugify(name)
		self.name = name
		self.text = text

	def check(self):
		self.name = bleach.clean(self.name)
		self.text = bleach.clean(self.text)
		return self
