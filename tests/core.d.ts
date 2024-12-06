
/**
 * Base object header file
 */
declare var Object: ObjectConstructor;
declare var Array: ArrayConstructor;
declare var String: StringConstructor;
declare var Number: NumberConstructor;
declare var Boolean: BooleanConstructor;
declare var Function: FunctionConstructor;
declare var IArguments: IArgumentsConstructor;
declare var RegExp: RegExpConstructor;

interface ObjectConstructor {
    new (value?: any): Object;
    (): any;
    (value: any): any;
}
interface ArrayConstructor {
	new (arrayLength?: number): any[];
	new (arrayLength: number, ...items: any[]): any[];
	(arrayLength?: number): any[];
	(arrayLength: number, ...items: any[]): any[];
	isArray(arg: any): arg is any[];
}
interface StringConstructor {
	new (value?: any): string;
	(value?: any): string;
}
interface NumberConstructor {
	new (value?: any): number;
	(value?: any): number;
}
interface BooleanConstructor {
	new (value?: any): boolean;
	(value?: any): boolean;
}
interface FunctionConstructor {
	new (value?: any): Function;
	(value?: any): Function;
}
interface IArgumentsConstructor {
	new (value?: any): IArguments;
	(value?: any): IArguments;
}
interface RegExpConstructor {
	new (value?: any): RegExp;
	(value?: any): RegExp;
}

interface Object {
	test_objMethod(): string
}
interface Array<T> {
	test_arrMethod(): string
}
interface String {
	test_strMethod(): string
}

interface Number {
	dataGet(): string
}

interface Boolean {
	test_boolMethod(): string
}

interface Function {
	test_funcMethod(): string
}

interface IArguments {}
interface RegExp {}

interface DEBUGVALUE {
	isEnable:boolean
}

