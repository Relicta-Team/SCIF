

import enum
import re

class CodeContext:
	def __init__(self,nsDict):
		self.nsDict = nsDict

class ASTNode:
	def __init__(self, nodetype, children=None, value=None):
		self.nodetype = nodetype
		self.children = children if children else []
		self.value = value

		self.lineno = -1 #-1 is system node

	def setLineNumber(self,num):
		self.lineno = num

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
	
	def getCode(self,codeCtx:CodeContext=None):
		if self.value is not None:
			return ""
		result = ""
		for child in self.children:
			if child is None: continue
			if isinstance(child, ASTNode):
				result += child.getCode(codeCtx) + ";" #because program is statement based
			else:
				result += f"{child}"
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
	
	def getCode(self,codeCtx:CodeContext=None):
		return self.value

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
	
	def getCode(self,codeCtx:CodeContext):
		return self.value

class AssignmentNode(ASTNode):
	def __init__(self, target, expression):
		super().__init__('Assign', children=[target, expression])

	def getCode(self,codeCtx:CodeContext):
		ident = self.children[0]
		rval = self.children[1]
		return f"{ident.getCode(codeCtx)} = {rval.getCode(codeCtx)}"


class IfNode(ASTNode):
	def __init__(self, condition, true_block, false_block=None):
		codes = [condition,true_block]
		if false_block is not None:
			codes.append(false_block)
		super().__init__('If', children=codes)

	def getCode(self,codeCtx:CodeContext):
		cbIf = self.children[1]
		if isinstance(cbIf, CodeBlock) and len(cbIf.children) == 1:
			cbIf = cbIf.children[0]
		if len(self.children) == 2:
			return f"if {self.children[0].getCode(codeCtx)} {cbIf.getCode(codeCtx)}"
		cbEl = self.children[2]
		if isinstance(cbEl, CodeBlock) and len(cbEl.children) == 1:
			cbEl = cbEl.children[0]
		return f"if {self.children[0].getCode(codeCtx)} {cbIf.getCode(codeCtx)} else {cbEl.getCode(curline)}"


class CodeBlock(ASTNode):
	"""children is a list of statements"""
	def __init__(self, statements):
		super().__init__('CodeBlock', children=statements)

	def getCode(self,codeCtx:CodeContext):
		codes = "{"
		for x in self.children:
			codes += x.getCode(codeCtx) + ";"
		return codes + "}"

class GroupedExpression(ASTNode):
	def __init__(self, expression):
		super().__init__('GroupExpr', children=[expression])

	def getCode(self,codeCtx:CodeContext):
		return f"({self.children[0].getCode(codeCtx)})"