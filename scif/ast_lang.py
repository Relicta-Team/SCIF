

class ASTNode:
	def __init__(self, nodetype, children=None, value=None):
		self.nodetype = nodetype
		self.children = children if children else []
		self.value = value

	def __repr__(self):
		if self.value is not None:
			return f"{self.nodetype}({self.value})"
		return f"{self.nodetype}({', '.join(map(str, self.children))})"
	
	def pretty_print(self, indent=0):
		tab = "    " * indent
		if self.value is not None:
			return f"{tab}{self.nodetype}: {self.value}\n"
		result = f"{tab}{self.nodetype}:\n"
		for child in self.children:
			result += child.pretty_print(indent + 1)
		return result

class LiteralNode(ASTNode):
	def __init__(self, value):
		super().__init__('Literal', value=value)

class IdentifierNode(ASTNode):
	def __init__(self, name):
		super().__init__('Identifier', value=name)

class AssignmentNode(ASTNode):
	def __init__(self, target, expression):
		super().__init__('Assignment', children=[target, expression])