

declare var NonClass: _octor;


interface _octor {
    new (value?: any): NonClass;
    (): any;
    (value: any): any;
}

interface NonClass {
	isEnable:boolean
}
