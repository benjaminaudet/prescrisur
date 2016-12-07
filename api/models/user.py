from slugify import slugify
from pymongo import ASCENDING
from flask import current_app
from passlib.hash import pbkdf2_sha256
from itsdangerous import TimedJSONWebSignatureSerializer as URLSafeSerializer, BadSignature, SignatureExpired

from base_model import BaseModel


class User(BaseModel):
	def __init__(self, _id=None, email=None, password=None, password_hash=None, name=None, roles=None, confirmed=False, token=None, **kwargs):
		self._id = _id if _id else slugify(email)
		self.email = email
		self.password_hash = self.hash_password(password, password_hash)
		self.name = name
		self.roles = roles if roles else []
		self.confirmed = confirmed
		self.token = token

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

	def generate_auth_token(self):
		s = URLSafeSerializer(current_app.config['SECRET_KEY'], expires_in=3153600000)
		self.token = s.dumps(self.email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

	@staticmethod
	def verify_auth_token(token):
		s = URLSafeSerializer(current_app.config['SECRET_KEY'])
		try:
			email = s.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'])
		except BadSignature:
			return None # invalid token
		return User.get_by_email(email)

	def clean(self):
		delattr(self, 'password_hash')
		delattr(self, 'token')
		return self

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
