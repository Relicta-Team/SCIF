// mesh


export namespace mesh {

	export class mesh {
		addEventHandler //addeventhandler;
		addMPEventHandler //addmpeventhandler;
		addTorque //addtorque;
		animate //animate;
		animateSource //animatesource;
		attachTo //attachto;
		detach //detach;
		disableCollisionWith //disablecollisionwith;
		enableCollisionWith //enablecollisionwith;
		getActionParams //actionparams;
		getAllLODs //alllods;
		getAllVars //allvariables;
		getAngularVelocity //angularvelocity;
		getAngularVelocityModelSpace //angularvelocitymodelspace;
		getAnimationSourcePhase //animationsourcephase;
		getBoundingBox //boundingbox;
		getBoundingBoxReal //boundingboxreal;
		getBoundingCenter //boundingcenter;
		getCenterOfMass //getcenterofmass;
		getCollisionDisabledWith //collisiondisabledwith;
		getDir //getdir;
		getDirVisual //vectordirvisual;
		getLightDetachObject //lightdetachobject;
		getLightingAt //getlightingat;
		getModelInfo //getmodelinfo;
		getObjectTextures //getobjecttextures;
		getPhysicsCollisionFlag //getphysicscollisionflag;
		getPos //getpos;
		getPosASL //getposasl;
		getPosATL //getposatl;
		getPosATLVisual //getposatlvisual;
		getPosAslVisual //getposaslvisual;
		getPosVisual //getposvisual;
		getPosWorld //getposworld;
		getPosWorldVisual //getposworldvisual;
		getRelDir //getreldir;
		getRelPos //getrelpos;
		getScale //getobjectscale;
		getSelectionNames //selectionnames;
		getSelectionPosition //selectionposition;
		getSelectionVectorDirAndUp //selectionvectordirandup;
		getVar //getvariable;
		getVectorDir //vectordir;
		getVectorSide //vectorside;
		getVectorSideVisual //vectorsidevisual;
		getVectorUp //vectorup;
		getVectorUpVisual //vectorupvisual;
		getVelocity //velocity;
		getVelocityModelSpace //velocitymodelspace;
		isSimpleObject //issimpleobject;
		lightAttachObject //lightattachobject;
		modelToWorld //modeltoworld;
		modelToWorldVisual //modeltoworldvisual;
		modelToWorldVisualWorld //modeltoworldvisualworld;
		modelToWorldWorld //modeltoworldworld;
		removeAllEventHandlers //removealleventhandlers;
		removeEventHandler //removeeventhandler;
		removeMPEventHandler //removempeventhandler;
		screenToWorld //screentoworld;
		screenToWorldDirection //screentoworlddirection;
		setAllowDamage //allowdamage;
		setAngularVelocity //setangularvelocity;
		setAngularVelocityModelSpace //setangularvelocitymodelspace;
		setAnimSpeedCoef //setanimspeedcoef;
		setAnimationPhase //animationphase;
		setCenterOfMass //setcenterofmass;
		setDir //setdir;
		setDropInterval //setdropinterval;
		setHide //hideobject;
		setHideSelection //hideselection;
		setLightAmbient //setlightambient;
		setLightBrightness //setlightbrightness;
		setLightColor //setlightcolor;
		setLightConePars //setlightconepars;
		setLightFlareMaxDistance //setlightflaremaxdistance;
		setLightFlareSize //setlightflaresize;
		setLightIntensity //setlightintensity;
		setLightUseFlare //setlightuseflare;
		setLightVolumeShape //setlightvolumeshape;
		setMass //setmass;
		setMaterial //setobjectmaterial;
		setObjectTexture //setobjecttexture;
		setParticleCircle //setparticlecircle;
		setParticleClass //setparticleclass;
		setParticleParams //setparticleparams;
		setParticleRandom //setparticlerandom;
		setPhysicsCollisionFlag //setphysicscollisionflag;
		setPos //setpos;
		setPosASL //setposasl;
		setPosASLW //setposaslw;
		setPosATL //setposatl;
		setPosWorld //setposworld;
		setScale //setobjectscale;
		setSimulation //enablesimulation;
		setVar //setvariable;
		setVectorDir //setvectordir;
		setVectorDirAndUp //setvectordirandup;
		setVectorUp //setvectorup;
		setVelocity //setvelocity;
		setVelocityModelSpace //setvelocitymodelspace;
		setVelocityTransformation //setvelocitytransformation;
		vectorModelToWorld //vectormodeltoworld;
		vectorModelToWorldVisual //vectormodeltoworldvisual;
		vectorWorldToModel //vectorworldtomodel;
		vectorWorldToModelVisual //vectorworldtomodelvisual;
		worldToModel //worldtomodel;
		worldToModelVisual //worldtomodelvisual;
		worldToScreen //worldtoscreen;
	}
	function AGLtoASL(posAGL:array):array { return null as any }; //agltoasl
	function ASLtoAGL(posASL:array):PositionAGL { return null as any }; //asltoagl
	function ASLtoATL(pos:array):array { return null as any }; //asltoatl
	function ATLtoASL(pos:array):array { return null as any }; //atltoasl
	function createSimpleObject(className:string, positionASL:array, local:Boolean):Object { return null as any }; //createsimpleobject
	function createUnit(type:string, position:Object|Group|array|Position2D, group:Group, init:string, skill:number, rank:string):{{Feature|warning|'''void''' { return null as any }; //createunit
	function createVehicle(type:string, position:array):Object { return null as any }; //createvehicle
	function createVehicleLocal(type:string, position:array):Object { return null as any }; //createvehiclelocal
	function deleteVehicle(objects:array):void {}; //deletevehicle
	function getAllMissionObjects(type:string):array { return null as any }; //allmissionobjects
	function getBoundingBox(clippingType:number, object:Object):array { return null as any }; //boundingbox
	function getBoundingBoxReal(clippingType:number, object:Object):array { return null as any }; //boundingboxreal
	function getDir(pos1:Object|Position2D|Position3D, pos2:Object|Position2D|Position3D):number { return null as any }; //getdir
	function getDirVisual(pos1:Object|Position2D|Position3D, pos2:Object|Position2D|Position3D):number { return null as any }; //getdirvisual
	function getNearObjects(position:array|Position2D|Object, typeName:string, radius:number):array { return null as any }; //nearobjects
	function getRopes(ropesOwner:Object):array { return null as any }; //ropes
	function isInPolygon(position:array|Object|Group, polygon:array):Boolean { return null as any }; //inpolygon
	function lineIntersectsObjs(elementN:arrayformat[begPos|endPos|ignoreObj1|ignoreObj2|sortByDistance|flags]):arrayformat[result1|result2|...] { return null as any }; //lineintersectsobjs
	function lineIntersectsSurfaces(elementN:arrayformat[begPosASL|endPosASL|ignoreObj1|ignoreObj2|sortMode|maxResults|LOD1|LOD2|returnUnique]):arrayformat[result1|result2|...] { return null as any }; //lineintersectssurfaces
	function lineIntersectsWith(elementN:arrayformat[begPos|endPos|objIgnore1|objIgnore2|sortByDistance]):arrayformat[result1|result2|...] { return null as any }; //lineintersectswith
	function nearEntities(area:string|Object|array:, types:array, matchExactType:Boolean, aliveOnly:Boolean, includeCrew:Boolean):array { return null as any }; //nearentities
	function nearestObjects(position:Object|arrayinformatPositionAGL|Position2D, types:array, radius:number, 2Dmode:Boolean):array { return null as any }; //nearestobjects
	function ropeAttachEnabled(entity:Object):Boolean { return null as any }; //ropeattachenabled
	function ropeAttachTo(entity:Object, rope:Object):void {}; //ropeattachto
	function ropeAttachedObjects(ropesOwner:Object):array { return null as any }; //ropeattachedobjects
	function ropeAttachedTo(cargo:Object):Object { return null as any }; //ropeattachedto
	function ropeCreate(fromObject:Object, fromPoint:string|array, length:number, ropeStart:array, ropeEnd:array, ropeType:string, nSegments:number):Object { return null as any }; //ropecreate
	function ropeDestroy(rope:Object):void {}; //ropedestroy
	function ropeDetach(attachedObject:Object, rope:Object):void {}; //ropedetach
	function ropeEndPosition(rope:Object):array { return null as any }; //ropeendposition
	function ropeGetLength(rope:Object):number { return null as any }; //ropelength
	function ropeSegments(rope:Object):array { return null as any }; //ropesegments
	function ropeUnwound(rope:Object):Boolean { return null as any }; //ropeunwound
	const meshNull; //objnull
}