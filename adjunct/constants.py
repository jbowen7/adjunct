import ast


# Whitelist of python __builtins__
# The VirtualMachine uses eval() for evaluating a compiled AST, therefore the python
# builtins must be restricted. There are so many functions which can be dangerous:
# __import__, globals, locals, eval, exec, call, getattr, hasattr, delattr, setattr, compile, etc...
PYTHON_BUILTINS_WHITELIST = {
	'len': len,
	'print': print,
	'range': range,
}

# Whitelist of ast Nodes
# One of the steps during parsing is to walk through the AST and check nodes against this whitelist.
# If a node not in this list is encountered a Syntax Error is raised.  This step during parsing does two things:
# 1) GRAMMAR: abstractly defines the Adjunct grammar (even if it is just a subset of python grammar)
# 2) Security: provides a level of security at the parsing layer. Security is of utmost importance since
# the interpretor uses python's eval() to evaluate user supplied source code
# IMPORTANT: take great care with Nodes that can grant introspection or traversal abilities
# For example, with ast.Attribute, this is possible: "().__class__.__bases__[0].__subclasses__()"
AST_NODE_WHITELIST = [
	ast.Module, ast.Num, ast.Str, ast.FormattedValue, ast.JoinedStr, ast.List, ast.Tuple, ast.Set,
	ast.Dict, ast.NameConstant, ast.Name, ast.Load, ast.Store, ast.Del, ast.Expr, ast.BinOp, ast.Add, ast.Sub,
	ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.BoolOp, ast.And, ast.Or, ast.Compare, ast.Eq, ast.NotEq, ast.Lt,
	ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn, ast.Call, ast.keyword, ast.IfExp, ast.Subscript,
	ast.Index, ast.Assign, ast.Pass, ast.If, ast.For, ast.Break, ast.Continue,
]

# filename passed to compile for the evaluation of adjunct source
# used to reference pointers after interrupts
VM_COMPILE_FILENAME = '<adjunct>'


# Exit values for VirtualMachine
EXIT_SUCCESS = 0  # succesfully completed
EXIT_FAILURE = 1  # Catch all error
EXIT_INTERRUPT = 50  # Default interrupt exit code
