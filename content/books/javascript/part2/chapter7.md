---
title: React 组件基础
subtitle: 在 Next.js 中构建 UI
date: 2025-11-13T08:23:14+08:00
description:
keywords:
draft: false
---

熟悉 Next.js 必须先补一点 React 知识。毕竟 Next.js 是建立在 React 之上的。在本章，我们快速介绍 React 组件的核心概念：**组件、状态 (State)、属性 (Props)**，并通过实际编码体验在 Next.js 中构建前端 UI 的基本方法。

**React 组件是什么？** 可以把 React 组件理解为 UI 界面的积木块。每个组件描述了界面上可重用的一部分，并且可以像函数一样接受输入（即属性）并返回要在页面上展示的元素结构。

在 Next.js 中，每个页面其实就是一个 React 组件（导出默认组件）。除此之外，我们还可以在 `components/` 目录中创建许多可重用的 “小” 组件，然后在页面组件中组合使用。

来看一个最简单的 React 组件定义（使用函数式组件）：

```js
// components/Hello.js
export default function Hello(props) {
  return <h1>你好，{props.name}！</h1>;
}
```

这个组件名为 `Hello`，通过 `props.name` 显示一个问候语。我们可以在页面中使用它：

```ts
// pages/index.tsx
import Hello from '../components/Hello';
export default function Home() {
  return <Hello  />;
}
```

页面渲染结果将是一个 `<h1>` 标签，上面写着 “你好，小明！”。这里，`<Hello />` 就像使用 HTML 标签一样，是我们的自定义组件。属性 作为输入传给组件，在组件内部通过 `props.name` 获取。**这体现了 React 组件的第一个关键点：组件 = 渲染结果 (UI) = f(props)**。给定相同的 props，组件应返回相同的界面结构。

**状态 (State) 与事件处理：** 除了由外部传入的数据（Props），组件还可以有自己的内部状态，这就是 State。状态使组件可以记住信息并根据用户交互而改变。一个经典例子是计数器组件，每点击一个按钮计数加一：

```ts
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0); // 声明一个状态变量 count，初始值0
  return (
    <div>
      <p>当前计数：{count}</p>
      <button onClick={() => setCount(count + 1)}>增加</button>
    </div>
  );
}
```

这里我们用了 React 的 Hook **`useState`** 来声明状态变量。`useState(0)` 返回一个数组：第一个元素是当前状态值（初始为 0），第二个是更新状态的函数。每当点击按钮，我们调用 `setCount(count + 1)` 更新状态。React 会自动重新渲染组件，展示新的计数值。整个过程不需要我们手工操作 DOM，React 内部会高效地计算出需要更新的部分，然后更新界面。

读者可能会想，这和 Java/C++ 的 GUI 框架很像，但实现方式有区别：React 采用**声明式 UI** 思想，我们只需声明当状态为某值时界面长什么样。至于状态变化后如何高效更新 DOM，React 的 Diff 算法会搞定。而传统 GUI 需手动更新界面，每次状态改变都要指挥界面怎么变化。这也是 React 让开发者省心的原因之一。

**属性 (Props) vs 状态 (State)：** 两者的区别常被问到。简而言之：

*   **Props** 是组件对外的数据接口，由父组件传入，组件自身无法修改（类似函数参数）。
    
*   **State** 是组件自己管理的数据，只能在组件内部初始化和更新，外部组件不能直接修改它。
    

一句话区分：Props 是**外部赋值**，State 是**内部自有** 。两者任一发生变化，都会触发组件重新渲染。

**事件绑定：** 上例中按钮的点击事件采用了 JSX 的语法 `onClick={函数}` 绑定。需要注意在 React 中，以 `on` 开头的大驼峰属性（如 onClick, onChange）就是绑定相应事件的监听函数。不同于原生 DOM 的事件，React 内部会做一层合成，提供一致的事件对象，且不用担心事件兼容性。

