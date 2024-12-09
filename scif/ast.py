


class Node:
	def __init__(self, value):
		self.value = value

	def __repr__(self):
		return str(self.value)

	def __str__(self):
		return str(self.value)
	
	def __add__(self, other):
		return Node(self.value + other.value)