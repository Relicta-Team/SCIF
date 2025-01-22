// engine


export namespace engine {

	export class namespace {
		getAllVars //allvariables;
		getVar //getvariable;
		setVar //setvariable;
	}
	export class location {
		getAllVars //allvariables;
		getObjectName //name;
		getVar //getvariable;
		setName //setname;
		setText //settext;
		setVar //setvariable;
	}
	function callExtension(extension:string, function:string, arguments:array):arrayinformat[result|returnCode|errorCode]|where: { return null as any }; //callextension
	function cfgGet(config:Config, name:string):Config { return null as any }; //>>
	function codeToString(code:Code):string { return null as any }; //tostring
	function compile(expression:string):Code { return null as any }; //compile
	function compileScript(path:string, final:Boolean, prefixHeader:string):Code { return null as any }; //compilescript
	function copyFromClipboard():string { return null as any }; //copyfromclipboard
	function copyToClipboard(text:string):void {}; //copytoclipboard
	function createDialog(dialogName:string, forceOnTop:Boolean):display { return null as any }; //createdialog
	function createLocation(location:Location):Location { return null as any }; //createlocation
	function cutRSC(className:string, effect:string, speed:number, showInMap:Boolean, drawOverHUD:Boolean):void {}; //cutrsc
	function deleteLocation(location:Location):void {}; //deletelocation
	function enableEnvironment(ambientLife:Boolean, ambientSound:Boolean, windyCoef:number):void {}; //enableenvironment
	function endMission(endType:string):void {}; //endmission
	function fadeSpeech(time:number, volume:number):void {}; //fadespeech
	function forceUnicode(mode:number):any { return null as any }; //forceunicode
	function format(formatString:string, varN:any):string { return null as any }; //format
	function freeExtension(extension:string):Boolean|void { return null as any }; //freeextension
	function fromJson(jsonValue:string):Canbeoneof: { return null as any }; //fromjson
	function getActionKeys(userAction:string):array { return null as any }; //actionkeys
	function getActiveSQFScripts():array { return null as any }; //diag_activesqfscripts
	function getAddonFiles(pboPrefix:string, fileExtension:string):array { return null as any }; //addonfiles
	function getAllAddonsInfo():array { return null as any }; //alladdonsinfo
	function getAllExtensions():array { return null as any }; //allextensions
	function getAllMissionEventHandlers():array { return null as any }; //diag_allmissioneventhandlers
	function getCurrentNamespace():Namespace { return null as any }; //currentnamespace
	function getDeltaTime():number { return null as any }; //diag_deltatime
	function getEntities(typesInclude:array, typesExclude:array, includeCrews:Boolean, excludeDead:Boolean):array { return null as any }; //entities
	function getEventHandlerInfo(oper:Object|Group|widget|display, type:string, id:number):arrayinformat[exists|isLast|total]|emptyarray[]|where: { return null as any }; //geteventhandlerinfo
	function getFPS():number { return null as any }; //diag_fps
	function getFPSMin():number { return null as any }; //diag_fpsmin
	function getFrameNo():number { return null as any }; //diag_frameno
	function getHashValue(value:array|Boolean|Code|Config|Group|Namespace|NaN|number|Object|Side|string):string { return null as any }; //hashvalue
	function getLoadedModsInfo():array { return null as any }; //getloadedmodsinfo
	function getMissionPath(filename:string):string { return null as any }; //getmissionpath
	function getModParams(modClass:string, options:array):array { return null as any }; //modparams
	function getProductVersion():arrayinformat[name|nameShort|version|build|branch|isModded|platform|architecture]: { return null as any }; //productversion
	function getScopeLevel():number { return null as any }; //diag_scope
	function getStackTrace():array { return null as any }; //diag_stacktrace
	function getSystemTime():array { return null as any }; //systemtime
	function getSystemTimeUTC():array { return null as any }; //systemtimeutc
	function getTickTime():number { return null as any }; //diag_ticktime
	function getTime():number { return null as any }; //time
	function getTypeName(anything:any):string { return null as any }; //typename
	function getTypeOf(obj:Object):string { return null as any }; //typeof
	function getWorldName():string { return null as any }; //worldname
	function inAreaArray(positions:array):array:Objectsand/orPositionsinsidethearea { return null as any }; //inareaarray
	function inputMouse(combocode:string):Boolean { return null as any }; //inputmouse
	function isEqualRef(val1:any, val2:any):Boolean { return null as any }; //isequalref
	function isEqualTo(val1:any, val2:any):Boolean { return null as any }; //isequalto
	function isEqualType(val1:any, val2:any):Boolean { return null as any }; //isequaltype
	function isEqualTypeAll(arr:array(any''SinceArma3v2.09.149634''), val:any):Boolean { return null as any }; //isequaltypeall
	function isEqualTypeAny(val:any, types:array):Boolean { return null as any }; //isequaltypeany
	function isEqualTypeArray(arr1:array(any''SinceArma3v2.09.149634''), arr2:array):Boolean { return null as any }; //isequaltypearray
	function isKindOf(class1:string, class2:string, targetConfig:Config):Boolean { return null as any }; //iskindof
	function isNotEqualRef(val1:any, val2:any):Boolean { return null as any }; //isnotequalref
	function isNotEqualTo(val1:any, val2:any):Boolean { return null as any }; //isnotequalto
	function loadFile(fileName:string):string { return null as any }; //loadfile
	function parseText(text:string):StructuredText { return null as any }; //parsetext
	function preprocessFile(fileName:string):string { return null as any }; //preprocessfile
	function preprocessFileLineNumbers(fileName:string):string { return null as any }; //preprocessfilelinenumbers
	function regexFind(haystack:string, pattern:string, startOffset:number):array { return null as any }; //regexfind
	function regexMatch(haystack:string, pattern:string):Boolean { return null as any }; //regexmatch
	function regexReplace(haystack:string, pattern:string, replaceString:string):string { return null as any }; //regexreplace
	function removeAllMissionEventHandlers(type:string):void {}; //removeallmissioneventhandlers
	function removeMissionEventHandler(type:string, index:number):void {}; //removemissioneventhandler
	function ropeCut(rope:Object, length:number):void {}; //ropecut
	function saveMissionProfileNamespace():Boolean { return null as any }; //savemissionprofilenamespace
	function saveProfileNamespace():void {}; //saveprofilenamespace
	function screenToWorld(screen:array):array|worldpositiononsurface[x|y|0] { return null as any }; //screentoworld
	function scriptDone(handle:ScriptHandle):Boolean { return null as any }; //scriptdone
	function selectPlayer(unitName:Object):void {}; //selectplayer
	function setFog(time:number, fogValue:number, fogDecay:number, fogBase:number):void {}; //setfog
	function setGroupOwner(group:Group, clientID:number):Boolean { return null as any }; //setgroupowner
	function setLocalWindParams(strength:number, diameter:number):void {}; //setlocalwindparams
	function setMousePosition(x:number, y:number):void {}; //setmouseposition
	function setOvercast(time:number, overcast:number):void {}; //setovercast
	function setRain(time:number, rain:number):void {}; //setrain
	function setScopeName(name:string):void {}; //scopename
	function setScriptName(name:string):void {}; //scriptname
	function setViewDistance(distance:number):void {}; //setviewdistance
	function setWaves(time:number, value:number):void {}; //setwaves
	function setWindDir(time:number, value:number):void {}; //setwinddir
	function setWindStr(time:number, value:number):void {}; //setwindstr
	function showChat(bool:Boolean):void {}; //showchat
	function sleep(delay:number):void {}; //sleep
	function supportInfo(mask:string):array { return null as any }; //supportinfo
	function systemChat(text:string):void {}; //systemchat
	function terminate(FSMHandle:number):void {}; //terminate
	function toJSON(UNKNOWN):any { return null as any }; //tojson
	function uiSleep(delay:number):void {}; //uisleep
	function worldToScreen(position:array):array { return null as any }; //worldtoscreen
	const cameraOn; //cameraon
	const canSuspend; //cansuspend
	const currentLanguage; //language
	const freeLook; //freelook
	const is3den; //is3den
	const is3denMultiplayer; //is3denmultiplayer
	const is3denPreview; //is3denpreview
	const isFilePatchingEnabled; //isfilepatchingenabled
	const isGameFocused; //isgamefocused
	const isSteamOverlayEnabled; //issteamoverlayenabled
	const missionConfigFile; //missionconfigfile
	const missionName; //missionname
	const missionNameSource; //missionnamesource
	const missionNamespace; //missionnamespace
	const nullScript; //scriptnull
	const profileName; //profilename
	const profileNameSteam; //profilenamesteam
	const profileNamespace; //profilenamespace
	const worldSize; //worldsize
}