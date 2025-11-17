---
title: 静态站点生成与动态路由
subtitle: 构建博客列表
date: 2025-11-13T09:09:21+08:00
description:
keywords:
draft: true
---

通过前面章节，我们已经可以开发静态页面并实现客户端交互了。但现代 Web 应用往往需要与数据交互，呈现动态内容。本章将深入讲解 Next.js 的**静态站点生成 (Static Site Generation, SSG)**，并结合**动态路由**实现一个简单博客模块，演示如何预渲染带参数的多页面应用。

**静态站点生成 (SSG)：** Next.js 提供了预渲染页面的两种方式：SSG 和 SSR。SSG 发生在构建时（build time），Next.js 会在打包阶段运行指定函数获取数据，生成静态 HTML 文件。这样生成的页面在每次请求时无需重新渲染，直接由服务器或 CDN 返回现成 HTML，因而**加载极快**且**非常利于 SEO**。

要在 Next.js 页面启用 SSG，需要导出一个异步函数 `getStaticProps`。Next.js 构建时将调用它，获取页面所需的数据作为 props 注入页面组件。一个最简单的例子：

```ts
// pages/hello.tsx
export async function getStaticProps() {
  return {
    props: { message: "静态生成的问候语" }
  };
}
export default function HelloPage({ message }) {
  return <div>{message}</div>;
}
```

构建后，`/hello` 路径就会有一个静态页面，内容为 “静态生成的问候语”。如果这个信息来自数据库或文件，那么构建时 Next.js 会连同数据一起生成 HTML。

**动态路由与 `getStaticPaths`：** 上面例子是单页静态数据。如果我们有一组数据，各自需要独立的页面（如多篇博客文章），就需要用动态路由来生成多个静态页面。Next.js 使用 `getStaticPaths` 函数配合动态路由文件，共同实现这一功能。

步骤：

1.  创建动态路由页面文件。如 `pages/posts/[id].tsx`，表示文章详情页，路径中有变量 `id`。
    
2.  在该文件中，导出 `getStaticPaths` 函数。该函数需要返回一个包含若干 `paths` 的对象，每个 `path` 对应一个可生成的动态路由，以及一个 `fallback` 设置。
    
    例如：
    
    ```ts
    export async function getStaticPaths() {
      const paths = [
        { params: { id: '1' } },
        { params: { id: '2' } }
      ];
      return { paths, fallback: false };
    }
    ```
    
    表示在构建时要预先生成 `/posts/1` 和 `/posts/2` 两个页面，且其他未列出的 id 将返回 404（因为 fallback: false）。
    
