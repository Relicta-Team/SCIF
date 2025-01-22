import json
import os
import re
import requests
import urllib3

dictNatives = {}
nativeAssocRefs = {}

def prepareNativeCommands():
	lines = []
	with open(os.path.dirname(__file__) + '\\native.txt',mode='r') as f:
		lines = f.read().splitlines()
	

	for lineId, line in enumerate(lines):
		type = line[0:1]
		cmdFull = line[2:]
		if type == "t":
			print(f'skip token type: {cmdFull}')
			continue
		
		if re.findall(r'\w+\s\|(?!\|)',cmdFull):
			native, repl = cmdFull.split('|')
			native = native.rstrip()
			repl = repl.lstrip()

			needReverse = False

			if repl.startswith('[reverse]'):
				repl = repl[9:].lstrip()
				needReverse = True
			rpgrp = re.match(r'(\w+)\:(\@\w+|(\w+)\.(\w+)|\=\w+)',repl)
			if rpgrp is None: raise Exception(f'invalid replacer: {cmdFull} at index {lineId}')

			module = rpgrp.group(1)
			if not module in dictNatives: 
				print(f'REGISTER MODULE: "{module}"')
				dictNatives[module] = {}
			
			mdlDict = dictNatives[module]
			
			member = rpgrp.group(2)
			className = ""
			isStatic = False
			isConst = False
			isMethod = False

			if member.startswith('@'): isStatic = True; member = member[1:]
			if member.startswith('='): isConst = True; member = member[1:]

			if not isStatic and not isConst:
				className = rpgrp.group(3)
				member = rpgrp.group(4)
				isMethod = True
			cmdName = None
			if type == "b":
				ngrp = re.match(r'(\w+(?:\,\w+)*)\s(\w+|[+-/*%]|>>)\s(\w+(?:\,\w+)*)',native)
				lval = ngrp.group(1)
				cmdName = ngrp.group(2)
				rval = ngrp.group(3)
				if ',' in lval or ',' in rval:
					# todo if lvalue has , then insert new lcommand
					lval = lval.replace(',','|')
					rval = rval.replace(',','|')
					#raise Exception(f'invalid command: {cmdFull} at index {lineId}')
			
			if type == "u":
				ngrp = re.match(r'(\w+|[+-/*%]|>>)\s(\w+(?:\,\w+)*)',native)
				cmdName = ngrp.group(1)
				rval = ngrp.group(2)
				if ',' in rval:
					rval = rval.replace(',','|')
			if type == "n":
				ngrp = re.match(r'(\w+)',native)
				cmdName = ngrp.group(1)

			if cmdName is None: raise Exception(f'invalid command: {cmdFull} at index {lineId}') 

			if isMethod:
				if not className in mdlDict: 
					print(f'REGISTER CLASS: "{className}"')
					mdlDict[className] = {
						"type" : "class",
						"members": {}
					}
				
				if member in mdlDict[className]['members']: 
					curMem = mdlDict[className]['members'][member]
					# add rval to curMem
				else:
					ddat = {
						"reversed": needReverse,
						"nativeName" : cmdName,
						"cmdType": type,
					}
					mdlDict[className]['members'][member] = ddat
					if type == 'b':
						ddat['lval'] = lval
						ddat['rval'] = rval
					if type == 'u':
						ddat['rval'] = rval
					nativeAssocRefs[cmdName.lower()] = ddat

			if isStatic:
				if member in mdlDict:
					curMem = mdlDict[member] 
					#add rval to curMem

				else:
					mdlDict[member] = {
						"type": "static",
						"reversed": needReverse,
						"nativeName" : cmdName,
						"cmdType": type,
					}

					nativeAssocRefs[cmdName.lower()] = mdlDict[member]
			if isConst:
				mdlDict[member] = {
					"type": "const",
					"reversed": needReverse,
					"nativeName" : cmdName,
					"cmdType": type,
				}

				nativeAssocRefs[cmdName.lower()] = mdlDict[member]

	return dictNatives

dict_assoc_fpath = {">>":"cfg_gg_n","-":"oper_minus","+":"oper_plus"}

