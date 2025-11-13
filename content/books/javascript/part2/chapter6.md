---
title: 初识 Next.js
subtitle: 项目搭建与开发环境
date: 2025-11-13T08:19:11+08:00
description:
keywords:
draft: false
---

终于来到本书的重头戏 —— Next.js 全栈框架。Next.js 是由 Vercel 开发的基于 React 的前后端同构框架，提供了开箱即用的服务端渲染（SSR）、静态生成（SSG）、API 路由等功能。可以说，Next.js 将原本需要自行搭建的 React 应用架构、服务端渲染配置等都帮你封装好了，让我们能专注于业务逻辑的编写。

**Next.js 定位：** 你可以把 Next.js 看作是一个**全栈式的 React 框架**，既能构建浏览器端的界面，又能处理服务器端的渲染和 API 请求。对于熟悉后端的读者来说，这意味着用 Next.js 可以一个人写前端页面、写后端接口，甚至直接部署整套应用，非常高效。

Next.js 有如下核心特点：

*   **文件式路由：** 在 `pages/` 目录下创建 React 组件文件，就自动成为对应路径的页面，免去手动配置路由的麻烦。
    
*   **预渲染支持：** 支持**静态站点生成**和**服务端渲染**，对于 SEO 和初始加载性能非常有利。
    
*   **内置 API 路由：** 在 `pages/api/` 下创建文件即可定义后端接口（Node.js 环境运行），方便地与前端页面集成。
    
*   **开发体验佳：** 自动代码分割、Fast Refresh 热更新、内置支持 CSS 模块和 Sass 等，让开发 React 应用如虎添翼。
    
*   **部署便利：** 尤其部署到 Vercel 平台时，一键即可上线，更有针对 Next.js 的优化。
    

听起来相当诱人吧？下面我们开始实际体验 Next.js。首先需要安装 Node.js（上一章已介绍）以支持 Next.js 的运行。然后使用官方脚手架工具 `create-next-app` 初始化一个 Next.js 项目。

**创建 Next.js 项目：** 打开终端，输入：

```sh
npx create-next-app@latest hello-next --typescript
```

这将使用最新版本的脚手架，在当前目录下创建名为 `hello-next` 的项目，并已集成 TypeScript。根据提示进行选项选择（或者直接在命令中加上 `--typescript` 强制 TS 模板）。项目创建完毕后，进入目录：

```sh
cd hello-next
npm run dev
```

稍等片刻，终端提示开发服务器启动在 `http://localhost:3000`。用浏览器访问该地址，你会看到 Next.js 的默认欢迎页面。这说明我们的 Next.js 应用已经成功跑起来！🎉

**Next.js 项目结构：** 打开项目文件夹，你会发现一个很清晰的结构：

```
hello-next/
├── pages/            # 页面目录
│   ├── index.tsx     # 默认首页，对应路径 "/"
│   ├── about.tsx     # 示例页面，对应路径 "/about"
│   └── api/          # API 路由目录
│       └── hello.ts  # 示例API接口，对应 "/api/hello"
├── public/           # 公共静态文件（可直接通过 URL 访问）
│   └── vercel.svg    # 示例资源文件
├── styles/           # 样式文件目录
│   ├── Home.module.css  # 首页组件对应的模块化CSS
│   └── globals.css     # 全局CSS
├── components/       # 组件目录（可能需要自行创建）
├── next.config.js    # Next.js 配置文件
└── package.json      # 项目依赖配置
```

*   `pages` 目录最重要，其中的 React 组件文件会自动映射为应用路径。例如 `pages/index.tsx` 是首页，`pages/about.tsx` 对应 `/about` 路径。Next.js 利用这个约定，实现了无需手动配置的文件式路由系统，非常高效。
    
*   `pages/api` 目录内的文件则被认为是后端接口，URL 以 `/api/文件名` 访问。例如项目自带的示例接口 `/api/hello`，返回一段 JSON 数据 。
    
*   `public` 目录下的文件可直接通过 `http://localhost:3000/文件名` 访问，不需要特殊处理，常用来放置图片、favicon 等静态资产。
    
*   其它如 `styles`、`components` 目录没有特殊规则，仅用于组织代码结构。
    

**修改页面内容：** 为了熟悉开发流程，我们做个小实验：打开 `pages/index.tsx`（这是一个 React 组件），将其中 `<h1>` 标签内的文本改为 `"Hello Next!"`。保存文件，切换到浏览器页面，神奇的事情发生了——页面内容自动刷新，显示出我们修改后的文字！😯 这就是 Next.js 带来的开发者体验：内置的 **Fast Refresh** 功能在检测到代码更改后，自动局部刷新页面并保留组件状态，所见即所得，开发效率极高。

**服务端渲染效果：** Next.js 默认对所有页面使用**预渲染**（预先生成 HTML）。在开发模式下体现不明显，但我们可以验证一下：查看浏览器页面的源代码（View Page Source），你会发现首页的 HTML 中已经包含了我们组件渲染后的静态内容，而不仅仅是一个空壳。对于传统 React 应用，初始 HTML 通常是空白，需要 JavaScript 加载后再填充。而 Next.js 在服务器端就已经把页面内容算好，直接发送给浏览器。这对搜索引擎优化（SEO）和首屏加载速度非常有帮助。

**配置与脚本：** Next.js 项目在 `package.json` 中定义了一些有用的 npm 脚本：

*   `npm run dev`：启动开发服务器（无需每次编译，保存自动热更新）。
    
*   `npm run build`：构建项目（进行优化、打包，生成静态产物用于生产环境）。
    
*   `npm run start`：运行上一条构建出的应用（生产模式）。
    

在开发阶段，你主要使用 `npm run dev`。当准备部署上线时，运行一次 `build`，然后用 `start` 在服务器上跑即可。Next.js 内置了优化步骤，包括代码压缩、树摇优化等，确保最终上线的代码体积小、性能高。

**小结：** 本章我们成功创建并运行了一个 Next.js 项目。你学到了 Next.js 的核心定位：**一个集成了 React 前端和 Node.js 后端的同构框架**。它的文件路由机制让页面组织更直观，内置的预渲染提升了性能和 SEO，开发体验也因热刷新而如沐春风。通过修改页面内容，你体验了 Next.js 开发的便捷。接下来我们将深入 Next.js 的各个方面，包括使用 React 组件构建 UI、页面路由与导航、样式设计、数据获取等，为实战做准备。

