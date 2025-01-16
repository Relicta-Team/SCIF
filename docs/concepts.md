> [!WARNING]
> Концепты в этом разделе находятся на рассмотрении и доработке.


# Модули

Модули ограниченно поддерживаются в языковой среде.
Они предназначаются для разрешения зависимостей и линковки на этапе компиляции. Из модулей поддерживается 2 ключевых слова import и export. Код в root скоупе файла будет выполнен единожды при первом импорте. Это можно использовать для инициализации начальных состояний модуля либо выполнения проверок времени компиляции.

Полезная информация о модулях: 
	https://doka.guide/js/modules/
	https://metanit.com/web/javascript/19.1.php

```js
//file1.ts

export function func1(val:number) {print(val)}
export namespace Name {
	export var a = 3;
}

print("file1 inialized");

//main.ts

import { func1, Name } from "./file1"; //called file1 initialized once

function main() {
	func1(Name.a);
}
```

# Атрибуты

В стандартном ts существуют декораторы. Они применимы только к классам и членам методов.
Для реализации полезных особенностей в языковой среде существует поддержка атрибутов:

> [!WARNING]
> Требуется реализация атрибутов для методов (примеры для чего, например inline)

# Исключения

Обновлённая языковая среда поддерживает исключения. Помимо определений исключений в пользовательском коде исключения оборачивают:
1. Скриптовый планировщик
2. События виджетов

Для правильной обёртки событий виджетов нужно помнить, что некоторые события должны иметь возвращаемое значение при выбрасывании исключения. Допускается возможность добавления обработчика не выбрасывающего исключения, но это нужно указать явно при добавлении события.

Для оборачивания лямбда-функций на этапе компиляции потребуется просто встроить блок try-catch. В случае с передачей переменной необходимо сгенерировать уникальный блок по типу:

```js
//from
display.addEventHandler("KeyDown",codeRef)

//to 
display.setVar("evh_keydown_1",codeRef)
display.addEventHandler(
	"KeyDown",
	(args:...any[]) => {
		let retval = null;
		try {
			retval = args[0].getVar("evh_keydown_1").call(args);
		} catch (ex:Exception)
		{
			console.error(`Unhandled display exception: ${ex}`);
		}
		return retval;
	}
)

```

# Разрешение зависимостей

В старой версии кода важно соблюдать порядок определения модулей для следования зависимостям. В новой версии распределение модулей по порядку ложится на плечи компилятора.

В первую очеред соблюдается общее правило определения для кода:
1. функции
2. типы (классы + структуры) в упорядоченном виде
3. данные (переменные) принимающие литералы
4. вычисляемые переменные (те, которые в rvalue принимают выражение)

### Пример 1:
```js
//file1.ts
import {ns} from "file2"
func1() {ns.a = 5};
export var aref = ns.a;
getval() {return aref}

//file2.ts
import {func1,getval} from "file1"
func2() { func1() }
export namespace ns {
	export var a = getval();
}

//main
main()
{
	func2()
}
```

В данном случае образуется циклическая зависимость. Такого не должно появляться. Для решения проблемы нужно строить акцикличный граф и проверять наличие циклиеских зависимостей. В каждой функции хранятся данные какие переменные получаются.

Пример обычной зависимости:
```js
var b:any = geta();
var a = 34;
function geta() {return a}
```
Отсортированный вариант
```js
function geta() {return a}
var a = 34;
var b:any = geta();
```



# Динамическое определение типа

В случае когда нам неизвестен тип данных для операции 
```js
	let plRef = runtime.ccmpNative("_r = player; _r");
	let rv = plRef.getVar("nonvar",false)
```

Выражение getVar являлось бы вызовом функции:
`(["nonvar",false] call plRef)`

В таких случаях используется подход опреденеия операции времени выполнения:

```sqf
objOperMap = hashMap [
	...
	["getVar",{
		(_this select 0) getvariable (_this select 1)
	}]
];
opCall = {
	params ["_lvar","_opName","_argList"];
	if equalTypes(_lvar,objNull) exitWith {
		[_lvar,_argsList] call (objOperMap get _opName)
	};
	if equalTypes(_lvar,nullPtr) exitWith {
		callFuncReflectParams(_lvar,_opName,_argList)
	};
};
```

# Замыкания

> [!WARNING]
> Концепт не рекомендуется к реализации. При необходимости передачи контекста в функцию следует использовать ручной подход

Внутри локальных функций возможно использование внешних функций

```js
function test()
{
	let a = 1;
	let b = (x,y) => {
		let c = a; //a pass from parent scope
	};

	b(4,5);
}
```

Замыкания реализуются программно передавая список переменных в массиве. После обработки код в нативе будет выглядеть следующим образом:

```sqf
test = {
	private _a = 1;
	private _b = [{
		params ["_p","_ctx_"];
		_ctx_ params ["_a"];
		_p call {
			params ["_x","_y"];
			private _c = _a;
		};
	},[_a]];

	[[4,5],_b select 1] call (_b select 0);
};
```

Там где контекст не захватывает никаких переменных данная конструкция не будет создана

# Асинхронность

> [!CAUTION]
> Не доработано

Текущие вопросы:
- Передача контекста в асинхронном выполнении (переменные)
- Паузы в циклах

```js
async function test_async() { 
	print("started");
	sleep(5);
	print("before end");
	return 123;
}

let t = get_tick_time();
print("before asnyc");
await test_async();
print("after async " + get_tick_time_diff(t).toString());
```

```sqf
test_async = [{
	print("started");
	invokeAfterDelay(test_async select 1,5)
},
{
	print("before end");
	123
}];
...
```