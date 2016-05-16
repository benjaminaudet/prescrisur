from slugify import slugify
from pymongo import ASCENDING
from passlib.hash import pbkdf2_sha256

from base_model import BaseModel


class User(BaseModel):
	def __init__(self, _id=None, email=None, password=None, password_hash=None, name=None, roles=None, confirmed=False):
		self._id = _id if _id else slugify(email)
		self.email = email
		self.password_hash = self.hash_password(password, password_hash)
		self.name = name
		self.roles = roles if roles else []
		self.confirmed = confirmed

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
	def get_by_email(cls, email):
		user = cls.collection.find_one({'email': email})
		if not user:
			return None
		return User(**user)

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

	def confirm(self):
		self.confirmed = True
		return self.save()

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
