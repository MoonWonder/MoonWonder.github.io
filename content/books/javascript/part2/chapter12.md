---
title: 构建后端 API
subtitle: Next.js API 路由实战
date: 2025-11-17T17:53:47+08:00
description:
keywords:
draft: false
---

除了页面，Next.js 还能充当后端服务器，编写 API 接口供前端调用。这意味着使用 Next.js，我们无需另起一个 Express/Koa 服务，就能在同一项目里完成前后端开发。本章介绍 Next.js 的 **API Routes** 用法，并通过实战演练构建一个简单的留言提交接口，体验前后端一体化的开发流程。

**什么是 API Routes？** Next.js 提供了一个特殊的路由机制：在 `pages/api` 目录下创建的文件会被视为后端路由，每个文件对应一个 HTTP 接口路径 。这些接口由 Node.js 在服务端运行，可以处理请求、读写数据库、验证权限等，就像常规后端一样。不同的是，我们不用设置服务器监听端口、路由解析，这些 Next.js 都自动帮我们做了。

API Route 文件默认导出一个处理函数，函数签名类似 `(req, res) => { ... }`，与 Node.js 原生的 HTTP 模块或 Express 中的中间件风格一致。例子：

```ts
// pages/api/hello.js
export default (req, res) => {
  res.status(200).json({ message: "Hello API" });
};
```

这个接口对应路径 `/api/hello`，收到任意请求就返回 JSON `{ message: "Hello API" }`。Next.js 会自动为其提供 `req` 和 `res` 对象（实际上是 Node.js HTTP IncomingMessage 和 ServerResponse 对象），让我们可以像写 Express 一样处理请求。因为这些代码只在服务器执行，我们可以安全地接触数据库秘钥等敏感信息，不会泄露给客户端。

**构建留言提交接口：** 现在，我们动手创建一个简单的留言 API，并在前端页面调用它，实现留言的提交和反馈。

1.  **创建 API Route 文件：** 新建 `pages/api/feedback.ts`：
    
    ```ts
    import type { NextApiRequest, NextApiResponse } from 'next';
    
    interface Feedback {
      id: number;
      text: string;
    }
    
    let feedbacks: Feedback[] = [];  // 用内存数组暂存留言（演示用，实际应存数据库）
    
    export default function handler(req: NextApiRequest, res: NextApiResponse) {
      if (req.method === 'POST') {
        const { text } = req.body;
        if (!text) {
          res.status(400).json({ error: '留言内容不能为空' });
        } else {
          const newFeedback = { id: Date.now(), text };
          feedbacks.push(newFeedback);
          res.status(200).json({ message: '提交成功', feedback: newFeedback });
        }
      } else if (req.method === 'GET') {
        res.status(200).json({ feedbacks });
      } else {
        res.status(405).json({ error: '方法不被允许' });
      }
    }
    ```
    
    这段代码实现了一个简单的反馈接口：
    
    *   如果客户端发送 `POST` 请求，我们从请求体 `req.body` 提取 `text`（需要确保请求头 `Content-Type: application/json`，Next.js 自动会解析 JSON body），如果留言为空返回 400 错误，否则创建一个反馈对象存入内存数组，并返回成功消息和刚添加的反馈。
        
    *   如果收到 `GET` 请求，则返回所有反馈列表。
        
    *   对于其他请求方法（PUT/DELETE 等），返回 405 方法不允许。
        
    
    我们用一个全局变量 `feedbacks` 模拟存储，为简单起见不引入数据库。需要注意的是，在无服务器架构中全局变量不会持久保存，但 Next.js API Route 运行在 Node.js 服务上，存在期间内存数据会一直保留。不过**别依赖这种行为在生产环境存数据**，这里仅作演示。
    
