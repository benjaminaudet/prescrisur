from functools import wraps
from datetime import datetime
from flask import jsonify, abort
from flask.ext.login import current_user

from api.services.logger import Logger


def required_role(role):
	def wrapper(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			if not current_user.is_authenticated:
				abort(401)
			elif role not in current_user.roles:
				return jsonify({'role_needed': role}), 403
			return f(*args, **kwargs)
		return wrapped
	return wrapper


def monitored():
	logger = Logger('prescrisur.monitor', '/tmp')
	msg = "%s %s %s:%s %d"

	def wrapper(f):
		fname = f.func_name

		@wraps(f)
		def wrapped(*args, **kwargs):
			uid = 'anonymous'
			func_arg = None
			if current_user.is_authenticated:
				uid = current_user._id
			timestarted = datetime.utcnow()
			if kwargs:
				func_arg = kwargs.values()[0]
			try:
				res = f(*args, **kwargs)
				dt = ((datetime.utcnow() - timestarted).total_seconds() * 1000)
				logger.info(msg % (timestarted.time().isoformat(), uid, fname, func_arg, dt))
				return res
			except:
				dt = ((datetime.utcnow() - timestarted).total_seconds() * 1000)
				logger.info(msg % (timestarted.time().isoformat(), uid, fname, func_arg, dt))
				raise

		return wrapped
	return wrapper
