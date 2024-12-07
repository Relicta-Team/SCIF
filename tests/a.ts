
import { B } from "./b"
import * as cref from "./cfold/c"

export class A {
	method_a() {return ""}
	varx(){}
}
var t = 0;
//var obj = new MediaStream()
var x = new Object()
x.test_objMethod()
var int:number = 3

var nmb = new String("")
nmb.test_strMethod()
var cls = new NonClass()


int.dataGet()

//not exist tests
var obj = new MediaStream()
obj.getTracks()
var telem = document.getElementById("id")

int.components = 5;

var v = new B()
v.method_b()

var temp = cref.bref;

var cx = new cref.C()