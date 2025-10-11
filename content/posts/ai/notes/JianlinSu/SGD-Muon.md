---
title: SGD Muon
subtitle:
date: 2025-08-26T20:34:14+08:00
draft: false
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
lastmod: 2025-09-21T14:21:09+08:00
---

读科学空间博客 流形上的最速下降 系列的笔记。

<!--more-->
### 前置知识：
$msign(M)=U\times V^T$，其中 $M=U\Sigma V^T$ 为 SVD 分解。

像Adagrad、RMSprop、Adam等自适应学习率优化器的特点是通过除以梯度平方的滑动平均的平方根来调整每个参数的更新量，这达到了两个效果：1、损失函数的常数缩放不影响优化轨迹；2、每个参数分量的更新幅度尽可能一致。Muon正好满足这两个特性：

$$msign(M)=(MM^T)^{-\frac{1}{2}}M=M(M^TM)^{-\frac{1}{2}}$$

如果不可逆取伪逆。

可以发现当 $M$ 为对角阵时 Muon 退化为 SignSGD

### 笔记：
1. SGD+超球面
  1. 优化器可以转换为找到一个满足一定要求（原文中是 $ 度量\leq x $ ）向量，且因为这个要求使得这个向量是好求的。
  2. 在前面向量变 $度量 \leq x$ 的基础上再加上要求，$\delta$ 向量与原向量垂直。这样就能满足原向量的模长不变。
2. Muon+正交
