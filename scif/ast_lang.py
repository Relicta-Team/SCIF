

import enum
import re

class CodeContext:
	def __init__(self,nsDict,commDict):
		self.nsDict = nsDict
		self.commDict = commDict
		# managed comments list
		self.commList = list(commDict.items())
		self.curLine = 1

		self.ignoreNextLines = False
		
		self.vars = {}
		self.scopeStack = []

		self.functionSignatureStack = []
	
	def pushFunctionSignature(self,signature):
		self.functionSignatureStack.append(signature)
	def popFunctionSignature(self):
		assert len(self.functionSignatureStack) > 0
		self.functionSignatureStack.pop()

	def getCurFunctionSignature(self):
		if len(self.functionSignatureStack) == 0: return None
		return self.functionSignatureStack[-1]

	def addVar(self,varnode):
		assert len(self.vars) > 0
		self.vars[self.scopeStack[-1]][varnode.value] = varnode

	def pushScope(self,scopeNode):
		self.scopeStack.append(scopeNode)
		self.vars[scopeNode] = {}
	
	def popScope(self):
		assert len(self.scopeStack) > 0
		curScope = self.scopeStack.pop()
		self.vars.pop(curScope)

	def scopeIsEmpty(self):
		return len(self.scopeStack) == 0

	def getVarByName(self,name):
		for scopeName,vars in reversed(self.vars.items()):
			if name in vars:
				return vars[name]
		return None


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

	def getCalculatedType(self):
		return TypeNameSpec("any")

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
	
	def __checks_handlecomments(self,diff,codeCtx:CodeContext):
		if codeCtx.commList and codeCtx.commList[0][0] < self.lineno:
			# create generator
			start = self.lineno - diff
			end = self.lineno
			stack = []
			i = start
			while i < end:
				if not codeCtx.commList:
					stack.append("\n")
					i += 1
					continue
				cline,cval = codeCtx.commList[0]
				if cline == i:
					codeCtx.commList.pop(0)
					if cval.startswith("/*"):
						stack.append(cval)
						i += cval.count("\n")
						continue
					if cval.startswith("//"):
						stack.append(cval)
						stack.append("\n")
						i += 1
						continue
				else:
					stack.append("\n")
					i += 1
			return ''.join(stack)
		return '\n' * diff

	def _getNextLines(self,codeCtx:CodeContext):
		if codeCtx.ignoreNextLines: return ""
		# TODO add ident for all codeblocks here??..
		"""Must be called only once per node"""
		diff = self._checkLine(codeCtx)
		if diff > 0:
			if codeCtx.commList and codeCtx.commList[0][0] < self.lineno:
				return self.__checks_handlecomments(diff,codeCtx)
			else:
				return '\n' * diff
		else:
			return ""

	def getFirstInside(self,codeCtx:CodeContext,optPredicate=None,deleteOnFound=False):
		if optPredicate is None: return None
		for t in tuple(self.children):
			if optPredicate(t):
				if deleteOnFound: self.children.remove(t)
				return t
			else:
				cx = t.getFirstInside(codeCtx,optPredicate,deleteOnFound)
				if cx is not None: return cx
		return None
	
	def getAllInside(self,codeCtx:CodeContext,optPredicate=None,deleteOnFound=False):
		if optPredicate is None: return []
		result = []
		for t in tuple(self.children):
			if optPredicate(t):
				result.append(t)
				if deleteOnFound: self.children.remove(t)
			else:
				result.extend(t.getAllInside(codeCtx,optPredicate))
		return result
	
	def removeNode(self,codeCtx:CodeContext,refNode):
		for t in tuple(self.children):
			if t == refNode:
				self.children.remove(t)
			else:
				t.removeNode(codeCtx,refNode)
		return
