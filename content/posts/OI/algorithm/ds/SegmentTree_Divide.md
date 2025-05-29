---
author: "MoonWonder"
author_link: "moonwonder.top"
title: "SegmentTree_Divide"
date: 2021-02-13T11:22:34+08:00
lastmod: 2021-02-13T11:22:34+08:00
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

## 线段树分治

有的时候我们会碰到一类数据结构问题，它需要我们支持往集合中插入一个元素、删除一个元素、询问三个操作。如果我们发现，插入一个元素时信息很容易维护，但删除一个元素时就不那么容易了，那么我们可以考虑线段树分治，来离线解决这类在线算法不那么优秀的数据结构题。

线段树分治，说白了就是按照时间轴建一棵线段树。容易发现集合中每个元素存活的时间是一个区间。于是考虑对线段树上每一个节点建立一个 vector。对于每个元素在线段树上递归，如果发现该元素的存活时间区间完全覆盖了当前节点所表示的区间就直接将该元素的编号插入当前节点的 vector 中，否则就按照线段树区间查询的套路将大区间拆成左右两个小区间分别递归即可。最后一遍 dfs，递归到某个节点 \(x\) 的时候就将 \(x\) 的 vector 中的元素的贡献计算出来并分别递归左右儿子节点，如果是叶子节点就直接输出答案，回溯的时候撤销贡献即可。

伪代码大致长这样：

``` cpp
void iterate(int k){

	for(int i=0;i<s[k].v.size();i++){
		int x=s[k].v[i];
		计算 x 的贡献
	}
	if(s[k].l==s[k].r) 输出答案
	else iterate(k<<1),iterate(k<<1|1);//递归左右儿子
	撤销贡献

}
```
