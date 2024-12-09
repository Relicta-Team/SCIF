from lexer import lexer,tokens
import ply.yacc as yacc

p_start = 'program'

def p_program(p):
	'''program : VAR_DEF IDENT ASSIGN NUMBER SEMICOLON 
			   | VAR_DEF IDENT ASSIGN NUMBER SEMICOLON program
	'''
	#p[0] = p[2]
	#print(f'{p[1]} {p[2]} = {p[4]}')
	#todo tokenize

def p_error(p):
	print(f"Syntax error in input! Unexpected token: {p.value} ({p.type}) at line {p.lineno};")

parser = yacc.yacc()


def generateAST(input):
	return parser.parse(input)

if __name__ == '__main__':
	import os
	with open(os.path.dirname(__file__) + '\\input.txt') as f:
		input = f.read()
	generateAST(input)