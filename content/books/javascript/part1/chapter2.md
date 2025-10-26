---
title: Chapter2
subtitle:
date: 2025-10-26T21:30:04+08:00
description:
keywords:
draft: false
---
### 第 2 章 JavaScript 语法速通：ES6+ 新特性

在上一章初步认识了 JavaScript，现在我们以幽默的方式来一场 “语法大串讲”，快速浏览现代 JavaScript（ES6 及以上）中的核心特性。你将看到，曾经让 Java 开发者头疼的繁琐代码，可以用几种巧妙的语法糖大幅简化。

**1. `let` 和 `const`：块级作用域与常量**  
在 ES6 之前，JavaScript 只有 `var` 用于声明变量，并且它的作用域规则十分怪异：`var` 是函数作用域或全局作用域，**不**受块级 `{}` 限制。这导致一些意料之外的行为。例如：

```js
for (var i = 0; i < 3; i++) {
  // ...
}
console.log(i);  // 居然还能访问到 i，输出 3，因为 var 没有块级作用域
```

ES6 引入了 `let` 关键字来声明块级作用域变量，以及 `const` 声明常量。`let` 定义的变量仅在定义它的 `{}` 内有效，避免了 `var` 提升和作用域污染的问题 ；`const` 则保证变量值不被重新赋值（但如果变量引用的是对象，仍可修改对象的属性）。

来看个例子体会差异：

```js
if (true) {
  var foo = "hello";
  let bar = "world";
}
console.log(foo); // 正常输出 "hello"
console.log(bar); // ReferenceError: bar is not defined (因为 bar 只在块内有效)
```

使用 `let` 可以有效杜绝很多由于作用域不当引起的 bug，大大提高代码可靠性。而 `const` 则鼓励我们多用常量、一旦赋值就不再改变，从而写出更可预测的代码。需要注意，`const` 只保证变量绑定不可变，但对于引用类型的数据，内部状态仍可更改，例如：

```js
const obj = { name: "Alice" };
obj.name = "Bob";   // 允许：修改对象属性
// obj = { age: 18 };  错误：不允许重新赋值新对象给 obj
```

**2. 箭头函数 (`=>`)：更简洁的函数表达式**  
JavaScript 经常需要编写回调函数，以前我们使用 `function` 关键字定义，语法比较冗长。ES6 引入了箭头函数，让我们可以用 `=>` 更简洁地定义函数。例如：

```js
// 传统匿名函数
[1, 2, 3].map(function(x) { return x * x; }); // 输出 [1,4,9]

// 箭头函数
[1, 2, 3].map(x => x * x); // 输出 [1,4,9]
```

是不是清爽不少？箭头函数不仅短小，而且**不会创建自己的 `this`**，它的 `this` 值由外层（定义时的作用域）决定 。这对处理回调中的 `this` 十分有用。例如：

```js
function Person() {
  this.age = 0;
  setInterval(() => {
    this.age++; 
    console.log(this.age);
  }, 1000);
}
new Person();
// 每隔1秒输出递增的年龄，因为箭头函数的 this 固定为外层 Person 实例
```

如果使用普通函数，`setInterval` 回调里的 `this` 会指向全局（或 undefined 严格模式下），需要用 `self = this` 等套路保存外部 `this`。箭头函数让代码既简洁又优雅地避免了 `this` 陷阱 。

需要注意的是，箭头函数不能用作构造函数（没有 `prototype`），也没有自己的 `arguments` 对象。但在多数回调场景，这不是问题。

**3. 模板字符串：字符串拼接如此顺滑**  
还记得 C++/Java 里繁琐的字符串拼接吗？在 JavaScript ES5 时代，我们也经常写：

```js
let name = "Alice";
console.log("Hello, " + name + "!");
```

