---
title: 页面路由与导航
subtitle: Next.js 的文件路由机制
date: 2025-11-13T08:27:54+08:00
description:
keywords:
draft: false
---

在传统的后端开发中，我们经常需要配置 URL 路由，例如使用注解或 XML 来映射 URL 到处理函数。而在 Next.js 中，这件事情变得简单优雅得多——**文件即路由**。本章我们将详解 Next.js 的页面路由机制，以及如何在页面之间实现无刷新的导航。

**文件路由概念：** 正如第 6 章所述，Next.js 使用 `pages` 目录结构来自动生成路由。规则如下：

*   `pages/index.tsx` 对应站点根路径 `/`。
    
*   `pages/about.tsx` 对应 `/about` 路径。
    
*   可以通过创建子文件夹形成嵌套路由，例如 `pages/blog/list.tsx` 会对应 `/blog/list`。
    
*   **动态路由**：文件名中包含方括号表示动态参数。例如 `pages/posts/[id].tsx` 匹配 `/posts/任意值` 的路径，其中 `id` 是参数名。本章后面我们先聚焦静态路由，动态路由在第 10 章详细介绍。
    
*   特殊文件：`pages/404.tsx` 会被用作自定义 404 页面，`pages/_app.tsx` 用于自定义顶级应用组件等。
    

这种基于文件和目录的路由方式，让我们只要依据项目结构组织页面文件，就自动拥有相应的 URL，无需像 React Router 那样编写额外的路由配置代码。

**新增页面示例：** 假设我们要为网站添加一个 “关于我们” 页面。只需在 `pages` 目录下新建 `about.tsx`，内容写一个简单的 React 组件：

```ts
// pages/about.tsx
export default function About() {
  return <h1>关于我们</h1>;
}
```

保存后，运行开发服务器并访问 `http://localhost:3000/about`，你将看到 “关于我们” 的标题。这就是 Next.js 文件路由的魅力所在——新增页面就像创建普通文件一样简单，路径命名也一目了然，极大提高了开发效率和可维护性。

**导航链接：** 有了多个页面，我们需要在页面之间跳转。虽然可以使用传统 `<a href="/about">` 标签，但这样会导致浏览器刷新重载，无法发挥单页应用的优势。Next.js 提供了内置的 `<Link>` 组件，实现客户端路由跳转，无需刷新。

使用方法：

```ts
import Link from 'next/link';

function Navbar() {
  return (
    <nav>
      <Link href="/"><a>首页</a></Link>
      <Link href="/about"><a>关于我们</a></Link>
    </nav>
  );
}
```

把这个导航组件放在 `_app.tsx` 或每个页面，点击链接时，Next.js 拦截点击事件，使用 HTML5 History API 修改 URL 并加载目标页。由于 Next.js 会预先为页面打包代码，客户端跳转非常快，且不会整页刷新，保持 SPA (单页应用) 的流畅体验。

请注意，使用 `<Link>` 时，其子元素通常是一个 `<a>` 标签用于显示文本（如上例所示）。Next.js 要求 `<Link>` 内必须有一个可点击元素。在 Next.js 12 以后，如果不给 `<Link>` 子元素，会出现 Warning，因此推荐像以上这样写完整的 `<Link href="..."><a>文本</a></Link>` 结构。

**客户端导航 vs 服务端导航：** Next.js 智能地处理 `<Link>` 导航：如果目标页面已经预取（prefetch）过，则立刻渲染页面组件；否则会通过 fetch 请求后台获取对应页面的代码 / 数据，然后呈现。整个过程由 Next.js 框架打理，开发者无需手动操心。**相比传统多页应用，Next.js 的页面切换几乎感觉不到刷新，体验和单页应用一样顺滑**。

> 提示：Next.js 默认会在空闲时预取页面链接，因此当某个链接出现在视口内时，其对应页面代码已经在后台加载了。这就是为什么点击 `<Link>` 导航常常是瞬间完成的原因。

**路由总结：**

*   Next.js 基于约定的文件系统路由，大幅减少了路由配置工作，结构清晰 。
    
*   静态路由创建非常简单，动态路由使用方括号语法代表参数（我们稍后章节详解）。
    
*   内置 `<Link>` 组件提供了无刷新导航能力，应始终优先使用。
    
*   如果需要编程式导航（如表单提交后跳转），Next.js 也提供了 `useRouter` 钩子，可调用其中的 `router.push('/target')` 方法实现，与 `<Link>` 效果一致。
    

**实践：为示例站点添加导航菜单**  
继续扩展我们的示例应用（上一章的待办清单）。我们为首页和 “关于” 页之间添加导航。修改 `_app.tsx`：

```ts
// pages/_app.tsx
import type { AppProps } from 'next/app';
import Link from 'next/link';
import '../styles/globals.css';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <div>
      <nav style={{ padding: '10px', borderBottom: '1px solid #ccc' }}>
        <Link href="/"><a style={{ marginRight: '15px' }}>首页</a></Link>
        <Link href="/about"><a>关于我们</a></Link>
      </nav>
      <Component {...pageProps} />
    </div>
  );
}
export default MyApp;
```

这里我们简单使用内联样式做了一个横向导航栏，将其包裹在每个页面内容上方。现在启动开发服务器，在首页你会看到导航菜单，点击 “关于我们” 链接，无刷新地跳转到 about 页面；再点“首页”，又回来。整个过程中页面状态（如我们的待办列表）会根据需要重建或保留，Next.js 默认会卸载旧页面组件、挂载新页面组件，因此不同页面间不存在组件实例的共享。

**注意：** 如果需要跨页面保留状态，如做音乐播放器这种场景，可以利用 `_app.tsx` 将状态提升到顶层应用，从而不同页面共用。但大多数普通情况，每次页面切换组件会重建，需重新获取数据或初始化状态。

至此，我们已经掌握 Next.js 文件路由的基本用法，并亲手实践了页面导航。**Next.js 将繁琐的路由配置隐藏在约定之下，让开发者专注于页面本身**。这种理念和 Ruby on Rails 等后端框架的 “约定优于配置” 类似，降低了上手难度。下一章我们将进一步美化页面样式，引入流行的 Tailwind CSS 框架，为应用增添亮丽的外观。
