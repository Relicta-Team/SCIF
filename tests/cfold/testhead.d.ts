

declare var NonClass: ObjectConstructorX;


interface ObjectConstructorX {
    new (value?: any): NonClass;
    (): any;
    (value: any): any;
}

interface NonClass {
	isEnable:boolean
}
