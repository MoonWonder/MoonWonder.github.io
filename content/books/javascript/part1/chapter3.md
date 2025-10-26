---
title: Chapter3
subtitle:
date: 2025-10-26T21:32:27+08:00
description:
keywords:
draft: false
---

### 第 3 章 深入 JavaScript：搞定闭包、原型与 `this`

本章我们聚焦 JavaScript 的核心概念和一些 “奇妙” 特性，包括闭包、`this` 和原型继承。这些概念经常令初学者困惑，但对于有工程经验的你来说，只需一点类比就能豁然开朗。

**闭包（Closure）：函数里的 “小精灵”**  
如果你听过 “闭包” 这个词，可能会觉得高深莫测。其实闭包的原理可以打个比方：想象在函数内部藏了一个**记性很好的小精灵**，它能记住函数被定义时周围的环境（变量），即使函数执行完，这些变量也不会丢失。当日后再次调用这个内部函数时，这些被记住的变量仍然保持着当初的值，这种现象就叫闭包。

用正式一点的话说，**闭包是函数与其周围状态（词法环境）的组合** 。也就是说，闭包让一个函数可以访问并保留其词法作用域中的变量。当我们在 JavaScript 中定义函数时，每次都会创建闭包——函数本身和对外部变量的引用绑定在一起 

来看个例子体会闭包的威力：

```js
function createCounter() {
  let count = 0;
  return function() {
    count++;
    console.log("计数器：" + count);
  };
}
const counter = createCounter();
counter(); // 输出: 计数器：1
counter(); // 输出: 计数器：2
counter(); // 输出: 计数器：3
```

这里 `createCounter` 返回了一个内部函数。注意，`createCounter` 在第一次调用后，其内部局部变量 `count` 按理说应该随函数执行完毕而销毁。然而，由于内部函数引用了 `count`，闭包使得 `count` 的值被一直保留下来。每次调用 `counter()`，它都能访问和修改 `createCounter` 作用域中的 `count` 变量。闭包实现了一种**数据私有化**：`count` 对外不可见，却始终驻留在内部函数的作用域里。好一个忠诚勤劳的 “小精灵”！

闭包在 JavaScript 中非常常见。比如我们常用的事件监听器、定时器回调，都经常利用闭包保存一些状态。理解闭包有助于我们编写模块化的代码，例如实现私有变量、封装业务逻辑等。在调试时也要注意闭包可能导致的内存占用，因为被闭包引用的外部变量不会被垃圾回收，需要手动注意避免不必要的闭包引用。

**`this` 的多变与箭头函数：**  
JavaScript 的 `this` 关键字可谓 “千面娇娃”，在不同场景下扮演不同角色，让不少人直呼看不懂。这里我们总结 `this` 常见的指向规则：

*   **作为对象方法调用：** `obj.method()` 调用时，`method` 内部的 `this` 指向该对象 `obj`。例如：
    
    ```js
    const pet = {
      name: "旺财",
      speak: function() {
        console.log(this.name + "在叫：汪汪！");
      }
    };
    pet.speak(); // 输出: 旺财在叫：汪汪！
    ```
    
    上例中，`speak` 方法内的 `this` 即指向调用它的对象 `pet`。
    
*   **普通函数调用：** `func()` 直接调用一个函数（非作为对象属性），在非严格模式下函数内 `this` 默认指向全局对象（浏览器中是 `window`，Node 中是 `global`）；在严格模式下则为 `undefined`。比如：
    
    ```js
    function foo() {
      console.log(this);
    }
    foo(); // 非严格模式下输出 Window（全局对象）
    ```
    
    这一点和 C++/Java 的习惯很不同——它们没有类似的全局 `this` 概念。JavaScript 设计如此，主要历史原因是早期方便直接调用函数访问全局。
    
*   **构造函数调用：** 使用 `new Func()` 时，`Func` 内部的 `this` 被绑定到新创建的对象。例如：
    
    ```js
    function Person(name) {
      this.name = name;
    }
    const p = new Person("Tom");
    // 构造过程中 this 指向 p，赋值后 p.name === "Tom"
    ```
    
*   **`call/apply`/`bind` 强制绑定：** JavaScript 提供了 `func.call(thisArg, ...)` 和 `func.apply(thisArg, [...])` 来指定调用时的 `this`。还有 `func.bind(thisArg)` 可生成一个永久绑定 `this` 的新函数。比如：
    
    ```js
    function greet() { console.log("Hi, " + this.name); }
    const alice = { name: "Alice" };
    greet.call(alice); // 输出: Hi, Alice
    ```
    
    通过 `call` 我们把 `greet` 函数的 `this` 硬生生成了 `alice` 对象。
    

