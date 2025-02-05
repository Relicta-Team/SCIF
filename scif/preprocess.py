import os
import re

PAT_INLINEMACRO = re.compile(r'\binline_macro\b',re.MULTILINE)
PAT_MACROCONST = re.compile(r'\bmacro_const\((\w+)\)',re.MULTILINE)
PAT_MACROFUNC = re.compile(r'\bmacro_func\((\w+)\,((\(*[^\(\)]*\)*)*)\)',re.MULTILINE)
PAT_DEFINE = re.compile(r'\#\s*define\s*(\w+)(\s*\(([^\)]*)\))?')
PAT_INCLUDE = re.compile(r'\#\s*include\s*(?:\"([\.\\\/\d\w]+)\"|<([\.\\\/\d\w]+)>)')

def normalizePath(path):
	return os.path.realpath(os.path.normpath(path))

def loadAndPreprocess(path,pset):
	path = normalizePath(path)
	if not os.path.exists(path): return (None,None)
	with open(path,encoding='utf-8') as f:
		return preprocessFile(f.read(),path,pset)

def preprocessFile(content,fullpath,pathes=set(),prepDictOut=dict()) -> tuple[str,dict]|tuple[None,None]:
	fullpath = os.path.abspath(fullpath)
	if fullpath in pathes:
		return (None, None)
	pathes.add(fullpath)
	
	prepDict = prepDictOut #key preprocName, value {realName:str, isFunc:bool, params:[], content:str}

	#collect preproc info
	nextMacroConstFunc = ""
	lastMacroDefName = ""
	def nextIsMacroConst(): return nextMacroConstFunc != ""
	nextMacroFunc = {"name":"","signature":""}
	def nextIsMacroFunc(): return nextMacroFunc["name"] != ""
	nextIsInline = False
	
	isPrepprocHandleNextline = False

	def _determineDataType(data):
		if re.match(r'\s*\[\s*-?\s*\d*(\.\d+)?\s*(\s*\,\s*-?\s*\d*(\.\d+)?\s*){1}\]',data): return "vector2"
		if re.match(r'\s*\[\s*-?\s*\d*(\.\d+)?\s*(\s*\,\s*-?\s*\d*(\.\d+)?\s*){2}\]',data): return "vector3"
		if re.match(r'\s*\[\s*-?\s*\d*(\.\d+)?\s*(\s*\,\s*-?\s*\d*(\.\d+)?\s*){3}\]',data): return "vector4"
		if re.match(r"\s*[\'\"]",data): return "string"
		if re.match(r"\s*-?\d+",data): 
			return "float" if "." in data else "int"
		if re.match(r"\s*-?\d+",data): return "number"
		if re.match(r"\s*(true|false)",data,re.IGNORECASE) or re.search(r'(\|\||\&\&)',data): return "bool"
		if re.match(r"\s*null",data,re.IGNORECASE): return "null"
		try:
			executed = eval(data.replace("\n",''))
			if type(executed) == bool: return "bool"
			if type(executed) == int: return "int"
			if type(executed) == float: return "float"
			if type(executed) == str: return "string"
			return "any"
		except:
			return "any"

	def _prepParam(pval):
		if not pval.startswith("_"): 
			return "_" + pval
		return pval

	_skipEnumsPrefixList = []
	for line in content.splitlines():
		if line == '': continue
		if re.match(r'^\s*//',line): continue
		#skip enum
		enumGrp = re.match(r'^\s*enum\s*\(\w+\,(\w+)\)',line)
		if enumGrp:
			if enumGrp.group(1) not in _skipEnumsPrefixList:
				_skipEnumsPrefixList.append(enumGrp.group(1))
			continue

		minc_grp = re.search(PAT_INCLUDE,line)
		if minc_grp:
			pathBase = minc_grp.group(1)
			path = normalizePath(pathBase)
			# join() automatically resolve path (e.g. double dots)
			path = os.path.join(os.path.dirname(fullpath),path)
			_, preprocOut = loadAndPreprocess(path,pathes)
			if not preprocOut:
				print(f'Failed to load \"{path}\" \n\tfrom {fullpath}')
				
				#! exceptions are not allowed, only warn messages
				#raise Exception(f'Failed to load \"{path}\" from {fullpath}')
			continue

		mcst_grp = re.search(PAT_MACROCONST,line)
		if mcst_grp:
			nextMacroConstFunc = mcst_grp.group(1)
			content = content.replace(mcst_grp.group(0),"")
			continue

		mcf_grp = re.search(PAT_MACROFUNC,line)
		if mcf_grp:
			assert mcf_grp.group(0).count("(") == mcf_grp.group(0).count(")"), f'Missmatch macrofunc open/close count {mcf_grp.group(0)}'
			assert "\n" not in mcf_grp.group(0), f'Newline in macrofunc {mcf_grp.group(0)}'

			nextMacroFunc['name'] = mcf_grp.group(1)
			nextMacroFunc['signature'] = mcf_grp.group(2)
			content = content.replace(mcf_grp.group(0),"")
			continue
		
		minl_grp = re.search(PAT_INLINEMACRO,line)
		if minl_grp:
			nextIsInline = True
			#remove inline only after all code is collected
			#content = content.replace(minl_grp.group(0),"")
			continue
		
		mdf_grp = re.search(PAT_DEFINE,line)
		if mdf_grp:
			
			#skip if macro is enum type
			if any((x for x in _skipEnumsPrefixList if mdf_grp.group(1).startswith(x))):
				continue

			if nextIsMacroConst() or nextIsMacroFunc() or nextIsInline:
				ppFunc = mdf_grp.group(1)
				isFunc = False
				paramList = []
				if mdf_grp.group(3):
					isFunc = True
					paramList = mdf_grp.group(3).split(',')
				
				macroContent = line[line.find(mdf_grp.group(0)) + len(mdf_grp.group(0)):]
				if re.search(r'\\\s*$',macroContent):
					macroContent = re.sub(r'\\\s*$',r'',macroContent)
					isPrepprocHandleNextline = True

				lastMacroDefName = ppFunc

				prepDict[ppFunc] = {
					'realName': "-null=realName-",
					'isFunc': isFunc,
					'params': paramList,
					'realParams': [_prepParam(x) for x in paramList],
					'content': macroContent,
					'removable': line,
					"type": "any",
					'defined': fullpath,
					# !"addSemicolon": False, do not add; example: vec2(1,vec2(2,3)) -> [1,[2,3];<<<];
				}
				if nextIsMacroConst():
					prepDict[ppFunc]['pptype'] = "const"
					prepDict[ppFunc]['realName'] = nextMacroConstFunc
					nextMacroConstFunc = ""
					assert len(paramList) == 0, "macro_const cannot be a function with arguments"
				if nextIsMacroFunc():
					prepDict[ppFunc]['pptype'] = "func"
					prepDict[ppFunc]['realName'] = nextMacroFunc['name']
					prepDict[ppFunc]['type'] = nextMacroFunc['signature']
					nextMacroFunc = {"name":"","signature":""}
				if nextIsInline:
					prepDict[ppFunc]['pptype'] = "inline"
					keyNames = set()
					prepDict[ppFunc]['toStringParams'] = keyNames
					for p in paramList:
						if re.search(r'\#'+p+r'\b',macroContent):
							keyNames.add(p)
					nextIsInline = False
				
				continue
			else:
				print("warning: unknown define type: " + line)
		if isPrepprocHandleNextline:
			isPrepprocHandleNextline = re.search(r'\\\s*$',line) != None
			prepDict[lastMacroDefName]['removable'] += '\n' + line
			line = re.sub(r'\\\s*$',r'',line)
			prepDict[lastMacroDefName]['content'] += '\n' + line

	content = re.sub(PAT_INLINEMACRO,'',content)

	# get regex pattern
	pat_allMacroNames = re.compile(r'\b(' + '|'.join(prepDict.keys()) + r')\b')
	iterateMacros = True
	while iterateMacros:
		iterateMacros = False
		for macroName,macroInfo in prepDict.items():
			if macroInfo['pptype'] == "const":
				if macroInfo['isFunc']:
					raise NotImplementedError('macro function not implemented')
					content = content.replace(macroInfo['removable'],macroInfo['content'] + ";")
				# replace header
				dtype = _determineDataType(macroInfo['content'])
				if dtype == "any":
					raise Exception(f"invalid macro type: {macroInfo['content']}")
				content = content.replace(macroInfo['removable'],f"const decl({dtype}) {macroInfo['realName']} = {macroInfo['content']};")

				content = re.sub(r'\b'+macroName+r'\b',macroInfo['realName'],content)
			elif macroInfo['pptype'] == "inline":
				content = content.replace(macroInfo['removable'],"")
				if macroInfo['isFunc']:
					while True:
						macGrp = re.search(r'\b'+macroName+r'\(',content)
						if not macGrp: break
						start,end = macGrp.span()
						paramList = []
						scopes = 1
						for let in list(content[end:]):
							if let == "(":
								scopes += 1
								paramList[-1] += let
							elif let == ")":
								scopes -= 1
								if scopes == 0:
									break
								paramList[-1] += let
							elif let == ',' and scopes == 1:
								paramList.append('')
								pass
							else:
								if not paramList: paramList.append('')
								paramList[-1] += let
						# handle macro with paramcount
						assert len(paramList) == len( macroInfo['params'])

						baseStruct = macroInfo['content']
						for i,parDat in enumerate(paramList):
							parName = macroInfo['params'][i]
							parToString = parName in macroInfo['toStringParams']
							if parToString:
								baseStruct = re.sub(r'\#'+parName+r'\b',"\""+parDat+"\"",baseStruct)
							else:
								baseStruct = re.sub(r'\b'+parName+r'\b',parDat,baseStruct)
						#replace macro content
						content = content.replace(f"{macGrp.group(0)}{','.join(paramList)})",baseStruct)
				else:
					content = re.sub(r'\b' + macroName + r'\b',macroInfo['content'],content)
				# post check if inside macro
				#if re.search(pat_allMacroNames,content):
				#	iterateMacros = True
			elif macroInfo['pptype'] == "func":
				if macroInfo['isFunc']:
					params = macroInfo['realParams']
					baseContent = macroInfo['content']
					for i,pname in enumerate(macroInfo['params']):
						baseContent = re.sub(r'\b'+pname+r'\b',params[i],baseContent)
					codeContent = "{"+f"params[{','.join([f'\"{x}\"' for x in params])}]" + baseContent + "}"
					content = content.replace(macroInfo['removable'],f"decl({macroInfo['type']}) {macroInfo['realName']} = {codeContent};")
					
					# replace calling macro to function calling
					while True:
						macGrp = re.search(r'\b'+macroName+r'\(',content)
						if not macGrp: break
						start,end = macGrp.span()
						paramList = []
						scopes = 1
						for let in list(content[end:]):
							if let == "(":
								scopes += 1
								paramList[-1] += let
							elif let == ")":
								scopes -= 1
								if scopes == 0:
									break
								paramList[-1] += let
							elif let == ',' and scopes == 1:
								paramList.append('')
								pass
							else:
								if not paramList: paramList.append('')
								paramList[-1] += let
						# handle macro with paramcount
						assert len(paramList) == len(params)
						#replace macro content
						content = content.replace(f"{macGrp.group(0)}{','.join(paramList)})",f"[{','.join(paramList)}] call {macroInfo['realName']}")
						pass
					pass
				else:
					codeContent = "{" + macroInfo['content'] + "}"
					content = content.replace(macroInfo['removable'],f"decl({macroInfo['type']}) {macroInfo['realName']} = {codeContent};")

					content = re.sub(r'\b'+macroName+r'\b',f"(call {macroInfo['realName']})",content)
				# post check if inside macro
				#if re.search(pat_allMacroNames,content):
				#	iterateMacros = True
			else:
				raise Exception(f"invalid macro type: {macroInfo.get('type','unknwon')}")

	
	return (content, prepDict)

if __name__ == '__main__':
	with open(os.path.dirname(__file__) + '\\input.txt') as f:
		input = f.read()
	content, dictInfo = preprocessFile(input,normalizePath(f.name))
	print(content)
	pass