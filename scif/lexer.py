import ply.lex as lex
import re
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
	'from': 'FROM',
	'to': 'TO',
	'step': 'STEP',
	'foreach': 'FOREACH',
	'in': 'IN',
	'break': 'BREAK',
	'continue': 'CONTINUE',
	"private": "LVDECLARE",
	"params": "PARAMS",
}

langSpec = (
	"NAMESPACESPEC",
	"DECLSPEC",
	"ENUMSPEC",
	"INLINEMACROSPEC",
	"CONSTSPEC",
	"MACROCONSTSPEC",
)

conditions_symbols = (
	'LT','GT','LTE','GTE','EQUALV','EQUALVT','NOTEQUALV','NOTEQUALVT','OR','AND'
)

math_symbols = (
	'PLUS','MINUS','MUL','DIV','MOD','POWER'
)

t_LT = r'<'
t_GT = r'>'
t_LTE = r'<='
t_GTE = r'>='
t_EQUALV = r'==' 
t_NOTEQUALV = r'!='
t_AND=r'&&'
t_OR=r'\|\|'

t_PLUS = r'\+'
t_MINUS = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_POWER = r'\^'

tokens = (
	#preprocessor
	'PP_COMMENTLINE',
	'PP_COMMENTBLOCK',
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
	
	) + tuple(reserved.values()) + conditions_symbols + math_symbols + langSpec


literals = '();={}:!,[]'

states = (
	('string', 'inclusive'),
	('declspec', 'inclusive'),
)

t_ignore = ' \t\r'
def t_PP_COMMENTLINE(t): 
	r'((//.*?)(\n|$))'
	regx = re.match(r'((//.*?)(\n|$))',t.value)
	t.value = regx.group(2)
	t.lexer.commentsDict[t.lineno] = t.value
	if regx.group(3) == '\n':
		t.lexer.lineno += 1
	#return t
def t_PP_COMMENTBLOCK(t): 
	#r'\/\*.*\*\/'
	r'(/\*(.|\n)*?\*/)'
	ncr = t.value.count("\n")
	t.lexer.commentsDict[t.lineno] = t.value
	t.lexer.lineno += ncr
	#return t

def t_PP_DIRECTIVE(t):
	r'\#(include|define|undef)'
	t.type = t.value.upper()
	return t


def t_NAMESPACESPEC(t):
	r'namespace\([a-zA-Z_][a-zA-Z0-9_]*\s*\,\s*[a-zA-Z_][a-zA-Z0-9_;]*\)'
	return t

def t_DECLSPEC(t):
	r'decl\('
	t.lexer.push_state('declspec')
	t.lexer.declspec_start = t.lexpos
	#return t

def t_declspec_oparen(t):
	r'\('
	t.lexer.push_state('declspec')
def t_declspec_chars(t):
	r'[^\(\)]'

def t_declspec_end(t):
	r'[\)]'
	
	t.lexer.pop_state()
	if t.lexer.current_state() == 'INITIAL':
		t.type = 'DECLSPEC'
		t.value = t.lexer.lexdata[t.lexer.declspec_start:t.lexpos+1]
		return t

def t_ENUMSPEC(t):
	r'enum\([a-zA-Z_][a-zA-Z0-9_]*\s*\,\s*[a-zA-Z_][a-zA-Z0-9_]*\)'
	return t

def t_INLINEMACROSPEC(t):
	r'\binline_macro\b'
	return t

def t_CONSTSPEC(t):
	r'\bconst\b'
	return t

def t_MACROCONSTSPEC(t):
	r'\bmacro_const\([a-zA-Z_][a-zA-Z0-9_]*\s*\,\s*[a-zA-Z_][a-zA-Z0-9_]*\)'
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
	t.type = reserved.get(t.value.lower(), 'IDENT')
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
	print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
	t.lexer.skip(1)

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

lexer = lex.lex(reflags=lex.re.UNICODE | lex.re.DOTALL)
lexer.commentsDict = {}

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

