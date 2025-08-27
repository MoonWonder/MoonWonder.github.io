---
title: SGD Muon
subtitle:
date: 2025-08-26T20:34:14+08:00
draft: true
author:
  name:
  link:
  email:
  avatar:
description:
keywords:
license:
comment: true
weight: 0
tags:
  - optimize
  - math
categories:
  - notes
hiddenFromHomePage: false
hiddenFromSearch: false
hiddenFromRelated: false
hiddenFromFeed: false
summary:
resources:
  - name: featured-image
    src: featured-image.jpg
  - name: featured-image-preview
    src: featured-image-preview.jpg
toc: true
math: false
lightgallery: false
password:
message:

# See details front matter: https://fixit.lruihao.cn/documentation/content-management/introduction/#front-matter
---

读科学空间博客 流形上的最速下降 系列的笔记。

<!--more-->

1. SGD+超球面
  1. 优化器可以转换为找到一个满足一定要求（原文中是 $ 度量\leq x $ ）向量，且因为这个要求使得这个向量是好求的。
  2. 在前面向量变 $度量 \leq x$ 的基础上再加上要求，$\delta$ 向量与原向量垂直。这样就能满足原向量的模长不变。
2. Muon+正交
