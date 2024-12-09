
# Языковые требования

Для преобразования потребуется модифицировать исходный код:
- все выражения глобального пространства обернуть в функцию-инициализатор. В некоторых языках нет возможности выполнения кода в модулях.
- переменные не должны инициализироваться в выполняемом контексте
- в хедерах для правильной конверсии перечислений добавить спецификаторы


# Спецификаторы аннотаций

| specificator | description | example |
| --- | --- | --- |
| decl() | спецификатор типа (функции или переменной). Для юнионов используется косая черта. Для перечисления параметров используется точка с запятой. | decl(int) testvar = 3;<br/>decl(int(float|int;bool)) testfunc = {params["_num","_boolval"]};
| enum() | спецификатор перечисления макроопределений | enum(ENUM_PREFIX_)<br/>#define ENUM_PREFIX_A 1<br/>#define ENUM_PREFIX_B 2
| namespace() | спецификатор пространств имён. Нужен для сопоставления типов переменных | namespace(module)<br/>module_var1 = 3;<br/>module_var2 = ""; 


## decl

int - variable
int[] - static array (onedim)
int[][] - static array (2 dim)
Array<int> - tuple

# Встроенные типы

- int - целое число
- float - дробное число
- string
- bool 
- code
- void - nulltype or any

Containers:
ref - reference type (array wrapper)
array - default array type
map - native hashmap
set - native hashset

Variable storage support:
- mesh - gameobject
- actor - visualized unit
- display 
- widget

OOP:
- object - location-based type
- struct - hashmap based object

Other:
- thread_handle - internal thread handle
- text - structured text
- config - internal config values
- namespace_storage - missionamespace/

# Компиляция в натив

весь код преобразуется в нативное представление для максимальной оптимизации. Все переменные и функции имеют укороченные имена-идентификаторы.

Код компилируется в объектные файлы (каждый модуль отдельная единица).
Это нужно для hot-reload функциональности а также инкрементальной сборки.

```sqf
//module1.sqf
#define hashcodePath1_NAMESPACE_VAR 

hashcodePath1_NAMESPACE_VAR = 1;

//module2.sqf
#define hashcodePath2_NAMESPACE_VAR

hashcodePath2_NAMESPACE_VAR = 2;
```

После компиляции происходит линковка модулей:
```sqf
//addressation
#define hashcodePath1_NAMESPACE_VAR x00001
#define hashcodePath2_NAMESPACE_VAR x00002

//runtime
hashcodePath1_NAMESPACE_VAR = 1;
hashcodePath2_NAMESPACE_VAR = 2;
```

# Доступ к нативному коду

Для доступа к данным на основе названия идентификаторов используется специальная таблица ассоциаций символов.
Например мы написали переменную

```js
var someTestNumber = 1;
```

При компиляции в натив код выглядит следующим образом:

```sqf
//src\location\constnum.sqf
x424 = 1; //424 is unical id of variable
_symtab set ['someTestNumber','x424']; //_symtab defined outside
```

Для доступа снаружи вне контекста выполняемого кода:

```
//загружаем скомпилированный модуль
_modulePtr = ["src\location\constnum.sqf"] call loadModule; //return dict["symbols","runtime"]
_num = [_modulePtr,"someTestNumber"] call moduleGetVal;
[_modulePtr,"someTestNumber",_num + 1] call moduleSetVar;

```

Для доступа в рантайме с помощью глобальной таблицы символов: 

```sqf

_ptr = symtab get "someTestNumber";
missionnamespace getvariable _ptr;

```
Так как в рантайме такой поход может понадобится только внутри биндингов renode то производительность не будет проблемой.


# Регистрозависимость

### Переменные
Так как все переменные генерируются со своими уникальными идентификаторами то тут нет проблем с регистрами.

### Структуры
У структур (hashmapobject) члены являются элементами словаря. Они по умолчанию регитсрозависимы.

### Классы
Классы не регистрозависимы (однако реализовать регистрозависимость можно в будущем)