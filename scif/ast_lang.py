

import enum
import re


class ASTNode:
	def __init__(self, nodetype, children=None, value=None):
		self.nodetype = nodetype
		self.children = children if children else []
		self.value = value

	#overload [] operator
	def __getitem__(self, index):
		return self.children[index]

	def __repr__(self):
		if self.value is not None:
			return f"{self.nodetype}({self.value})"
		return f"{self.nodetype}({', '.join(map(str, self.children))})"
	
	def pretty_print(self, indent=0):
		tab = "    " * indent
		if self.value is not None:
			return f"{tab}{self.nodetype}: {self.get_string_value_repr()}\n"
		result = f"{tab}{self.nodetype}:\n"
		for child in self.children:
			if isinstance(child, ASTNode):
				result += child.pretty_print(indent + 1)
			else:
				result += f"{tab}    NOT_NODE:{child}\n"
		return result

	def get_string_value_repr(self):
		return self.value

class ValueNode(ASTNode):
	"""RValue node abstract"""
	def __init__(self, nodetype, children=None, value=None):
		super().__init__(nodetype, children, value)
		self.typename:TypeNameSpec = TypeNameSpec('any')

class LiteralNode(ValueNode):
	"""Literal value (int,string etc...)"""
	def __init__(self, value):
		super().__init__('Lit', value=value)
		self.typename = TypeNameSpec('any')
	
	def get_string_value_repr(self):
		return f"({self.typename}){super().get_string_value_repr()}"

class TypeNameSpec:
	def __init__(self, typename):
		self.stringRepr = typename

	def __repr__(self):
		return self.stringRepr

class IdentifierNode(ValueNode):
	"""Identifier container (local,global,func)"""
	class Type(enum.Enum):
		UNKNOWN = 0
		LOCAL_VARIABLE = 1
		GLOBAL_VARIABLE = 2
		GLOBAL_FUNCTION = 3

		def __repr__(self):
			return f"ID_T_{self.name}"

	def __init__(self, name):
		super().__init__('Ident', value=name)
		self.identType = IdentifierNode.Type.UNKNOWN
		if name.startswith('_'):
			self.identType = IdentifierNode.Type.LOCAL_VARIABLE

	def get_string_value_repr(self):
		return f"[{self.identType.name}] {self.typename} {super().get_string_value_repr()}"

class AssignmentNode(ASTNode):
	def __init__(self, target, expression):
		super().__init__('Assign', children=[target, expression])