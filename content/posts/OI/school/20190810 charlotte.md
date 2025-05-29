---
categories:
- OI
- 省中集训
- 20190810
date: "2019-08-29 01:50:59.239"
modified: "2019-08-29 07:07:15.735"
tags:
- 结论
- 省中集训
title: 20190810 夏洛特——charlotte

---

# 20190810 夏洛特——charlotte

### 思路：

设$Dis=A到B的哈曼顿距离$,$T=Tb-Ta$

1. 如果$T<Dis$,则一定不能到达直接输出$No$

2. 如果$T=Dis$,则一定能到达,输出$Yes$

3. 如果$T>Dis$,分为两类:

​ 如果$T-Dis$为偶数,则多余的路程可以来回走动,最后一定恰好能到达

​ 如果$T-Dis$为奇数,则一定不能通过来回走动消耗多余路程,一定到达不了

最后只要按照Ti排序,检查相邻两个点是否合法即可

### 代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
template <typename T> inline void read(T &F)
{
    F=0;int R=1;char CH=getchar();
    while(!isdigit(CH)&&CH!='-') CH=getchar();
    if(CH=='-') R=-1;else F=(CH^48);CH=getchar();
    while(isdigit(CH)) F=(F<<1)+(F<<3)+(CH^48),CH=getchar(); F*=R;
}
struct place{
    int ti,xi,yi;
    friend bool operator < (place a,place b){return a.ti<b.ti;}
}pi[100010];
int jl(int i){return abs(pi[i].xi-pi[i-1].xi)+abs(pi[i].yi-pi[i-1].yi);}
int main()
{
    //freopen("charlotte.in","r",stdin);
    //freopen("charlotte.out","w",stdout);
    int T;
    read(T);
    while(T--)
    {
        int n;
        read(n);
        for(int i=1;i<=n;i++)
            read(pi[i].ti),read(pi[i].xi),read(pi[i].yi);
        sort(pi+1,pi+n+1);
        int fl=0;
        for(int i=1;i<=n;i++)
        {
            if(pi[i].ti-pi[i-1].ti<jl(i)) {fl=1,puts("No");break;}
            else if((pi[i].ti-pi[i-1].ti-jl(i))%2) {fl=1,puts("No");break;}
        }
        if(!fl) puts("Yes");
    }
    return 0;
}
```
