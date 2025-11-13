---
title: 初探 TypeScript
subtitle: 给 JavaScript 加上类型安全
date: 2025-11-13T08:13:22+08:00
description:
keywords:
draft: false
---

学完了 JavaScript，你也许会开始想念 C++/Java 那样严谨的类型检查：“动态类型确实灵活，但要是能有个机制在编译期帮我发现类型错误就好了。” 别急，TypeScript 正是为此而生。本章介绍 **TypeScript** —— JavaScript 的超级 “变形金刚”：它在 JavaScript 基础上增加了静态类型检查等特性，相当于给 JavaScript 强化了静态类型系统。

**TypeScript 是什么？** 简单来说，TypeScript（简称 TS）是 JavaScript 的**静态类型超集**，最终会被编译成纯 JavaScript 在浏览器或 Node.js 中运行 。换言之，**任何合法的 JavaScript 代码也是合法的 TypeScript 代码**，但 TS 加入了类型注解、接口、泛型等特性，帮助开发者在编码阶段就发现潜在错误 。

用一句话总结：> **TypeScript = JavaScript + 静态类型支持** 。

举个例子，JavaScript 允许以下 “离谱” 操作发生而不报错：

```js
let user = { name: "Alice" };
console.log(user.age.toFixed(2));
```

这段代码中，`user` 对象根本没有 `age` 属性，`user.age` 是 `undefined`，但 JavaScript 在运行时才会发现错误（尝试读取 `undefined.toFixed` 导致 TypeError）。而 TypeScript 则可以在编译阶段就指出问题所在：

```ts
interface User { name: string; age: number; }
let user: User = { name: "Alice", age: 25 };
console.log(user.age.toFixed(2));
// 假如我们错误地写了 user.heigth：
// Error: Property 'heigth' does not exist on type 'User'. Did you mean 'height'?:contentReference[oaicite:37]{index=37}
```

如上，TypeScript 通过**接口 (Interface)** 定义了 `User` 的结构，要求必须有 `name` 和 `age`。如果我们访问了不存在的 `heigth` 属性，TS 编译器立即报错，提示我们可能拼写错了 `height`。这样一来，许多 JavaScript 在运行时才暴露的问题，可以提前在编码时避免。

**静态类型检查：** TS 让我们可以在变量和函数上添加类型注解。例如：

```ts
function add(x: number, y: number): number {
  return x + y;
}
let sum: number = add(5, 3);
// add("hello", 4);  // 错误：参数类型不匹配
```

这里我们声明函数 `add` 接受两个 `number` 返回 `number`，TS 会确保只能传入数字。如果像注释中那样传入字符串，将在编译时报错，而无需等到运行时报错。对于大项目而言，静态类型检查如同一个可靠的安全网，帮我们捕获了许多潜在 bug，提高了代码的健壮性 。

**接口与类：** TypeScript 提供了接口来定义对象的类型结构。例如上面的 `interface User` 定义了用户对象应该有哪些属性及类型。接口有点类似于 Java 中的接口或 C++ 中的 struct，但 TypeScript 的接口是**形状（结构）匹配**的，只要对象具有接口要求的形态，就认为符合该接口（这称为 “鸭子类型”）。这比 Java 严格的名义类型更灵活。

TS 也支持 `class` 语法，并且可以用 `implements` 关键字让类实现接口、用 `extends` 继承父类。对你来说，这些概念几乎与 Java 如出一辙，只不过**底层仍是通过原型继承**。比如：

```ts
interface Animal { name: string; speak(): void; }

class Dog implements Animal {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
  speak(): void {
    console.log(`${this.name} 汪汪！`);
  }
}
```

上例中我们定义了 Animal 接口，然后 Dog 类实现它。一旦写错函数签名或属性类型，TS 编译器会立即指出。在这一点上，TypeScript 带来的安心感与 Java 颇为类似。

**泛型（Generics）：** 如果你熟悉 Java/C++ 的模板或泛型，那么 TS 的泛型语法也非常友好。例如，实现一个泛型函数来返回传入参数（即 “恒等函数”）：

```ts
function identity<T>(value: T): T {
  return value;
}
let num = identity<number>(123);  // 推断 T 为 number，num 类型为 number
let str = identity("abc");        // 类型推断 T 为 string，str 类型为 string
```

上述 `<T>` 就是泛型参数，调用时可以手动指定类型，也可让编译器自动推断。泛型让我们编写可重用的组件，支持多种类型而不丢失类型信息。例如 Java 中的集合类在 TS 里也可以用泛型实现。

**工具类型与类型推断：** TS 还有很多强大特性，例如**联合类型**（用 `|` 表示多个可能类型）、**类型别名**、**内置工具类型**（如 Partial、Pick 等用于变换类型）等等。这些高级特性让 TypeScript 的类型系统具备相当的表达力，甚至可以进行简单的类型级编程。虽然初学者不必一下掌握所有，但知道这些能力存在有助于你理解 TS 的强大。

**在现有代码中引入 TypeScript：** TypeScript 可渐进式采用。你可以先把 JavaScript 文件改名为 `.ts`，然后逐步为关键模块添加类型注解，编译器会根据需要推断剩余部分的类型。对于大型旧项目，可先在 tsconfig 中开启 `allowJs` 以兼容 JS 文件，再慢慢重构为 TS。TypeScript 兼容 JavaScript，所以完全可以平滑过渡。

**开发体验提升：** 使用 TypeScript 的另一个显著好处是开发工具的智能提示更准确丰富。VS Code 等编辑器会在你键入代码时依据类型信息给出补全和文档提示。这种**自文档化**的代码让协作更加高效。一些低级错误（如属性名拼写错误、参数类型不匹配）也会在保存时就被红色波浪线标出，让你即时修正，而不用等运行出错再回溯。

**实战改造：** 让我们把第 3 章的 `createCounter` 函数改写成 TypeScript 风格试试：

```ts
function createCounter(): () => void {
  let count: number = 0;
  return function() {
    count++;
    console.log("计数器：" + count.toFixed(0));
  };
}
const counter = createCounter();
counter();
counter();
// 以上 TS 编译通过，行为与之前相同
```

我们给 `count` 注明类型为 number，`createCounter` 函数签名也指明返回值是一个无参、无返回的函数。整个逻辑保持不变，但代码意图对阅读者和编译器都更加明确。如果一不小心写错属性名或类型，TS 会立即提示，让我们放心许多。

**小结：** TypeScript 为 JavaScript 注入了静态类型的强心针，弥补了大型项目中动态类型可能导致的不足。通过 TS，Java/C++ 开发者熟悉的类型注解、接口、泛型等概念都能在前端世界重现 。当然，TypeScript 的出现并非要完全替代 JavaScript，而是在开发阶段提供工具支持，编译后仍输出标准的 JavaScript 代码以兼容所有环境。你大可以把 TS 当作写好了会自动 “翻译” 成 JS 的高级语言。在后续章节中，我们将使用 TypeScript 来开发 Next.js 应用，相信有了类型系统的保驾护航，你的全栈开发之路会更加顺畅、安全。
