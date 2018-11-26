class AdjunctSyntaxError(SyntaxError):
	"""Syntax Errors raised during adjunct parsing"""
	pass


class AdjunctAttributeError(AttributeError):
	"""Attribute Errors raised when accessing illegal or invalid identifiers"""
	pass


class AdjunctCompilerError(Exception):
	"""Raised if Adjunct compiler encounters errors"""
	pass


class AdjunctInterrupt(Exception):
	"""
	This isn't actually an exception, it's used internally by VirtualMachine for flow control.
	When sleep()/pause()/etc functions are encountered during the eval of Adjunct source, this exception
	is raised to exit eval, however, it is caught. Introspection is then performed on the stack
	to determine state (pointers, regiesters, etc)
	"""
	pass
