

import enum
import re

class CodeContext:
	def __init__(self,nsDict,commDict):
		self.nsDict = nsDict
		self.commDict = commDict
		# managed comments list
		self.commList = list(commDict.items())
		self.curLine = 1

class ASTNode:
	def __init__(self, nodetype, lineNum, children=None, value=None):
		self.nodetype = nodetype
		self.children = children if children else []
		self.value = value

		self.lineno = lineNum #-1 is system node

	def setLineNumber(self,num):
		self.lineno = num

	#overload [] operator
	def __getitem__(self, index):
		return self.children[index]

	def __repr__(self):
		if self.value is not None:
			return f"{self.get_node_type_repr()}({self.value})"
		return f"{self.get_node_type_repr()}({', '.join(map(str, self.children))})"
	
	def pretty_print(self, indent=0):
		tab = "    " * indent
		if self.value is not None:
			return f"{tab}{self.get_node_type_repr()}: {self.get_string_value_repr()}\n"
		result = f"{tab}{self.get_node_type_repr()}:\n"
		for child in self.children:
			if isinstance(child, ASTNode):
				result += (f"L{child.lineno}")
				result += child.pretty_print(indent + 1)
			else:
				result += f"{tab}    NOT_NODE:{child}\n"
		return result
	
	def getCode(self,codeCtx:CodeContext=None):
		if self.value is not None:
			raise Exception(f"Unhandled getCode value condition for ast type: {self.__class__}")
			return ""
		result = self._getNextLines(codeCtx) + ""
		for child in self.children:
			if child is None: continue
			if isinstance(child, ASTNode):
				result += child.getCode(codeCtx) + ";" #because program is statement based
			else:
				result += f"{child}"
		return result

	def get_string_value_repr(self):
		return self.value
	
	def get_node_type_repr(self):
		return self.nodetype

	def _checkLine(self,codeCtx:CodeContext):
		if self.lineno <= 0: return 0
		if self.lineno > codeCtx.curLine:
			diff = self.lineno - codeCtx.curLine
			codeCtx.curLine = self.lineno
			return diff
		return 0
	
	def _getNextLines(self,codeCtx:CodeContext):
		"""Must be called only once per node"""
		diff = self._checkLine(codeCtx)
		if diff > 0:
			if codeCtx.commList:
				cline,cval = codeCtx.commList[0]
				if self.lineno >= cline:
					codeCtx.commList.pop(0)
					if cval.startswith("/*"):
						lastIdx = cline+cval.count("\n") 
						stackNL = []
						for i in range(1,diff+1):
							if i < cline: 
								stackNL.append("\n")
							if i == cline: 
								stackNL.append(cval)
							if i > cline and i <= lastIdx: 
								stackNL.append("")
							if i >= lastIdx: 
								stackNL.append("\n")

						return "".join(stackNL)
					
					if cval.startswith("//"):
						if diff < 2: 
							raise Exception(f"Cannot emplace line comment at {self.lineno}: {cline}")
						origStrNL = '\n' * diff
						return origStrNL[:-1] + cval + '\n'

						# start = origStrNL[:-1]
						#return '\n' * (diff-1) + cval
					
				# unsuported comment type or not a comment
				return '\n' * diff
			else:
				return '\n' * diff
		else:
			return ""

class ValueNode(ASTNode):
	"""RValue node abstract"""
	def __init__(self, nodetype, lineNum, children=None, value=None):
		super().__init__(nodetype,lineNum, children, value)
		self.typename:TypeNameSpec = TypeNameSpec('any')

class LiteralNode(ValueNode):
	"""Literal value (int,string etc...)"""
	def __init__(self, lineNum, value):
		super().__init__('Lit', lineNum, value=value)
		self.typename = TypeNameSpec('any')
	
	def get_string_value_repr(self):
		return f"({self.typename}){super().get_string_value_repr()}"
	
	def getCode(self,codeCtx:CodeContext=None):
		return self._getNextLines(codeCtx) + self.value

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

		def __repr__(self):
			return f"ID_T_{self.name}"

	def __init__(self, lineNum, name):
		super().__init__('Ident', lineNum, value=name)
		self.identType = IdentifierNode.Type.UNKNOWN
		if name.startswith('_'):
			self.identType = IdentifierNode.Type.LOCAL_VARIABLE
		else:
			self.identType = IdentifierNode.Type.GLOBAL_VARIABLE

	def get_string_value_repr(self):
		return f"[{self.identType.name}] {self.typename} {super().get_string_value_repr()}"
	
	def getCode(self,codeCtx:CodeContext):
		return self._getNextLines(codeCtx) + self.value

