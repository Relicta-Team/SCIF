import ply.lex as lex

tokens = (
	'VAR_DEF',
	'IDENT',
	'ASSIGN',
	'NUMBER',
	'SEMICOLON',
	)

t_ignore = ' \t\r'

def t_VAR_DEF(t):
	r'var'
	return t

def t_IDENT(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	return t

def t_ASSIGN(t):
	r'='
	return t

def t_NUMBER(t):
	r'\d+'
	return t

def t_SEMICOLON(t):
	r';'
	return t

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer = lex.lex(reflags=lex.re.UNICODE | lex.re.DOTALL)

if __name__ == '__main__':
	with open('input.txt') as f:
		input = f.read()
	lexer.input(input)

	tokens = []
	while True:
		tok = lexer.token()
		if not tok: break
		tokens.append(tok)
		print(tok)

