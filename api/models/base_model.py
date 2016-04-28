import re
import jsonpickle
from pymongo import MongoClient, ASCENDING


client = MongoClient()
db = client.Prescrisur


class classproperty(object):
	def __init__(self, fget):
		self.fget = fget

	def __get__(self, owner_self, owner_cls):
		return self.fget(owner_cls)


class BaseModel(object):

	@classproperty
	def collection(cls):
		return db[cls.__name__]

	@classmethod
	def get(cls, obj_id):
		obj = cls.collection.find_one({'_id': obj_id})
		if not obj:
			return None
		return cls(**obj)

	@classmethod
	def _search(cls, query, proj=None, limit=0):
		if not proj:
			proj = {}
		objs = cls.collection.find(query, proj, limit=limit).sort('name', ASCENDING)
		if not objs:
			return []
		return list(objs)

	@classmethod
	def search_by_name(cls, name):
		regx = re.compile('^' + name, re.IGNORECASE)
		return cls._search({'name': regx}, {'name': 1, 'status': 1}, limit=200)

	def serialize(self):
		to_string = jsonpickle.encode(self, unpicklable=False)
		return jsonpickle.decode(to_string)

	def create(self):
		self.collection.insert_one(self.serialize())

	def save(self, upsert=True):
		self.collection.update_one({'_id': self._id}, {'$set': self.serialize()}, upsert=upsert)
