// render


export namespace render {

	function camCommit(camera:Object, time:number):void {}; //camcommit
	function camCreate(type:string, position:array):Object { return null as any }; //camcreate
	function cutText(layer:number|string, text:string, type:string, speed:number, showInMap:Boolean, isStructuredText:Boolean, drawOverHUD:Boolean): { return null as any }; //cuttext
	function drawIcon3D(UNKNOWN):any { return null as any }; //drawicon3d
	function drawLaser(position:array, direction:array, beamColor:array, dotColor:array, dotSize:number, beamThickness:number, beamMaxLength:number, isIR:Boolean):void {}; //drawlaser
	function drawLine3D(start:array, end:array, color:array|Color(RGBA), width:number):void {}; //drawline3d
	function enableCaustics(bool:Boolean):void {}; //enablecaustics
	function getAllCameras():array { return null as any }; //allcameras
	function getApertureParams():arrayinformat[aperture|isForced|estimatedAperture|estimatedLuminance|minCustom|stdCustom|maxCustom|customLuminance|isCustomForced|blinding]|where: { return null as any }; //apertureparams
	function getCursorObject():Object { return null as any }; //cursorobject
	function getCursorTarget():Object { return null as any }; //cursortarget
	function getLighting():arrayinformat[ambientLightColor|ambientLightBrightness|lightDirection|starsVisibility]: { return null as any }; //getlighting
	function getObjectViewDistance():array { return null as any }; //getobjectviewdistance
	function getParticlesQuality():number { return null as any }; //particlesquality
	function getPiPViewDistance():number { return null as any }; //getpipviewdistance
	function getResolution():array { return null as any }; //getresolution
	function getShadowDistance():number { return null as any }; //getshadowdistance
	function getTextureInfo(texture:string):arrayinformat[width|height|rgbaAverageColour]where: { return null as any }; //gettextureinfo
	function getVideoOptions():HashMap { return null as any }; //getvideooptions
	function getViewDistance():number { return null as any }; //viewdistance
	function intersect(lval:any, rval:any):any { return null as any }; //intersect
	function lineIntersects(elementN:arrayformat[begPos|endPos|objIgnore1|objIgnore2]:):arrayformat[result1|result2|...] { return null as any }; //lineintersects
	function posScreenToWorld(map:widget, x:number, y:number):array { return null as any }; //posscreentoworld
	function positionCameraToWorld(cameraPos:PositionRelative):array { return null as any }; //positioncameratoworld
	function postProcessEffectAdjust(effect:string|number, settings:array):void {}; //ppeffectadjust
	function postProcessEffectCommit(handles:array, commit:number):void {}; //ppeffectcommit
	function postProcessEffectCommitted(handle:number):Boolean { return null as any }; //ppeffectcommitted
	function postProcessEffectCreate(nameN:string, priorityN:number):array { return null as any }; //ppeffectcreate
	function postProcessEffectDestroy(effects:array):void {}; //ppeffectdestroy
	function postProcessEffectEnable(effectArray:array, enable:Boolean):void {}; //ppeffectenable
	function postProcessEffectEnabled(effect:string):Boolean { return null as any }; //ppeffectenabled
	function screenToWorldDirection(screen:array):array { return null as any }; //screentoworlddirection
	function setAperture(aperture:number):void {}; //setaperture
	function setApertureNew(minimum:number, standard:number, maximum:number, luminance:number):void {}; //setaperturenew
	function setHorizonParallaxCoef(coef:number):void {}; //sethorizonparallaxcoef
	function setObjectViewDistance(objectDistance:number, shadowDistance:number):void {}; //setobjectviewdistance
	function setPiPEffect(lval:any, rval:any):any { return null as any }; //setpipeffect
	function setPiPEffectForceInnVG(ppHandle:number, force:Boolean):void {}; //ppeffectforceinnvg
	function setPiPViewDistance(distance:number):void {}; //setpipviewdistance
	function setShadowDistance(value:number):void {}; //setshadowdistance
	function showHUD(UNKNOWN):any { return null as any }; //showhud
	const isPiPEnabled; //ispipenabled
}