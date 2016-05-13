# coding=utf-8
import datetime
from page import Page


class News(Page):
	def __init__(self, name, text, _id=None, author=None, created_at=None, updated_at=None, **kwargs):
		super(News, self).__init__(name, text, _id)
		self.author = author
		self.created_at = created_at if created_at else datetime.datetime.now().isoformat()
		self.updated_at = updated_at

	def set_author(self, user):
		del user.password_hash
		self.author = user
		return self

	def refresh_update_date(self):
		self.updated_at = datetime.datetime.now().isoformat()
		return self