class ValueNode(ASTNode):
	"""RValue node abstract"""
	def __init__(self, nodetype, lineNum, children=None, value=None):
		super().__init__(nodetype,lineNum, children, value)
		self.typename:TypeNameSpec = TypeNameSpec('any')

	def getCalculatedType(self):
		return self.typename

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
	
	def __eq__(self, value):
		if value is None: return False
		if isinstance(value, TypeNameSpec):
			value = value.stringRepr
		return self.stringRepr == value
	def __ne__(self, value):
		return not self.__eq__(value)
	
	def getFunctionSignatureParams(self):
		firstParen = self.stringRepr.find("(")
		if firstParen < 0: raise Exception("Invalid typename: " + self.stringRepr)
		paramsSign = self.stringRepr[firstParen+1:-1].split(";")
		return paramsSign

	def getReturnType(self):
		firstParen = self.stringRepr.find("(")
		if firstParen < 0: raise Exception("Invalid typename: " + self.stringRepr)
		return self.stringRepr[:firstParen]

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
		self.formatter = "{value}"
		if name.startswith('_'):
			self.identType = IdentifierNode.Type.LOCAL_VARIABLE
		else:
			self.identType = IdentifierNode.Type.GLOBAL_VARIABLE

	def get_string_value_repr(self):
		return f"[{self.identType.name}] {self.typename} {super().get_string_value_repr()}"
	
	def getCode(self,codeCtx:CodeContext):
		val = self.value
		if self.identType == IdentifierNode.Type.LOCAL_VARIABLE:
			varDecl = codeCtx.getVarByName(val)
			if varDecl is None:
				raise Exception(f"Unknown variable: {val} at line: {self.lineno}")
		if self.identType == IdentifierNode.Type.LOCAL_VARIABLE and val.startswith("_"):
			val = val[1:]
		val = self.formatter.format(value=val)
		return self._getNextLines(codeCtx) + val

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

		#if isinstance(rval, LiteralNode):
		ident.typename = rval.getCalculatedType()
		
		if self.assignType == AssignmentNode.AssignType.LV_INIT:
			codeCtx.addVar(ident)
			ident.formatter = "let {value}"
			#if ident.typename != "any":
			ident.formatter += f': {ident.typename}'
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
		if self._isSingleStatement(cbIf):
			cbIf = cbIf.children[0] # one-statement implicit block
		if len(self.children) == 2:
			return f"{nl}if {ifCond.getCode(codeCtx)} {cbIf.getCode(codeCtx)}"
		cbEl = self.children[2]
		if self._isSingleStatement(cbEl):
			cbEl = cbEl.children[0] # one-statement implicit block
		
		return f"{nl}if {ifCond.getCode(codeCtx)} {cbIf.getCode(codeCtx)} else {cbEl.getCode(codeCtx)}"

	def _isSingleStatement(self,block):
		return isinstance(block,CodeBlock) and \
			len(block.children) == 1 and \
			(
				not isinstance(block.children[0],IfNode) and 
				not isinstance(block.children[0],ExitWithNode)
			)

class ExitWithNode(ASTNode):
	def __init__(self, lineNum, condition,exit):
		super().__init__('ExitWith', lineNum, children=[condition,exit])
		self.markExitWith = None

	def isMarkedExitWith(self):
		return self.markExitWith

	def getCode(self,codeCtx:CodeContext):
		prefix = f'{self.markExitWith}: ' if self.isMarkedExitWith() else ''
		return f"{self._getNextLines(codeCtx)}{prefix}if {self.children[0].getCode(codeCtx)} {self.children[1].getCode(codeCtx)}"

class CodeBlock(ASTNode):
	"""children is a list of statements"""
	def __init__(self, lineNum, statements, closeLineNum=-1):
		super().__init__('CodeBlock', lineNum, children=statements)
		self.lineno_closer = closeLineNum

	def getCode(self,codeCtx:CodeContext):
		codes = self._getNextLines(codeCtx) +"{"
		for x in self.children:
			codes += x.getCode(codeCtx) + ";"
		diffLines = (self.lineno_closer - self.lineno) - codes.count('\n')
		codeCtx.curLine += diffLines # делаем смещение чтобы логика некстлайнов не сломалась
		return codes + ("}" if diffLines <= 0 else ('\n'*diffLines)+"}")

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
	

