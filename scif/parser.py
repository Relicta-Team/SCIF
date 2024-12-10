from lexer import lexer,tokens
import ply.yacc as yacc

from ast_lang import *

start = 'statement'

def p_statement(p):
	'''statement : assignment
				 | expression
	'''
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
	p[0] = ('literal', p[1])

def p_error(p):
	print(f"Syntax error in input! Unexpected token: {p.value} ({p.type}) at line {p.lineno};")

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
		generateAST(input)
	except Exception as e:
		print(e)