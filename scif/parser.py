from lexer import lexer,tokens
import ply.yacc as yacc
import re
from visitor import visit_global
from native_commands import nativeAssocRefs,prepareNativeCommands


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
	p[0] = ASTNode('Program', 0, children=p[1])

def p_statement(p):
	# todo add control_structures, code_block, use '(', ')' for condition
	'''statement : moduleMemberDeclare
				 | expression
				 | assignment
	'''
	p[0] = p[1]

def p_controlStructuresRValue(p):
	'''controlStructuresRValue : ifStructure
							   | paramsDecl	   
	'''
	# | expression IDENT expression
	# | IDENT expression
	# | IDENT
	if len(p) == 4:
		raise Exception("Binary commands not implemented")
	elif len(p) == 3:
		raise Exception("Unary commands not implemented")
		pass #unary cmd
	elif len(p) == 2 and p.slice[1].type == 'IDENT':
		raise Exception("Nular commands not implemented")
		pass #nullar cmd
	else:
		p[0] = p[1]

def p_paramsDecl(p):
	'''paramsDecl : PARAMS arrayConstant
				  | expression PARAMS arrayConstant
	'''
	if len(p) == 3:
		p[0] = ParamsDecl(p.slice[1].lineno, p[2])
	else:
		p[0] = ParamsDecl(p.slice[2].lineno, p[3], p[1])

def p_ifStructure(p):
	# | whileStructure
	# 					 | forStructure
	# 					 | foreachStructure 
	'''ifStructure : IF expression THEN codeBlock
	               | IF expression THEN codeBlock ELSE codeBlock
	'''
	if len(p) == 5:
		p[0] = IfNode(p.slice[1].lineno, p[2], p[4])
	else:
		p[0] = IfNode(p.slice[1].lineno, p[2], p[4], p[6])

def p_codeBlock(p):
	'''codeBlock : OPEN_BRACE statements CLOSE_BRACE
	'''
	p[0] = CodeBlock(p.slice[1].lineno, p[2])