class AssignmentNode(ASTNode):
	def __init__(self, lineNum, target, expression):
		super().__init__('Assign', lineNum, children=[target, expression])
		self.assignType = AssignmentNode.AssignType.UNKNOWN

	class AssignType(enum.Enum):
		UNKNOWN = 0
		LV_INIT = 1
		LV_ASSIGN = 2
		GV_INIT = 3 # this type used for global var decl
		GV_ASSIGN = 4

	def get_node_type_repr(self):
		return f'{super().get_node_type_repr()} [{self.assignType.name}]'

	def getCode(self,codeCtx:CodeContext):
		ident = self.children[0]
		rval = self.children[1]
		
		return f"{ident.getCode(codeCtx)} {self._getNextLines(codeCtx)}= {rval.getCode(codeCtx)}"


class IfNode(ASTNode):
	def __init__(self, lineNum, condition, true_block, false_block=None):
		codes = [condition,true_block]
		if false_block is not None:
			codes.append(false_block)
		super().__init__('If', lineNum, children=codes)

	def getCode(self,codeCtx:CodeContext):
		
		nl = self._getNextLines(codeCtx)

		ifCond = self.children[0]
		cbIf = self.children[1]
		if isinstance(cbIf, CodeBlock) and len(cbIf.children) == 1:
			cbIf = cbIf.children[0] # one-statement implicit block
		if len(self.children) == 2:
			return f"{nl}if {ifCond.getCode(codeCtx)} {cbIf.getCode(codeCtx)}"
		cbEl = self.children[2]
		if isinstance(cbEl, CodeBlock) and len(cbEl.children) == 1:
			cbEl = cbEl.children[0] # one-statement implicit block
		
		return f"{nl}if {ifCond.getCode(codeCtx)} {cbIf.getCode(codeCtx)} else {cbEl.getCode(curline)}"


class CodeBlock(ASTNode):
	"""children is a list of statements"""
	def __init__(self, lineNum, statements):
		super().__init__('CodeBlock', lineNum, children=statements)

	def getCode(self,codeCtx:CodeContext):
		codes = self._getNextLines(codeCtx) +"{"
		for x in self.children:
			codes += x.getCode(codeCtx) + ";"
		return codes + "}"

class GroupedExpression(ASTNode):
	def __init__(self, lineNum, expression):
		super().__init__('GroupExpr', lineNum, children=[expression])

	def getCode(self,codeCtx:CodeContext):
		return f"{self._getNextLines(codeCtx)}({self.children[0].getCode(codeCtx)})"
	
class GroupedStatement(GroupedExpression):
	def __init__(self, lineNum, statement):
		super().__init__('GroupStmt', lineNum, children=[statement])

class WhileNode(ASTNode):
	def __init__(self, lineNum, condition, block):
		super().__init__('While', lineNum, children=[condition,block])

	def getCode(self,codeCtx:CodeContext):
		return f"{self._getNextLines(codeCtx)}while {self.children[0].getCode(codeCtx)} {self.children[1].getCode(codeCtx)}"
	
class ForNode(ASTNode):
	def __init__(self, lineNum, var, start, end, block, step=None):
		states = [var,start,end,block]
		if step is not None:
			states.append(step)
		super().__init__('For', lineNum, children=states)

	def getCode(self,codeCtx:CodeContext):
		forIter = self.children[0]
		begin = self.children[1]
		end = self.children[2]
		block = self.children[3]
		if len(self.children) == 4:
			return f"{self._getNextLines(codeCtx)}for ({forIter.getCode(codeCtx)}; {begin.getCode(codeCtx)}; {end.getCode(codeCtx)};) {block.getCode(codeCtx)}"
		else:
			step = self.children[4]
			return f"{self._getNextLines(codeCtx)}for ({forIter.getCode(codeCtx)}; {begin.getCode(codeCtx)}; {end.getCode(codeCtx)}; {step.getCode(codeCtx)}) {block.getCode(codeCtx)}"
	
class ForeachNode(ASTNode):
	def __init__(self, lineNum, collection, block):
		super().__init__('Foreach', lineNum, children=[collection,block])

	def getCode(self,codeCtx:CodeContext):
		return f"{self._getNextLines(codeCtx)}foreach {self.children[0].getCode(codeCtx)} {self.children[1].getCode(codeCtx)}"