3.  同时在页面文件中还要导出 `getStaticProps(context)` 函数，用于针对每个路径获取数据。Next.js 会对每个 `paths` 调用一次 `getStaticProps`，传入的 context.params 包含动态参数，例如 `{ id: '1' }`。
    
    例如：
    
    ```ts
    export async function getStaticProps({ params }) {
      const data = await fetch(`https://example.com/posts/${params.id}.json`);
      return { props: { post: data } };
    }
    ```
    
    这样，构建时会获取 id=1 的文章数据注入页面，生成 `/posts/1` 静态 HTML，同理生成 `/posts/2`。
    

通过 `getStaticPaths` 和 `getStaticProps` 的配合，Next.js 能够在构建阶段**批量生成**带参数的静态页面。这非常适合博客、产品展示等内容相对固定的网站。

**实战：构建博客列表和详情页**  
让我们模拟开发一个简单博客模块。我们有几篇示例文章的数据，使用静态生成技术创建列表页和若干详情页。

*   首先，准备数据源。为简单起见，我们在项目中新建文件 `data/posts.json`，内容：
    
    ```json
    [
      { "id": 1, "title": "Next.js 入门", "content": "欢迎学习 Next.js 全栈开发！" },
      { "id": 2, "title": "拥抱 TypeScript", "content": "在 Next.js 中使用 TypeScript 提升安全性和开发体验。" }
    ]
    ```
    
    假设实际应用中数据来自 CMS 或数据库，这里用 JSON 文件代替。
    
*   创建博客列表页：在 `pages` 下新建 `posts/index.tsx`。作为列表页，它将列出所有文章标题并链接到详情页。
    
    ```ts
    import Link from 'next/link';
    import posts from '../../data/posts.json';
    
    export async function getStaticProps() {
      // 此处直接读取本地 JSON 数据，真实场景可从数据库/API 获取
      return { props: { posts } };
    }
    
    interface Post { id: number; title: string; }
    interface Props { posts: Post[]; }
    
    export default function PostsPage({ posts }: Props) {
      return (
        <div>
          <h1>博客列表</h1>
          <ul>
            {posts.map(post => (
              <li key={post.id}>
                <Link href={`/posts/${post.id}`}><a>{post.title}</a></Link>
              </li>
            ))}
          </ul>
        </div>
      );
    }
    ```
    
    这里我们在 `getStaticProps` 中导入了本地 JSON 列表，将其作为 props 提供给页面组件。页面组件遍历 posts 数组，生成链接列表。`<Link href={/posts/${post.id}}>` 指向对应详情页路径。
    
*   创建博客详情页：新建文件 `pages/posts/[id].tsx`。这是动态路由页面，每篇文章一个路径。
    
    ```ts
    import posts from '../../data/posts.json';
    
    export async function getStaticPaths() {
      // 从数据源获取所有文章的id列表
      const paths = posts.map(post => ({
        params: { id: post.id.toString() }
      }));
      return { paths, fallback: false };  // 未列出的id均返回404
    }
    
    export async function getStaticProps({ params }) {
      const postId = parseInt(params.id);
      const post = posts.find(p => p.id === postId);
      return { props: { post } };
    }
    
    interface Post { id: number; title: string; content: string; }
    interface Props { post: Post | undefined; }
    
    export default function PostPage({ post }: Props) {
      if (!post) return <div>文章不存在</div>;
      return (
        <div>
          <h1>{post.title}</h1>
          <p>{post.content}</p>
        </div>
      );
    }
    ```
    
    这里 `getStaticPaths` 将我们的示例数据列表转换成 paths 数组，例如 `[{ params: { id: '1'}}, { params: { id: '2'}}]`，表示构建 `/posts/1` 和 `/posts/2` 两个静态页面。`fallback: false` 表示除此之外的路径直接返回 404。
    
    `getStaticProps` 则根据 `params.id` 找到对应文章对象，并将其传入页面。页面组件简单展示文章标题和内容。这里有个基本的错误处理：若根据 id 没找到文章，则返回一个 “文章不存在” 的提示。
    
*   将博客列表页链接纳入导航：修改 `_app.tsx` 增加导航项：
    
    ```ts
    <Link href="/posts"><a class>博客</a></Link>
    ```
    
    现在导航栏多了 “博客” 入口。
    
*   运行 `npm run build` 进行生产构建，然后 `npm start` 运行，或在开发模式下直接查看。访问 `http://localhost:3000/posts`，会看到博客列表页列出了两篇文章标题。点击任意标题，跳转到对应详情页面，URL 如 `/posts/1`，页面显示文章内容。这些详情页都是构建时预生成的静态页面，刷新时也无需请求后台，速度非常快。
    

**SSG 还是 SSR？**  
看到这里，你可能想问：既然 SSG 这么好，是不是任何场景都用 SSG？实际上需要权衡。SSG 适合内容改动不频繁或可接受一定延迟更新的场景，比如博客、文档网站等。一旦生成，所有用户访问都是静态文件，可以承受巨大流量。但对于更新频繁或需要个性化的页面，SSR 或客户端渲染可能更合适。

Next.js 也支持**增量静态再生成 (ISR)**，即在构建后按需重新生成过期的静态页面，这可以兼顾性能和内容新鲜度。但具体细节较复杂，这里不展开。

**小结：** 本章通过开发博客模块，展示了 Next.js 静态站点生成和动态路由的使用。我们利用 `getStaticProps` 在构建时获取数据，并通过动态路由与 `getStaticPaths` 预生成了多篇文章页面。这种方式让应用既保留了 React 的动态开发体验，又能享受静态页面的性能优势。**静态生成的页面加载快、SEO 友好，非常适合内容型网站**。下一章我们将讨论服务端渲染（SSR），看看在需要实时数据的场景下 Next.js 如何应对，让你学会根据需求选择合适的渲染模式。