def p_namespaceDeclare(p:yacc.YaccProduction):
	'''namespaceDeclare : NAMESPACESPEC
	'''
	mtch = re.match(r'namespace\((\w+)\s*,\s*([\w;]+)\)',p[1])
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
				  | controlStructuresLValue SEMICOLON statements
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
				  | controlStructuresRValue
				  | arrayConstant
	'''
	if len(p) == 4:
		p[0] = GroupedExpression(p.slice[1].lineno, p[2])
	else:
		if isinstance(p[1], str):  # Если идентификатор
			p[0] = IdentifierNode(p.slice[1].lineno, p[1])
		else:  # Если литерал
			p[0] = p[1]

def p_arrayConstant(p):
	'''arrayConstant : OPEN_BRACKET arrayValueList CLOSE_BRACKET
					 | OPEN_BRACKET CLOSE_BRACKET
	'''
	if len(p) == 4:
		p[0] = ArrayConstant(p.slice[1].lineno, p[2])
	else:
		p[0] = ArrayConstant(p.slice[1].lineno, [])

def p_arrayValueList(p):
	'''arrayValueList : expression
					  | expression ',' arrayValueList
	'''
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = [p[1]] + p[3]

def p_controlStructuresLValue(p):
	'''controlStructuresLValue : whileStructure
							   | forStructure
							   | foreachStructure
	'''
	p[0] = p[1]

def p_whileStructure(p): #* в проде нигде не передается значение или ссылка на код в condition-блоке
	'''whileStructure : WHILE codeBlock DO codeBlock
	'''
	p[0] = WhileNode(p.slice[1].lineno, p[2], p[4])

def p_forStructure(p):
	'''forStructure : FOR STRING FROM expression TO expression DO codeBlock
					| FOR STRING FROM expression TO expression STEP expression DO codeBlock
	'''
	forVar = LiteralNode(p.slice[2].lineno, p[2])
	forVar.typename = TypeNameSpec('int')
	if len(p) == 9:
		p[0] = ForNode(p.slice[1].lineno, forVar, p[4], p[6], p[8])
	else:
		p[0] = ForNode(p.slice[1].lineno, forVar, p[4], p[6], p[8], p[10])

def p_foreachStructure(p):
	'''foreachStructure : codeBlock FOREACH expression
	'''
	p[3].lineno = p[1].lineno
	p[0] = ForeachNode(
		#p.slice[1].lineno
		p[1].lineno
		, p[3], p[1])

def p_assignment(p):
	'''assignment : IDENT '=' expression
				  | LVDECLARE IDENT '=' expression
	'''
	if len(p) == 4:
		target = IdentifierNode(p.slice[1].lineno, p[1])
		exp = p[3]
		p[0] = AssignmentNode(p.slice[2].lineno, target, exp)
	else:
		target = IdentifierNode(p.slice[2].lineno, p[2])
		target.identType = IdentifierNode.Type.LOCAL_VARIABLE
		exp = p[4]
		p[0] = AssignmentNode(p.slice[3].lineno, target, exp)
		p[0].assignType = AssignmentNode.AssignType.LV_INIT
	# if isCompileContext:
	# 	if isinstance(exp, LiteralNode):
	# 		target.typename = exp.typename
	# 	target.identType = IdentifierNode.Type.GLOBAL_VARIABLE
	# 	p[0].assignType = AssignmentNode.AssignType.GV_INIT


def p_moduleMemberDeclare(p):
	'''moduleMemberDeclare : moduleVarDeclare
						   | moduleFuncDeclare
	'''
	p[0] = p[1]

def p_moduleVarDeclare(p):
	'''moduleVarDeclare : DECLSPEC assignment
	'''
	identObj:IdentifierNode = p[2][0]
	identObj.identType = IdentifierNode.Type.GLOBAL_VARIABLE
	identObj.typename = TypeNameSpec(p[1][5:-1])
	p[2].assignType = AssignmentNode.AssignType.GV_INIT
	p[0] = p[2]

def p_moduleFuncDeclare(p):
	'''moduleFuncDeclare : DECLSPEC IDENT '=' codeBlock
	'''
	identName = IdentifierNode(p.slice[2].lineno, p[2])
	identName.identType = IdentifierNode.Type.GLOBAL_VARIABLE
	identName.typename = TypeNameSpec(p[1][5:-1])
	p[0] = FunctionDeclaration(p.slice[2].lineno, identName, p[4])

def p_literal(p):
	'''literal : NUMBER
			   | STRING
			   | BOOLEAN
	'''
	p[0] = LiteralNode(p.slice[1].lineno, p[1])
	ptype = p.slice[1].type
	if ptype == 'NUMBER':
		p[0].typename = TypeNameSpec('float')
	elif ptype == 'STRING':
		p[0].typename = TypeNameSpec('string')
	elif ptype == 'BOOLEAN':
		p[0].typename = TypeNameSpec('bool')

# def p_PP_COMMENTBLOCK(p):
# 	'''prog : ppAnyComment
# 	   statement : ppAnyComment statement
# 	   | statement ppAnyComment
# 	   expression : ppAnyComment expression
# 	   | expression ppAnyComment
# 	   literal : ppAnyComment literal
# 	   | literal ppAnyComment
# 	'''
# 	p[0] = p[1]
# 	pass

# def p_ppAnyComment(p):
# 	'''ppAnyComment : PP_COMMENTBLOCK
# 					| PP_COMMENTLINE
# 	'''
# 	p[0] = p[1]

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
					#debuglog=logging.getLogger(),
					
					)
except Exception as e:
	print(f"PARSER GENERAION ERROR: {e}")
	exit()


def generateAST(input):
	return parser.parse(input)

if __name__ == '__main__':
	import os
	
	# prepareNativeCommands()
	with open(os.path.dirname(__file__) + '\\input.txt') as f:
		input = f.read()
	try:
		astdata = generateAST(input)
		print(f"NS_INFO: {globNamespaceDecl}")
		print(astdata.pretty_print())
		print("\n" + ("*" * 30))
		ctx = CodeContext(globNamespaceDecl,lexer.commentsDict)
		print( '\n'.join( [f'L{ind+1}: {lin}' for ind, lin in enumerate(astdata.getCode(ctx).split("\n"))] ) )
		#visit_global(astdata,debugPrint=True)
	except Exception as e:
		print(e.with_traceback(e.__traceback__))