from pymongo import MongoClient


class DB(MongoClient):
	def __init__(self, collection=None):
		MongoClient.__init__(self)
		self.db = self.Prescrisur
		self.collection = self.db[collection]
