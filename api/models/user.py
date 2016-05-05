from passlib.hash import pbkdf2_sha256

from base_model import BaseModel


class User(BaseModel):
	def __init__(self, _id=None, password=None, password_hash=None, name=None, role=None):
		self._id = _id
		self.password_hash = password_hash if password_hash else pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
		self.name = name
		self.role = role

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

	def verify_password(self, password):
		return pbkdf2_sha256.verify(password, self.password_hash)

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
