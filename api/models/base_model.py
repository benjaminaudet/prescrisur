import re
import jsonpickle
from pymongo import MongoClient, ASCENDING, DESCENDING

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
	def get(cls, obj_id=None):
		if not obj_id:
			return cls.all()
		obj = cls.collection.find_one({'_id': obj_id})
		if not obj:
			return None
		return cls(**obj)

	@classmethod
	def delete(cls, obj_id):
		return cls.collection.delete_one({'_id': obj_id})

	@classmethod
	def all(cls):
		objs = cls.collection.find().sort([('created_at', DESCENDING), ('_id', ASCENDING)])
		if not objs:
			return []
		return list(objs)

	@classmethod
	def _search(cls, query, proj='default', limit=0):
		if proj == 'default':
			proj = {'name': 1, 'status': 1}
		objs = cls.collection.find(query, proj, limit=limit).sort('name', ASCENDING)
		if not objs:
			return []
		return list(objs)

	@classmethod
	def search_by_name(cls, name, proj=None):
		regx = re.compile(name, re.IGNORECASE)
		return cls._search({'name': regx}, proj, limit=200)

	def serialize(self):
		to_string = jsonpickle.encode(self, unpicklable=False)
		return jsonpickle.decode(to_string)

	def create(self):
		self.collection.insert_one(self.serialize())

	def save(self, upsert=True):
		self.collection.update_one({'_id': self._id}, {'$set': self.serialize()}, upsert=upsert)
