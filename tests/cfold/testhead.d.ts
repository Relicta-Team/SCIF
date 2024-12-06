

declare var NonClass: ObjectConstructor;


interface ObjectConstructor {
    new (value?: any): NonClass;
    (): any;
    (value: any): any;
}

interface NonClass {
	isEnable:boolean
}