def downloadCMDSignature(cmdName):
	# address: https://community.bistudio.com/wiki/cmd
	# template info: https://community.bistudio.com/wiki/Template:RV
	# load page by cmd name

	pathCommandCached = f'.\\cmd_cache\\{dict_assoc_fpath.get(cmdName,cmdName)}.txt'
	if os.path.exists(pathCommandCached):
		with open(pathCommandCached,'r',encoding='utf-8') as f:
			return f.read()

	urlCmdSearch = cmdName
	if urlCmdSearch.startswith('diag_'):
		urlCmdSearch = urlCmdSearch[5:]
	url = f'https://community.bistudio.com/wikidata/api.php?action=query&format=json&list=search&srsearch={urlCmdSearch}'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}

	if cmdName not in ['-','>>']: #! some commands cannot be found
		r = requests.get(url, headers=headers)
		if r.status_code != 200: raise Exception(f'invalid cmd name: {cmdName}')
		data = r.json()
		if data['query']['searchinfo']['totalhits'] == 0: raise Exception(f'invalid cmd name: {cmdName}')
		realCMDName = '' #data['query']['search'][0]['title']

		for pageTitle in data['query']['search']:
			if pageTitle['title'].lower() == cmdName.lower() and not pageTitle['snippet'].startswith("#REDIRECT"):
				realCMDName = pageTitle['title']
				break
			if pageTitle['title'].lower().replace('_'," ") == cmdName.lower().replace('_'," ") and not pageTitle['snippet'].startswith("#REDIRECT"):
				realCMDName = pageTitle['title'].replace(' ',"_")
				break

		assert realCMDName
	else:
		if cmdName == '>>':
			realCMDName = 'config_greater_greater_name'
		else:
			realCMDName = cmdName

	#url = f'https://community.bistudio.com/wiki/{cmdName}'
	baseurl = 'https://community.bistudio.com/wikidata/api.php?'
	queryTemplate = f'{baseurl}action=query&titles={realCMDName}&prop=revisions&rvprop=content&format=json'

	r = requests.get(queryTemplate, headers=headers)
	if r.status_code != 200: raise Exception(f'invalid cmd name: {realCMDName}')
	data = r.json()
	
	native = list(data['query']['pages'].values())[0]['revisions'][0]["*"]
	native = native.replace('\\n','\n')
	
	#save cache
	with open(pathCommandCached,'w',encoding='utf-8') as f:
		f.write(native)
	
	return native

def getRegion(content,startPattern,endPattern):
	startIdx = content.find(startPattern)
	if startIdx == -1: return None
	pst = content[startIdx + len(startPattern):]
	endIdx = pst.find(endPattern)
	if endIdx == -1: return None
	return pst[:endIdx]

def checkNular(content,cmdName):
	content = re.sub(r'\'\'\'(\w+)\'\'\'',r'\1',content) # replace '''musicVolume'''
	if (content.lower() == cmdName.lower()): return True
	return re.match(r'^\s*\[\['+cmdName+r'\]\]',content,re.IGNORECASE)

def checkUnary(content,cmdName):
	return re.match(r'\[\['+cmdName+r'\]\]',content,re.IGNORECASE)

def checkBinary(content,cmdName):
	if cmdName == ">>": return True
	return re.match(r'\s*\w+\s*\[\['+cmdName+r'\]\]\s*(\[|\w+)',content,re.IGNORECASE)

mapFuncCheck = {
	"u": checkUnary,
	"n": checkNular,
	"b": checkBinary
}

