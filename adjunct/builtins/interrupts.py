import inspect
from adjunct.exceptions import AdjunctInterrupt
from adjunct.constants import VM_COMPILE_FILENAME


def _interrupt():
	"""
	Used to interrupt the evaluation of Adjunct source. This is not meant to be called directly,
	but should be called by the functions below
	:raises: AdjunctInterrupt(adjunct linenumber, function name, args, locals)
	"""
	# Handle stackframe without leaking requires deferencing (try/finally assures this)
	# https://docs.python.org/3/library/inspect.html
	try:
		frame = inspect.currentframe().f_back  # currentframe is for _interrupt. We want the stack below
		c_func = frame.f_code.co_name  # The name of the function that called _interrupt
		c_func_args = inspect.getargvalues(frame).args
		c_func_locals = inspect.getargvalues(frame).locals
		# We need to find the linenu in the adjunct that is responsible for this whole stack
		while frame is not None:
			if inspect.getframeinfo(frame).filename == VM_COMPILE_FILENAME:
				break
			frame = frame.f_back
		assert frame is not None, f"_interrupt must be part of an adjunct stack"
		lineno = frame.f_lineno

	finally:
		if frame is not None:
			del frame
	raise AdjunctInterrupt(lineno, c_func, c_func_args, c_func_locals)


def wait(seconds):
	"""
	A basic function to sleep or wait for X seconds
	"""
	return _interrupt()


def exit():
	"""
	Exits an adjunct script
	"""
	return _interrupt()
