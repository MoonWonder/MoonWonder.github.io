---
title: 服务端渲染：实时数据页面开发
subtitle:
date: 2025-11-17T17:38:25+08:00
description:
keywords:
draft: true
---


上一章我们学习了静态生成，对于不常变化的数据非常有效。但如果页面需要**每次请求都拿最新数据**（例如股票行情、当天新闻等），静态页面在构建后就变得陈旧，不再适用。这时就需要用到 Next.js 的另一种预渲染模式：**服务端渲染 (Server-Side Rendering, SSR)**。本章我们探讨 SSR 的用法，并结合实例实现一个简单的实时数据页面。

**SSR vs SSG：** SSG 在构建时生成页面，而 SSR 则是在**每次请求时**生成页面。也就是说，当用户请求一个 SSR 页面，Next.js 服务器会先运行页面的 `getServerSideProps` 函数获取数据，然后和 React 组件一起渲染出 HTML 返回给客户端。由于数据现查现用，SSR 页面总是最新的。当然成本是每次都要等待服务器处理，响应时间相对静态页面会稍慢一些。此外，SSR 页面无法直接部署到纯静态托管，需要 Node.js 服务器支持。

Next.js 中要实现 SSR，只需在页面组件中导出 `getServerSideProps` 而不是 `getStaticProps`。它的用法基本相同，只不过**每次请求都会调用**。举例：

```ts
export async function getServerSideProps(context) {
  const res = await fetch('https://api.example.com/data');
  const data = await res.json();
  return { props: { data } };
}
```

页面组件接收到 `data` 渲染即可。Next.js 知道有这个函数存在，会在每个请求触发它，并且**永远不缓存页面**（除非你自己做缓存）。

**实践：创建新闻播报页面**  
假设我们要开发一个 “今日新闻播报” 页面，每次有人访问都显示最新的新闻列表。为简单起见，使用一个免费新闻 API 或自己模拟数据。

*   在 `pages` 下新建 `news.tsx`：
    
    ```ts
    export async function getServerSideProps() {
      const res = await fetch('https://api.example.com/news/today');
      const newsList = await res.json();
      return { props: { newsList } };
    }
    
    interface News { title: string; url: string; }
    interface Props { newsList: News[]; }
    
    export default function NewsPage({ newsList }: Props) {
      return (
        <div>
          <h1>今日新闻</h1>
          <ul>
            {newsList.map((news, index) => (
              <li key={index}>
                <a href={news.url} target="_blank" rel="noopener noreferrer">
                  {news.title}
                </a>
              </li>
            ))}
          </ul>
        </div>
      );
    }
    ```
    
    这里 `getServerSideProps` 每次都会请求外部新闻 API，获取当天新闻数据。我们将其传入组件，渲染成链接列表（在新窗口打开）。
    
*   增加导航入口方便访问：修改 `_app.tsx`：
    
    ```ts
    <Link href="/news"><a class>新闻</a></Link>
    ```
    
    保存，运行 `npm run dev` 观察效果。如果没有真实 API，可以把 fetch 换成读取本地模拟 JSON 的逻辑。访问 `http://localhost:3000/news`，可以看到新闻列表。尝试刷新页面，每次 `getServerSideProps` 都会运行，从服务端获取（模拟的）最新数据并渲染。查看页源码，会发现 HTML 中已经包含了新闻列表内容（SSR 已经输出了完整 HTML）。
    
*   进一步，你可以在网络面板观察请求：当访问 `/news` 时，浏览器收到的是一个 HTML 文档，包含我们渲染好的列表；而点导航进入其他页面再返回新闻页时，Next.js 可能会走客户端路由机制，通过 API fetch 数据然后客户端渲染（具体行为由 Next.js 内部策略决定）。但不论如何，对最终用户而言，内容都是最新的。
    

**SSR 注意事项：**

1.  **数据获取时间**：SSR 会增加页面首字节 (TTFB) 时间，因为要等服务器取完数据才能响应。因此应尽量优化 `getServerSideProps` 内部逻辑，避免做太多无关计算。
    
2.  **缓存与性能**：默认 SSR 每次都全新渲染。如果一些数据并非每秒变化，合理利用缓存可极大提高性能。例如可以在 `getServerSideProps` 里自己实现简易缓存，或借助外部缓存中间件。Next.js 也允许通过 Response Header 控制浏览器或 CDN 缓存策略。
    
3.  **上下文参数**：`getServerSideProps(context)` 提供请求相关信息，如 `context.query` (URL 查询参数), `context.params` (动态路由参数), `context.req`/`res` (Node.js 请求响应对象) 等。你可以利用这些，做例如权限校验、重定向等操作。返回值除了 `{ props: {...} }`，还可以返回 `{ redirect: { destination: '/login', permanent: false } }` 实现服务端重定向用户去登录等。
    
4.  **安全性**：因为 SSR 代码在服务器运行，可以安全地使用秘钥访问数据库等。不过需要注意不要把敏感信息放在返回的 props 里，因为那些最终会发送给浏览器。
    

**SSR 还是 CSR？**  
有人可能问：“SSR 已经解决了服务端获取数据问题，那为什么还需要前端自己 fetch 数据？” 实际上，两者可以并存。**CSR（客户端渲染）** 依然适用于某些需要高度交互或对首屏要求不高的场景，比如一个需要用户操作后才显示数据的组件，就完全没必要用 SSR。Next.js 建议的模式是：尽量用 SSG 提升性能，必要时用 SSR 获取实时数据，其他交互再使用 CSR。这种混合模式能在性能和动态性之间取得平衡。

**总结：** 本章我们学习了 Next.js 的服务端渲染，通过 `getServerSideProps` 实现了每次请求动态获取数据并渲染页面。SSR 非常适合展示实时更新或个性化的内容，因为它能够拿到请求上下文并返回最新数据。然而，其性能相对静态内容较差，要根据具体场景慎重选择。Next.js 为我们封装好了 SSR 机制，我们只需专注于获取数据和渲染逻辑即可。到此，你已经掌握 Next.js 两大预渲染模式 (SSG & SSR)，在全栈开发中可根据需求灵活运用，打造出既快又智能的应用。
