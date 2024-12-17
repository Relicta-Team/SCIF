import json
import os
import re
import requests
import urllib3

dictNatives = {}

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
			if isConst:
				mdlDict[member] = {
					"type": "const",
					"reversed": needReverse,
					"nativeName" : cmdName,
					"cmdType": type,
				}

	return dictNatives


def downloadCMDSignature(cmdName):
	# address: https://community.bistudio.com/wiki/cmd
	# template info: https://community.bistudio.com/wiki/Template:RV
	# load page by cmd name
	url = f'https://community.bistudio.com/wikidata/api.php?action=query&format=json&list=search&srsearch={cmdName}'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}

	r = requests.get(url, headers=headers)
	if r.status_code != 200: raise Exception(f'invalid cmd name: {cmdName}')
	data = r.json()
	if data['query']['searchinfo']['totalhits'] == 0: raise Exception(f'invalid cmd name: {cmdName}')
	realCMDName = data['query']['search'][0]['title']

	#url = f'https://community.bistudio.com/wiki/{cmdName}'
	baseurl = 'https://community.bistudio.com/wikidata/api.php?'
	queryTemplate = f'{baseurl}action=query&titles={realCMDName}&prop=revisions&rvprop=content&format=json'

	r = requests.get(queryTemplate, headers=headers)
	if r.status_code != 200: raise Exception(f'invalid cmd name: {cmdName}')
	data = r.json()
	
	native = list(data['query']['pages'].values())[0]['revisions'][0]["*"]
	native = native.replace('\\n','\n')

	return native

def getRegion(content,startPattern,endPattern):
	startIdx = content.find(startPattern)
	if startIdx == -1: return None
	pst = content[startIdx + len(startPattern):]
	endIdx = pst.find(endPattern)
	if endIdx == -1: return None
	return pst[:endIdx]

def getNativeSignature(cmdName):
	cmtxt = downloadCMDSignature(cmdName)
	raise NotImplementedError()

def __dumpNativeDict(dta):
	lines = []
	for module,contentMdl in dta.items():
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
				statList.append(f'\tstatic {memName}(); //{memData["nativeName"]}')
			elif memData['type'] == 'const':
				constList.append(f'\tconst {memName}; //{memData["nativeName"]}')
			else:
				raise Exception(f'invalid type: {memData["type"]}')
		
		statList.sort()
		constList.sort()

		lines.extend(statList)
		lines.extend(constList)
		
		pass
	
	with open('native_commands_dump.h','w') as f:
		f.write('\n'.join(lines))

if __name__ == '__main__':
	#downloadCMDSignature("lineintersectsSurfaces")
	dta = prepareNativeCommands()
	__dumpNativeDict(dta)

	print(f'registered: {len(dictNatives)}')