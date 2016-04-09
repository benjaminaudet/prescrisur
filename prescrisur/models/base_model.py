import re
import jsonpickle
from pymongo import MongoClient


class classproperty(object):
	def __init__(self, fget):
		self.fget = fget

	def __get__(self, owner_self, owner_cls):
		return self.fget(owner_cls)


class DB(MongoClient):
	def __init__(self, collection=None):
		MongoClient.__init__(self)
		self.db = self.Prescrisur
		self.collection = self.db[collection]


class BaseModel(object):
	@classproperty
	def collection(cls):
		db = DB(cls.__name__)
		return db.collection

	@classmethod
	def get(cls, obj_id):
		obj = cls.collection.find_one({'_id': obj_id})
		if not obj:
			return None
		return cls(**obj)

	@classmethod
	def search(cls, query):
		regx = re.compile('^' +query, re.IGNORECASE)
		objs = cls.collection.find({'name': regx})
		if not objs:
			return []
		return map(lambda o: cls(**o), objs)

	def serialize(self):
		to_string = jsonpickle.encode(self, unpicklable=False)
		return jsonpickle.decode(to_string)

	def save(self):
		self.collection.save(self.serialize())
