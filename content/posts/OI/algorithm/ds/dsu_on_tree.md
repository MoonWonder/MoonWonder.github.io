---
author: "MoonWonder"
author_link: "moonwonder.top"
title: "dsu_on_tree"
date: 2021-02-09T19:03:41+08:00
lastmod: 2021-02-09T19:03:41+08:00
draft: false
description: ""
license: ""

tags: []
categories: []
hiddenFromHomePage: false

featuredImage: ""
featuredImagePreview: ""

toc: true
autoCollapseToc: true
lightgallery: true
linkToMarkdown: true
share:
  enable: true
comment: true
---

## 算法介绍

启发式合并，顾名思义，就是根据人类直观的感受对已有算法的优化。譬如冰茶姬的启发式就是对于两个大小不一样的集合，我们大小小的并到大的，这样就可以有效地将冰茶姬的深度控制在 $\log n$ 级别（或许这就是树上启发式合并中那个"dsu"的来历吧）。

树上启发式合并的思想也与之类似。树上启发式合并，俗称 dsu on tree，是一种解决子树问题的离线算法，不允许修改。它能在 $\mathcal O(nT\log n)$ 的复杂度内离线维护某个子树内的信息，其中 $T$ 是加入一个节点的复杂度，一般为 $\mathcal O(1)$ 或 $\mathcal O(\log n)$。

那么树上启发式合并究竟该怎样应用呢？先考虑一个问题：一棵树上每个节点有一个颜色，求每个点的子树中所有节点中不同颜色的个数。

考虑一个最暴力的做法，从根开始 dfs，再维护一个桶 $c_x$ 表示颜色 $x$ 出现的次数。在 dfs 某个节点 $u$ 的过程中，先 dfs 它的所有儿子 $v$ 求出其儿子的答案，每次 dfs 完之后清空桶。然后将 $u$ 子树内所有点都加入桶中统计答案。

这样显然是错误的，一条链就可以把它卡成 $n^2$。但我们注意到 dfs 完某个节点 $u$ 后，有且只有 $u$ 的子树中的节点被加入桶中。回忆当年学树链剖分的时候对重儿子的定义，考虑以此入手对我们的算法进行一个小小的优化：

1.  dfs $u$ 的所有轻儿子 $v$，统计 $v$ 的答案，并清空桶。
2.  dfs $u$ 的重儿子 $son_u$，不清空桶。显然此时有且只有 $son_u$ 子树中的点被加入了桶中。
3.  dfs 一遍 $u$ 的轻儿子 $v$，将 $v$ 的子树内的节点加入桶中。
4.  计算出 $u$ 的答案。

为什么这样复杂度就对了呢？考虑每个点会被 dfs 多少次。对于每个点到根节点的路径，每出现一条轻边就会导致该点被多 dfs 一次，故一个节点 dfs 的次数与其到根节点的路径上轻边的个数同阶。而在学树链剖分我们知道一个点到根节点的路径上的重链个数是 $\log n$ 级别的，故个点到根节点的路径上轻边的个数也是 $\log n$ 级别的，复杂度 $n\log n$。

最后解释一下为什么它被称作"启发式合并"。对于每个点 $u$，设其子树的集合为 $T_1, T_2, T_3, \dots, T_k$，那么 dsu on tree 的本质实际上是将 $T_1, T_2, \dots, T_k$ 的信息合并起来，而借鉴启发式合并的思想，我们选出 $|T_i|$ 的 $i$，并将其它集合的信息都合并到 $T_i$ 中。所以说树上启发式合并本质上是用 dsu 启发式合并的思想解决多集合的合并问题。

最后给出伪代码：

``` cpp
void calcans(int x,int f){//计算答案
	for(int e=hd[x];e;e=nxt[e]){
		int y=to[e];if(y==f||y==wson[x]) continue;
		calcans(y,x);消除y的贡献
	}
	if(wson[x]) calcans(wson[x],x);//dfs重儿子
	把x的贡献合并进去
	for(int e=hd[x];e;e=nxt[e]){
		int y=to[e];if(y==f||y==wson[x]) continue;
		把y的子树内所有节点的贡献合并进去
	}
    记录答案
}
```

## 例题

### CF600E

@import "../../problems/CF600E.md" {line_begin=69 line_end=72}

@import "../../problems/CF600E.md" {line_begin=74 }
