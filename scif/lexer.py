import ply.lex as lex

"""
	For example tokenize see:
		https://github.com/eliben/pycparser/blob/main/pycparser/c_lexer.py
		https://github.com/Prabhat-Deshmukh022/Typescript_lexer_parser/blob/main/Yacc_Code.py


"""

reserved = {
	'if': 'IF',
	'else': 'ELSE',
	'then': 'THEN',
	'exitwith': 'EXITWITH',
	'while': 'WHILE',
	'do': 'DO',
	'for': 'FOR',
	'in': 'IN',
	'break': 'BREAK',
	'continue': 'CONTINUE',
}

conditions_symbols = (
	'LT','GT','LTE','GTE','EQUALV','EQUALVT','NOTEQUALV','NOTEQUALVT','OR','AND'
)

t_LT = r'<'
t_GT = r'>'
t_LTE = r'<='
t_GTE = r'>='
t_EQUALV = r'==' 
t_NOTEQUALV = r'!='
t_AND=r'&&'
t_OR=r'\|\|'

tokens = (
	#preprocessor
	'PP_COMMENT_LINE',
	'PP_COMMENT_BLOCK',
	'PP_DIRECTIVE',
	'PP_IF',
	'PP_ELSE',
	'PP_ENDIF',

	#regular
	'IDENT',
	'NUMBER',
	'STRING',
	"BOOLEAN",
	'NULAR_OP',
	'UNARY_OP',
	'BINARY_OP',
	
	#'ASSIGN',
	'SEMICOLON',
	'OPEN_PAREN',
	'CLOSE_PAREN',
	'OPEN_BRACKET',
	'CLOSE_BRACKET',
	'OPEN_BRACE',
	'CLOSE_BRACE',
	
	) + tuple(reserved.values()) + conditions_symbols


literals = '();={}:!,[]'

states = (
	('string', 'inclusive'),
)

t_ignore = ' \t\r'
t_PP_COMMENT_LINE = r'//.*'
t_PP_COMMENT_BLOCK = r'/\*.*\*/'

def t_PP_DIRECTIVE(t):
	r'\#(include|define|undef)'
	t.type = t.value.upper()
	return t



# t_ASSIGN = r'='
t_SEMICOLON = r';'
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_OPEN_BRACKET = r'\['
t_CLOSE_BRACKET = r'\]'
t_OPEN_BRACE = r'\{'
t_CLOSE_BRACE = r'\}'

def t_BOOLEAN(t):
	r'(true|false)'
	return t

def t_IDENT(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.type = reserved.get(t.value, 'IDENT')
	return t

def t_NUMBER(t):
	r'(((\$|0x)[0-9a-fA-F]+)|(\.[0-9]+))|(\b[0-9]+(\.[0-9]+|[eE][-+]?[0-9]+)?)\b'
	#t.value = float(t.value)
	return t

def t_STRING(t):
	r'[\"\']'
	t.lexer.push_state('string')
	t.lexer.string_start = t.lexpos

def t_string_chars(t):
	r'[^"\'\n]+'

def t_string_end(t):
	r'[\"\']'
	t.lexer.pop_state()
	t.type = 'STRING'
	t.value = t.lexer.lexdata[t.lexer.string_start+1:t.lexpos]
	return t

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

lexer = lex.lex(reflags=lex.re.UNICODE | lex.re.DOTALL)

if __name__ == '__main__':
	import os
	with open(os.path.dirname(__file__) + '\\input.txt') as f:
		input = f.read()
	lexer.input(input)

	tokens = []
	while True:
		tok = lexer.token()
		if not tok: break
		tokens.append(tok)
		print(tok)

