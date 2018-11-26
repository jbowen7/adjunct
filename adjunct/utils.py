from adjunct.exceptions import (
	AdjunctSyntaxError,
	AdjunctAttributeError,
)


def is_valid_identifier(name):
	"""
	Adjunct identifiers:
		1) must be valid python identifiers
		2) must NOT begin with an underscore
	"""
	retval = name.isidentifier()
	if len(name) > 1:
		if name[0] == '_':
			retval = False
	return retval


class AdjunctObject:
	"""
	Wraps objects to make them safe for use with Adjunct
	This class is not strictly needed, but it is recommended if there is uncertainty
	about the attributes of an object, that is, whether they can be used
	to do nasty things
	"""
	def __init__(self, obj):
		setattr(self, '__obj', obj)

	def __getattr__(self, name):
		if self.__is_safe_identifier(name) is False:
			raise AdjunctAttributeError(f"{type(self.__obj).__name__} object has no attribute {name}")
		return self.__obj.__getattr__(name)

	def __setattr__(self, name, value):
		if self.__is_safe_identifier(name) is False:
			raise AdjunctSyntaxError("invalid syntax")
		return self.__obj.__setattr__(name, value)

	def __is_safe_identifier(self, name):
		retval = name.isidentifier()
		# Identifiers with double underscores are not accessible in Adjunct
		if len(name) > 1:
			if name[0:2] == '__':
				retval = False
		return retval


