import logging
import ast as Ast

from adjunct.exceptions import AdjunctSyntaxError, AdjunctCompilerError
from adjunct.constants import AST_NODE_WHITELIST
from adjunct.utils import is_valid_identifier


LOGGER = logging.getLogger(__name__)


class ValidateName(Ast.NodeTransformer):
	"""
	use this to keep scope on VirtualMachine
	"""

	def visit_Name(self, node):
		if not is_valid_identifier(node.id):
			raise AdjunctSyntaxError(node)

		#node = Ast.copy_location(Ast.Subscript(
		#	value=Ast.Name(id='self', ctx=Ast.Load()),
		#	slice=Ast.Index(value=Ast.Str(s=node.id)),
		#	ctx=node.ctx
		#), node)
		#Ast.fix_missing_locations(node)
		return node


class Parser:
	def wrap(self, node):
		return Ast.Module(body=[node])

	def parse(self, text):
		assert isinstance(text, str)
		tree = Ast.parse(text)

		# Security: check nodes against AST Node whitelist
		for node in Ast.walk(tree):
			if type(node) not in AST_NODE_WHITELIST:
				raise AdjunctSyntaxError(node)

		# More security: check identifiers for __
		tree = ValidateName().visit(tree)

#		LOGGER.debug(f"Parser.parse() -> {Ast.dump(tree, include_attributes=True)}")
		return tree

	def dump(self, ast, include_attributes=True):
		return Ast.dump(ast, include_attributes=include_attributes)

	def parseprint(self, text):
		ast = self.parse(text)
		return self.dump(ast)

# Be careful when implementing Security for Call
# a simpole node wrap of subscript is not sufficient
# for example:
# a = object.bad_method
# a() # one way to access methods that are attributes..
#class RewriteCall(Ast.NodeTransformer):
#	"""
#	Disallow all built-in callables.
#	Whitelist calls in Namespace
#	"""
#	def visit_Call(self, node):
#		assert isinstance(node.func, Ast.Name)
#		self.generic_visit(node)
#
#		name_node = node.func
#		node.func = Ast.Subscript(
#			value=Ast.Name(id='namespace', ctx=Ast.Load()),
#			slice=Ast.Index(value=Ast.Str(s=name_node.id)),
#			ctx=Ast.Load()
#		)
#		#TODO:jbowen7 fix_missing_locations sets lineno=1 and coloffset=0 for each node.. is that ok?
#		Ast.fix_missing_locations(node)
#		return node


class Compiler:
	"""
	The AST is compiled into an instruction set which is evaluated one at a time.
	The VirtualMachine then evaluates the return of each instruction by introspection
	and makes decisions about the it (VirtualMachine) should do next (continue, sleep, dump, etc).
	"""
	def __init__(self):
		self.instructions = []

	def compile(self, ast):
		if isinstance(ast, Ast.Module):
			mode = 'exec'
		elif isinstance(ast, ast.Expression):
			mode = 'eval'
		else:
			raise AdjunctCompilerError("ast must be an instance of ast.Module or ast.Expression")
		return compile(ast, 'Adjunct', mode=mode)


