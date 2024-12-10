


class Node:
	def __init__(self, line):
		self.line = line


#preprocessor 
class Directive(Node):
	pass

class Include(Directive):
	def __init__(self, line, path):
		super().__init__(line, path)

class DefineVar(Directive):
	def __init__(self, line, name, value):
		super().__init__(line)
		self.name = name
		self.value = value

class DefineFunc(Directive):
	def __init__(self, line, name, args, body):
		super().__init__(line)
		self.name = name
		self.args = args
		self.body = body

class Operator(Node):
	def __init__(self, line, opName):
		super().__init__(line)
		self.opName = opName

class NularOp(Operator):
	def __init__(self, line, opName):
		super().__init__(line, opName)

class UnaryOp(Operator):
	def __init__(self, line, opName, expr):
		super().__init__(line, opName)
		self.expr = expr

class BinaryOp(Operator):
	def __init__(self, line, opName, left, right):
		super().__init__(line, opName)
		self.left = left
		self.right = right