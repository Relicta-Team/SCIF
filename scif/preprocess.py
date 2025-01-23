import os
import re

PAT_MACROCONST = re.compile(r'macro_const\((\w+)\)',re.MULTILINE)

PAT_DEFINE = re.compile(r'\#\s*define\s*(\w+)(\s*\(([^\)]*)\))?')

def preprocessFile(content):
	prepDict = {} #key preprocName, value {realName:str, isFunc:bool, params:[], content:str}

	#collect preproc info
	nextMacroConstFunc = ""
	lastMacroDefName = ""
	def nextIsMacroConst(): return nextMacroConstFunc != ""
	isPrepprocHandleNextline = False

	def _determineDataType(data):
		# todo determine arrays vec4,vec3
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

		mcst_grp = re.search(PAT_MACROCONST,line)
		if mcst_grp:
			nextMacroConstFunc = mcst_grp.group(1)
			content = content.replace(mcst_grp.group(0),"")
			continue
		
		mdf_grp = re.search(PAT_DEFINE,line)
		if mdf_grp:
			
			#skip if macro is enum type
			if any((x for x in _skipEnumsPrefixList if mdf_grp.group(1).startswith(x))):
				continue

			if nextIsMacroConst():
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
					'realName': nextMacroConstFunc,
					'isFunc': isFunc,
					'params': paramList,
					'content': macroContent,
					'removable': line,
					"type": "any",
				}
				
				nextMacroConstFunc = ""
				continue
			else:
				print("warning: unknown define type: " + line)
		if isPrepprocHandleNextline:
			isPrepprocHandleNextline = re.search(r'\\\s*$',line) != None
			prepDict[lastMacroDefName]['removable'] += '\n' + line
			line = re.sub(r'\\\s*$',r'',line)
			prepDict[lastMacroDefName]['content'] += '\n' + line


	for macroName,macroInfo in prepDict.items():
		if macroInfo['isFunc']:
			raise NotImplementedError('macro function not implemented')
			content = content.replace(macroInfo['removable'],macroInfo['content'] + ";")
		else:
			# replace header
			dtype = _determineDataType(macroInfo['content'])
			if dtype == "any":
				raise Exception(f"invalid macro type: {macroInfo['content']}")
			content = content.replace(macroInfo['removable'],f"const decl({dtype}) {macroInfo['realName']} = {macroInfo['content']};")

			content = re.sub(r'\b'+macroName+r'\b',macroInfo['realName'],content)

	print(content)
	return content

if __name__ == '__main__':
	with open(os.path.dirname(__file__) + '\\input.txt') as f:
		input = f.read()
	print(preprocessFile(input))