2.  **创建前端页面来提交留言：** 新建 `pages/feedback.tsx`：
    
    ```ts
    import { useState } from 'react';
    
    export default function FeedbackPage() {
      const [text, setText] = useState('');
      const [response, setResponse] = useState<string | null>(null);
    
      const handleSubmit = async () => {
        try {
          const res = await fetch('/api/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
          });
          const result = await res.json();
          if (res.ok) {
            setResponse(`✅ ${result.message}`);
          } else {
            setResponse(`❌ 错误: ${result.error}`);
          }
        } catch (err) {
          setResponse('❌ 提交失败，请重试');
        }
      };
    
      return (
        <div>
          <h1>留言板</h1>
          <textarea
            rows={4}
            value={text}
            onChange={e => setText(e.target.value)}
            placeholder="写下你的留言..."
          />
          <br />
          <button onClick={handleSubmit}>提交留言</button>
          {response && <p>{response}</p>}
        </div>
      );
    }
    ```
    
    这个页面有一个文本框和提交按钮。点击按钮时，使用 `fetch` 向我们刚写的 `/api/feedback` 接口发起 POST 请求。注意这里 `fetch` 的 URL 直接写相对路径 `/api/feedback` 即可，因为 Next.js 前后端同域部署，无需填写域名。我们设置请求头 `Content-Type: application/json` 并传送 JSON 字符串 body。然后等待响应，根据 `res.ok` 判断是否成功，分别设置不同的反馈信息到 state。`response` state 用于显示提交成功或失败的提示。
    
3.  **将留言板入口加入导航：** 更新 `_app.tsx`：
    
    ```ts
    <Link href="/feedback"><a class>留言板</a></Link>
    ```
    
    这次我们将 “留言板” 放在导航最后，没有 `mr-6`（可以根据喜好加）。
    
4.  **测试功能：** 运行开发服务器，进入 http://localhost:3000/feedback 页面。输入一些文字，点击提交。如果输入为空，接口会返回错误提示（红❌）；输入不为空，应看到 “提交成功” 提示（绿✅）。此时我们的 `feedbacks` 数组也加入了一条数据。如果你打开 http://localhost:3000/api/feedback 用 GET 方法访问，可以看到接口返回的所有 feedback 列表 JSON，其中包括刚刚提交的留言。
    
    由于我们没有实现持久存储，所以刷新页面会导致反馈列表丢失（内存重置）。但如果使用数据库，那么通过 Next.js API route 写一个类似的 CRUD 接口，可以完成标准的增删改查操作。
    

**API Routes vs 独立后端：**  
对于简单项目，Next.js API 足以胜任，并且带来前后端同构的便利（同一个代码库共享类型、工具链等）。但对于非常复杂的后端服务，可能还是拆分出去更合理。Next.js API Routes 主要适合于**中小型项目的后端需求**或**前端特定的轻量后端服务**（如对接第三方 API、简单表单处理等）。你完全可以在 API Route 里引入任何 Node.js 包，如数据库驱动、ORM 等，实现完整功能。

值得一提的是，Next.js 还支持 **Serverless 模式** 部署，其 API Routes 会被当作无状态函数独立部署。这种模式下每个请求都会新实例化函数，像我们上例使用全局变量存数据就不起作用了。因此**别在 API Route 中依赖内存状态**，最好把数据存在外部 DB 或缓存中。

**小结：** 本章我们运用 Next.js API 路由机制，构建了一个前后端交互的小功能。通过在 `pages/api` 下创建文件并编写请求处理逻辑，我们实现了一个留言提交接口。前端页面使用 `fetch` 调用该接口，完成了数据的提交和反馈。这个流程展示了 Next.js 真正的 “全栈” 能力：**一个框架同时搞定了浏览器端界面和服务器端 API**。对于开发者来说，不用在多个项目间来回切换，大幅提升了效率。在后续实际项目中，你可以依据需求添加更多 API 路由，如用户登录、表单提交、获取数据列表等，实现完整的后端功能。至此，第二部分的内容告一段落，你已经初步掌握 Next.js 的核心机制：页面路由、预渲染、样式、数据获取、以及 API 后端开发。在下一部分，我们将进入综合实战，运用这些技能开发一个完整的 Next.js 在线商城应用。
