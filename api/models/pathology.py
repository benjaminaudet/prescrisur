# coding=utf-8
import re
import bleach
import datetime
from slugify import slugify
from pymongo import DESCENDING

from base_model import BaseModel
from speciality import Speciality
from substance import Substance

bleach.ALLOWED_TAGS += ['p', 'br', 'span', 'div', 'img', 'i', 'u']
bleach.ALLOWED_ATTRIBUTES.update({'a': ['href', 'title', 'target']})


class Pathology(BaseModel):
	AUTHORIZED_TYPES = ['specialities', 'substances']
	RECO_LABELS = {
		'none': None,
		'alert': 'Molécule sous surveillance particulière',
		'middle': 'Molécule recommandée sous surveillance particulière',
		'ok': 'Molécule Recommandée (voir RCP)'
	}

	def __init__(self, name, _id=None, levels=None, intro=None, conclu=None, updated_at=None):
		self._id = _id if _id else slugify(name)
		self.name = name
		self.levels = levels if levels else []
		self.intro = intro
		self.conclu = conclu
		self.updated_at = updated_at

	@classmethod
	def search_by_substance(cls, subst_id):
		return cls._search({'$or': [
			{'levels.entries.product._id': subst_id},
			{'levels.levels.entries.product._id': subst_id},
			{'levels.levels.levels.entries.product._id': subst_id},
			{'levels.levels.levels.levels.entries.product._id': subst_id}
		]}, {'name': 1, 'status': 1})

	@classmethod
	def all(cls):
		objs = cls.collection.find({}, {'name': 1, 'updated_at': 1}).sort('updated_at', DESCENDING)
		if not objs:
			return []
		return list(objs)

	def check(self):
		self.name = bleach.clean(self.name)
		self.intro = self._linkify_grade(bleach.clean(self.intro))
		self.conclu = self._linkify_grade(bleach.clean(self.conclu))
		self.levels = map(lambda l: self._check_level(l), self.levels)
		return self

	def _check_level(self, level):
		level['name'] = bleach.clean(level['name'])
		if 'text' in level:
			level['text'] = self._linkify_grade(bleach.clean(level['text']))
		if 'levels' in level:
			if len(level['levels']) == 0:
				del level['levels']
			else:
				level['levels'] = map(lambda l: self._check_level(l), level['levels'])
		if 'entries' in level:
			if len(level['entries']) == 0:
				del level['entries']
			else:
				level['entries'] = map(lambda e: self._check_entry(e), level['entries'])
		return level

	def _check_entry(self, entry):
		# Check type
		assert entry['type'] in self.AUTHORIZED_TYPES
		# Check product
		assert 'product' in entry
		entry['product'] = self._check_entry_product(entry['product'], entry['type'])
		# Check reco
		assert 'reco' in entry
		entry['reco'] = self._check_entry_reco(entry['reco'])
		# Check info
		if 'info' in entry:
			entry['info'] = self._linkify_grade(entry['info'])
		return entry

	def _check_entry_reco(self, reco):
		assert '_id' in reco
		assert reco['_id'] in self.RECO_LABELS.keys()
		reco['name'] = self.RECO_LABELS[reco['_id']]
		return reco

	@staticmethod
	def _check_entry_product(product, product_type):
		if product_type == 'specialities':
			return Speciality(**product)
		elif product_type == 'substances':
			return Substance(**product)
		else:
			raise ValueError()

	@staticmethod
	def _linkify_grade(text):
		regx = re.compile('(Grade (?:A|B|C))(?!</a>)')
		return regx.sub(r'<a class="grade" href="http://localhost:5000/#/pages/presentation">\1</a>', text)

	def refresh_update_date(self):
		self.updated_at = datetime.datetime.now().isoformat()
		return self


