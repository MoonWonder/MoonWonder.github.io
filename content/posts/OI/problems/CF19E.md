---
tags: 
  - 二分图
  - 最近公共祖先,LCA
  - 差分
  - Notebooks/OI/OJ/Luogu
title: CF19E-Fairy
date: '2021-01-06 21:43:14.891509'
modified: '2021-01-06 21:43:14.891550'
math: true
---
# CF19E-Fairy
## 题目:
### 题目描述:
Once upon a time there lived a good fairy A. One day a fine young man B came to her and asked to predict his future. The fairy looked into her magic ball and said that soon the fine young man will meet the most beautiful princess ever and will marry her. Then she drew on a sheet of paper $ n $ points and joined some of them with segments, each of the segments starts in some point and ends in some other point. Having drawn that picture, she asked the young man to erase one of the segments from the sheet. Then she tries to colour each point red or blue so, that there is no segment having points of the same colour as its ends. If she manages to do so, the prediction will come true. B wants to meet the most beautiful princess, that's why he asks you to help him. Find all the segments that will help him to meet the princess.
### 输入格式:
The first input line contains two integer numbers: $ n $ — amount of the drawn points and $ m $ — amount of the drawn segments ( $ 1<=n<=10^{4},0<=m<=10^{4} $ ). The following $ m $ lines contain the descriptions of the segments. Each description contains two different space-separated integer numbers $ v $ , $ u $ ( $ 1<=v<=n,1<=u<=n $ ) — indexes of the points, joined by this segment. No segment is met in the description twice.
### 输出格式:
In the first line output number $ k $ — amount of the segments in the answer. In the second line output $ k $ space-separated numbers — indexes of these segments in ascending order. Each index should be output only once. Segments are numbered from 1 in the input order.
### 样例:
#### 样例输入1:
```
4 4
1 2
1 3
2 4
3 4

```
#### 样例输出1:
```
4
1 2 3 4 
```
#### 样例输入2:
```
4 5
1 2
2 3
3 4
4 1
1 3

```
#### 样例输出2:
```
1
5 
```
## 思路:

## 实现:
```cpp
// Problem: CF19E Fairy
// Contest: Luogu
// URL: https://www.luogu.com.cn/problem/CF19E
// Memory Limit: 250 MB
// Time Limit: 1500 ms
// Author: Ybw051114
//
// Powered by CP Editor (https://cpeditor.org)

#include "ybwhead/ios.h"
const int maxn = 1e5 + 10;
vector<pair<int, int>> e[maxn];
void add(int u, int v, int w)
{
    e[u].pb(pii(v, w));
}
int n, m;
int vis[maxn];
int dis[maxn];
int cnt, sp, s[maxn];
int ee[maxn];
int dfs1(int u)
{
    vis[u] = 1;
    for (auto v : e[u])
    {
        if (!vis[v.first])
        {
            dis[v.first] = dis[u] ^ 1;
            ee[v.second] = 1;
            dfs1(v.first);
        }
        else if (!ee[v.second])
        {
            ee[v.second] = 1;
            if (dis[u] == dis[v.first])
            {
                cnt++, s[u]++, s[v.first]--;
                sp = v.second;
            }
            else
                s[u]--, s[v.first]++;
        }
    }
}
int ans[maxn], tot;
int dfs(int u)
{
    vis[u] = 1;
    for (auto v : e[u])
    {
        if (!vis[v.first])
        {
            dfs(v.first);
            if (s[v.first] == cnt)
                ans[++tot] = v.second;
            s[u] += s[v.first];
        }
    }
}
int main()
{
    yin >> n >> m;
    for (int i = 1; i <= m; i++)
    {
        int u, v;
        yin >> u >> v;
        add(u, v, i), add(v, u, i);
    }
    for (int i = 1; i <= n; i++)
        if (!vis[i])
            dfs1(i);
    if (!cnt)
    {
        yout << m << endl;
        for (int i = 1; i <= m; i++)
            yout << i << " ";
        return 0;
    }
    memset(vis, 0, sizeof(vis));
    for (int i = 1; i <= n; i++)
        if (!vis[i])
            dfs(i);
    // cout << cnt << endl;
    if (cnt == 1)
        ans[++tot] = sp;
    sort(ans + 1, ans + tot + 1);
    yout << tot << endl;
    for (int i = 1; i <= tot; i++)
    {
        yout << ans[i] << " ";
    }
    return 0;
}
```