def getNativeSignature(cmdName,cmdType='u'):
	'''
	dict: {signature [], description: '', return: {}}
	signature: [
		{
			name:str - name param
			nativeType:str - native type name
			type:str - typescript type
			description:str - param description
		}
		...
	],
	return: {
		nativeType:str - native type name
		type:str - typescript type
		description:str - return value description
	}
	'''
	if cmdName.lower() in [ \
		'tojson', \
		'remoteexec', \
		'remoteexeccall', \
		'servercommand', \
		'intersect', \
		'setpipeffect', \
		'drawicon3d', \
		'showhud' \
	]: return None

	cmtxt = downloadCMDSignature(cmdName)
	cmdInfo = {
		"signature": []
	}
	lineBuff = cmtxt.split('\n')

	def _sanitizeText(text):
		
		#replace <br>
		text = re.sub(r'\<br\>',r'\n',text)
		
		#replace [[(w+)]]
		text = re.sub(r'\[\[(\w+)\]\]',r'\1',text)

		#img remove
		text = re.sub(r'\[\[File\:[^\]]*\]\] ','',text)

		# position format removing
		text = re.sub(r'\[\[[^|]+\|(\w+)\]\]',r'\1',text)

		#links replace eg: [[Title Effect Type]]
		text = re.sub(r'\[\[([^\]]*)\]\]',r'\1',text)

		#replace {{GVI|\w+|\d+\.\d+[}]*}}
		text = re.sub(r'\{\{GVI\|(\w+)\|(\d+\.\d+)[^}]*\}\}',r'\1 v\2',text)

		return text
	
	def _nativeTypeToTS(nativeType):
		nativeType = nativeType.replace(" to ","|")
		return nativeType
	
	def _isCommand(line):
		return re.match(r'^\|\w+=\s*(.*)$',line)
	
	for lineNum, line in enumerate(lineBuff):
		
		grp = re.match(r'^\|descr=\s*(.*)$',line)
		if grp:
			descText = grp.group(1)
			for i in lineBuff[lineNum+1:]:
				if _isCommand(i):
					break
				descText += '\n' + i
			cmdInfo['description'] = _sanitizeText(descText)
			continue
		grp = re.match(r'^\|s\d+=\s*(.*)$',line)
		if grp:
			# signature catched
			# header required if need validate command type
			#cmdParamNames = re.findall(_sanitizeText(grp.group(1)))
			if not mapFuncCheck[cmdType](grp.group(1),cmdName): continue

			
			argsList = [] #{name,type}
			stext = ""
			for i in lineBuff[lineNum+1:]:
				if (i == ''): continue

				i = _sanitizeText(i)

				#paramNum, name, nativeType, description
				grpPar = re.match(r'\|p(\d+)=\s*(\w+)\:\s*([^\-]+)(- .*)?$',i)					

				if grpPar:
					#assert grpPar.group(1) == str(len(argsList)+1)
					
					#! skip corrupted wiki pages
					if cmdName.lower() not in ['nearestobjects']:
						assert re.match(r".*(\d+)",grpPar.group(1)).group(1) == str(len(argsList)+1), 'invalid param num'

					argsList.append({
						"name": grpPar.group(2),
						"nativeType": grpPar.group(3),
						"type": _nativeTypeToTS(grpPar.group(3)),
						"description": _sanitizeText(grpPar.group(4)[2:] if grpPar.group(4) else '')
					})

					#adding second descriptions line
					# for i in lineBuff[lineNum+1:]:
					# 	if i == '': continue
					# 	if _isCommand(i):
					# 		break
					# 	argsList[-1]['description'] += '\n' + _sanitizeText(i)
					
				else:
					sSince = re.match(r'\|s\d+since=\s*(.*)$',i)
					if sSince:
						cmdInfo['description'] += '\n' + f"Since ver. {sSince.group(1)}"
						continue

					pSince = re.match(r'\|p\d+since=\s*(.*)$',i)
					if pSince:
						stext += i
						continue
					pReturn = re.match(r'\|r(\d+)=\s*(.*)$',i.replace('\n','<br>'))
					if pReturn:
						firstMin = pReturn.group(2).find(' - ')
						if firstMin == -1:
							tpart = pReturn.group(2)
							dpart = ''
						else:
							tpart = pReturn.group(2)[:firstMin]
							dpart = pReturn.group(2)[firstMin+3:]
						cmdInfo['return'] = {
							"nativeType": tpart,
							"type": _nativeTypeToTS(tpart),
							"description": _sanitizeText(dpart)
						}
						#adding next returns
						doBreakFromReturn = False
						for i in lineBuff[lineNum+1:]:
							if i == '': continue
							if _isCommand(i):
								doBreakFromReturn = True
								break
							cmdInfo['return']['description'] += '\n' + _sanitizeText(i)
						if doBreakFromReturn: break
						continue
					if _isCommand(i):
						break
					else:
						argsList[-1]['description'] += '\n' + i
			cmdInfo['signature'] = argsList

	#post check
	if cmdType == 'n' and len(cmdInfo['signature']) != 0: raise Exception(f'command {cmdName} must be nular')

	return cmdInfo

def __dumpNativeDict(dta):
	lines = []
	for (it, (module,contentMdl)) in enumerate(dta.items()):
		print(f"parsing module {it+1} of {len(dta)}: {module}")
		lines.append(f'// {module}\n\n')
		
		statList = []
		constList = []
		for memName,memData in contentMdl.items():
			if memData['type'] == 'class':
				clsList = []
				for cmemName,cmemData in memData['members'].items():
					clsList.append(f'\t\t{cmemName} //{cmemData["nativeName"]};')
				clsList.sort()
				clsList.insert(0,f'\tclass {memName}')

				lines.extend(clsList)
			elif memData['type'] == 'static':
				sig = getNativeSignature(memData['nativeName'],memData['cmdType'])
				if sig is None:
					commentPrefix = ""
				else:
					commentPrefix = "\t/**\n"
					commentPrefix += f"\t * {sig['description']}"
					for param in sig['signature']:
						commentPrefix += f"\n\t * @param {param['name']} {param['description']}"

					commentPrefix += f"\n\t * @returns {sig['return']['description']}"
					commentPrefix += "\n*/"

				statList.append(commentPrefix + f'\tstatic {memName}(); //{memData["nativeName"]}')
			elif memData['type'] == 'const':
				constList.append(f'\tconst {memName}; //{memData["nativeName"]}')
			else:
				raise Exception(f'invalid type: {memData["type"]}')
		
		statList = sorted(statList,key=lambda x: re.search('static (\w+)',x).group(1))
		constList = sorted(constList,key=lambda x: re.search('const (\w+)',x).group(1))
		#statList.sort()
		#constList.sort()

		lines.extend(statList)
		lines.extend(constList)
		
		pass
	
	with open('native_commands_dump.h','w',encoding='utf-8') as f:
		f.write('\n'.join(lines))

if __name__ == '__main__':
	#sig = getNativeSignature("-")
	dta = prepareNativeCommands()
	__dumpNativeDict(dta)

	print(f'registered: {len(dictNatives)}')