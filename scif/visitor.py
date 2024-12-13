import re
from ast_lang import *

def visit_global(programm,debugPrint=False):
	curLine = 1
	if not isinstance(programm, ASTNode) or programm.nodetype != 'Program':
		raise Exception("Programm must be of type Program")
	


