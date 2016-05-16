from functools import wraps

from flask import jsonify, abort
from flask.ext.login import current_user


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