**React JSX 简介：** 你可能注意到，我们的组件返回值写的是类似 HTML 的标记 `<div>...</div>`。这其实是 **JSX** 语法（JavaScript XML），是 React 推荐的定义 UI 的方式。JSX 允许我们在 JavaScript 代码中直接书写类似 HTML 的结构，使代码可读性大大提升。JSX 最终会被编译成普通的 JavaScript 对象描述（React.createElement 调用），所以浏览器并不直接执行 JSX。你可以把 JSX 理解为一种**模板语言和 JavaScript 的混合体**，在 JSX 中使用 `{}` 包裹任意 JS 表达式，十分灵活。

例如：

```js
const name = "Next.js";
const element = <h1>欢迎学习 {name}！</h1>;
```

JSX 会被转译为等价的 `React.createElement('h1', null, '欢迎学习 ', name, '！')` 调用。

Next.js 默认支持 JSX/TSX 语法，无需额外配置。只要你编写 `.jsx` 或 `.tsx` 文件，就能使用 JSX 来描述组件结构。

**实战：构建一个简单的互动组件**  
我们来练习创建自己的组件并在 Next.js 页面中使用。目标是实现一个简单的待办事项清单组件，可以添加任务并在列表中显示。

1.  在 `components/` 下新建 `TodoList.tsx`：
    
    ```ts
    import { useState } from 'react';
    
    interface Todo {
      id: number;
      text: string;
    }
    
    export default function TodoList() {
      const [todos, setTodos] = useState<Todo[]>([]);
      const [input, setInput] = useState("");
    
      const handleAdd = () => {
        if (!input.trim()) return;
        const newTodo: Todo = { id: Date.now(), text: input.trim() };
        setTodos([...todos, newTodo]);
        setInput("");
      };
    
      return (
        <div>
          <h3>待办事项</h3>
          <ul>
            {todos.map(item => (
              <li key={item.id}>{item.text}</li>
            ))}
          </ul>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="输入新任务"
          />
          <button onClick={handleAdd}>添加</button>
        </div>
      );
    }
    ```
    
    这里我们用了两个状态：`todos` 保存任务列表数组，`input` 保存当前输入框内容。每次点击 “添加” 按钮，会将输入框的文本作为新任务加入列表（前提是非空）。列表通过 `todos.map` 映射为 `<li>` 展示。输入框用 `onChange` 事件更新 `input` 状态，实现双向绑定。
    
2.  打开 `pages/index.tsx`，在默认导出的组件中引入并使用 `TodoList`：
    
    ```ts
    import TodoList from '../components/TodoList';
    
    export default function Home() {
      return (
        <div>
          <h1>我的待办</h1>
          <TodoList />
        </div>
      );
    }
    ```
    
3.  保存文件，切换到浏览器查看结果。现在首页应该显示 “我的待办” 标题，下方有输入框和 “添加” 按钮。试着输入一些文字并点击“添加”，它们会立即出现在下方列表中。我们的交互式组件生效了！整个过程中，无需刷新页面，React 根据状态变化自动高效地更新了 DOM。
    

这个小例子说明了在 Next.js 中编写 React 组件与在普通 React 项目中并无二致。Next.js 为我们配置好了一切，直接投入编码即可。同时也展现了 React 的 “响应式 UI” 思维：界面随状态而动，开发者不需要手工操作页面元素。

**与 C++/Java GUI 框架的不同：**  
如果你有使用 Qt、Swing 之类的经验，会发现 React 的编程模式相当 “声明式”。我们没有手工创建控件对象，也没有指定布局管理，而是通过 JSX 直接声明界面结构。交互上，我们没有注册监听函数去直接操作其他组件，而是调用 `setState` 更新状态值，React 根据新状态重新渲染需要变动的部分 UI。这种模式初学时有些抽象，但一旦习惯，会觉得省心很多。正如 React 的口号：“把界面看作状态的函数”，数据决定界面如何呈现。

**本章小结：** 我们学习了 React 组件的基础，以及在 Next.js 中如何组织和使用组件。掌握了**组件**的概念，理解 **props** 和 **state** 的作用，你就具备了构建动态用户界面的能力。React 的出现改变了前端开发范式，通过组件化和声明式 UI，复杂的交互变得易于管理。随着你对组件的理解加深，将能创造出更丰富的界面。在接下来的章节中，我们会把组件、状态等技能应用到 Next.js 项目各处，打造出功能完备的应用界面。
