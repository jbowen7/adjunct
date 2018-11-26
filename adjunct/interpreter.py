import logging
import inspect
from adjunct.constants import (
	PYTHON_BUILTINS_WHITELIST,
	VM_COMPILE_FILENAME,
	EXIT_SUCCESS,
	EXIT_FAILURE,
	EXIT_INTERRUPT,
)
from adjunct.exceptions import AdjunctInterrupt
from adjunct.parser import Parser
from adjunct.utils import is_valid_identifier
from adjunct.builtins import BUILTINS


LOGGER = logging.getLogger(__name__)


class VirtualMachine:
	"""
	VirtualMachine keeps a namespace as a dictionary which is accessible via __getitem__ and __setitem__
	namespace __builtins__ contain both Adjunct builtins (priority) and Python Builtins
	"""
	def __init__(self, text=None):
		assert isinstance(text, str)

		self.exit_code = EXIT_SUCCESS
		self.exception = None
		self.namespace = {}
		self.namespace['__builtins__'] = {**PYTHON_BUILTINS_WHITELIST, **BUILTINS}  # Adjunct builtins have priority

		if text:
			self.ast = self.parse(text)

	def parse(self, text):
		assert isinstance(text, str)
		return Parser().parse(text)

	def import_function(self, function, name=None):
		assert inspect.isfunction(function)
		name = name if isinstance(name, str) else function.__name__
		assert is_valid_identifier(name)
		self.namespace[name] = function

	def eval(self):
		self.exit_code = EXIT_FAILURE

		try:
			eval(compile(self.ast, VM_COMPILE_FILENAME, mode='exec'), self.namespace)
			self.exit_code = EXIT_SUCCESS

		except AdjunctInterrupt as signal:
			self.exception = signal
			self.exit_code = EXIT_INTERRUPT
			lineno, f_name, f_args, f_locals = signal.args
			self.last_line = lineno
			self.interrupted_by = f_name
			self.interrupted_by_args = f_args
			self.interrupted_by_locals = f_locals
			LOGGER.debug(f"Adjunct interrupted: ({lineno}) ({f_name} ({f_args}) ({f_locals})")

		except Exception as e:
			self.exception = e
			self.exit_code = EXIT_FAILURE