怎么样，是不是眼花缭乱 🤯？别急，ES6 的箭头函数在某种程度上帮我们简化了 `this` 问题。**箭头函数没有自己的 `this`**，它会捕获外层（定义时）环境的 `this` 值。这意味着在箭头函数内部访问 `this`，就是在访问外部上下文的 `this`。因此，箭头函数非常适合用作回调，以避免 `this` 被改变。例如：

```js
const team = {
  name: "勇士队",
  players: ["Stephen", "Klay"],
  showList: function() {
    this.players.forEach(player => {
      console.log(this.name + " 球员：" + player);
    });
  }
};
team.showList();
// 输出:
// 勇士队 球员：Stephen
// 勇士队 球员：Klay
```

如果不用箭头函数，而用普通匿名函数，`forEach` 内部函数的 `this` 将指向全局，无法访问到 `team.name`。箭头函数完美地保持了外部 `this`（即 `team` 对象）。正因如此，许多框架（如 React）中大量使用箭头函数来避免手动绑定 `this`。

你可以把 `this` 看作 JavaScript 里一个爱变装的角色，根据剧情需要（调用方式）换不同衣服。而箭头函数就像给 `this` 套上了保护壳，使它不受外界干扰。

**原型与继承：**  
在 JavaScript 中，一切几乎都是对象，对象之间通过**原型链**建立继承关系。不同于 Java/C++ 基于类（class）的继承模型，JavaScript 采用**原型继承**模型：每个对象都有一个 “隐藏属性” 指向它的原型对象（可以理解为模版对象），对象在查找属性时，如果自身没有会沿着原型链向上查找。

ES6 虽然引入了 `class` 关键字，但实际上只是语法糖，本质还是基于原型机制。例如：

```js
class Animal {
  speak() { console.log("Animal speaks"); }
}
class Dog extends Animal {
  speak() { console.log("Woof!"); }
}
let d = new Dog();
d.speak(); // 输出: Woof!
```

在底层，`Dog` 的原型继承了 `Animal` 的原型，实例 `d` 调用 `speak` 时，找到的是 `Dog.prototype.speak`；如果没有，则会沿原型链查找 `Animal.prototype.speak`。JavaScript 这套继承机制实现简单灵活，因此 **JavaScript 是典型的原型继承的面向对象语言**，不像 Java、C++ 等严格按类构造对象。

值得注意的是，你可以动态地给原型添加方法，影响所有继承该原型的对象。例如：

```js
function Person(name) {
  this.name = name;
}
Person.prototype.sayHi = function() {
  console.log("Hi, I'm " + this.name);
};
let p1 = new Person("Alice");
p1.sayHi(); // 输出: Hi, I'm Alice
let p2 = new Person("Bob");
p2.sayHi(); // 输出: Hi, I'm Bob
```

我们定义了构造函数 `Person` 及其原型方法 `sayHi`。两个实例 `p1`、`p2` 分别调用时，`this` 指向各自实例，输出各自的名字。可以看到，它们**共享**了原型上的同一个 `sayHi` 函数定义。这种机制节省内存并且灵活：可以在程序运行时修改 `Person.prototype.sayHi`，所有实例的方法行为将随之改变（在大型项目中这并不推荐，只作了解）。

概括来说，**原型继承**允许我们用对象去模版另一个对象，直接继承其属性和方法，不需要像类那样先定义抽象蓝图再实例化。这赋予了 JavaScript 极大的动态性。但对于习惯了 class 的开发者，刚接触可能会有些不适应。好消息是，ES6 `class` 让语法看起来更像传统类，方便面向对象思维的人使用。不过记住，其本质仍是原型链。

**小结：** 本章揭开了 JavaScript 一些核心概念的神秘面纱。**闭包**就像函数里驻守的 “小精灵”，使函数记住定义时的环境 ；**`this`** 则如同变装演员，根据调用场景变化多端，而箭头函数给它套上 “紧身衣”，固定了其指向；**原型继承**则是 JavaScript 面向对象的基石，与传统类继承各有千秋，却更为灵活。理解这些概念后，你将更游刃有余地编写复杂的 JavaScript 程序，并避免掉入常见陷阱。
