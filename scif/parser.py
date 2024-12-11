from lexer import lexer,tokens
import ply.yacc as yacc

# https://community.bistudio.com/wiki/Operators


from ast_lang import *

start = 'prog'

def p_prog(p):
	'''prog : statements
	'''
	p[0] = p[1]

def p_statement(p):
	# todo add control_structures, code_block, use '(', ')' for condition
	'''statement : assignment
				 | expression
	'''
	p[0] = p[1]

def p_statements(p):
	'''statements : statement
				  | statement SEMICOLON statements
				  | empty
	'''
	if len(p) > 2:
		p[0] = [p[1]] + p[3] if p[3]!= None else []
		pass
	else:
		if p[1] != None:
			p[0] = p[1]
	

def p_expression(p):
	'''expression : literal
				  | IDENT
	'''
	p[0] = ('rvalue', p[1])


def p_assignment(p):
	'''assignment : IDENT '=' expression
	'''
	p[0] = ('set_glob', p[1], p[3])

def p_literal(p):
	'''literal : NUMBER
			   | STRING
			   | BOOLEAN
	'''
	p[0] = p[1]

def p_error(p):
	print(f"Syntax error in input! Unexpected token: {p.value} ({p.type}) at line {p.lineno};")

def p_empty(p):
	'''empty :
	'''
	pass

parser = None
try:
	import sys
	parser = yacc.yacc(debug=True)
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
		print(astdata)
	except Exception as e:
		print(e)