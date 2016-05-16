from passlib.hash import pbkdf2_sha256
from pymongo import ASCENDING

from base_model import BaseModel


class User(BaseModel):
	def __init__(self, _id=None, password=None, password_hash=None, name=None, roles=None):
		self._id = _id
		self.password_hash = self.hash_password(password, password_hash)
		self.name = name
		self.roles = roles if roles else []

	@property
	def email(self):
		return self._id

	@property
	def is_active(self):
		return True

	@property
	def is_authenticated(self):
		return True

	@property
	def is_anonymous(self):
		return False

	@classmethod
	def all(cls):
		objs = cls.collection.find().sort('name', ASCENDING)
		if not objs:
			return []
		users = []
		for u in objs:
			del u['password_hash']
			users.append(u)
		return users

	@staticmethod
	def hash_password(password=None, password_hash=None):
		if password_hash:
			return password_hash
		if password:
			return pbkdf2_sha256.encrypt(password, rounds=20000, salt_size=32)
		return None

	def verify_password(self, password):
		return pbkdf2_sha256.verify(password, self.password_hash)

	def add_role(self, role):
		if role not in self.roles:
			self.roles.append(role)
		return self

	def remove_role(self, role):
		if role in self.roles:
			self.roles.remove(role)
		return self

	def get_id(self):
		return self._id

	def __eq__(self, other):
		if isinstance(other, User):
			return self.get_id() == other.get_id()
		return NotImplemented

	def __ne__(self, other):
		equal = self.__eq__(other)
		if equal is NotImplemented:
			return NotImplemented
		return not equal
