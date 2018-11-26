from adjunct.builtins.interrupts import (
	wait,
	exit,
)

BUILTINS = {
	'wait': wait,
	'exit': exit,
}

__all__ = ['BUILTINS']
