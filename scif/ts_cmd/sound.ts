// sound


export namespace sound {

	function addMusicEventHandler(type:string, function:string|Code):number { return null as any }; //addmusiceventhandler
	function fadeSound(time:number, volume:number):void {}; //fadesound
	function getAudioOptionVolumes():array { return null as any }; //getaudiooptionvolumes
	function getMusicPlayedTime():number { return null as any }; //getmusicplayedtime
	function getMusicVolume():number { return null as any }; //musicvolume
	function getSoundParams(id:number):arrayinformat[path|curPos|length|time|volume]|where: { return null as any }; //soundparams
	function getSoundVolume():number { return null as any }; //soundvolume
	function playMusic(musicName:string, start:number):void {}; //playmusic
	function playSound(soundName:string, isSpeech:Boolean|number, offset:number):Object { return null as any }; //playsound
	function playSound3D(filename:string, soundSource:Object, isInside:Boolean, soundPosition:array, volume:number, soundPitch:number, distance:number, offset:number, local:Boolean):number { return null as any }; //playsound3d
	function playSoundUI(sound:string, volume:number, soundPitch:number, isEffect:Boolean, offset:number):number { return null as any }; //playsoundui
	function preloadSound(soundName:string):Boolean { return null as any }; //preloadsound
	function removeAllMusicEventHandlers(type:string):void {}; //removeallmusiceventhandlers
	function removeMusicEventHandler(type:string, id:number):void {}; //removemusiceventhandler
	function say3D(from:Object|array, sound:string|array):Object { return null as any }; //say3d
	function stopSound(id:number):void {}; //stopsound
}