class FunctionDeclaration(ASTNode):
	def __init__(self, lineNum, name, block):
		super().__init__('FunctionDecl', lineNum, children=[name,block])

	def getCode(self,codeCtx:CodeContext):
		n = self.getFirstInside(codeCtx,lambda node: node.nodetype == 'Params',True)
		if n is None: raise Exception(f"Function declaration must have params at line: {self.lineno}")
		if len(n.children) > 1: raise Exception(f"Function declaration must have only one param at line: {self.lineno}")

		ptypes = self.children[0].typename.getFunctionSignatureParams()
		baseNL = self._getNextLines(codeCtx)
		
		pnames = n.children[0]
		pbuilder = []
		if len(ptypes) != len(pnames.children): raise Exception(f"Function param/signature error: p {len(pnames.children)}; s {len(ptypes)} at line: {self.lineno}")
		
		codeCtx.pushScope(self.children[1])
		
		#params preparing
		for i,pname in enumerate(pnames.children):
			defVal = None
			if isinstance(pname,ArrayConstant):
				if len(pname.children) != 2: raise Exception(f"Function decl error: param with default value must be 2-size array; line {self.lineno}")
				dvalNode =  pname.children[1]
				codeCtx.ignoreNextLines = True
				defVal = dvalNode.getCode(codeCtx)
				codeCtx.ignoreNextLines = False
				pname = pname.children[0]
			if pname.typename != "string": raise Exception(f"Function params must be strings at line: {self.lineno}")
			if not pname.value.startswith("_"): raise Exception(f"Function params must start with _ at line: {self.lineno}")
			curType = ptypes[i]
			curParam = [pname.value[1:],': ',curType]
			if defVal is not None:
				curParam.append(' = ')
				curParam.append(defVal)
			pbuilder.append(''.join(curParam))
			
			codeCtx.addVar(IdentifierNode(self.children[0].lineno,pname.value))
		
		functionSignature = self.children[0].typename
		freturn = functionSignature.getReturnType()
		codeCtx.pushFunctionSignature(functionSignature)
		self.prepBody(codeCtx)
		funcCode = f"{baseNL}function {self.children[0].getCode(codeCtx)}({', '.join(pbuilder)}): {freturn} {self.children[1].getCode(codeCtx)}"
		codeCtx.popScope()
		codeCtx.popFunctionSignature()
		assert codeCtx.scopeIsEmpty()
		
		return funcCode
	
	def prepBody(self,codeCtx:CodeContext):
		assert len(self.children) > 1
		rootBlock:CodeBlock = self.children[1]
		def __visit(node:CodeBlock,scopeLevel:int=0):
			lastIdx = len(node.children)-1
			for i,x in enumerate(node.children):
				if isinstance(x,ExitWithNode):
					if scopeLevel > 0:
						x.markExitWith = f'label_{scopeLevel}'
					__visit(x.children[1],scopeLevel+1)
				if isinstance(x,IfNode):
					for cbInternal in x.children:
						if isinstance(cbInternal,CodeBlock):
							__visit(cbInternal,scopeLevel+1) 
				if i == lastIdx:
					if scopeLevel <= 1:
						if any((isinstance(x,_tSTMT) for _tSTMT in self.__returnableStatements)): 
							node.children[i] = ReturnStatement(x.lineno,x)
					else:
						node.children.append(BreakScope_exitwithStatement(x.lineno,f'label_{scopeLevel-1}'))
		__visit(rootBlock)

	__returnableStatements = [GroupedExpression,ValueNode]

class ReturnStatement(ASTNode):
	def __init__(self, lineNum, value):
		super().__init__('Return', lineNum, children=[value])

	def getCode(self,codeCtx:CodeContext):
		return f"{self._getNextLines(codeCtx)}return {self.children[0].getCode(codeCtx)}"

class BreakScope_exitwithStatement(ASTNode):
	def __init__(self, lineNum, value):
		super().__init__('lbl_exit', lineNum, children=[value])

	def getCode(self,codeCtx:CodeContext):
		return f"{self._getNextLines(codeCtx)}break {self.children[0]}"

class ArrayConstant(ASTNode):
	def __init__(self, lineNum, values):
		super().__init__('Array', lineNum, children=values)

	def getCode(self,codeCtx:CodeContext):
		return f"[{','.join([x.getCode(codeCtx) for x in self.children])}]"
	
class ParamsDecl(ASTNode):
	def __init__(self, lineNum, pnames, leftval=None):
		params = [pnames]
		if leftval is not None:
			params.append(leftval)
		super().__init__('Params', lineNum, children=params)

	def getCode(self,codeCtx:CodeContext):
		return f"PARAMS({','.join([x.getCode(codeCtx) for x in self.children])})"