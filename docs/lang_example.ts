
//simple function, var, const
function f1() {return 0}; //all members are case sensitive (in compiled code converted to addresses and push real names into symbol table)
function F1() {return ""};
var v1 = 0;
const ct1 = 0;

//exporting members
export namespace glob {
	export function test() {}

	export var a = 3;
	//namespace nested
	export namespace nested {
		export function test() {}
		export var a = 4;
	}
}

glob.a = 123;
glob.nested.a = 321;

//control flow base
function flow_example():number {
	//if, else
	if (false) {}
	if (false) {} else {}
	
	//elif's
	if (false) {}
	else if(false) {}
	else if(false) {}
	else {}
	
	//switch
	let a = 3;
	switch (a) {
		case 321: break;
		case 123: break;
		default: break;
	}

	//while
	while (false) {}
	//invert while
	do {} while (false);

	//for
	let range = (beg,end) => [beg,end]; //for test only decl
	for (let val of range(0,10)) {} //optimized variant (sqf native)
	// slower variant
	for (let i = 0; i < 10; i++) {} //inlining states into native forloop (no used deprecated for overloading)

	//foreach
	let arr = [1,2,3];
	let get_foreach_index = ()=> 0; //special function for foreach
	for (let i of arr) { let _foreachindex = get_foreach_index(); }

	//break, continue
	for (let i of arr) {
		if (i == 2) {
			break;
		}
		if (i == 1) {
			continue;
		}
	}

	//return
	return 0;
};

//templates
export function f2<T>(x:T) {return x}
function f3<A,B,C,D,E,F>(a:A,b:B,c:C,d:D,e:E,f:F):F {return f}

//types
type num_alias = number;
type union_test = number | string;
type tuple_test = [num_alias,string];
type array_test = num_alias[];

let nal:num_alias = 3;
let ut:union_test = 3;
	ut = "3";
let tt:tuple_test = [3,"3"];
let raa:array_test = [1,2,3];

//classes
class c1 {
	public a = 3;
	public b = "3";
	public func() {}
}

class c2 extends c1 {
	public c = 3;
	public d = "3";
	public func2() {}

	//overloading
	public func(){}
}
//instance
let c1i = new c1();
let c2i = new c2();
c1i.b = "5"
c2i.b = "100";
c2i.d = c1i.b;


//class generic
class c3<T,E> {
	public a:T;
	public b:E;
	public func(a:T,b:E):E {return b}
}

//instance generic
let c3i = new c3<string,number>();
c3i.a = "3";
c3i.b = 4;
c3i.func("3",4);

//enums
enum e1 {
	a = 3,
	b = 4
}
enum strenum {
	one = "one",
	two = "two"
}

let enumval = e1.a;
let strenumval = strenum.two;

type multi_type = e1 | strenum | "two" | 4424 | boolean; //union of enum or value
let multi_type_val:multi_type = e1.a;
multi_type_val = strenum.two;
multi_type_val = "two";
multi_type_val = 4424;
multi_type_val = true;

//type with generics
type type_with_gen<T> = T | number;
let type_with_gen_val:type_with_gen<string> = 3;
type_with_gen_val = "3";

//interface
interface i1 {
	a: number;
	b: string;
}
interface i2 extends i1 {
	c: number;
	d: string;
}

class clsinterf implements i2 {
	public a = 3;
	public b = "3";
	public c = 3;
	public d = "3";
}

//abstract class
abstract class abscls {
	public a = 3;
	public b = "3";
	public abstract func():void;
}

//type checkings and casting
function type_checking(a:i1,b:i2) {
	//istypeof
	if (a instanceof clsinterf) {}
	
	//runtime checks
	let v = "obj";
	v += "ect";
	let tva = typeof a;
	if (tva == v) {}

	//cast
	let casted:object = b as i1; //implicit only downcast
}

//attributes and decorators
function attr() {}

[attr()] //special syntax for function
function fattr():void {}

function fdecor() {
	return function (target: any) {};
}

function vdecor() {
	return function (target: any) {};
}

class cattr {
	@fdecor()
	method() {}

	@vdecor()
	public a = 3;
}

//getters and setters
class cgetset {
	public a = 3;
	public get b() {return this.a}
	public set b(v) {this.a = v}
}

let cgs = new cgetset()
cgs.b = cgs.b + 3;

//static
class cstatic {
	public static a = 3;
	public static get b() {return this.a}
	public static set b(v) {this.a = v}
	public static funcstat() {return ""};
}

cstatic.b = cstatic.b + cstatic.a
cstatic.funcstat()