ES6 提供了 **模板字符串** (Template Literals)，使用反引号 `` ` `` 包裹字符串，并以 `${...}` 插入变量或表达式。这样拼接字符串如同行云流水，一气呵成 ：

```js
let name = "Alice";
console.log(`Hello, ${name}!`);  // 输出: Hello, Alice!
```

模板字符串不仅可插入变量，还支持多行字符串而无需烦人的换行符：

```js
let poem = `窗前明月光，
疑似地上霜。`;  // 直接保留换行格式
```

可以说，模板字符串让字符串拼接像说相声抖包袱一样顺滑自然，告别了加号连接的凌乱。在需要动态构造 HTML 片段或控制台输出时，模板字符串简直是神器。

**4. 解构赋值与展开运算符：优雅地处理对象和数组**  
解构赋值（Destructuring）允许我们从数组或对象中一口气取出所需的数据，写法简洁直观

数组解构示例：

```js
const arr = [1, 2, 3];
const [first, second, third] = arr;
console.log(first, second, third); // 输出: 1 2 3
```

对象解构示例：

```js
const person = { name: "Bob", age: 25 };
const { name, age } = person;
console.log(name, age); // 输出: Bob 25
```

通过解构，我们避免了一一从对象取值的重复代码，使意图更加清晰。此外，解构在函数形参中也很有用：

```js
function greet({ name, age }) {
  console.log(`你好，${name}！你今年${age}岁了。`);
}
const user = { name: "小明", age: 18, id: 123 };
greet(user);  // 输出: 你好，小明！你今年18岁了。
```

上面直接将对象 `user` 解构为函数参数，额外的 `id` 属性被自动忽略，代码简明扼要。

展开运算符（Spread `...`）则让我们快速组合或克隆数组、对象。例如：

```js
let arr1 = [1, 2];
let arr2 = [...arr1, 3, 4];        // 展开 arr1，结果 [1,2,3,4]

let obj1 = { a: 1, b: 2 };
let obj2 = { ...obj1, b: 3, c: 4 }; // 克隆 obj1 并修改/增加属性，obj2 为 { a:1, b:3, c:4 }
```

展开运算符也用于函数调用，将数组变为参数序列，非常方便：

```js
Math.max(...[5, 8, 3]); // 等价于 Math.max(5,8,3)，结果 8
```

解构与展开让代码更为 “优雅”，常常可以一行搞定以前好几行的操作。

**5. 其他简洁之处：默认参数、`for...of` 循环**  
现代 JavaScript 还引入了许多小而实用的改进：

*   **默认参数值：** 定义函数时直接为参数指定默认值，避免再在函数体内写 `param = param || 'default'` 的逻辑。
    
*   **`for...of` 循环：** 优雅遍历数组（以及大部分可迭代对象），替代传统的 `for` 索引循环，代码更语义化。
    
*   **简洁对象字面量：** 当对象的属性名和变量名相同时，可以直接写 `{ foo, bar }` 代替 `{ foo: foo, bar: bar }`。
    
*   **箭头函数的隐式返回：** 箭头函数如果函数体直接是一个表达式，可省略花括号和 `return` 关键字，简化代码。
    

通过这一系列语法糖，JavaScript 终于甩掉了 “繁琐难用” 的古老形象，蜕变成一门可以写得很优雅的语言。对于有 C++/Java 背景的读者，你会发现很多 ES6+ 特性跟熟悉的概念暗暗契合：块级作用域、箭头函数类似于 C++ 的 lambda、模板字符串的用法和 Python 的 f-string 异曲同工。

**实战练习：ES5 与 ES6+ 比一比**  
理解语法不如实践。让我们把一段旧式 JavaScript 代码改写成现代风格，体会差异。例如，将一个数组中的数字翻倍并筛选出偶数：

_ES5 写法：_

```js
var arr = [1, 2, 3, 4];
var doubled = arr.map(function(x) {
  return x * 2;
});
var evens = doubled.filter(function(x) {
  return x % 2 === 0;
});
console.log(evens);
```

_ES6+ 写法：_

```js
const arr = [1, 2, 3, 4];
const evens = arr.map(x => x * 2).filter(x => x % 2 === 0);
console.log(evens);
```

可以看到，新语法让代码长度几乎减半、可读性却倍增。这对于大规模项目的维护性和开发效率都有极大帮助。

**本章小结：** 现代 JavaScript 提供了丰富的语法特性，使代码更加简洁、表达力更强。从 `let/const` 到箭头函数，从模板字符串到解构赋值，这些 ES6+ 特性极大地改善了开发者体验 。作为 C++/Java 开发者，你会发现很多概念似曾相识，但又更加灵活。不必担心一时记不住所有语法糖，在后续实践中你将反复用到它们，自然就运用自如了。
