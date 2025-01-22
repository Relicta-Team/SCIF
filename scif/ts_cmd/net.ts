// net


export namespace net {

	function addBackpackGlobal(unit:Object, backpack:string):void {}; //addbackpackglobal
	function enableSimulationGlobal(entity:Object, enable:Boolean):void {}; //enablesimulationglobal
	function getAllPlayers():array { return null as any }; //allplayers
	function getAllUsers():array { return null as any }; //allusers
	function getClientState():string { return null as any }; //getclientstate
	function getClientStateNumber():number { return null as any }; //getclientstatenumber
	function getServerTime():number { return null as any }; //servertime
	function getUserInfo(playerID:string, infoIndex:number):any { return null as any }; //getuserinfo
	function hideObjectGlobal(object:Object, hidden:Boolean):void {}; //hideobjectglobal
	function isLocal():void {}; //local
	function isRemoteExecuted():Boolean { return null as any }; //isremoteexecuted
	function publicVariable(varName:string):void {}; //publicvariable
	function publicVariableClient(clientID:number, varName:string):void {}; //publicvariableclient
	function publicVariableServer(varName:string):void {}; //publicvariableserver
	function remoteExec(lval:any, rval:any):any { return null as any }; //remoteexec
	function remoteExecCall(lval:any, rval:any):any { return null as any }; //remoteexeccall
	function removeBackpackGlobal(unit:Object):void {}; //removebackpackglobal
	function serverCommand(lval:any, rval:any):any { return null as any }; //servercommand
	function serverCommandExecutable(command:string):Boolean { return null as any }; //servercommandexecutable
	function setHideObjectGlobal(object:Object):void {}; //hideobjectglobal
	function setObjectMaterialGlobal(obj:Object, selection:number|string, material:string):void {}; //setobjectmaterialglobal
	function setObjectTextureGlobal(object:Object, selection:number|string, texture:string):void {}; //setobjecttextureglobal
	const clientOwner; //clientowner
	const isMultiplayer; //ismultiplayer
	const isServer; //isserver
	const remoteExecutedOwner; //remoteexecutedowner
	const serverName; //servername
}