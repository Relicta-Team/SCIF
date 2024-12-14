from lexer import lexer,tokens
import ply.yacc as yacc
import re
from visitor import visit_global


# https://community.bistudio.com/wiki/Operators


from ast_lang import *

class ParserError(Exception):
	pass

start = 'prog'
globNamespaceDecl = {}

isCompileContext = True

def p_prog(p):
	'''prog : statements
	'''
	p[0] = ASTNode('Program', children=p[1])

def p_statement(p):
	# todo add control_structures, code_block, use '(', ')' for condition
	'''statement : moduleMemberDeclare
				 | expression
				 | assignment
				 | controlStructures
	'''
	p[0] = p[1]

def p_controlStructures(p):
	'''controlStructures : ifStructure
	'''
	p[0] = p[1]

def p_ifStructure(p):
	# | whileStructure
	# 					 | forStructure
	# 					 | foreachStructure 
	'''ifStructure : IF expression THEN codeBlock
	               | IF expression THEN codeBlock ELSE codeBlock
	'''
	if len(p) == 5:
		p[0] = IfNode(p[2], p[4])
	else:
		p[0] = IfNode(p[2], p[4], p[6])

def p_codeBlock(p):
	'''codeBlock : OPEN_BRACE statements CLOSE_BRACE
	'''
	p[0] = CodeBlock(p[2])

def p_namespaceDeclare(p:yacc.YaccProduction):
	'''namespaceDeclare : NAMESPACESPEC
	'''
	mtch = re.match('namespace\((\w+)\s*,\s*([\w;]+)\)',p[1])
	namespaceName = mtch.group(1)
	patternsStartWith = mtch.group(2).split(';')
	if len(globNamespaceDecl) > 0:
		raise ParserError('namespace already declared:')
	globNamespaceDecl["real_name"] = namespaceName
	globNamespaceDecl["prefix_list"] = patternsStartWith
	globNamespaceDecl["line"] = p.lexer.lineno

def p_statements(p):
	'''statements : statement
				  | statement SEMICOLON statements
				  | empty namespaceDeclare statements
				  | empty
	'''
	# ! empty namespaceDeclare statements need fix

	if len(p) > 2:
		p[0] = [p[1]] + p[3]
	elif p[1] is not None:
		p[0] = [p[1]]
	else:
		p[0] = []
	

def p_expression(p):
	'''expression : literal
				  | IDENT
				  | OPEN_PAREN expression CLOSE_PAREN
	'''
	if len(p) == 4:
		p[0] = GroupedExpression(p[2])
	else:
		if isinstance(p[1], str):  # Если идентификатор
			p[0] = IdentifierNode(p[1])
			p[0].setLineNumber(p.lexer.lineno)
		else:  # Если литерал
			p[0] = p[1]


def p_assignment(p):
	'''assignment : IDENT '=' expression
	'''
	target = IdentifierNode(p[1])
	exp = p[3]
	p[0] = AssignmentNode(target, exp)
	p[0].setLineNumber(p.lexer.lineno)
	target.setLineNumber(p.lexer.lineno)
	if isCompileContext:
		if isinstance(exp, LiteralNode):
			target.typename = exp.typename
		target.identType = IdentifierNode.Type.GLOBAL_VARIABLE


def p_moduleMemberDeclare(p):
	'''moduleMemberDeclare : DECLSPEC assignment
	'''
	identObj:IdentifierNode = p[2][0]
	identObj.identType = IdentifierNode.Type.GLOBAL_VARIABLE
	identObj.typename = TypeNameSpec(p[1][5:-1])
	p[0] = p[2]

def p_literal(p):
	'''literal : NUMBER
			   | STRING
			   | BOOLEAN
	'''
	p[0] = LiteralNode(p[1])
	p[0].setLineNumber(p.lexer.lineno)
	ptype = p.slice[1].type
	if ptype == 'NUMBER':
		p[0].typename = TypeNameSpec('float')
	elif ptype == 'STRING':
		p[0].typename = TypeNameSpec('string')
	elif ptype == 'BOOLEAN':
		p[0].typename = TypeNameSpec('bool')

def p_error(p):
	print(f"Syntax error in input! Unexpected token: {p.value} ({p.type}) at line {p.lineno};")

def p_empty(p):
	'''empty :
	'''
	pass

parser = None
try:
	import sys
	#import logging
	#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
	parser = yacc.yacc(debug=True, 
					#debuglog=logging.getLogger()
					)
except Exception as e:
	print(f"PARSER GENERAION ERROR: {e}")
	exit()


def generateAST(input):
	return parser.parse(input)

if __name__ == '__main__':
	import os
	with open(os.path.dirname(__file__) + '\\input.txt') as f:
		input = f.read()
	try:
		astdata = generateAST(input)
		print(f"NS_INFO: {globNamespaceDecl}")
		print(astdata.pretty_print())
		print("\n" + ("*" * 30))
		print(astdata.getCode())
		#visit_global(astdata,debugPrint=True)
	except Exception as e:
		print(e)