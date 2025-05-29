---
author: ybw051114
author_link: hugo.ybw051114.cf
title: dp2
date: 2021-02-09T00:00:00.000Z
lastmod: 2021-02-09T00:00:00.000Z
draft: true
description: ''
license: ''
tags: []
categories: []
hiddenFromHomePage: false
featuredImage: ''
featuredImagePreview: ''
toc: true
autoCollapseToc: true
lightgallery: true
linkToMarkdown: true
share: {enable: true}
comment: true
---

[上一篇笔记](https://www.luogu.com.cn/blog/Troverld/dp-shua-ti-bi-ji)因为写的太多已经卡了起来……不得不另开新坑了。

# LI.[CF115E Linear Kingdom Races](https://www.luogu.com.cn/problem/CF115E)

思路1.

设$f[i][j]$表示：

当前DP到第$i$位，且最右边的一个没有修的路是第$j$条路，的最大收益。

则有

$f[i][i]=\max\limits_{j=0}^{i-1}f[i-1][j]$

这是在$i$号路不修的情况。

对于其它的情况，有$f[i][j]=f[i-1][j]-a_i$，其中$a_i$表示修路的代价，且有$0\leq j<i$。

然后考虑举办的比赛。

对于一场比赛$(l,i,x)$，所有的$f[i][j](j<l)$都能获得$x$的收益。比赛可以直接在右端点处开`vector`储存。

这样时空复杂度都是$O(n^2)$的。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int n,m,f[2][200100],val[200100],res;
vector<pair<int,int> >v[200100];
inline void read(int &x){
	x=0;
	char c=getchar();
	while(c>'9'||c<'0')c=getchar();
	while(c>='0'&&c<='9')x=(x<<3)+(x<<1)+(c^48),c=getchar();
}
inline void print(int x){
	if(x<=9)putchar('0'+x);
	else print(x/10),putchar('0'+x%10);
}
signed main(){
	read(n),read(m),memset(f,0x80,sizeof(f));
	for(int i=1;i<=n;i++)read(val[i]);
	for(int i=1,l,r,x;i<=m;i++)read(l),read(r),read(x),v[r].push_back(make_pair(l,x));
	f[0][0]=0;
	for(int i=1;i<=n;i++){
		memset(f[i&1],0x80,sizeof(f[i&1]));
		for(int j=0;j<i;j++)f[i&1][i]=max(f[i&1][i],f[!(i&1)][j]);
		for(int j=0;j<i;j++)f[i&1][j]=f[!(i&1)][j]-val[i];
		for(auto j:v[i])for(int k=0;k<j.first;k++)f[i&1][k]+=j.second;
//		for(int j=0;j<=i;j++)printf("%lld ",f[i&1][j]);puts("");
	}
	for(int i=0;i<=n;i++)res=max(res,f[n&1][i]);
	print(res);
	return 0;
} 
```

思路2.

先把空间复杂度解决掉。

发现$i$时刻的$f$数组与$i-1$时刻的$f$数组区别只有这些：

1.  $f[i]$的变动。

2.  $f[0\sim i-1]$的$-a_i$。

3.  比赛的收益。

那么我们完全可以自始至终只用一个$f$数组。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int n,m,f[200100],val[200100],res;
vector<pair<int,int> >v[200100];
inline void read(int &x){
	x=0;
	char c=getchar();
	while(c>'9'||c<'0')c=getchar();
	while(c>='0'&&c<='9')x=(x<<3)+(x<<1)+(c^48),c=getchar();
}
inline void print(int x){
	if(x<=9)putchar('0'+x);
	else print(x/10),putchar('0'+x%10);
}
signed main(){
	read(n),read(m),memset(f,0x80,sizeof(f));
	for(int i=1;i<=n;i++)read(val[i]);
	for(int i=1,l,r,x;i<=m;i++)read(l),read(r),read(x),v[r].push_back(make_pair(l,x));
	f[0]=0;
	for(int i=1;i<=n;i++){
		for(int j=0;j<i;j++)f[i]=max(f[i],f[j]);
		for(int j=0;j<i;j++)f[j]-=val[i];
		for(auto j:v[i])for(int k=0;k<j.first;k++)f[k]+=j.second;
//		for(int j=0;j<=i;j++)printf("%lld ",f[i&1][j]);puts("");
	}
	for(int i=0;i<=n;i++)res=max(res,f[i]);
	print(res);
	return 0;
} 
```

思路3.

发现所有操作只有三种：单点赋值（1），区间求$\\max$（1），区间加/减（2,3）。

而这些都是线段树的常规操作。

于是大力往上一套完事。复杂度$O(n\log n)$

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
#define lson x<<1
#define rson x<<1|1
#define mid ((l+r)>>1)
int n,m,val[200100],res;
vector<pair<int,int> >v[200100];
inline void read(int &x){
	x=0;
	char c=getchar();
	while(c>'9'||c<'0')c=getchar();
	while(c>='0'&&c<='9')x=(x<<3)+(x<<1)+(c^48),c=getchar();
}
inline void print(int x){
	if(x<=9)putchar('0'+x);
	else print(x/10),putchar('0'+x%10);
}
struct SegTree{
	int mx,tag;
}seg[800100];
void pushup(int x){
	seg[x].mx=max(seg[lson].mx,seg[rson].mx);
}
void ADD(int x,int y){
	seg[x].tag+=y,seg[x].mx+=y;
}
void pushdown(int x){
	ADD(lson,seg[x].tag),ADD(rson,seg[x].tag),seg[x].tag=0;
}
void modify(int x,int l,int r,int L,int R,int vl){
	if(l>R||r<L)return;
	if(L<=l&&r<=R){ADD(x,vl);return;}
	pushdown(x),modify(lson,l,mid,L,R,vl),modify(rson,mid+1,r,L,R,vl),pushup(x);
}
int query(int x,int l,int r,int L,int R){
	if(l>R||r<L)return 0x8080808080808080;
	if(L<=l&&r<=R)return seg[x].mx;
	pushdown(x);
	return max(query(lson,l,mid,L,R),query(rson,mid+1,r,L,R));
}
void setup(int x,int l,int r,int P,int vl){
	if(l>P||r<P)return;
	if(l==r){seg[x].mx=vl,seg[x].tag=0;return;}
	pushdown(x),setup(lson,l,mid,P,vl),setup(rson,mid+1,r,P,vl),pushup(x);
}
void build(int x,int l,int r){
	if(l==r){seg[x].mx=0x8080808080808080;return;}
	build(lson,l,mid),build(rson,mid+1,r),pushup(x); 
}
signed main(){
	read(n),read(m);
	for(int i=1;i<=n;i++)read(val[i]);
	for(int i=1,l,r,x;i<=m;i++)read(l),read(r),read(x),v[r].push_back(make_pair(l,x));
	build(1,1,n+1),setup(1,1,n+1,1,0);
	for(int i=1;i<=n;i++){
		setup(1,1,n+1,i+1,query(1,1,n,1,i));
		modify(1,1,n+1,1,i,-val[i]);
		for(auto j:v[i])modify(1,1,n+1,1,j.first,j.second);
//		for(int j=0;j<=i;j++)printf("%lld ",f[i&1][j]);puts("");
	}
	print(query(1,1,n+1,1,n+1));
	return 0;
} 
```

# LII.[CF264B Good Sequences](https://www.luogu.com.cn/problem/CF264B)

状态很显然。设$f[i]$表示位置$i$的最长长度。

关键是转移------暴力转移是$O(n^2)$的。我们必须找到一个更优秀的转移。

因为一个数的质因子数量是$O(\\log n)$的，而只有和这个数具有相同质因子的数是可以转移的；

因此我们可以对于每个质数$p$，设一个$mx_p$表示所有有$p$作为质因子的$x$的$f_i$的最大值。

关于质因子应该怎么得出嘛……线性筛一下即可。

复杂度$O(n\\log n)$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
const int N=1e5;
int n,pri[N+10],pre[N+10],mx[N+10],f[N+10],res;
void ural(){
	for(int i=2;i<=N;i++){
		if(!pri[i])pri[++pri[0]]=i,pre[i]=pri[0];
		for(int j=1;j<=pri[0]&&i*pri[j]<=N;j++){
			pri[i*pri[j]]=true,pre[i*pri[j]]=j;
			if(!(i%pri[j]))break;
		}
	}
}
int main(){
	scanf("%d",&n),ural();
	for(int i=1,x,t;i<=n;i++){
		scanf("%d",&x),f[i]=1;
		t=x;
		while(t!=1)f[i]=max(f[i],mx[pre[t]]+1),t/=pri[pre[t]];
		t=x;
		while(t!=1)mx[pre[t]]=f[i],t/=pri[pre[t]];
		res=max(res,f[i]);
	}
	printf("%d\n",res);
	return 0;
}
```

# LIII.[CF285E Positions in Permutations](https://www.luogu.com.cn/problem/CF285E)

神题orz……

我也是第一次听说有个叫**二项式反演**的神奇东西……

它具体有两个形式：

1.  $F(n)=\\sum\\limits_{i=0}^n(-1)^i\\dbinom{n}{i}G(i)\\Leftrightarrow G(n)=\\sum\\limits_{i=0}^n(-1)^i\\dbinom{n}{i}F(i)$

2.  $F(n)=\\sum\\limits_{i=0}^n\\dbinom{n}{i}G(i)\\Leftrightarrow G(n)=\\sum\\limits_{i=0}^n(-1)^{n-i}\\dbinom{n}{i}F(i)$

3.  $F(n)=\\sum\\limits_{i=n}^?(-1)^i\\dbinom{i}{n}G(i)\\Leftrightarrow G(n)=\\sum\\limits_{i=n}^?(-1)^i\\dbinom{i}{n}F(i)$

4.  $F(n)=\\sum\\limits_{i=n}^?\\dbinom{i}{n}G(i)\\Leftrightarrow G(n)=\\sum\\limits_{i=n}^?(-1)^{i-n}\\dbinom{i}{n}F(i)$

这题可以考虑设$G(i)$表示"完美数"恰好为$i$的方案数，再设$F(i)$表示"完美数"$\\geq i$的方案数。

肯定有$F(m)=\\sum\\limits\_{i=m}^n?\\times G(i)$，其中$?$是某个系数。

则对于$G(i)$中的某种方案，我们需要从$i$个位置中挑出$m$个位置，然后只观察这$m$个位置而忽略其它地方。显然，共有$\\dbinom{i}{m}$种方法。

因此有$F(m)=\\sum\\limits\_{i=m}^n\\dbinom{i}{m}G(i)$。

套用4，得到$G(m)=\\sum\\limits\_{i=m}^n(-1)^{i-m}\\dbinom{i}{m}F(i)$。

考虑DP求$F$。

我们设$f[i][j][k=0\/1][l=0/1]$表示：

前$i$位，有$j$个完美数，并且数字$i$选没选的状态是$k$，数字$i+1$选没选的状态是$l$的方案数。

需要注意的是，我们**只**注意完美的位置，至于其它位置填什么吗……最后阶乘一下。

因此有：

1.  第$i$位是完美位

1.1. 填入$i-1$

则有

$f[i][j][0][0]+=f[i-1][j-1][0][0]$

$f[i][j][1][0]+=f[i-1][j-1][0][1]$

1.2.填入$i+1$

则有

$f[i][j][0][1]+=f[i-1][j-1][0][0]+f[i-1][j-1][1][0]$

$f[i][j][1][1]+=f[i-1][j-1][0][1]+f[i-1][j-1][1][1]$

2.  第$i$位空置

则有

$f[i][j][0][0]+=f[i-1][j][0][0]+f[i-1][j][1][0]$

$f[i][j][1][0]+=f[i-1][j][0][1]+f[i-1][j][1][1]$

然后特殊转移：

1.第$1$位：

1.1.空置：$f[1][0][0][0]=1$

1.2.放$i+1$：$f[1][1][0][1]=1$

（注意，这里不需要特别讨论放$i$的情况------这就是为什么$F(i)$的定义是$\\geq i$的方案数）

2.第$n$位

废去1.2.填入$i+1$的方案即可。

最终有$F(i)=(n-i)!(f[n][i][0][0]+f[n][i][1][0])$

因为除了完美位外其它的位置都是可以阶乘随便填的。

然后套我们之前的式子，

$G(m)=\\sum\\limits\_{i=m}^n(-1)^{i-m}\\dbinom{i}{m}F(i)$

即可。

（如果要求所有$G(m)$可以直接FFT卷积，不过这题不需要罢了）

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int n,m,f[1010][1010][2][2],fac[1010],inv[1010],F[1010],res;
int ksm(int x,int y){
	int z=1;
	for(;y;y>>=1,x=(1ll*x*x)%mod)if(y&1)z=(1ll*z*x)%mod;
	return z;
}
int C(int x,int y){
	return 1ll*fac[x]*inv[y]%mod*inv[x-y]%mod;
}
int main(){
	scanf("%d%d",&n,&m),f[1][0][0][0]=f[1][1][0][1]=1;
	fac[0]=1;
	for(int i=1;i<=n;i++)fac[i]=(1ll*fac[i-1]*i)%mod;
	inv[n]=ksm(fac[n],mod-2);
	for(int i=n-1;i>=0;i--)inv[i]=(1ll*inv[i+1]*(i+1))%mod;
	for(int i=2;i<=n;i++)for(int j=0;j<=i;j++){
		if(j){
			f[i][j][0][0]=f[i-1][j-1][0][0];
			f[i][j][1][0]=f[i-1][j-1][0][1];
			if(i<n)f[i][j][0][1]=(f[i-1][j-1][0][0]+f[i-1][j-1][1][0])%mod;
			if(i<n)f[i][j][1][1]=(f[i-1][j-1][0][1]+f[i-1][j-1][1][1])%mod;
		}
		f[i][j][0][0]=(0ll+f[i][j][0][0]+f[i-1][j][0][0]+f[i-1][j][1][0])%mod;
		f[i][j][1][0]=(0ll+f[i][j][1][0]+f[i-1][j][0][1]+f[i-1][j][1][1])%mod;
	} 
	for(int i=0;i<=n;i++)F[i]=1ll*fac[n-i]*(f[n][i][0][0]+f[n][i][1][0])%mod;
	for(int i=m;i<=n;i++)(res+=(((i-m)&1?-1ll:1ll)*(1ll*C(i,m)*F[i]%mod)+mod)%mod)%=mod;
	printf("%d\n",res);
	return 0;
} 
```

# LIV.[CF559C Gerald and Giant Chess](https://www.luogu.com.cn/problem/CF559C)

DP只要一与排列组合或是容斥等等东西结合在一起就会变得极其毒瘤……

我们设$f_i$表示：走到第$i$个黑格子上，且之前没有走到任何一个黑格子时的方案数。

则我们如果将棋盘的右下角看作是第$n+1$个黑格子，$f\_{n+1}$就是答案。

我们将黑格子按照行优先，如果行相同列优先的顺序排序，这样就明确了DP顺序。

则我们有$f_i=C_{X_i+Y_i}^{X_i}-\\sum\\limits_{i=1}^{i-1}f_j\*C_{(X_i-X_j)+(Y_i-Y_j)}^{X_i-X_j}$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
const int N=2e5;
const int mod=1e9+7;
int n,fac[200100],inv[200100],f[2010];
pair<int,int>p[2010];
int ksm(int x,int y){
	int z=1;
	for(;y;y>>=1,x=(1ll*x*x)%mod)if(y&1)z=(1ll*z*x)%mod;
	return z;
}
int C(int x,int y){
	return 1ll*fac[x]*inv[y]%mod*inv[x-y]%mod;
}
int main(){
	fac[0]=1;
	for(int i=1;i<=N;i++)fac[i]=(1ll*fac[i-1]*i)%mod;
	inv[N]=ksm(fac[N],mod-2);
	for(int i=N-1;i>=0;i--)inv[i]=(1ll*inv[i+1]*(i+1))%mod;
	scanf("%d%d%d",&p[1].first,&p[1].second,&n),n++,p[1].first--,p[1].second--;
	for(int i=2;i<=n;i++)scanf("%d%d",&p[i].first,&p[i].second),p[i].first--,p[i].second--;
	sort(p+1,p+n+1);
	for(int i=1;i<=n;i++){
		f[i]=C(p[i].first+p[i].second,p[i].first);
		for(int j=1;j<i;j++)if(p[j].first<=p[i].first&&p[j].second<=p[i].second)f[i]=(f[i]-1ll*f[j]*C(p[i].first-p[j].first+p[i].second-p[j].second,p[i].first-p[j].first)%mod+mod)%mod;
	}
	printf("%d\n",f[n]);
	return 0;
}
```

# LV.[CF621E Wet Shark and Blocks](https://www.luogu.com.cn/problem/CF621E)

一眼，$b\\leq 10^9$，矩阵快速幂。

再一眼，$x\\leq 100$，$x^3$刚好，因此可以矩乘；

然后每个块里面的东西都是一样的，仍然可以矩乘；

然后OK。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int n,m,p,q,cnt[10];
struct mat{
	int a[110][110];
	mat(){memset(a,0,sizeof(a));}
	friend mat operator *(const mat &x,const mat &y){
		mat z;
		for(int i=0;i<q;i++)for(int j=0;j<q;j++)for(int k=0;k<q;k++)(z.a[i][j]+=1ll*x.a[i][k]*y.a[k][j]%mod)%=mod;
		return z;
	}
}I,X;
int main(){
	scanf("%d%d%d%d",&n,&m,&p,&q);
	for(int i=0,x;i<n;i++)scanf("%d",&x),cnt[x]++;
	for(int i=0;i<q;i++)for(int j=0;j<10;j++)X.a[i][(i*10+j)%q]+=cnt[j];
	for(int i=0;i<q;i++)I.a[i][i]=1;
	for(;m;X=X*X,m>>=1)if(m&1)I=I*X;
	printf("%d\n",I.a[0][p]);
	return 0;
} 
```

# LVI.[The Chocolate Spree](https://www.luogu.com.cn/problem/CF633F)

~~奇奇怪怪的直径题~~

思路1.用多种东西拼出来直径

我们设$f[i][0/1/2/3]$表示：

$0$：子树内一条路径的最大值

$1$：子树内两条路径的最大值

$2$：子树内一条路径，且起点为$x$的最大值

$3$：子树内两条路径，且有一条起点为$x$的最大值

则答案为$f[1][1]$。

考虑如何转移。

设$son_x$为$x$的儿子集合。

则：

$f[x][0]=\\max{\\max\\limits\_{y\\in son_x}f[y][0],f[p][2]+f[q][2]+val_x}$

$f[x][1]$：

可以是子树$f[1]$的最大值；

可以通过子树里面一个$f[0]$，再加上（$f[2]+f[2]+val_x$）拼出的一条路径构成；

也可以通过$f[3]+f[2]+val_x$构成。

$f[x][2]=\\max\\limits\_{y\\in son_x}f[y][2]+val_x$

$f[x][3]=f[p][2]+f[q][1]+val_x$

至于$p$和$q$的选择，可以只记录$f[0]$，$f[1]$和$f[3]$前三大的值，也可以直接偷懒`vector`排序水过。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long 
int n,val[100100],head[100100],f[100100][4],cnt,res;
//0:a chain in the subtree
//1:two chains in the subtree
//2:a chain in the subtree with x is the starting point
//3:two chains in the subtree with x is one of the staring points
struct node{
	int to,next;
}edge[200100];
void ae(int u,int v){
	edge[cnt].next=head[u],edge[cnt].to=v,head[u]=cnt++;
	edge[cnt].next=head[v],edge[cnt].to=u,head[v]=cnt++;
}
void match(int x,int a,int b,int c){//use half chains from A and B to form a complete chain, and use a full chain from C.
	if(a!=b&&b!=c&&c!=a)f[x][1]=max(f[x][1],f[a][2]+f[b][2]+val[x]+f[c][0]);
}
void dfs(int x,int fa){
	vector<pair<int,int> >v0,v2,v3;
	for(int i=head[x],y;i!=-1;i=edge[i].next){
		if((y=edge[i].to)==fa)continue;
		dfs(edge[i].to,x);
		f[x][0]=max(f[x][0],f[edge[i].to][0]);
		f[x][1]=max(f[x][1],f[edge[i].to][1]);
		f[x][2]=max(f[x][2],f[edge[i].to][2]);
		f[x][3]=max(f[x][3],f[edge[i].to][3]);
		v0.push_back(make_pair(f[edge[i].to][0],edge[i].to));
		v2.push_back(make_pair(f[edge[i].to][2],edge[i].to));
		v3.push_back(make_pair(f[edge[i].to][3],edge[i].to));
	}
	f[x][2]+=val[x],f[x][3]+=val[x];
	sort(v0.begin(),v0.end()),reverse(v0.begin(),v0.end());
	while(v0.size()<3)v0.push_back(make_pair(0,0));
	sort(v2.begin(),v2.end()),reverse(v2.begin(),v2.end());
	while(v2.size()<3)v2.push_back(make_pair(0,0));
	sort(v3.begin(),v3.end()),reverse(v3.begin(),v3.end());
	while(v3.size()<3)v3.push_back(make_pair(0,0));
	f[x][0]=max(f[x][0],v2[0].first+v2[1].first+val[x]);
	f[x][1]=max(f[x][1],v0[0].first+v0[1].first);
	if(v0[0].second!=v2[0].second)f[x][3]=max(f[x][3],v0[0].first+v2[0].first+val[x]);
	else f[x][3]=max(f[x][3],max(v0[0].first+v2[1].first,v0[1].first+v2[0].first)+val[x]);
	for(int i=0;i<3;i++)for(int j=0;j<3;j++)for(int k=0;k<3;k++)match(x,v2[i].second,v2[j].second,v0[k].second);
	if(v2[0].second!=v3[0].second)f[x][1]=max(f[x][1],v2[0].first+v3[0].first+val[x]);
	else f[x][1]=max(f[x][1],max(v2[1].first+v3[0].first,v2[0].first+v3[1].first)+val[x]);
}
signed main(){
	scanf("%lld",&n),memset(head,-1,sizeof(head));
	for(int i=1;i<=n;i++)scanf("%lld",&val[i]);
	for(int i=1,x,y;i<n;i++)scanf("%lld%lld",&x,&y),ae(x,y);
	dfs(1,0);
	printf("%lld\n",f[1][1]);
	return 0;
}
```

思路2.二次扫描+换根

因为这两条路径一定会被一条边分成两半，两条路径各在一半里面，所以可以换根换出最大的断边。

设$f[x]$表示$x$的子树中，以$x$为起点的路径的最大值

设$g[x]$表示$x$子树的直径。

设$h[x]$表示除了$x$子树外的其余部分，以$x$的父亲为起点的路径最大值

设$d[x]$表示除了$x$子树外剩余部分的直径。

则答案为$\\max(g[x]+d[x])$。

$f$和$g$可以一遍普通DP就能算出来；

我们设$v$集合表示在$x$的儿子中从大到小排序后的$f$集合，

$u$集合表示在$x$的儿子中从大到小排序后的$g$集合，

则$d[x]$可以从父亲边选一条，儿子边选一条；或者选两条儿子边；或者继承父亲的$d$或儿子的$g$。

即：

`d[y]=max({d[x],max(h[x],(y==v[0]||y==v[1]?f[v[2]]:f[v[1]]))+(y==v[0]?f[v[1]]:f[v[0]])+val[x],(y==u[0]?g[u[1]]:g[u[0]])});`

$h[x]$可以选择继承父亲的，也可以选择另一个兄弟的$f$，即：

`h[y]=max(h[x],(y==v[0]?f[v[1]]:f[v[0]]))+val[x];`

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int n,f[100100],g[100100],h[100100],d[100100],head[100100],cnt,res,val[100100];
struct node{
	int to,next;
}edge[200100];
void ae(int u,int v){
	edge[cnt].next=head[u],edge[cnt].to=v,head[u]=cnt++;
}
void dfs1(int x,int fa){
	g[x]=val[x];
	for(int i=head[x],y;i!=-1;i=edge[i].next){
		if((y=edge[i].to)==fa)continue;
		dfs1(y,x);
		g[x]=max(g[x],f[x]+f[y]+val[x]);
		g[x]=max(g[x],g[y]);
		f[x]=max(f[x],f[y]);
	}
	f[x]+=val[x];
}
bool cmp1(const int &x,const int &y){
	return f[x]>f[y];
}
bool cmp2(const int &x,const int &y){
	return g[x]>g[y];
}
void dfs2(int x,int fa){
	vector<int>v,u;
	for(int i=head[x],y;i!=-1;i=edge[i].next){
		if((y=edge[i].to)==fa)continue;
		v.push_back(edge[i].to),u.push_back(edge[i].to);
	}
	sort(v.begin(),v.end(),cmp1),v.push_back(0),v.push_back(0);
	sort(u.begin(),u.end(),cmp2),u.push_back(0);
	for(int i=head[x],y;i!=-1;i=edge[i].next){
		if((y=edge[i].to)==fa)continue;
		d[y]=max({d[x],max(h[x],(y==v[0]||y==v[1]?f[v[2]]:f[v[1]]))+(y==v[0]?f[v[1]]:f[v[0]])+val[x],(y==u[0]?g[u[1]]:g[u[0]])});
		res=max(res,g[y]+d[y]);
//		printf("(%d,%d):%d,%d,%d,%d\n",x,y,g[y],max(h[x],(y==v[0]||y==v[1]?f[v[2]]:f[v[1]])),(y==v[0]?f[v[1]]:f[v[0]]),val[x]);
		h[y]=max(h[x],(y==v[0]?f[v[1]]:f[v[0]]))+val[x];
		dfs2(y,x);
	}
}
signed main(){
	scanf("%lld",&n),memset(head,-1,sizeof(head));
	for(int i=1;i<=n;i++)scanf("%lld",&val[i]);
	for(int i=1,x,y;i<n;i++)scanf("%lld%lld",&x,&y),ae(x,y),ae(y,x);
	dfs1(1,0),dfs2(1,0);
//	for(int i=1;i<=n;i++)printf("%lld ",f[i]);puts("");
//	for(int i=1;i<=n;i++)printf("%lld ",g[i]);puts("");
//	for(int i=1;i<=n;i++)printf("%lld ",h[i]);puts("");
	printf("%lld\n",res);
	return 0;
}
```

# LVII.[CF809D Hitchhiking in the Baltic States](https://www.luogu.com.cn/problem/CF809D)

设$f_i$表示长度为$i$的LIS结尾的最小值。为了方便，设$g_i$表示前一个物品的$f_i$（即滚动数组）；

则对于一个$[l,r]$的物品：

1.  对于$g\_{i-1}&lt;l$的位置，有$f_i=\\max(g_i,l)$。

2.  对于$g_{i-1}\\in[l,r-1]$的位置，有$f_i=\\max(g_i,g_{i-1}+1)$。

3.  对于$g\_{i-1}\\geq r$的位置，转移不了，因此直接有$f_i=g_i$。

考虑用平衡树实现。

对于转移1，因为$f_i$是递增的所以这个转移只对第一个$\\geq l$的位置$i$生效。效果相当于直接插入一个数字$l$。

对于转移2，因为我们已经插入过一个$l$了，因此实际上已经全体右移一位了，所以直接打一个$+1\\ \\operatorname{tag}$即可。

对于转移3，直接删去第一个$\\geq r$的$f$即可。

操作采取fhq treap实现（因为要区间修改）。splay也可以实现。

```cpp
#include<bits/stdc++.h>
using namespace std;
#define lson t[x].ch[0]
#define rson t[x].ch[1]
int cnt,n,root;
struct treap{
	int ch[2],val,rad,sz,tag;
}t[300100];
int newnode(int val){
	cnt++,t[cnt].rad=rand()*rand(),t[cnt].sz=1,t[cnt].val=val;
	return cnt;
}
void pushup(int x){
	t[x].sz=t[lson].sz+t[rson].sz+1;
}
void ADD(int x,int val){
	t[x].tag+=val,t[x].val+=val;
}
void pushdown(int x){
	if(!x)return;
	if(lson)ADD(lson,t[x].tag);
	if(rson)ADD(rson,t[x].tag);
	t[x].tag=0;
}
int merge(int x,int y){
	if(!y)return x;
	if(!x)return y;
	pushdown(x),pushdown(y);
	if(t[x].rad>t[y].rad){t[x].ch[1]=merge(t[x].ch[1],y),pushup(x);return x;}
	else{t[y].ch[0]=merge(x,t[y].ch[0]),pushup(y);return y;}
}
void split(int x,int val,int &u,int &v){//u:the subtree which <val;v:the subtree which >=val
	if(!x){u=v=0;return;}
	pushdown(x);
	if(t[x].val<val)u=x,split(rson,val,rson,v);
	else v=x,split(lson,val,u,lson);
	pushup(x);
}
int kth(int x,int k){
	if(!k)return 0;
	while(true){
		pushdown(x);
		if(t[lson].sz>=k)x=lson;
		else if(t[lson].sz+1<k)k-=t[lson].sz+1,x=rson;
		else return x;
	}
}
int suf(int val){//the largest node >= val
	int u=0,v=0,res;
	split(root,val,u,v);
	if(!v)return 0;
	res=kth(v,1);
	root=merge(u,v);
	return res;
}
void ins(int val){
	int a=0,b=0;
	split(root,val,a,b);
	root=merge(a,merge(newnode(val),b));
}
void del(int val){
	int a=0,b=0,c=0,d=0;
	split(root,val,a,b);
	split(b,val+1,c,d);
	c=merge(t[c].ch[0],t[c].ch[1]);
	root=merge(a,merge(c,d));
} 
void iterate(int x){
	if(!x)return;
	pushdown(x),iterate(lson),printf("%d ",t[x].val),iterate(rson);
}
void add(int l,int r){
	int a=0,b=0,c=0,d=0;
	split(root,l,a,b);
	split(b,r,c,d);
	if(c)ADD(c,1);
//	printf("A "),iterate(a),puts("");
//	printf("B "),iterate(c),puts("");
//	printf("C "),iterate(d),puts("");
	root=merge(a,merge(c,d));
}
int main(){
	scanf("%d",&n);
	for(int i=1,l,r;i<=n;i++){
		scanf("%d%d",&l,&r);
		if(i==1){ins(l);continue;}
		int x=suf(r);
		add(l,r);
		if(x)del(t[x].val);
		ins(l);
	}
	printf("%d\n",t[root].sz);
	return 0;
} 
```

# LVIII.[CF767C Garland](https://www.luogu.com.cn/problem/CF767C)

有两种可行方法：

1.  对于一个点，它存在两个儿子，使得这两个儿子的子树中个存在一棵子树，它们的$size$都是$1\/3$。

2.  对于一个点，它的$size$是$2\/3$，并且它的子树中存在一个子树，它的$size$是$1\/3$。

然后我们只需要对于每个节点记录$has1[x]$表示子树中是否有一个$size=1\/3$的节点即可。复杂度$O(n)$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,rt,head[1001000],sum[1001000],all,val[1001000],cnt,has1[1001000];
struct node{
	int to,next;
}edge[1001000];
void ae(int u,int v){
	edge[cnt].next=head[u],edge[cnt].to=v,head[u]=cnt++;
}
void dfs(int x){
	sum[x]=val[x];
	for(int i=head[x];i!=-1;i=edge[i].next){
		dfs(edge[i].to),sum[x]+=sum[edge[i].to];
		if(has1[edge[i].to]){
			if(!has1[x])has1[x]=has1[edge[i].to];
			else{printf("%d %d\n",has1[x],has1[edge[i].to]);exit(0);}
		}
	}
	if(sum[x]==all*2&&has1[x]&&x!=rt){printf("%d %d\n",x,has1[x]);exit(0);}
	if(sum[x]==all)has1[x]=x;
}
int main(){
	scanf("%d",&n),memset(head,-1,sizeof(head));
	for(int i=1,x;i<=n;i++){
		scanf("%d%d",&x,&val[i]),all+=val[i];
		if(!x)rt=i;
		else ae(x,i);
	}
	if(all%3!=0){puts("-1");return 0;}
	all/=3;
	dfs(rt);
	puts("-1");
	return 0;
}
```

# LIX.[CF815C Karen and Supermarket](https://www.luogu.com.cn/problem/CF815C)

思路：一看就是树DP。

设$f[i][j][0/1]$表示：

在以$i$为根的子树中，选了$j$个物品，并且从$i$到$1$的路径上的点 没有\/有 全部选上的最小花费。

则初始$f[i][0][0]=0$，$f[i][1][1]=c_i-d_i$，$f[i][1][0]=d_i$。其它全赋成$\\infty$。

之后背包转移即可。$1$可以从$0$和$1$转移来，而$0$只能从$0$转移。

复杂度$O(n^2)$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int n,m,f[5010][5010][2],head[5010],cnt,c[5010],d[5010],sz[5010],g[5010];//0:anything in the subtree 1:path from root must hold
struct node{
	int to,next;
}edge[5010];
void ae(int u,int v){
	edge[cnt].next=head[u],edge[cnt].to=v,head[u]=cnt++;
}
void dfs(int x){
	sz[x]=1,f[x][0][0]=0,f[x][1][0]=c[x],f[x][1][1]=c[x]-d[x];
	for(int e=head[x],y;e!=-1;e=edge[e].next){
		y=edge[e].to,dfs(y);
		for(int i=0;i<=sz[x]+sz[y];i++)g[i]=0x3f3f3f3f3f3f3f3f;
		for(int i=1;i<=sz[x];i++)for(int j=0;j<=sz[y];j++)g[i+j]=min(g[i+j],f[x][i][1]+min(f[y][j][0],f[y][j][1]));
		for(int i=0;i<=sz[x]+sz[y];i++)f[x][i][1]=g[i];
		for(int i=0;i<=sz[x]+sz[y];i++)g[i]=0x3f3f3f3f;
		for(int i=0;i<=sz[x];i++)for(int j=0;j<=sz[y];j++)g[i+j]=min(g[i+j],f[x][i][0]+f[y][j][0]);
		for(int i=0;i<=sz[x]+sz[y];i++)f[x][i][0]=g[i];
		sz[x]+=sz[y];
	}
}
signed main(){
	scanf("%lld%lld",&n,&m),memset(head,-1,sizeof(head)),memset(f,0x3f,sizeof(f));
	for(int i=1,x;i<=n;i++){
		scanf("%lld%lld",&c[i],&d[i]);
		if(i>1)scanf("%lld",&x),ae(x,i);
	}
	dfs(1);
//	for(int i=1;i<=n;i++)printf("%d ",sz[i]);puts("");
	for(int i=1;i<=n+1;i++){
		if(min(f[1][i][0],f[1][i][1])<=m)continue;
		printf("%lld\n",i-1);break;
	}
	return 0;
} 
```

# LX.[CF837D Round Subset](https://www.luogu.com.cn/problem/CF837D)

思路：

设$f[l][i][j][k]$表示：

前$l$位，选出$j$个，这$j$个物品能否拥有$j$个$5$和$k$个$2$（`bool`型）

接下来开始削减位数。

第一维可以直接$01$背包掉。现在只剩$f[i][j][k]$三维。

因为这是`bool`，我们就可以想办法把它压成`int`。

于是设$f[i][j]$表示：选择$i$个物品，拥有$j$个$5$时，最多能拥有多少个$2$。

则答案为$\\max{\\min(i,f[m][i])}$。

复杂度为$O(n^2m\\log_5a)$，可以通过。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,f[210][13000],lim,res;
pair<int,int>p[210];
pair<int,int>read(){
	long long x;
	scanf("%I64d",&x);
	pair<int,int>ret=make_pair(0,0);
	while(!(x%5))x/=5,ret.first++;
	while(!(x&1))x>>=1,ret.second++;
	return ret;
}
int main(){
	scanf("%d%d",&n,&m),memset(f,-1,sizeof(f));
	for(int i=1;i<=n;i++)p[i]=read(),lim+=p[i].first;
	f[0][0]=0;
	for(int i=1;i<=n;i++)for(int j=min(i,m);j;j--)for(int k=lim;k>=p[i].first;k--)if(f[j-1][k-p[i].first]!=-1)f[j][k]=max(f[j][k],f[j-1][k-p[i].first]+p[i].second);
	for(int i=1;i<=lim;i++)res=max(res,min(i,f[m][i]));
	printf("%d\n",res);
	return 0;
}
```

# LXI.[CF868F Yet Another Minimization Problem](https://www.luogu.com.cn/problem/CF868F)

这种题一般来说只有决策单调性一种优化方法。不过，决策单调性可以有很多种应用，例如单调队列或是斜率优化。这题可以选择比较少见的分治优化。

明显，可以设$f[i][j]$表示前$i$个位置分成$j$段的最大收益。显然，暴力是$O(n^2k)$的。

如果我们按照$j$一遍一遍地跑的话，是可以考虑在$i$上面进行优化的、

考虑设$f[i]$表示$f[i][j-1]$，$g[i]$表示$f[i][j]$，

然后设$w[l,r]$表示区间$[l,r]$的费用，

则我们是否可以证明它具有决策单调性？

即：

对于$\\forall i_1&lt;i_2$，设它们分别从$j_1$，$j_2$转移来最优，则必有$j_1\\leq j_2$。

则必有

$g_{j_1}+w[j_1+1,i_1]\\leq g_{j_2}+w[j_2+1,i_1],g_{j_2}+w[j_2+1,i_2]\\leq g_{j_1}+w[j_1+1,i_2]$

我们可以考虑反证法。假设有$j_1>j_2$，

则对于上面的两个不等式里，如果两个都取到了$=$，则交换$j_1,j_2$没有影响。

否则，我们不妨设在第一个式子里取到了$&lt;$，

即

$g_{j_1}+w[j_1+1,i_1]&lt;g_{j_2}+w[j_2+1,i_1],g_{j_2}+w[j_2+1,i_2]\\leq g_{j_1}+w[j_1+1,i_2]$

移项得

$w[j_1+1,i_1]-w[j_2+1,i_1]&lt;g_{j_2}-g_{j_1},g_{j_2}-g_{j_1}\\leq w[j_1+1,i_2]-w[j_2+1,i_2]$

两边合并$g_2-g_1$，得

$w[j_1+1,i_1]-w[j_2+1,i_1]&lt;w[j_1+1,i_2]-w[j_2+1,i_2]$

这两项全部只有后面的$i_1$和$i_2$不同。但$i_1&lt;i_2$，因此这是不可能成立的，往区间后面加数后答案必不会减少。

然后就可以分治了。每一轮我们存储对于当前区间$[l,r]$可行的决策点$[L,R]$，对于$[l,r]$的中点$mid$，我们找到最优转移位置$mp$，然后继续分治$([l,mid-1],[L,mp])$与$([mid+1,r],[mp,R])$。

关于如何计算$w[l,r]$吗……类似的莫队一下，因为单次分治中左右端点总移动距离是$n\\log n$的（每一层里面左右端点总次数是$O(n)$的，然后一共$\\log n$层）。

总复杂度$O(nk\\log n)$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int n,m,num[101000],cnt[101000],res,f[100100],g[100100];
int u,v;
void Push(int x){
	res+=cnt[num[x]],cnt[num[x]]++;
}
void Pop(int x){
	cnt[num[x]]--,res-=cnt[num[x]];
}
int Calc(int l,int r){
	while(u>l)Push(--u);
	while(v<r)Push(++v);
	while(u<l)Pop(u++);
	while(v>r)Pop(v--);
	return res;
}
void solve(int l,int r,int L,int R){
	if(l>r||L>R)return;
	int mp=-1,mn=0x3f3f3f3f3f3f3f3f,mid=(l+r)>>1;
	for(int i=L;i<=R;i++){
		int tmp=Calc(i+1,mid);
		if(f[i]+tmp<mn)mp=i,mn=f[i]+tmp;
	}
	g[mid]=mn;
	solve(l,mid-1,L,mp),solve(mid+1,r,mp,R);
}
signed main(){
	scanf("%lld%lld",&n,&m);
	for(int i=1;i<=n;i++)scanf("%lld",&num[i]);
	u=v=1,cnt[num[1]]++;
	for(int i=1;i<=n;i++)f[i]=Calc(1,i);
	while(--m)solve(1,n,0,n-1),memcpy(f,g,sizeof(g));
	printf("%lld\n",f[n]);
	return 0;
}
```

# LXII.[CF908D New Year and Arbitrary Arrangement](https://www.luogu.com.cn/problem/CF908D)

思路：

期望题果然还是恶心呀……

我们设$f[i][j]$表示当串中有$i$个`a`和$j$个`ab`时的方案数。为了方便，设$A=\\dfrac{P_a}{P_a+P_b},B=\\dfrac{P_b}{P_a+P_b}$。

显然，可以这样转移：

$f[i][j]=f[i+1][j]_A+f[i][i+j]_B$

因为，如果串后面加上一个`a`，概率是$A$，并且加完后唯一的影响就是$i+1$；如果加入一个`b`，概率是$B$，加完后前面每一个`a`都会与这个`b`形成一对`ab`。

那么边界条件呢？

显然，当$i+j\\geq k$时，只要再往后面加入一个`b`，过程就停止了。

则这个的期望长度应该是：

$B_\\sum\\limits\_{a=0}^{\\infty}(i+j+a)_A^a$

其中，枚举的这个$a$是在终于搞出一个`b`前，所刷出的`a`的数量。

为了方便，我们设$i+j=c$，并用$i$替换$a$。即：

$B_\\sum\\limits\_{i=0}^{\\infty}(c+i)_A^i$

因为$A+B=1$，我们可以用$(1-A)$代$B$。

即：

$(1-A)_\\sum\\limits\_{i=0}^{\\infty}(c+i)_A^i$

拆开括号得

$\\sum\\limits_{i=0}^{\\infty}(c+i)\*A^i-\\sum\\limits_{i=0}^{\\infty}(c+i)\*A^{i+1}$

一上来直接$\\infty$有些不直观，我们用$n$替换掉。

$\\sum\\limits_{i=0}^n(c+i)\*A^i-\\sum\\limits_{i=0}^n(c+i)\*A^{i+1}$

在第二个式子里面用$i+1$代掉$i$

$\\sum\\limits_{i=0}^n(c+i)\*A^i-\\sum\\limits_{i=1}^{n+1}(c+i-1)\*A^i$

将第一个$\\Sigma$中$i=0$的情况和第二个$\\Sigma$中$i=n+1$的情况分别提出

$c+\\sum\\limits_{i=1}^n(c+i)\*A^i-\\sum\\limits_{i=1}^n(c+i-1)_A^i-(c+n)_A^{n+1}$

合并两个$\\Sigma$

$c+\\sum\\limits\_{i=1}^nA^i-(c+n)\*A^{n+1}$

套等比数列求和公式（注意要先提出一个$A$使首项为$1$）

$c+A_\\dfrac{1-A^n}{1-A}-(c+n)_A^{n+1}$

注意到$1-A=B$

$c+A_\\dfrac{1-A^n}{B}-(c+n)_A^{n+1}$

现在，考虑$n\\rightarrow\\infty$的情况。即：

$\\lim\\limits\_{n\\rightarrow\\infty}c+A_\\dfrac{1-A^n}{B}-(c+n)_A^{n+1}$

注意到$0&lt;A&lt;1$，因此$\\lim\\limits\_{n\\rightarrow\\infty}A^n=0$

带入发现

$c+A_\\dfrac{1-0}{B}-(c+n)_0$

处理一下

$c+\\dfrac{A}{B}$

注意到我们一开始的定义了吗？

$A=\\dfrac{P_a}{P_a+P_b},B=\\dfrac{P_b}{P_a+P_b}$

以及$c=i+j$

代入得

$i+j+\\dfrac{P_a}{P_b}$

也就是说，边界条件就是$f[i][j]=i+j+\\dfrac{P_a}{P_b}(i+j\\geq k)$！！！

再搬出我们一开始的转移式

$f[i][j]=f[i+1][j]_A+f[i][i+j]_B$

完事。

哦，另外，还要思考一下答案到底是$f[0][0]$还是$f[1][0]$。

因为一开始的那些`b`，无论来多少个都是没用的，因此不如直接从$f[1][0]$开始。（事实上，你如果把转移式代回去或者打个表的话，你会发现就有$f[0][0]=f[1][0]$）

复杂度$O(k^2+\\log mod)$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,a,b,A,B,f[1010][1010],c;
const int mod=1e9+7;
int ksm(int x,int y){
    int z=1;
    for(;y;x=(1ll*x*x)%mod,y>>=1)if(y&1)z=(1ll*z*x)%mod;
    return z;
}
int dfs(int x,int y){
    if(x+y>=n)return x+y+c;
    if(f[x][y]!=-1)return f[x][y];
    int &res=f[x][y];res=0;
    (res+=1ll*dfs(x+1,y)*A%mod)%=mod;
    (res+=1ll*dfs(x,x+y)*B%mod)%=mod;
    return res;
}
int main(){
    scanf("%d%d%d",&n,&a,&b),A=1ll*a*ksm(a+b,mod-2)%mod,B=1ll*b*ksm(a+b,mod-2)%mod,c=1ll*a*ksm(b,mod-2)%mod,memset(f,-1,sizeof(f));
    printf("%d\n",dfs(1,0));
    return 0;
}
```

# LXIII.[CF1029E Tree with Small Distances](https://www.luogu.com.cn/problem/CF1029E)

我们发现，如果一个点与$1$连了边，那么它的儿子们以及它的父亲都会变成合法的。

因此我们可以设$f[i][0/1/2]$表示：$i$的某个儿子中有边\/$i$自己有边\/$i$的父亲**应该**有边的最小值。

转移：

$0$：可以从儿子的$0$或$1$转移，且儿子中至少有一个为$1$（即，找到$1$与$0$差最小的那个换成$1$）

$1$：$0\/1\/2$皆可，取$\\min$即可。

$2$：$0\/1$取$\\min$。

复杂度$O(n)$。

最后说一下答案，应该是$1$的所有儿子的$(f[x][1]-1)$的和，因为$1$的所有儿子都相当于连了一条免费的边。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,head[1001000],cnt,f[1001000][3],res;//0:have a son;1:itself;2:have a father 
struct node{
	int to,next;
}edge[2001000];
void ae(int u,int v){
	edge[cnt].next=head[u],edge[cnt].to=v,head[u]=cnt++;
}
void dfs(int x,int fa){
	int mn=0x3f3f3f3f;
	f[x][1]=1;
	for(int i=head[x],y;i!=-1;i=edge[i].next){
		if((y=edge[i].to)==fa)continue;
		dfs(y,x);
		f[x][0]+=min(f[y][0],f[y][1]),mn=min(mn,f[y][1]-f[y][0]);
		f[x][1]+=min(f[y][0],min(f[y][1],f[y][2]));
		f[x][2]+=min(f[y][0],f[y][1]);
		if(x==1)res+=f[y][1]-1;
	}
	f[x][0]+=max(mn,0);
}
int main(){
	scanf("%d",&n),memset(head,-1,sizeof(head));
	for(int i=1,x,y;i<n;i++)scanf("%d%d",&x,&y),ae(x,y),ae(y,x);
	dfs(1,0);
	printf("%d\n",res);
	return 0;
} 
```

# LXIV.[CF1059E Split the Tree](https://www.luogu.com.cn/problem/CF1059E)

我们假设对于每个位置，已经求出了它可以往上延伸的长度$len[x]$，然后考虑DP。

设$g[x]$表示子树被分完后的最小边的数量。再设$f[x]$表示当这个数量最小时，点$x$能够往上延伸的最长长度。

这运用了贪心的思想：**因为$g[x]$少一条边，肯定是要比$f[x]$无论大多少都是要更优的**。$f[x]$再大，也只对一条边有效，$f$中一条边和$g$中一条边，不都是一样的吗？

我们可以很轻松地得到转移方程：

$f[x]=\\max\\limits_{y\\in Sons_x}{f[y]}-1,g[x]=\\sum\\limits_{y\\in Sons_x}g[y]$

如果在上面的转移方程中，得到了$f[x]=-1$，那就意味着必须在$x$位置开新边，令$f[x]=len[x]$，$g[x]$加一。

现在主要的部分就是求出$len[x]$了。这个可以通过倍增法在$O(n\\log n)$时间里预处理出来。

则总复杂度为$O(n\\log n)$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int n,L,S,val[100100],len[100100],anc[100100][20],sum[100100],dep[100100],f[100100],g[100100];
vector<int>v[100100];
void dfs1(int x){
	for(int i=1;(1<<i)<=dep[x];i++)anc[x][i]=anc[anc[x][i-1]][i-1];
	for(int i=19,y=x;i>=0;i--){
		if(!anc[y][i])continue;
		if(sum[x]-sum[anc[y][i]]+val[anc[y][i]]>S)continue;
		if(dep[x]-dep[anc[y][i]]>=L)continue;
		len[x]+=(1<<i),y=anc[y][i];
	}
	for(auto y:v[x])anc[y][0]=x,dep[y]=dep[x]+1,sum[y]=sum[x]+val[y],dfs1(y);
}
void dfs2(int x){
	for(auto y:v[x])dfs2(y),f[x]=max(f[x],f[y]),g[x]+=g[y];
	f[x]--;
	if(f[x]==-1)f[x]=len[x],g[x]++;
}
signed main(){
	scanf("%lld%lld%lld",&n,&L,&S);
	for(int i=1;i<=n;i++){
		scanf("%lld",&val[i]);
		if(val[i]>S){puts("-1");return 0;}
	}
	for(int i=2,x;i<=n;i++)scanf("%lld",&x),v[x].push_back(i);
	dep[1]=1,sum[1]=val[1],dfs1(1),dfs2(1);
//	for(int i=1;i<=n;i++)printf("%lld ",len[i]);puts("");
	printf("%lld\n",g[1]);
	return 0;
} 
```

# LXV.[\[USACO20OPEN\]Sprinklers 2: Return of the Alfalfa P](https://www.luogu.com.cn/problem/P6275)

首先，一个合法的方案，肯定是有一条从左到右向下延伸的轮廓线：

例如：

![](https://cdn.luogu.com.cn/upload/image_hosting/rc3xmkc2.png)

其中，蓝色系格子是玉米，红色系格子是苜蓿；浅蓝色位置必须放玉米喷射器，深红色格子必须放苜蓿喷射器。深蓝和浅红格子放不放均可。更一般地说，所有的转角处，都是必须放喷射器的位置。

因此我们可以考虑DP：

假设一定至少放了一个玉米喷射器（有可能有没有任何玉米喷射器的情况，但当且仅当左下角可以放喷射器时，这时只要在左下角放一个苜蓿，其他位置就可以随便放或不放喷射器了），则设$f[i][j]$表示在位置$(i,j)$放了一个玉米时的方案数。

我们思考一下，当位置$(i,j)$已经被放入玉米后，有哪些位置的发射器种类以及决定了：

![](https://cdn.luogu.com.cn/upload/image_hosting/w5kcqce3.png)

如图，五角星格子就是$(i,j)$，

那么$(i,j)$左下角的深蓝色格子肯定已经被决定了；

第$(i-1)$行上，肯定有一个深红格子存在（不然$(i-1)$行就没有颜色了），因此实际上，只有以$(i,j+1)$为左上角的矩形，里面的颜色尚未决定。

因此我们设一个前缀和$s\_{i,j}$，表示以$(i,j)$为左上角的矩形里面有多少个位置没有牛。

先考虑初始化。

* * *

1.  位置$(i,j)$中$i\\neq 1$，即不位于第$1$行。

![](https://cdn.luogu.com.cn/upload/image_hosting/i5vqytt6.png)

如图，则位置$(i-1,1)$必有一个苜蓿。显然，只有位置$(i-1,1)$不是牛，该位置才可以作为起始点。

则$f[i][j]=2^{s_{1,1}-s_{i,j+1}-2}$。

* * *

2.  有$i=1$。

位置$(i-1,1)$的那个苜蓿不需要放，直接有

$f[i][j]=2^{s_{1,1}-s_{i,j+1}-1}$。

* * *

考虑转移。

我们枚举一个$(k,l)$，且$k&lt;i,l&lt;j$。

则位置$(i-1,l+1)$肯定有个苜蓿。如果位置$(i-1,l+1)$没有牛，则可以转移。

![](https://cdn.luogu.com.cn/upload/image_hosting/bvew8aib.png)

如图，黄星要想从紫星转移来，那么深红位置是必须放置苜蓿的。

则有$f[i][j]=\\sum\\limits_{k=1}^{i-1}\\sum\\limits_{l=1}^{j-1}f[k][l]_2^{s_{k,l+1}-s_{i,j+1}-2}_[(i-1,l+1)\text{没有牛}]$

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int n,s[2010][2010],f[2020][2020],bin[4001000],res;
char g[2010][2010];
int main(){
	scanf("%d",&n);
	for(int i=1;i<=n;i++)scanf("%s",g[i]+1);
	for(int i=n;i;i--)for(int j=n;j;j--)s[i][j]=s[i+1][j]+s[i][j+1]-s[i+1][j+1]+(g[i][j]=='.');
	bin[0]=1;
	for(int i=1;i<=s[1][1];i++)bin[i]=(bin[i-1]<<1)%mod;
//	for(int i=1;i<=n;i++){for(int j=1;j<=n;j++)printf("%d ",s[i][j]);puts("");}
	for(int i=1;i<=n;i++)for(int j=1;j<=n;j++){
		if(g[i][j]=='W')continue;
		if(g[i-1][1]=='.')f[i][j]=bin[s[1][1]-s[i][j+1]-2];
		if(i==1)f[i][j]=bin[s[1][1]-s[i][j+1]-1];
		for(int k=1;k<i;k++)for(int l=1;l<j;l++){
			if(g[k][l]=='W'||g[i-1][l+1]=='W')continue;
			(f[i][j]+=1ll*bin[s[k][l+1]-s[i][j+1]-2]*f[k][l]%mod)%=mod;
		}
		if(g[n][j+1]=='.')(res+=1ll*f[i][j]*bin[s[i][j+1]-1]%mod)%=mod;
		if(j==n)(res+=f[i][j])%=mod;
	}
//	for(int i=1;i<=n;i++){for(int j=1;j<=n;j++)printf("%d ",f[i][j]);puts("");}
	if(g[n][1]=='.')(res+=bin[s[1][1]-1])%=mod;
	printf("%d\n",res);
	return 0;
}
```

很明显这种东西是$O(n^4)$的，期望得分$24\\%$。考虑优化。

* * *

初始化过程是$O(n^2)$的，没问题。关键是转移的地方。

我们搬出式子：

$f[i][j]=\\sum\\limits_{k=1}^{i-1}\\sum\\limits_{l=1}^{j-1}f[k][l]_2^{s_{k,l+1}-s_{i,j+1}-2}_[(i-1,l+1)\text{没有牛}]$

先把这个东西拆成和$(i,j)$有关的和$(k,l)$有关的部分：

$f[i][j]=\\sum\\limits_{k=1}^{i-1}\\sum\\limits_{l=1}^{j-1}\\dfrac{f[k][l]_2^{s\_{k,l+1}}_[(i-1,l+1)\text{没有牛}]}{2^{s\_{i,j+1}+2}}$

再调整求和顺序：

$f[i][j]=\\dfrac{\\sum\\limits_{l=1}^{j-1}[(i-1,l+1)\text{没有牛}]\*\\sum\\limits_{k=1}^{i-1}f[k][l]\*2^{s_{k,l+1}}}{2^{s_{i,j+1}+2}}$

然后设一个前缀和$sum1[i][j]=\\sum\\limits_{k=1}^{i}f[k][j]\*2^{s_{k,j+1}}$

往里面一代：

$f[i][j]=\\dfrac{\\sum\\limits_{l=1}^{j-1}[(i-1,l+1)\text{没有牛}]\*sum1[i-1][l]}{2^{s_{i,j+1}+2}}$

这样复杂度就被优化成了$O(n^3)$，期望得分$54\\%$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
const int inv2=5e8+4;
int n,s[2010][2010],f[2020][2020],bin[4001000],inv[4001000],res,sum[2020][2020];
char g[2010][2010];
int main(){
	scanf("%d",&n);
	for(int i=1;i<=n;i++)scanf("%s",g[i]+1);
	for(int i=n;i;i--)for(int j=n;j;j--)s[i][j]=s[i+1][j]+s[i][j+1]-s[i+1][j+1]+(g[i][j]=='.');
	bin[0]=inv[0]=1;
	for(int i=1;i<=s[1][1];i++)bin[i]=(bin[i-1]<<1)%mod,inv[i]=(1ll*inv[i-1]*inv2)%mod;
//	for(int i=1;i<=n;i++){for(int j=1;j<=n;j++)printf("%d ",s[i][j]);puts("");}
	for(int i=1;i<=n;i++)for(int j=1;j<=n;j++){
		if(g[i][j]!='W'){
			if(g[i-1][1]=='.')f[i][j]=bin[s[1][1]-s[i][j+1]-2];
			if(i==1)f[i][j]=bin[s[1][1]-s[i][j+1]-1];
			for(int k=1;k<j;k++){
				if(g[i-1][k+1]=='W')continue;
				(f[i][j]+=1ll*sum[i-1][k]*inv[s[i][j+1]+2]%mod)%=mod;
			}
			if(g[n][j+1]=='.')(res+=1ll*f[i][j]*bin[s[i][j+1]-1]%mod)%=mod;
			if(j==n)(res+=f[i][j])%=mod;			
		}
		sum[i][j]=(1ll*f[i][j]*bin[s[i][j+1]]+sum[i-1][j])%mod;
	}
//	for(int i=1;i<=n;i++){for(int j=1;j<=n;j++)printf("%d ",f[i][j]);puts("");}
	if(g[n][1]=='.')(res+=bin[s[1][1]-1])%=mod;
	printf("%d\n",res);
	return 0;
}
```

继续尝试优化。

* * *

$f[i][j]=\\dfrac{\\sum\\limits_{l=1}^{j-1}[(i-1,l+1)\text{没有牛}]\*sum1[i-1][l]}{2^{s_{i,j+1}+2}}$

发现我们现在就可以设一个$sum2[i][j]=\\sum\\limits\_{l=1}^j[(i,l+1)\text{没有牛}]\*sum1[i][l]$

则直接有$f[i][j]=\\dfrac{sum2[i-1][j-1]}{2^{s\_{i,j+1}+2}}$

复杂度$O(n^2)$，期望得分$100\\%$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
const int inv2=5e8+4;
int n,s[2010][2010],f[2020][2020],bin[4001000],inv[4001000],res,sum1[2020][2020],sum2[2020][2020];
char g[2010][2010];
int main(){
	scanf("%d",&n);
	for(int i=1;i<=n;i++)scanf("%s",g[i]+1);
	for(int i=n;i;i--)for(int j=n;j;j--)s[i][j]=s[i+1][j]+s[i][j+1]-s[i+1][j+1]+(g[i][j]=='.');
	bin[0]=inv[0]=1;
	for(int i=1;i<=s[1][1];i++)bin[i]=(bin[i-1]<<1)%mod,inv[i]=(1ll*inv[i-1]*inv2)%mod;
//	for(int i=1;i<=n;i++){for(int j=1;j<=n;j++)printf("%d ",s[i][j]);puts("");}
	for(int i=1;i<=n;i++)for(int j=1;j<=n;j++){
		if(g[i][j]!='W'){
			if(g[i-1][1]=='.')f[i][j]=bin[s[1][1]-s[i][j+1]-2];
			if(i==1)f[i][j]=bin[s[1][1]-s[i][j+1]-1];
			(f[i][j]+=1ll*sum2[i-1][j-1]*inv[s[i][j+1]+2]%mod)%=mod;
			if(g[n][j+1]=='.')(res+=1ll*f[i][j]*bin[s[i][j+1]-1]%mod)%=mod;
			if(j==n)(res+=f[i][j])%=mod;			
		}
		sum1[i][j]=(1ll*f[i][j]*bin[s[i][j+1]]+sum1[i-1][j])%mod;
		sum2[i][j]=(sum2[i][j-1]+(g[i][j+1]=='W'?0:sum1[i][j]))%mod;
	}
//	for(int i=1;i<=n;i++){for(int j=1;j<=n;j++)printf("%d ",f[i][j]);puts("");}
	if(g[n][1]=='.')(res+=bin[s[1][1]-1])%=mod;
	printf("%d\n",res);
	return 0;
}
```

# LXVI.[\[USACO09MAR\]Cleaning Up G](https://www.luogu.com.cn/problem/P2943)

$n^2$的DP非常eazy，考虑如何优化。

首先，答案一定是$\\leq n$的，因为一定可以每一个数单独划一组，此时答案为$n$。

则一组里面最多只能有$\\sqrt{n}$个不同的数，不然平方一下就超过$n$了。

因此我们可以设$pos_i$表示不同的数有$i$个时，最远能够延伸到哪里。

再设$f[i]$表示位置$i$的答案。

则$f[i]=\\min\\limits\_{j=1}^{\\sqrt{n}}(f[pos_j]+j^2)$

关键是如何维护$pos$。我们只需要对于每个位置记录前驱$pre_i$，后继$suf_i$即可。如果一个位置是第一次出现，必有$pre_i&lt;pos_j$；这时就应该删去第一个有$suf_k>i$的$k$。

复杂度$O(n\\sqrt{n})$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int a[40100],n,m,f[40100],lim,pre[40100],suf[40100],pos[40100],val[40100],cnt[40100];
int main(){
	scanf("%d%d",&n,&m),lim=sqrt(n),memset(f,0x3f3f3f3f,sizeof(f)),f[0]=0;
	for(int i=1;i<=n;i++)scanf("%d",&a[i]),pre[i]=val[a[i]],suf[pre[i]]=i,suf[i]=n+1,val[a[i]]=i;
//	for(int i=1;i<=n;i++)printf("(%d %d)\n",pre[i],suf[i]);
	for(int i=1;i<=lim;i++)pos[i]=1;
	for(int i=1;i<=n;i++)for(int j=1;j<=lim;j++){
		cnt[j]+=(pre[i]<pos[j]);
		if(cnt[j]>j){
			cnt[j]--;
			while(suf[pos[j]]<=i)pos[j]++;
			pos[j]++;
		}
		f[i]=min(f[i],f[pos[j]-1]+j*j);
	}
//	for(int i=1;i<=n;i++)printf("%d ",f[i]);puts("");
	printf("%d\n",f[n]);
	return 0;
}
```

# LXVII.[\[USACO15JAN\]Moovie Mooving G](https://www.luogu.com.cn/problem/P3118)

思路1.

设$f[i][S]$表示在第$i$**场**（注意是场，不是部）电影时，已经看了$S$里面的电影是否合法。

然后贪心地取$|S|$最小的状态保存。光荣MLE了，$21\\%$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,len[20],sum[20],dis[30000],id[30000];
vector<int>v[20],g[30000],res[30000];
queue<int>q;
int main(){
	scanf("%d%d",&n,&m),memset(dis,0x3f3f3f3f,sizeof(dis));
	for(int i=0,x,y;i<n;i++){
		scanf("%d%d",&len[i],&x),sum[i+1]=sum[i]+x;
		for(int j=0;j<x;j++)scanf("%d",&y),v[i].push_back(y),id[sum[i]+j]=i;
	}
//	for(int i=0;i<=n;i++)printf("%d ",sum[i]);puts("");
	id[sum[n]]=n;
	for(int i=0;i<n;i++)for(int k=0;k<v[i].size();k++){
		int x=v[i][k];
		if(!x)q.push(sum[i]+k),dis[sum[i]+k]=0,res[sum[i]+k].push_back(1<<i);
		int ed=x+len[i];
		if(ed>=m){g[sum[i]+k].push_back(sum[n]);continue;}
		for(int j=0;j<n;j++){
			if(i==j)continue;
			vector<int>::iterator it=upper_bound(v[j].begin(),v[j].end(),ed);
			if(it==v[j].begin())continue;
			it--;
			if(*it+len[j]<ed)continue;
			g[sum[i]+k].push_back(sum[j]+it-v[j].begin());
		}
	}
//	for(int i=0;i<n;i++){for(int j=0;j<v[i].size();j++){printf("%d:",sum[i]+j);for(auto x:g[sum[i]+j])printf("%d ",x);puts("");}puts("");}
//	for(int i=0;i<=sum[n];i++)printf("%d ",id[i]);puts("");
	while(!q.empty()){
		int x=q.front();q.pop();
//		printf("%d:\n",x);
		for(auto y:g[x]){
			if(dis[y]<=dis[x])continue;
//			printf("%d\n",y);
			for(auto i:res[x])if(!(i&(1<<id[y]))){
				if(dis[y]!=dis[x]+1)dis[y]=dis[x]+1,res[y].clear();
				break;	
			}
			if(dis[y]!=dis[x]+1)continue;
			for(auto i:res[x])if(!(i&(1<<id[y])))res[y].push_back(i|(1<<id[y]));
			q.push(y);
		}
	}
	printf("%d\n",dis[sum[n]]==0x3f3f3f3f?-1:dis[sum[n]]);
	return 0;
}
```

思路2.

发现当一场电影结束后，无论这一场是在哪里看的都没关系。

因此我们设$f[S]$表示只看集合$S$里面的电影，最多能够看多久。

转移就枚举下一场看什么，二分一下小于等于$f[S]$的第一场比赛并观看即可。

复杂度$O(n2^n\\log C)$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,f[1<<20],len[20],res=0x3f3f3f3f;
vector<int>v[20];
int main(){
	scanf("%d%d",&n,&m);
	for(int i=0,x,y;i<n;i++){
		scanf("%d%d",&len[i],&x);
		while(x--)scanf("%d",&y),v[i].push_back(y);
	}
	for(int x=0;x<(1<<n);x++){
		if(f[x]>=m){res=min(res,__builtin_popcount(x));continue;}
		for(int i=0;i<n;i++){
			if(x&(1<<i))continue;
			vector<int>::iterator it=upper_bound(v[i].begin(),v[i].end(),f[x]);
			if(it==v[i].begin())continue;
			it--;
			f[x|(1<<i)]=max(f[x|(1<<i)],*it+len[i]);
		}
	}
	printf("%d\n",res==0x3f3f3f3f?-1:res);
	return 0;
} 
```

# LXVIII.[\[USACO17JAN\]Subsequence Reversal P](https://www.luogu.com.cn/problem/P3607)

思路：

发现，翻转一个子序列，就意味着两两互换子序列里面的东西。

于是我们就可以设$f[l][r][L][R]$表示：$\\max[1,l)=L,\min(r,n]=R$时的最长长度。

则边界为：$L>R$时，$f=-\\infty$；否则，如果$l>r$，$f=0$。

然后开始转移。

1.  不选

$f[l+1][r][L][R]$和$f[l][r-1][L][R]$

2.  选一个

当$a_l\\geq L$时，$f[l+1][r][a_l][R]+1$

当$a_r\\leq R$时，$f[l][r-1][L][a_r]+1$

3.  翻转（必须有$l&lt;r$）

当$a_r\\geq L$时，$f[l+1][r-1][a_r][R]+1$

当$a_l\\leq R$时，$f[l+1][r-1][L][a_l]+1$

当$a_r\\geq L$且$a_l\\leq R$时，$f[l+1][r-1][a_r][a_l]+2$

最终答案为$f[1][n][0][\infty]$，其中$\\infty=50$足矣。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,f[60][60][60][60],a[60];
int solve(int l,int r,int L,int R){
	if(L>R)return 0x80808080;
	if(l>r)return 0;
	if(f[l][r][L][R]!=-1)return f[l][r][L][R];
	int &res=f[l][r][L][R];res=0;
	res=max(res,solve(l+1,r,L,R));
	res=max(res,solve(l,r-1,L,R));
	if(a[l]>=L)res=max(res,solve(l+1,r,a[l],R)+1);
	if(a[r]>=L&&l!=r)res=max(res,solve(l+1,r-1,a[r],R)+1);
	if(a[r]<=R)res=max(res,solve(l,r-1,L,a[r])+1);
	if(a[l]<=R&&l!=r)res=max(res,solve(l+1,r-1,L,a[l])+1);
	if(a[l]<=R&&a[r]>=L&&l!=r)res=max(res,solve(l+1,r-1,a[r],a[l])+2);
//	printf("(%d,%d):(%d,%d):%d\n",l,r,L,R,res);
	return res;
}
int main(){
	scanf("%d",&n),memset(f,-1,sizeof(f));
	for(int i=1;i<=n;i++)scanf("%d",&a[i]);
	printf("%d\n",solve(1,n,0,50));
	return 0;
}
```

# LXIX.[\[USACO18JAN\]Stamp Painting G](https://www.luogu.com.cn/problem/P4187)

思路：

发现**任何具有一段长度大于等于$K$的相同颜色区间的串**都是合法的（这个区间被看作最后一次染色的目标）。

因此反向思考，我们求出所有不具有长度大于等于$k$的相同颜色区间的串数量，然后用总数量（$M^N$）减一下即可。

我们设$f[i]$表示前$i$位的方案数。

则有

$f[i]=\\begin{cases}M^i(1\\leq i&lt;K)\\(\\sum\\limits\_{j=i-K+1}^{i-1}f[j])(M-1)\\end{cases}$

复杂度$O(NK)$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int n,m,p,f[1001000],res=1;
int main(){
	scanf("%d%d%d",&n,&m,&p);
	f[0]=1;
	for(int i=1;i<p;i++,res=(1ll*res*m)%mod)f[i]=(1ll*f[i-1]*m)%mod;
	for(int i=p;i<=n;i++,res=(1ll*res*m)%mod){
		for(int j=i-p+1;j<i;j++)(f[i]+=f[j])%=mod;
		f[i]=1ll*f[i]*(m-1)%mod;
	}
//	for(int i=1;i<=n;i++)printf("%d ",f[i]);
	printf("%d\n",(mod+res-f[n])%mod);
	return 0;
}
```

然后套上前缀和，复杂度$O(N)$。

代码:

```cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int n,m,p,f[1001000],res=1,s[1001000];
int main(){
	scanf("%d%d%d",&n,&m,&p);
	f[0]=1;
	for(int i=1;i<p;i++,res=(1ll*res*m)%mod)f[i]=(1ll*f[i-1]*m)%mod,s[i]=(s[i-1]+f[i])%mod;
	for(int i=p;i<=n;i++,res=(1ll*res*m)%mod)f[i]=1ll*(s[i-1]-s[i-p]+mod)%mod*(m-1)%mod,s[i]=(s[i-1]+f[i])%mod;
	printf("%d\n",(mod+res-f[n])%mod);
	return 0;
}
```

# LXX.[\[USACO5.5\]贰五语言Two Five](https://www.luogu.com.cn/problem/P2750)

~~这题已经在我的收藏夹里面吃了大半年的灰了~~

发现当表格填到某个地方后，它一定是呈现出一条逐行递减的轮廓线的。

因此，我们设$f[a][b][c][d][e]$表示第$1$行填了$a$个……第$5$行填了$e$个的方案数。

则只有$5\\geq a\\geq b\\geq c\\geq d\\geq e\\geq 0$的状态才是合法的。

用记忆化搜索实现。之后对于每一位确定应该填什么即可。复杂度$25^7$（上界，真实复杂度远远不到）

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int f[6][6][6][6][6],n;
char tp[2],s[100],t[100];
bool che(char x,int y){
	return (!x)||x=='A'+y;
}
int dfs(int a,int b,int c,int d,int e){
	if(a+b+c+d+e==25)return 1;
	int &ret=f[a][b][c][d][e];
	if(ret)return ret;
	if(a<5&&che(s[a],a+b+c+d+e))ret+=dfs(a+1,b,c,d,e);
	if(b<a&&che(s[b+5],a+b+c+d+e))ret+=dfs(a,b+1,c,d,e);
	if(c<b&&che(s[c+10],a+b+c+d+e))ret+=dfs(a,b,c+1,d,e);
	if(d<c&&che(s[d+15],a+b+c+d+e))ret+=dfs(a,b,c,d+1,e);
	if(e<d&&che(s[e+20],a+b+c+d+e))ret+=dfs(a,b,c,d,e+1);
//	printf("%d %d %d %d %d:%d\n",a,b,c,d,e,res);
	return ret;
}
bool used[100];
int main(){
	scanf("%s",tp);
	if(tp[0]=='N'){
		scanf("%d",&n);
		int sum=0;
		for(int i=0;i<25;i++)for(s[i]='A';s[i]<='Z';s[i]++){
			if(used[s[i]])continue;
			used[s[i]]=true;
			memset(f,0,sizeof(f));
			int tmp=dfs(0,0,0,0,0);
			if(sum+tmp>=n)break;
			sum+=tmp;
			used[s[i]]=false;
		}
		printf("%s\n",s);
	}else{
		scanf("%s",t);
		int res=0;
		for(int i=0;i<25;i++)for(s[i]='A';s[i]<t[i];s[i]++){
			memset(f,0,sizeof(f));
			res+=dfs(0,0,0,0,0); 
		}
		printf("%d\n",res+1);
	}
	return 0;
}
```

# LXXI.[\[ABC163F\]path pass i](https://atcoder.jp/contests/abc163/tasks/abc163_f)

思路：

反向考虑。我们计算出不包含任何颜色为$i$的节点的路径的数量，再用总路径数一减就行。

则，我们删去所有颜色为$i$的节点，整棵树就会被分成许多连通块。则不经过任何一个颜色为$i$的节点的路径数量，就是$\\sum\\dfrac{(\\text{连通块大小})\*(\\text{连通块大小}+1)}{2}$。

设$f[i][j]$表示以$i$为根的子树中，删掉所有颜色为$j$的点后，有多少个点与$i$断开联系。再设$sz[i]$表示子树大小。

则$i$节点所在的连通块大小即为$sz[i]-f[i][j]$。

乍一看这状态是$O(n^2)$的。但是如果我们用`std::map`维护状态，并且在合并状态时启发式合并一下，复杂度就是$O(n\\log^2n)$的。

在节点$i$时，将所有$f\\big[j\big]\\big\[col[i]\\big]$（其中$j$是$i$的儿子）计入答案，它们被看作是一个连通块的根。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
#define sqr(x) 1ll*x*(x+1)>>1ll
typedef long long ll;
int n,col[200100],sz[200100];
map<int,int>f[200100];
vector<int>v[200100],res[200100];
void dfs(int x,int fa){
	sz[x]=1;
	for(int y:v[x]){
		if(y==fa)continue;
		dfs(y,x),sz[x]+=sz[y];
		int cc=sz[y];
		if(f[y].find(col[x])!=f[y].end())cc-=f[y][col[x]];
		res[col[x]].push_back(cc);
		if(f[x].size()<f[y].size())swap(f[x],f[y]);
		for(auto i:f[y])f[x][i.first]+=i.second; 
	}
	f[x][col[x]]=sz[x];
}
int main(){
	scanf("%d",&n);
	for(int i=1;i<=n;i++)scanf("%d",&col[i]);
	for(int i=1,x,y;i<n;i++)scanf("%d%d",&x,&y),v[x].push_back(y),v[y].push_back(x);
	dfs(1,0);
	for(int i=1;i<=n;i++)res[i].push_back(n-f[1][i]);
	for(int i=1;i<=n;i++){
		ll ans=sqr(n);
		for(auto j:res[i])ans-=sqr(j);
		printf("%lld\n",ans);
	}
	return 0;
}
```

# LXXII.[\[HEOI2016\/TJOI2016\]序列](https://www.luogu.com.cn/problem/P4093)

~~说实话我对于这道题应该归到DP还是树套树时曾经纠结了很久~~

我们回忆一下正牌的LIS：

对于$\\forall j&lt;i\\ \\land\\ a_j\\leq a_i$，$f[i]$可以从$f[j]$转移过来。

现在，我们设$mx_i,mn_i$分别表示位置$i$所有变化中的最大值以及最小值，

则对于$\\forall j&lt;i\\ \\land\\ mx_j\\leq a_i\\ \\land\\ a_j\\leq mn_i$，$f[i]$可以从$f[j]$转移过来。

直接暴力转移，复杂度$O(n^2)$，期望得分$50\\%$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,a[100100],mn[100100],mx[100100],f[100100],res;
int main(){
	scanf("%d%d",&n,&m);
	for(int i=1;i<=n;i++)scanf("%d",&a[i]),mn[i]=mx[i]=a[i];
	for(int i=1,x,y;i<=m;i++)scanf("%d%d",&x,&y),mn[x]=min(mn[x],y),mx[x]=max(mx[x],y);
	for(int i=1;i<=n;i++){
		for(int j=i-1;j;j--)if(mx[j]<=a[i]&&a[j]<=mn[i])f[i]=max(f[i],f[j]);
		f[i]++,res=max(res,f[i]);
	}
	printf("%d\n",res);
	return 0;
}
```

然后我们发现，如果把$(mx_j,a_j)$看成一对坐标的话，它又转变成矩形内部$\\max$了。

然后无脑树套树维护一下即可。

~~我吹爆树状数组套权值线段树！！！好写到爆！！！~~

```cpp
#include<bits/stdc++.h>
using namespace std;
const int N=100000;
#define mid ((l+r)>>1)
int n,m,a[100100],mn[100100],mx[100100],f[100100],res,cnt,root[100100];
struct node{
	int lson,rson,mx;
}seg[10010000];
void mod(int &x,int l,int r,int P,int val){
	if(l>P||r<P)return;
	if(!x)x=++cnt;
	seg[x].mx=max(seg[x].mx,val);
	if(l==r)return;
	mod(seg[x].lson,l,mid,P,val),mod(seg[x].rson,mid+1,r,P,val);
}
void MOD(int x,int y,int val){
	while(x<=N)mod(root[x],1,N,y,val),x+=x&-x;
}
int ask(int x,int l,int r,int P){
	if(!x||l>P)return 0;
	if(r<=P)return seg[x].mx;
	return max(ask(seg[x].lson,l,mid,P),ask(seg[x].rson,mid+1,r,P));
}
int ASK(int x,int y){
	int ans=0;
	while(x)ans=max(ans,ask(root[x],1,N,y)),x-=x&-x;
	return ans;
}
int main(){
	scanf("%d%d",&n,&m);
	for(int i=1;i<=n;i++)scanf("%d",&a[i]),mn[i]=mx[i]=a[i];
	for(int i=1,x,y;i<=m;i++)scanf("%d%d",&x,&y),mn[x]=min(mn[x],y),mx[x]=max(mx[x],y);
	for(int i=1;i<=n;i++){
		f[i]=ASK(a[i],mn[i]);
		f[i]++,res=max(res,f[i]);
		MOD(mx[i],a[i],f[i]);
	}
	printf("%d\n",res);
	return 0;
}
```

# LXXIII.[\[USACO19DEC\]Greedy Pie Eaters P](https://www.luogu.com.cn/problem/P5851)

考场上写了个暴力贪心（因为看到题面中的 `greedy` ……）然后光荣爆炸……

因为$n\\leq 300$，考虑区间DP。

设$f[i][j]$表示有且只有区间$[i,j]$里的$\\pi$被吃完后的最大收益。

则我们可以得到如下转移：

$f[i][j]=\\max\\limits\_{k=i}^{j}f[i][k-1]+???+f[k+1][j]$

含义为：我们特地留下第$k$个$\\pi$不吃，剩下全吃掉，然后选择能吃到第$k$个$\\pi$的最大的那头牛。

而这个$???$，就是那头牛的体重。

我们思考这头牛必须具有什么特征：

首先，它所吃掉的$\\pi$，必定是$[i,j]$的子区间；

其次，这个区间里必须包含第$k$个$\\pi$。

因此，我们设$g[i][j][k]$表示这样的牛的最大体重。

然后$g$也可以通过区间DP算出。

复杂度$O(n^3)$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,f[510][510],g[510][510][510];
int main(){
	scanf("%d%d",&n,&m);
	for(int i=1,x,y,z;i<=m;i++){
		scanf("%d%d%d",&z,&x,&y);
		for(int j=x;j<=y;j++)g[x][y][j]=max(g[x][y][j],z);
	}
	for(int k=1;k<=n;k++)for(int i=k;i>=1;i--)for(int j=k;j<=n;j++)g[i][j][k]=max(g[i][j][k],max(g[i+1][j][k],g[i][j-1][k]));
	for(int l=1;l<=n;l++)for(int i=1,j=i+l-1;j<=n;i++,j++)for(int k=i;k<=j;k++)f[i][j]=max(f[i][j],f[i][k-1]+g[i][j][k]+f[k+1][j]);
	printf("%d\n",f[1][n]);
	return 0;
}
```

# LXXIV.[\[USACO18DEC\]Sort It Out P](https://www.luogu.com.cn/problem/P5156)

集合中的数一定是某一条LIS的补集，这点还是比较好想的。

我们要集合的字典序最小，就是让集合的补集的字典序最大。

最大就可以考虑按位处理LIS中的数。

我们从后往前求LIS。我们设$f[i]$表示以当前位置开头的LIS的长度以及数量（类型是一个`pair`）。$f[i]$可以直接套BIT解决。

然后，对于每个$k$，我们将所有长度为$k$的位置丢到一个`vector`里面，即为确定序列**正数第$k$位**时的过程；然后从小往大遍历这些位置。就是正常的求第$k$大的常规思路。

**注意，因为是LIS，当你将一个数选入序列后，所有比它小的位置都不能再选了！！！**

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
#define pii pair<int,ll>
#define X first
#define Y second
#define mp make_pair
#define O mp(0,0)
const ll lim=1e18;
int n,a[100100],len;
bool on[100100];
pii f[100100],t[100100];
void operator +=(pii &x,const pii &y){
	if(x.X<y.X)x=y;
	else if(x.X==y.X)x.Y=min(lim,x.Y+y.Y);
}
void ADD(int x,pii y){while(x)t[x]+=y,x-=x&-x;}
pii ASK(int x){pii ret=O;while(x<=n)ret+=t[x],x+=x&-x;return ret;}
ll m;
vector<int>v[100100];
int main(){
	scanf("%d%lld",&n,&m);
	for(int i=1;i<=n;i++)scanf("%d",&a[i]);
	ADD(n,mp(0,1));
	for(int i=n;i;i--)f[i]=ASK(a[i]),f[i].X++,ADD(a[i],f[i]),len=max(len,f[i].X),v[f[i].X].push_back(i);
	printf("%d\n",n-len);
	for(int i=len,k=1;i;i--){
		reverse(v[i].begin(),v[i].end());
		for(auto j:v[i]){
			if(f[j].Y<m)m-=f[j].Y;
			else{
				on[a[j]]=true;
				while(k<j)f[k++]=O;
				break;
			}
		}
	}
	for(int i=1;i<=n;i++)if(!on[i])printf("%d\n",i);
	return 0;
}
```

# LXXV.[\[USACO20FEB\]Help Yourself G](https://www.luogu.com.cn/problem/P6146)

思路：

考虑将线段按照左端点排序。

设$f[i]$表示前$i$个线段的复杂度之和。

则$f[i]=2\*f[i-1]+2^{sum[l_i-1]}$。其中$sum_i$是右端点$\\leq i$的线段数目，$l_i$是$i$线段的左端点。

思考：

再往前的复杂度之和，无论第$i$根线段选与不选，都是无法改变的。因此要$\*2$。

当之前的线段与线段$i$交集为空时，联通块新增一块。这部分共有$2^{sum[l_i-1]}$种选法。

复杂度$O(n\\log n)$（排序是瓶颈，如果换成桶排就是$O(n)$的）

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int n,sum[200100],bin[100100],f[100100];
pair<int,int>p[100100];
int main(){
	scanf("%d",&n),bin[0]=1;
	for(int i=1;i<=n;i++)scanf("%d%d",&p[i].first,&p[i].second),sum[p[i].second]++,bin[i]=(bin[i-1]<<1)%mod;
	for(int i=1;i<=2*n;i++)sum[i]+=sum[i-1];
	sort(p+1,p+n+1);
	for(int i=1;i<=n;i++)f[i]=(2ll*f[i-1]+bin[sum[p[i].first-1]])%mod;
	printf("%d\n",f[n]);
	return 0;
}
```

# LXXVI.[高速公路](https://www.luogu.com.cn/problem/P3994)

简直恶心到爆炸……

首先，暴力的DP是非常简单的。设$dis_x$表示位置$x$到根的距离，则有

$$f_x=\\min\\limits_{y\\text{ is an ancestor of }x}f_y+p_x(dis_x-dis_y)+q_x$$

暴力一敲，期望得分$40\\%$。由于数据可能水了，实际得分$60\\%$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
int n,head[1001000],cnt,a[1001000],b[1001000],dis[1001000];
ll f[1001000];
struct node{
	int to,next,val;
}edge[1001000];
void ae(int u,int v,int w){
	edge[cnt].next=head[u],edge[cnt].to=v,edge[cnt].val=w,head[u]=cnt++;
}
vector<int>v;
void dfs(int x){
	for(auto y:v)f[x]=min(f[x],1ll*a[x]*(dis[x]-dis[y])+b[x]+f[y]);
	v.push_back(x);
	for(int i=head[x];i!=-1;i=edge[i].next)dis[edge[i].to]=dis[x]+edge[i].val,dfs(edge[i].to);
	v.pop_back();
}
int main(){
	scanf("%d",&n),memset(head,-1,sizeof(head)),memset(f,0x3f3f3f3f,sizeof(f)),f[1]=0;
	for(int i=2,x,y;i<=n;i++)scanf("%d%d%d%d",&x,&y,&a[i],&b[i]),ae(x,i,y);
	dfs(1);
	for(int i=2;i<=n;i++)printf("%lld\n",f[i]);
	return 0;
}
```

考虑斜率优化一下。

我们先把问题抽象到序列上。设有一个$j&lt;k&lt;i$，则如果$j$比$k$优，必有

$$f_j+p_i(dis_i-dis_j)+q_i\\leq f_k+p_i(dis_i-dis_k)+q_i$$

$$f_j+p_idis_i-p_idis_j\\leq f_k+p_idis_i-p_idis_k$$

$$f_j-f_k\\leq p_idis_j-p_idis_k$$

$$f_j-f_k\\leq p_i(dis_j-dis_k)$$

$$\\dfrac{f_j-f_k}{dis_j-dis_k}\\geq p_i$$

然后直接优化即可，因为$p_i$保证递增。

但是，因为是在树上，所以你从一颗子树中跑出来之后，还要复原原序列！

当然，复原是很简单的，因为斜率优化的过程中除了队首队尾的移动以外，唯一真正改动的位置就是最后的入队环节。这时候只需要记录这个位置原本放了什么即可。

但是，暴力地维护队列的话，就不能完美地应用"单调队列"的性质了，因此复杂度最劣仍然是$O(n^2)$。期望得分$60\\%$（听说常卡的好也能A？）

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
int n,head[1001000],cnt,a[1001000],b[1001000],q[1001000],l[1001000],r[1001000],cha[100100];
ll f[1001000],dis[1001000];
void read(int &x){
	x=0;
	char c=getchar();
	while(c>'9'||c<'0')c=getchar();
	while(c>='0'&&c<='9')x=x*10+c-48,c=getchar();
}
struct node{
	int to,next,val;
}edge[1001000];
void ae(int u,int v,int w){
	edge[cnt].next=head[u],edge[cnt].to=v,edge[cnt].val=w,head[u]=cnt++;
}
void dfs(int x){
	while(l[x]<r[x]&&(f[q[l[x]]]-f[q[l[x]+1]])>=(dis[q[l[x]]]-dis[q[l[x]+1]])*a[x])l[x]++;
	f[x]=(dis[x]-dis[q[l[x]]])*a[x]+b[x]+f[q[l[x]]];
	while(l[x]<r[x]&&(f[q[r[x]-1]]-f[q[r[x]]])*(dis[q[r[x]]]-dis[x])>=(f[q[r[x]]]-f[x])*(dis[q[r[x]-1]]-dis[q[r[x]]]))r[x]--;
	cha[x]=q[++r[x]],q[r[x]]=x;
	printf("%d:%d,%d:",x,l[x],r[x]);for(int i=l[x];i<=r[x];i++)printf("%d ",q[i]);puts("");
	for(int i=head[x];i!=-1;i=edge[i].next)dis[edge[i].to]=dis[x]+edge[i].val,l[edge[i].to]=l[x],r[edge[i].to]=r[x],dfs(edge[i].to);
	q[r[x]]=cha[x];
}
int main(){
	read(n),memset(head,-1,sizeof(head));
	for(int i=2,x,y;i<=n;i++)read(x),read(y),read(a[i]),read(b[i]),ae(x,i,y);
	l[1]=1,dfs(1);
	for(int i=2;i<=n;i++)printf("%lld\n",f[i]);
	return 0;
}
```

发现我们每个位置都那么费劲地移动左右端点太蠢了。不如直接套上一个二分。复杂度是妥妥的$O(n\\log n)$。

（这二分真的非常难写，各种边界太恶心了）

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
int n,head[1001000],cnt,a[1001000],b[1001000],q[1001000],l[1001000],r[1001000],cha[1001000];
ll f[1001000],dis[1001000];
void read(int &x){
	x=0;
	char c=getchar();
	while(c>'9'||c<'0')c=getchar();
	while(c>='0'&&c<='9')x=x*10+c-48,c=getchar();
}
struct node{
	int to,next,val;
}edge[1001000];
void ae(int u,int v,int w){
	edge[cnt].next=head[u],edge[cnt].to=v,edge[cnt].val=w,head[u]=cnt++;
}
void dfs(int x){
	int L,R,res;
	L=l[x],R=r[x]-1,res=r[x];
	while(L<=R){
		int mid=(L+R)>>1;
		if((f[q[mid]]-f[q[mid+1]])>=(dis[q[mid]]-dis[q[mid+1]])*a[x])L=mid+1;
		else R=mid-1,res=mid;
	} 
	l[x]=res;
	f[x]=(dis[x]-dis[q[l[x]]])*a[x]+b[x]+f[q[l[x]]];
	L=l[x]+1,R=r[x],res=l[x];
	while(L<=R){
		int mid=(L+R)>>1;
		if((f[q[mid-1]]-f[q[mid]])*(dis[q[mid]]-dis[x])>=(f[q[mid]]-f[x])*(dis[q[mid-1]]-dis[q[mid]]))R=mid-1;
		else res=mid,L=mid+1;
	}	
	r[x]=res;
	cha[x]=q[++r[x]],q[r[x]]=x;
	for(int i=head[x];i!=-1;i=edge[i].next)dis[edge[i].to]=dis[x]+edge[i].val,l[edge[i].to]=l[x],r[edge[i].to]=r[x],dfs(edge[i].to);
	q[r[x]]=cha[x];
}
int main(){
	read(n),memset(head,-1,sizeof(head));
	for(int i=2,x,y;i<=n;i++)read(x),read(y),read(a[i]),read(b[i]),ae(x,i,y);
	l[1]=1,dfs(1);
	for(int i=2;i<=n;i++)printf("%lld\n",f[i]);
	return 0;
}
```

# LXXVII.[\[CmdOI2019\]任务分配问题](https://www.luogu.com.cn/problem/P5574)

这道题与LXI.[CF868F Yet Another Minimization Problem](https://www.luogu.com.cn/problem/CF868F)长得很像。实际算法也类似。

首先，题意就是把所有数划分成$k$段，使得每段内部**正序对**数量之和最少。设$w(i,j)$表示区间$(i,j)$内部正序对数量。则很轻松就能得到

$$w(i-1,j+1)+w(i,j)\\geq w(i,j+1)+w(i-1,j)$$

因为其它所有正序对都在两个中被统计了，唯独$(i-1,j+1)$的正序对只有可能在前一半中被统计。因此此式显然成立，即四边形不等式成立，可以使用决策单调性优化。

因此直接套用分治+类似莫队的$w$求法即可。复杂度$O(nk\\log^2n)$。

代码（将正序对转换成了逆序对）：

```cpp
#include<bits/stdc++.h>
using namespace std;
typedef long long lol;
int n,m,t[25010],a[25010],ll,rr;
lol res,f[25010],g[25010];
void add(int x,int y){
	while(x<=n)t[x]+=y,x+=x&-x;
}
int ask(int x){
	int rt=0;
	while(x)rt+=t[x],x-=x&-x;
	return rt;
}
lol calc(int l,int r){
	if(l>r)return 0x3f3f3f3f3f3f3f3f;
	while(l>ll)add(a[ll],-1),res-=ask(a[ll]),ll++;
	while(l<ll)--ll,res+=ask(a[ll]),add(a[ll],1);
	while(r<rr)add(a[rr],-1),res-=ask(n)-ask(a[rr]),rr--;
	while(r>rr)++rr,res+=ask(n)-ask(a[rr]),add(a[rr],1);
	return res;
}
void func(int l,int r,int L,int R){
	if(l>r||L>R)return;
	int mid=(l+r)>>1,mp;
	lol mn=0x3f3f3f3f3f3f3f3f;
	for(int i=L;i<=R;i++)if(f[i]+calc(i+1,mid)<mn)mn=f[i]+calc(i+1,mid),mp=i;
	g[mid]=mn;
	func(l,mid-1,L,mp),func(mid+1,r,mp,R);
}
int main(){
	scanf("%d%d",&n,&m);
	for(int i=1;i<=n;i++)scanf("%d",&a[i]),a[i]=n-a[i]+1,res+=ask(n)-ask(a[i]),f[i]=res,add(a[i],1);
	ll=1,rr=n;
	while(--m)func(1,n,0,n-1),memcpy(f,g,sizeof(f));
	printf("%lld\n",f[n]);
	return 0;
}
```

# LXXVIII.[\[USACO12OPEN\]Bookshelf G](https://www.luogu.com.cn/problem/P1848)

转移很简单，直接设$f[i]$表示前$i$个位置书架的最小高度和即可。

考虑转移。

我们有暴力的公式

$$f[i]=\\min\\limits_{j=1}^{i}\\Big{f_{j-1}+\\max{h_j,\\dots,h_i}\\Big}$$

因为当$i$不变时，随着$j$的增长，那个$\\max$是单调不升的。因此我们可以用单调队列维护$\\max$的转折点，因为$\\max$一定是由一段一段组成的。

因为一整段里面的$\\max$都是一样的，因此它就只取决于那个$f_j$。因此我们只需要对于每一段维护一个$\\min{f_j}$即可。

法1.线段树

这个$f_j$当然可以用线段树求区间$\\min$。因为单调队列中，只有队首和队尾的两个元素的$\\min{f_j}+h_k$是每次都要重算的，因此总复杂度$O(n\\log n)$。用`std::multiset`维护单调队列中$\\min{f_j}+h_k$的值，在插入新元素时重算后投入`multiset`，弹出元素时扔出去即可。总复杂度$O(n\\log n)$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
#define lson x<<1
#define rson x<<1|1
#define mid ((l+r)>>1)
#define int long long
int n,m,s[100100],h[100100],f[100100],q[100100],p[100100],l,r,mn[400100];
void pushup(int x){
	mn[x]=min(mn[lson],mn[rson]);
}
void Modify(int x,int l,int r,int P,int val){
	if(l>P||r<P)return;
	if(l==r){mn[x]=val;return;}
	Modify(lson,l,mid,P,val),Modify(rson,mid+1,r,P,val),pushup(x);
}
int Ask(int x,int l,int r,int L,int R){
	if(l>R||r<L)return 0x3f3f3f3f3f3f3f3f;
	if(L<=l&&r<=R)return mn[x];
	return min(Ask(lson,l,mid,L,R),Ask(rson,mid+1,r,L,R));
}
multiset<int>ms;
signed main(){
	scanf("%lld%lld",&n,&m),memset(f,0x3f,sizeof(f)),f[0]=0;
	for(int i=1;i<=n;i++)scanf("%lld%lld",&h[i],&s[i]),s[i]+=s[i-1];
	l=r=1,ms.insert(0);
	for(int i=1,j=1;i<=n;i++){
		Modify(1,1,n,i,f[i-1]);
		while(s[i]-s[j-1]>m)j++;
		while(l<=r&&s[i]-s[q[l]-1]>m)ms.erase(ms.find(p[l++]));
		while(l<=r&&h[i]>=h[q[r]])ms.erase(ms.find(p[r--]));
		q[++r]=i;
		if(l<r)p[r]=h[q[r]]+Ask(1,1,n,q[r-1]+1,q[r]),ms.erase(ms.find(p[l])),ms.insert(p[r]);
		p[l]=h[q[l]]+Ask(1,1,n,j,q[l]),ms.insert(p[l]);
		f[i]=*ms.begin();
	}
	printf("%lld\n",f[n]);
	return 0;
}
```

法2.直接观察

实际上，这个$f$是单调不降的（注意它的定义）。因此$\\min{f_j}$一定出现在最左边的地方。因此直接用最左边的$f$值替换上面的$\\min$即可。因为复杂度瓶颈在`multiset`上，因此复杂度不变。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int n,m,s[100100],h[100100],f[100100],q[100100],p[100100],l,r;
multiset<int>ms;
signed main(){
	scanf("%lld%lld",&n,&m),memset(f,0x3f,sizeof(f)),f[0]=0;
	for(int i=1;i<=n;i++)scanf("%lld%lld",&h[i],&s[i]),s[i]+=s[i-1];
	l=r=1,ms.insert(0);
	for(int i=1,j=1;i<=n;i++){
		while(s[i]-s[j-1]>m)j++;
		while(l<=r&&s[i]-s[q[l]-1]>m)ms.erase(ms.find(p[l++]));
		while(l<=r&&h[i]>=h[q[r]])ms.erase(ms.find(p[r--]));
		q[++r]=i;
		if(l<r)p[r]=h[q[r]]+f[q[r-1]],ms.erase(ms.find(p[l])),ms.insert(p[r]);
		p[l]=h[q[l]]+f[j-1],ms.insert(p[l]);
		f[i]=*ms.begin();
	}
	printf("%lld\n",f[n]);
	return 0;
}
```

# LXXIX.[\[AGC013D\] Piling Up](https://www.luogu.com.cn/problem/AT2370)

一个很naive的思路就是设$f[i][j]$表示当前进行了$i$步，并且盒子中剩下了$j$个白球的方案数，然后直接DP即可。

但是这样是有问题的------它没有考虑到重复计算的问题。

我们不妨令$+$符号表示取出黑球，$-$符号表示取出白球。

则一种方式是$6\\xrightarrow{+-}6\\xrightarrow{--}5$，其中数字表示剩余白球数。

另一种方式是$4\\xrightarrow{+-}4\\xrightarrow{--}3$。很明显，两者即使盒中球数不同，但是序列是相同的。

为了避免重复计算，我们可以强制要求**只有过程中出现过$0$的序列**才是合法序列。

于是我们可以设$f[i][j][0/1]$表示进行$i$步，盒子中剩下$j$个白球，且（没有\/有）到过$0$的方案数。则答案即为$\\sum\\limits\_{i=0}^nf[m][i][1]$。

要注意的是，这里的转移过程必须保证**任意时刻球的数量必须在$[0,n]$范围之内**，因此对于不合法的状态要记得特判掉。

复杂度$O(nm)$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int n,m,f[3010][3010][2],res;//0: haven't reached 0; 1:have reached 0
int main(){
	scanf("%d%d",&n,&m);
	for(int i=0;i<=n;i++)f[0][i][i==0]=1;
	for(int i=0;i<m;i++)for(int j=0;j<=n;j++){
		if(j)(f[i+1][j][j==1]+=f[i][j][0])%=mod,(f[i+1][j][1]+=f[i][j][1])%=mod;//-+
		if(j)(f[i+1][j-1][j==1]+=f[i][j][0])%=mod,(f[i+1][j-1][1]+=f[i][j][1])%=mod;//--;
		if(j<n)(f[i+1][j][0]+=f[i][j][0])%=mod,(f[i+1][j][1]+=f[i][j][1])%=mod;//+-;
		if(j<n)(f[i+1][j+1][0]+=f[i][j][0])%=mod,(f[i+1][j+1][1]+=f[i][j][1])%=mod;//++;
	}
	for(int i=0;i<=n;i++)(res+=f[m][i][1])%=mod;
	printf("%d\n",res);
	return 0;
}
```

# LXXX.[\[AGC024E\] Sequence Growing Hard](https://www.luogu.com.cn/problem/AT2370)

首先，我们肯定能想到从第一个序列开始，**依次加入一个新数得到下一个序列**，同时还要保证字典序递增。我们如果让新数递增的话，就可以DP了。

我们首先观察往一个序列中加入一个不大于最大值的数会有多少种可能：

我们在$1323$中加入一个$3$，

|   位置  |    结果   |
| :---: | :-----: |
|   开头  | $31323$ |
| 第一个数后 | $13323$ |
| 第二个数后 | $13323$ |
| 第三个数后 | $13233$ |
| 第四个数后 | $13233$ |

明显所有结果全都符合要求，但是有重复计算的地方。

我们可以强制要求加数必须加在**连续一段相同的数的后面**，在上例中就是你无法在第一个、第三个数后面添加$3$。

我们可以设$f[i][j][k]$表示当前处理完成了前$i$个串，计划往第$i+1$个串里加入一个数$j$，并且有$k$个位置可以加入$j$的方案数。

则$f[i][j][k]$可以转移到：

1.  如果$k>0$，可以转移到$f[i][j][k-1]$，它的意义是我们跳过第$k$个位置不加。

2.  如果$k=0$，可以转移到$f[i][j+1][i]$，它的意义是第$j$个数已经全部加完，可以尝试$j+1$了。它有$i$个位置可以填，因为没有任何一个数与$j+1$相同，它可以直接加到任何数后面。

3.  无论何时，都可以转移到$f[i+1][j][k]$，意义是我们在第$k$个位置加入一个数。这共有$k+1$种加法，因为我们还有一种**在开头**的加法是一直可以的。

复杂度$O(n^3)$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,p,f[310][310][310];
//f[i][j][k]:we've finished constructing the first i sequences, now we're going to add the number j into the i+1-th sqeuence, and there're k places to add j into
int main(){
	scanf("%d%d%d",&n,&m,&p),f[0][1][0]=1;
	for(int i=0;i<=n;i++)for(int j=1;j<=m;j++)for(int k=i;k>=0;k--){
		if(k)(f[i][j][k-1]+=f[i][j][k])%=p;//we decide not to add j to the k-th place, so we could add it to the (k-1)-th place.
		else(f[i][j+1][i]+=f[i][j][k])%=p;//we have tried every place j could be added to, now it's time to try j+1, which could be added into any place
		(f[i+1][j][k]+=1ll*f[i][j][k]*(k+1)%p)%=p;//we decide to add j to the k-th place, and there are (k+1) places for us to add (including the last one)
	}
	printf("%d\n",f[n][m+1][n]);//all n sequences've been constructed, and all number've been tried
	return 0;
}
```

# LXXXI.[CF1312G Autocompletion](https://www.luogu.com.cn/problem/CF1312G)

[题解](https://www.luogu.com.cn/blog/Troverld/solution-cf1312g)

# LXXXII.[UOJ#11. 【UTR #1】ydc的大树](http://uoj.ac/problem/11)

很明显，如果我们令一个黑点$x$为树根，设它的"好朋友"集合为$\\mathbb{S}$，则路径$(x,\\operatorname{LCA}{\\mathbb{S}})$中所有白节点均可以使$x$不开心。这个可以用**树上差分**来进行路径加。现在关键是求出$\\operatorname{LCA}{\\mathbb{S}}$。

我们采取**二次扫描与换根法**。第一遍扫描，我们求出一个节点子树中所有黑点到它的距离的最大值，以及这些离它最远的黑点的$\\operatorname{LCA}$。我们用一个`std::pair<int,int>`来储存这两个值，记作$f_x$。

我们考虑怎么求出$f_x$出来------

设有一条边是$(x,y,z)$。则$f_x$会从`f[y].first+z`最大的那个$y$转移过来；但是，如果存在两个不同的$y$都是最大值，显然它们的$\\operatorname{LCA}$就是$x$本身。

这是求$f_x$的代码（如果不存在这个黑点，$f_x$即为$(-1,0)$）。

```cpp
void dfs1(int x,int fa){
	if(bla[x])f[x]=make_pair(0,x);else f[x]=make_pair(-1,0);
	for(auto i:v[x]){
		if(i.first==fa)continue;
		dfs1(i.first,x);
		if(f[i.first].first!=-1)f[x].first=max(f[x].first,f[i.first].first+i.second);
	}
	if(f[x].first==-1)return;
	int cnt=0;
	for(auto i:v[x]){
		if(i.first==fa)continue;
		if(f[i.first].first==-1)continue;
		if(f[i.first].first+i.second==f[x].first)cnt++,f[x].second=f[i.first].second;
	}
	if(cnt>1)f[x].second=x;
}
```

既然要二次扫描，我们自然要设一个$g_x$，表示$x$子树外所有节点到$x$的最大距离及它们的$\\operatorname{LCA}$。

$g_x$可以从这些东西转移过来：

1.  兄弟们的$f_y$；

2.  父亲的$g_y$；

3.  父亲自身（假如父亲是黑点的话）

我们把前两个东西丢进`vector`中按照`first`从大到小排序。选取最大值（当然不能是$f_x$自身）转移即可。

当然，如果前两个东西中没有任何黑点，要考虑从父亲自身转移。

这部分的代码：

```cpp
void dfs2(int x,int fa){
	vector<pair<int,int> >u;
	for(auto i:v[x])if(i.first!=fa&&f[i.first].first!=-1)u.push_back(make_pair(f[i.first].first+i.second,f[i.first].second));
	if(g[x]!=make_pair(-1,0))u.push_back(g[x]);
	sort(u.rbegin(),u.rend());
	for(auto i:v[x]){
		if(i.first==fa)continue;
		for(auto j:u){
			if(j.second==f[i.first].second)continue;
			if(g[i.first]==make_pair(0,0)){g[i.first]=j;continue;}
			if(g[i.first].first==j.first)g[i.first].second=x;
			break;
		}
		if(g[i.first]==make_pair(0,0))g[i.first]=(bla[x]?make_pair(i.second,x):make_pair(-1,0));
		else g[i.first].first+=i.second;
		dfs2(i.first,x);
	}
}
```

最终就是答案统计了。对于所有的黑点，如果`f[x].first==g[x].first`，显然$\\operatorname{LCA}$为$x$本身，可以忽略；否则，选取`f[x]`与`g[x]`中较大的那个的`second`，进行树上差分即可。

复杂度$O(n\\log n)$（瓶颈在于树上差分，求$g_x$部分的那个排序其实没有必要，但是如果这样写会更加清晰）。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,anc[100100][20],dep[100100],sum[100100],mx,cnt;
vector<pair<int,int> >v[100100];
pair<int,int>f[100100],g[100100];//first:the maximum route length; second:the lca of all the 'good friends'
bool bla[100100];
void dfs1(int x,int fa){
	if(bla[x])f[x]=make_pair(0,x);else f[x]=make_pair(-1,0);
	for(auto i:v[x]){
		if(i.first==fa)continue;
		dfs1(i.first,x);
		if(f[i.first].first!=-1)f[x].first=max(f[x].first,f[i.first].first+i.second);
	}
	if(f[x].first==-1)return;
	int cnt=0;
	for(auto i:v[x]){
		if(i.first==fa)continue;
		if(f[i.first].first==-1)continue;
		if(f[i.first].first+i.second==f[x].first)cnt++,f[x].second=f[i.first].second;
	}
	if(cnt>1)f[x].second=x;
}
void dfs2(int x,int fa){
	vector<pair<int,int> >u;
	for(auto i:v[x])if(i.first!=fa&&f[i.first].first!=-1)u.push_back(make_pair(f[i.first].first+i.second,f[i.first].second));
	if(g[x]!=make_pair(-1,0))u.push_back(g[x]);
	sort(u.rbegin(),u.rend());
	for(auto i:v[x]){
		if(i.first==fa)continue;
		for(auto j:u){
			if(j.second==f[i.first].second)continue;
			if(g[i.first]==make_pair(0,0)){g[i.first]=j;continue;}
			if(g[i.first].first==j.first)g[i.first].second=x;
			break;
		}
		if(g[i.first]==make_pair(0,0))g[i.first]=(bla[x]?make_pair(i.second,x):make_pair(-1,0));
		else g[i.first].first+=i.second;
		dfs2(i.first,x);
	}
}
void dfs3(int x,int fa){
	anc[x][0]=fa,dep[x]=dep[fa]+1;
	for(auto i:v[x])if(i.first!=fa)dfs3(i.first,x);
}
void dfs4(int x,int fa){
	for(auto i:v[x])if(i.first!=fa)dfs4(i.first,x),sum[x]+=sum[i.first];
}
int LCA(int x,int y){
	if(dep[x]>dep[y])swap(x,y);
	for(int i=19;i>=0;i--)if(dep[x]<=dep[y]-(1<<i))y=anc[y][i];
	if(x==y)return x;
	for(int i=19;i>=0;i--)if(anc[x][i]!=anc[y][i])x=anc[x][i],y=anc[y][i];
	return anc[x][0];
}
int main(){
	scanf("%d%d",&n,&m);
	for(int x;m--;)scanf("%d",&x),bla[x]=true;
	for(int i=1,x,y,z;i<n;i++)scanf("%d%d%d",&x,&y,&z),v[x].push_back(make_pair(y,z)),v[y].push_back(make_pair(x,z));
	g[1]=make_pair(-1,0);
	dfs1(1,0),dfs2(1,0),dfs3(1,0);
	for(int j=1;j<=19;j++)for(int i=1;i<=n;i++)anc[i][j]=anc[anc[i][j-1]][j-1];
	for(int i=1;i<=n;i++){
//		printf("%d:(%d,%d),(%d,%d)\n",i,f[i].first,f[i].second,g[i].first,g[i].second);
		if(!bla[i]||f[i].first==g[i].first)continue;
		int x,y=i;
		if(f[i].first>g[i].first)x=f[i].second;
		else x=g[i].second;
		int lca=LCA(x,y);
		sum[x]++,sum[y]++,sum[lca]--;
		if(anc[lca][0])sum[anc[lca][0]]--;
	}
	dfs4(1,0);
	for(int i=1;i<=n;i++)if(!bla[i])mx=max(mx,sum[i]);
	for(int i=1;i<=n;i++)if(!bla[i])cnt+=(sum[i]==mx);
	printf("%d %d",mx,cnt);
	return 0;
}
```

# LXXXIII.[CF261D Maxim and Increasing Subsequence](https://www.luogu.com.cn/problem/CF261D)

首先，我们可以发现，当这个重复次数很大的时候，答案就**等于序列中出现的不同权值个数**。实际上，这个"很大"就可以被当作"大于等于不同权值个数"。

不同权值个数实际上是$\\min(n,m)$级别的，其中$n$是序列长度，$m$是序列最大值。因此直接特判掉即可。

我们考虑**暴力DP**。设$f\_{i,j}$表明现在跑到序列中的第$i$个位置，且所有最后一个数小于等于$j$的LIS的长度的最大值。假如我们直接暴力扫过DP数组更新的话，最多最多更新$\\min(n,m)^2$次，即最终把DP数组中所有数全都更新到最大值。而又有$n\\times m\\leq2\\times10^7$，所以我们最终会发现复杂度最大只有$2\\times10^7$。时限$6$秒，轻松跑过。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int T,n,lim,m,a[100100],f[100100];
vector<int>v;
int main(){
	scanf("%d%d%d%d",&T,&n,&lim,&m);
	while(T--){
		v.clear();
		for(int i=0;i<n;i++)scanf("%d",&a[i]),v.push_back(a[i]);
		sort(v.begin(),v.end()),v.resize(unique(v.begin(),v.end())-v.begin());
		if(v.size()<=m){printf("%d\n",v.size());continue;}
		for(int i=0;i<n;i++)a[i]=lower_bound(v.begin(),v.end(),a[i])-v.begin()+1;
		for(int i=1;i<=v.size();i++)f[i]=0;
		for(int i=0;i<n*m;i++){
			int now=f[a[i%n]-1]+1;
			for(int j=a[i%n];j<=v.size();j++)if(f[j]<now)f[j]=now;else break;
			if(f[v.size()]==v.size())break;
		}
		printf("%d\n",f[v.size()]);
	}
	return 0;
}
```

# LXXXIV.[CF51F Caterpillar](https://www.luogu.com.cn/problem/CF51F)

也不知道算不算DP，反正就放这吧。

首先我们很轻松就能想到关于"环"，或者进一步地说，"边双连通分量"。因为最终图中不能有环，所以每个边双肯定最终会被缩成一个点。那么我们就也来缩一下。

在缩点之后，我们便得到了一片**森林**。

很明显对于每一棵树，我们都应该选择它的直径作为毛毛虫的主路径；然后将每一棵树的直径拼一起，便得到了一条大毛毛虫。

同时，叶子节点是不用管的------因为反正合并之后它还是叶子。

于是我们最终的答案就是：

$$(\\text{节点数}-\\text{边双数})+(\\text{联通块数}-1)+\\sum(\\text{连通块大小-直径大小-叶子数量}+2)$$

注意到那个"$+2$"，因为直径的端点既是叶子又在直径上，所以被算了两次，应该加回去。

同时孤立点注意特判掉。

~~问题来了，DP呢？问得好，求直径的时候可以用DP~~

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,col[20100],c,res,mx,leaf,sz;
namespace ECC{
	vector<int>v[20100];
	int dfn[20100],low[20100],tot;
	stack<int>s;
	void Tarjan(int x,int fa){
		dfn[x]=low[x]=++tot,s.push(x);
		for(auto y:v[x]){
			if(y==fa)continue;
			if(!dfn[y])Tarjan(y,x),low[x]=min(low[x],low[y]);
			else low[x]=min(low[x],dfn[y]);
		}
		if(dfn[x]!=low[x])return;
		c++;
		while(s.top()!=x)col[s.top()]=c,s.pop();
		col[s.top()]=c,s.pop();
	}
}
namespace Tree{
	vector<int>v[20100];
	int dis[20100];
	bool vis[20100];
	void dfs(int x){
		sz++,leaf+=(v[x].size()==1),vis[x]=true,dis[x]=1;
		for(auto y:v[x])if(!vis[y])dfs(y),mx=max(mx,dis[x]+dis[y]),dis[x]=max(dis[x],dis[y]+1);
	}
}
int main(){
	scanf("%d%d",&n,&m);
	for(int i=1,x,y;i<=m;i++)scanf("%d%d",&x,&y),ECC::v[x].push_back(y),ECC::v[y].push_back(x);
	for(int i=1;i<=n;i++)if(!ECC::dfn[i])ECC::Tarjan(i,0);
	res=n-c-1;
//	for(int i=1;i<=n;i++)printf("%d ",col[i]);puts("");
	for(int i=1;i<=n;i++)for(auto j:ECC::v[i])if(col[i]!=col[j])Tree::v[col[i]].push_back(col[j]);
	for(int i=1;i<=c;i++){
		if(Tree::vis[i])continue;
		mx=leaf=sz=0;
		Tree::dfs(i);
		res++;
		if(sz!=1)res+=sz-leaf-(mx-2);
	}
	printf("%d\n",res);
	return 0;
}
```

# LXXXV.[CF401D Roman and Numbers](https://www.luogu.com.cn/problem/CF401D)

思路：

我们设$num_i$表示$n$中出现了多少个数字$i$。然后就可以设$f[i][j]$表示当填入数字的状态是$i$，且当前数$\\%m$的余数是$j$时的方案数。则直接转移即可。

复杂度$O(18_2^{18}_m)$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
int m,num[10],a[10],pov[10],all,dig,dd;
ll n,f[1<<18][110],ten[20];
void teg(int ip){
	dig=0;
	for(int i=9;i>=0;i--)a[i]=ip%num[i],ip/=num[i],dig+=a[i];
}
int main(){
	scanf("%lld%d",&n,&m);
	while(n)num[n%10]++,n/=10,dd++;
	ten[0]=1;
	for(int i=1;i<=dd;i++)ten[i]=ten[i-1]*10;
	for(int i=0;i<10;i++)num[i]++;
	pov[9]=1;
	for(int i=8;i>=0;i--)pov[i]=pov[i+1]*num[i+1];
//	for(int i=0;i<10;i++)printf("%d ",num[i]);puts("");
//	for(int i=0;i<10;i++)printf("%d ",pov[i]);puts("");
	all=pov[0]*num[0];
	for(int i=1;i<10;i++)if(num[i]>1)f[pov[i]][(ten[dd-1]*i)%m]=1;
	for(int i=1;i<all;i++){
		teg(i);
//		printf("QWQ:%d:::",i);for(int j=0;j<10;j++)printf("%d ",a[j]);puts("");
		for(int j=0;j<m;j++){
//			printf("%d:%d\n",j,f[i][j]);
			if(!f[i][j])continue;
			for(int k=0;k<10;k++)if(num[k]-a[k]>1)f[i+pov[k]][(ten[dd-dig-1]*k+j)%m]+=f[i][j];		
		}
	}
	printf("%lld\n",f[all-1][0]);
	return 0;
}
```

# LXXXVI.[CF295D Greg and Caves](https://www.luogu.com.cn/problem/CF295D)

[题解](https://www.luogu.com.cn/blog/Troverld/solution-cf295d)

# LXXXVII.[CF938F Erasing Substrings](https://www.luogu.com.cn/problem/CF938F)

一个naive的想法是设$f\_{i,j}$表示在位置$[1,i]$中，我们删去了长度为$2^k(k\\in j)$的一些串，所能得到的最小字典序。使用二分+hash可以做到$O(n^2\\log^2 n)$，无法承受。

发现对于状态$f_{i,j}$，它已经确定了$i-j$位的串（因为所有$\\in j$的$2^k$之和就是$j$）；而依据字典序的性质，只有这$i-j$位所表示的字典序最小的那些状态，才会成为最终的答案。（当然，前提是状态$f_{i,j}$合法，即剩下的部分中可以安放下尚未被删去的串）

于是我们就可以考虑直接令$f\_{i,j}$表示在所有长度为$i-j$的串中，它是否是字典序最小的串之一；然后，就可以按照$i-j$递增的顺序进行DP。你自然可以倒着复原出路径，但是更好的方法是在DP第$i-j$位的时候，当我们找出了这位最小能填入什么字符后，直接输出。

下面我们考虑转移。一种情况是$f_{i,j}\\rightarrow f_{i+1,j}$，此时是第$i+1$位被保留下来，因此这个转移的前提是第$i+1$位上可以填入最小的字符；

还有一种情况就是第$i+1$位被删去，于是我们枚举$k\\notin j$，直接转移即可。

**注意到代码实现与此处描述有一些区别------描述中的递推式是刷表法，而代码中的递推式是填表法；同时，代码中的DP顺序上文已经提到，是$i-j$递增的顺序。**

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,all;
bool f[5010][5010];//f[i][j]:after erasing strings in j from the section [1,i-1], whether the (i-j) prefix can be the minimum or not
char s[5010];
int main(){
	scanf("%s",s+1),n=strlen(s+1);
	while((2<<m)<=n)m++;all=(1<<m);
	for(int i=0;i<all;i++)f[i][i]=true;//initial state:erasing all i characters in the prefix
	for(int i=1;i<=n-all+1;i++){
		char lim=127;
		for(int j=i;j<i+all;j++)if(f[j-1][j-i])lim=min(lim,s[j]);//find the minimum on the (i+1)-th character
		putchar(lim);
		for(int j=i;j<i+all;j++)f[j][j-i]=(f[j-1][j-i]&&(s[j]==lim));//leave j+1 empty
		for(int j=i;j<i+all;j++)for(int k=0;k<m;k++)if((j-i)&(1<<k))f[j][j-i]|=f[j-(1<<k)][j-i-(1<<k)];//put something on j+1
	}
	return 0;
} 
```

# LXXXVIII.[CF543D Road Improvement](https://www.luogu.com.cn/problem/CF543D)

常规换根DP题。

我们可以设$f_i$表示以$i$为根的子树中的方案数。则有转移式

$$f_i=\\prod\\limits_{j\\in son_i}(f_j+1)$$

其中$+1$的意思是将边$(i,j)$留作坏边。

显然换根DP就很好实现了。

但一个问题就是换根的时候可能会出现除数为$0$的情形；故我们不能直接简单地除以逆元。所以我们须要预处理出来前缀积与后缀积，这样就能在转移过程中避免逆元辣。

时间复杂度$O(n)$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int n,f[200100];
vector<int>v[200100],pre[200100],suf[200100];
void dfs1(int x){
	f[x]=1;
	for(auto y:v[x])dfs1(y),f[x]=1ll*f[x]*(f[y]+1)%mod;
	if(v[x].empty())return;
	pre[x].resize(v[x].size()),suf[x].resize(v[x].size());
	pre[x][0]=1;for(int i=1;i<v[x].size();i++)pre[x][i]=1ll*pre[x][i-1]*(f[v[x][i-1]]+1)%mod;
	suf[x].back()=1;for(int i=(int)v[x].size()-2;i>=0;i--)suf[x][i]=1ll*suf[x][i+1]*(f[v[x][i+1]]+1)%mod; 
}
void dfs2(int x,int qwq=1){
	for(int i=0;i<v[x].size();i++){
		int y=v[x][i];
		int tmp=1ll*pre[x][i]*suf[x][i]%mod*qwq%mod;
		f[y]=1ll*f[y]*(tmp+1)%mod;
		dfs2(y,tmp+1);
	}
}
int main(){
	scanf("%d",&n);
	for(int i=2,x;i<=n;i++)scanf("%d",&x),v[x].push_back(i);
	dfs1(1),dfs2(1);
	for(int i=1;i<=n;i++)printf("%d ",f[i]);
	return 0;
} 
```

# LXXXIX.[CF288E Polo the Penguin and Lucky Numbers](https://www.luogu.com.cn/problem/CF288E)

[题解](https://www.luogu.com.cn/blog/Troverld/solution-cf288e)

# LC.[CF GYM100739J.Longest cheap palindrome](https://codeforces.ml/gym/100739/problem/J)

我们设$f[i,j,k,l,r]$表示：

当前左端取到了位置$i$，右端取到了位置$j$；

当前选择的子序列长度为$k$；

区间$[i,l],[r,j]$中所有字符都被选择时，最小要付出的代价。

转移很简单，枚举左右两边下一个字符选到哪里即可。

这里有一份$O(n^8)$的代码，按理说是过不去的，但是因为每一重循环内部都剪掉了很多枝，所以最终的结果是过掉了。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
int n,m,lim,res;
ll cost[34][34],f[2][34][34][34][34];//f[k,i,j,l,r]:leftmost at i, rightmost at j, length of 2k, [i,l] and [r,j] have been chosen
char s[50];
int main(){
	scanf("%d%d%d",&n,&m,&lim),memset(f,0x3f,sizeof(f));
	scanf("%s",s+1);
	for(int i=1,a,b,c;i<=m;i++)scanf("%d%d%d",&a,&b,&c),cost[a][b]+=c;
	for(int i=1;i<=n;i++)for(int j=i+2;j<=n;j++)if(s[i]==s[j])f[1][i][j][i][j]=cost[i][i]+cost[j][j];
	for(int k=1;(k<<1)<=n;k++){
		for(int i=1,j=i+(k<<1)-1;j<=n;i++,j++){
			bool ok=true;
			for(int l=0;l<k;l++)ok&=(s[i+l]==s[j-l]);
			if(!ok)continue;
			f[k&1][i][j][i+k-1][i+k]=0;
			for(int u=i;u<=j;u++)for(int v=u;v<=j;v++)f[k&1][i][j][i+k-1][i+k]+=cost[u][v];
		}
		memset(f[!(k&1)],0x3f,sizeof(f[!(k&1)]));
		for(int i=1;i<=n;i++)for(int j=i+1;j<=n;j++)for(int l=i;l<=j;l++)for(int r=j;r>l;r--){
			if(f[k&1][i][j][l][r]>lim)continue;
			res=max(res,k<<1);
			for(int u=i-1;u;u--)for(int v=j+1;v<=n;v++){
				if(s[u]!=s[v])continue;
				if(l+1==r&&u==i-1&&v==j+1)continue;
				ll now=f[k&1][i][j][l][r];
				if(u==i-1)for(int w=u;w<=(l+1==r?j:l);w++)now+=cost[u][w];
				else now+=cost[u][u];
				if(v==j+1)for(int w=v;w>=(l+1==r?i:r);w--)now+=cost[w][v];
				else now+=cost[v][v];
				f[!(k&1)][u][v][u==i-1?l:u][v==j+1?r:v]=min(f[!(k&1)][u][v][u==i-1?l:u][v==j+1?r:v],now);
			}
		}	
	}
	printf("%d\n",res);
	return 0;
}
```

# LCI.[CF979E Kuro and Topological Parity](https://www.luogu.com.cn/problem/CF979E)

我们考虑在一张染色完成的图里，我们连上了一条边，会有何影响？

1.  在同色节点间连边------明显不会有任何影响
2.  在异色节点间连边，但是出发点是个偶点（即有偶数条路径以其为终点的节点）------终点的路径数增加了，但增加的是偶数，故也无影响。
3.  在异色节点间连边，但是出发点是个奇点------终点的路径数的奇偶态变化，有影响。

故我们只需要考虑状况三即可。

于是我们就可以构造出如下的DP：

设$f[i,j,k,l]$表示当前DP到了位置$i$，总路径数是$j$（$0\/1$），且无\/有奇黑点，无\/有奇白点。

下面以位置$i+1$填入白色为例：

1.  存在至少一个奇黑点（即$k=1$），则对于任意一组其它$i-1$个节点的连边方式，总有一种方式使得总数为奇，一种方式使得总数为偶（受此奇黑点的控制）。于是就有 $f[i,j,k,l]\\times 2^{i-1}\\rightarrow f[i+1,j,k,l]$与$f[i,j,k,l]\\times 2^{i-1}\\rightarrow f[i+1,\lnot j,k,\operatorname{true}]$。
2.  不存在奇黑点（即$k=0$），则无论怎么连，$i+1$的奇偶性都不会变化，始终为奇态（被看作是以它自己为起点的路径的终点）。故有$f[i,j,k,l]\\times 2^i\\rightarrow f[i+1,\lnot j,k,\operatorname{true}]$。

填入黑色则同理。

代码

```cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int n,p,a[100],f[100][2][2][2],bin[100],res;
//f[i][j][k][l]:the number of situations where there're odd/even roads which ends in i, there has(not) an odd black, has(not) an odd white
int main(){
	scanf("%d%d",&n,&p),bin[0]=1;
	for(int i=1;i<=n;i++)scanf("%d",&a[i]),bin[i]=(bin[i-1]<<1)%mod;
	f[0][0][0][0]=1;
	for(int i=0;i<n;i++)for(int j=0;j<2;j++)for(int k=0;k<2;k++)for(int l=0;l<2;l++){
		if(!f[i][j][k][l])continue;
		int tmp=f[i][j][k][l];
		if(a[i+1]!=0){//can be white
			if(k)(f[i+1][j][k][l]+=1ll*tmp*bin[i-1]%mod)%=mod,(f[i+1][j^1][k][true]+=1ll*tmp*bin[i-1]%mod)%=mod;
			else (f[i+1][j^1][k][true]+=1ll*tmp*bin[i]%mod)%=mod;
		}
		if(a[i+1]!=1){//can be black
			if(l)(f[i+1][j][k][l]+=1ll*tmp*bin[i-1]%mod)%=mod,(f[i+1][j^1][true][l]+=1ll*tmp*bin[i-1]%mod)%=mod;
			else (f[i+1][j^1][true][l]+=1ll*tmp*bin[i]%mod)%=mod;
		}
	}
	for(int k=0;k<2;k++)for(int l=0;l<2;l++)(res+=f[n][p][k][l])%=mod;
	printf("%d\n",res);
	return 0;
}
```

# LCII.[GYM102082E Eulerian Flight Tour](https://vjudge.net/problem/Gym-102082E)

（原题是PDF，没有题面的直接页面，就放一个vjudge的链接罢）

首先，当$n$是奇数时，完全图一定是欧拉图，故直接全连即可。

当$n$是奇数时，原图是欧拉图等价于补图上每个节点的度数都为奇。每个节点度数都为奇的充分必要条件是存在一座度数全为奇的生成森林。

这里有一种复杂度不太正确的解法：

考虑首先做一遍一般图匹配。接着，在原图中长度为$2$的路径连接着的所有点间做一般图匹配；然后是长度为$3$的路径……

这个算法的正确性显然------假如一条路径上的所有边都被选上了，只有两端的点的奇偶性改变了；而每个节点只会出现在一条路径的一端。为了避免两条路径有交，所以我们要按照长度处理，这样两条有交的路径就会被拆成两条无交的路径。

单次一般图匹配的复杂度是$O\\Big(n(n\\log n+m)\\Big)$（带花树算法）（别问，问就是不会，从网上弄的板子）；因为所有长度的路径数量之和是$O(n^2)$的，所以总复杂度是$\\sum n(n\\log n+m)=n^3\\log n+n^3=n^3\\log n$。

虽然理论复杂度能过，但实际上常数很大，最终T掉了。

代码（带花树部分来自网络，TLE）：

```cpp
#include<bits/stdc++.h>
using namespace std;
void read(int &x){
	x=0;
	char c=getchar();
	while(c>'9'||c<'0')c=getchar();
	while(c>='0'&&c<='9')x=(x<<3)+(x<<1)+(c^48),c=getchar();
}
const int N = 110;
int T,n,m,e,cnt,tot,ans,hd[N],p[N],match[N],pre[N],vst[N],dfn[N];
queue<int>q;
struct edge{int t,nxt;}es[N*N];
inline void Add(register int u,register int v){es[++tot]=(edge){v,hd[u]};hd[u]=tot;}
inline void add(register int u,register int v){Add(u,v),Add(v,u);}
int find(register int x){return x==p[x]?x:p[x]=find(p[x]);}
inline int lca(register int u,register int v){
	for(++cnt,u=find(u),v=find(v);dfn[u]!=cnt;){
		dfn[u]=cnt;
		u=find(pre[match[u]]);
		if(v)swap(u,v);
	}
	return u;
}
inline void blossom(register int x,register int y,register int w){
	while(find(x)!=w){
		pre[x]=y,y=match[x];
		if(vst[y]==2)vst[y]=1,q.push(y);
		if(find(x)==x)p[x]=w;
		if(find(y)==y)p[y]=w;
		x=pre[y];
	} 
} 
inline int aug(register int s){
	if((ans+1)*2>n)return 0;
	for(register int i=1;i<=n;++i)p[i]=i,vst[i]=pre[i]=0;
	while(!q.empty())q.pop();
	for(q.push(s),vst[s]=1;!q.empty();q.pop()) 
		for(register int u(q.front()),i(hd[u]),v,w;i;i=es[i].nxt){
			if(find(u)==find(v=es[i].t)||vst[v]==2)continue;
			if(!vst[v]){
				vst[v]=2;pre[v]=u;
				if(!match[v]){
					for(register int x=v,lst;x;x=lst)lst=match[pre[x]],match[x]=pre[x],match[pre[x]]=x;
					return 1;
				}
				vst[match[v]]=1,q.push(match[v]);
			}else blossom(u,v,w=lca(u,v)),blossom(v,u,w);
		}
	return 0;
}
bool g[N][N];
bool has[N];
bool no[N][N];
int dis[N][N],TOT;
int main(){
	read(n),read(m);
	for (int i=1,x,y;i<=m;++i)read(x),read(y),g[x][y]=true;
	TOT=n*(n-1)/2-m;
	if(n&1){
		printf("%d\n",TOT);
		for(int i=1;i<=n;i++)for(int j=i+1;j<=n;j++)if(!g[i][j])printf("%d %d\n",i,j);
	}else{
		for(int i=1;i<=n;i++)for(int j=1;j<=n;j++){
			if(!g[i][j])dis[i][j]=1;
			else dis[i][j]=0x3f3f3f3f;
			if(i==j)dis[i][j]=0;
		}
		for(int k=1;k<=n;k++)for(int i=1;i<=n;i++)for(int j=1;j<=n;j++)dis[i][j]=min(dis[i][j],dis[i][k]+dis[k][j]);
		for(int d=1;d<=n;d++){
			memset(hd,0,sizeof(hd)),tot=0;
			for(int i=1;i<=n;i++)for(int j=i+1;j<=n;j++)if(!has[i]&&!has[j]&&dis[i][j]==d)add(i,j);
			for (int i=1;i<=n;++i) if (!match[i]) ans+=aug(i);
			for (int i=1;i<=n;++i){
				if(!match[i]||has[i])continue;
				has[i]=true;
				if(match[i]>i)continue;
				int j=i;
				while(j!=match[i])for(int k=1;k<=n;k++)if(!g[j][k]&&dis[match[i]][k]+1==dis[match[i]][j]){g[j][k]=g[k][j]=no[j][k]=no[k][j]=true,j=k,TOT--;break;}
			}
			if(ans*2==n){
				for(int i=1;i<=n;i++){
					bool ok=false;
					for(int j=1;j<=n;j++)if(i!=j)ok|=!no[i][j];
					if(!ok){puts("-1");return 0;}
				}
				printf("%d\n",TOT);
				for(int i=1;i<=n;i++)for(int j=i+1;j<=n;j++)if(!g[i][j])printf("%d %d\n",i,j);
				return 0;
			}
		}
		puts("-1");
	}
	return 0;
}
```

下面是正解：

每个节点度数都为奇的充分必要条件还有一个，就是不存在点数为奇的连通块。假如该条件成立，我们考虑构造一组解。我们考虑对于每个连通块都求一棵生成树，然后断掉某些边使得每个节点度数都为奇。这个可以从叶子向上DP，如果一个节点的儿子中有偶数条边保留了，则其与父亲的边也需保留，否则则需断开。

需要注意的是，原图必须是连通图，等价于补图中不能有度数为$n-1$的节点。假如我们发现存在这样的节点，则如果当前生成树是唯一生成树，无解；否则，考虑找到另一棵生成树。这可以通过找到一条原树中没有的边，然后强制连上它，然后重新求生成树得到。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
void read(int &x){
	x=0;
	char c=getchar();
	while(c>'9'||c<'0')c=getchar();
	while(c>='0'&&c<='9')x=(x<<3)+(x<<1)+(c^48),c=getchar();
}
int n,m;
const int N=110;
vector<int>v[N];
int dsu[N],sz[N],deg[N];
int find(int x){return dsu[x]==x?x:dsu[x]=find(dsu[x]);}
bool merge(int x,int y){
	int p=find(x),q=find(y);
	if(p==q)return true;
	v[y].push_back(x),v[x].push_back(y),deg[y]++,deg[x]++,dsu[p]=q,sz[q]+=sz[p];
	return false;
} 
bool g[N][N];
bool no[N][N];
int TOT;
bool dfs(int x,int fa){
	bool ok=true;
	for(auto y:v[x]){
		if(y==fa)continue;
		if(dfs(y,x))no[y][x]=no[x][y]=true,ok^=1,TOT--;
	}
	return ok;
}
int main(){
	read(n),read(m);
	for (int i=1,x,y;i<=m;++i)read(x),read(y),g[x][y]=true;
	TOT=n*(n-1)/2-m;
	if(n&1){
		printf("%d\n",TOT);
		for(int i=1;i<=n;i++)for(int j=i+1;j<=n;j++)if(!g[i][j])printf("%d %d\n",i,j);
	}else{
		for(int i=1;i<=n;i++)dsu[i]=i,sz[i]=1;
		bool ok=false;
		for(int i=n;i;i--)for(int j=n;j>i;j--)if(!g[i][j])ok|=merge(i,j);
		for(int i=1;i<=n;i++)if(dsu[i]==i&&(sz[i]&1)){puts("-1");return 0;}
		int invalid=0;
		for(int i=1;i<=n;i++)if(deg[i]==n-1){
			if(!ok){puts("-1");return 0;}
			invalid=i;
		}
		if(invalid){
			for(int i=1;i<=n;i++)dsu[i]=i,sz[i]=1,deg[i]=0,v[i].clear();
			int x=0,y=0;
			for(int i=n;i;i--)for(int j=n;j>i;j--){
				if(g[i][j])continue;
				if(merge(i,j)&&!x&&!y)x=i,y=j;
			}
			for(int i=1;i<=n;i++)dsu[i]=i,sz[i]=1,deg[i]=0,v[i].clear();
			merge(x,y);
			for(int i=n;i;i--)for(int j=n;j>i;j--)if(!g[i][j])merge(i,j);
		}
		for(int i=1;i<=n;i++)if(dsu[i]==i)dfs(i,0);
		printf("%d\n",TOT);
		for(int i=1;i<=n;i++)for(int j=i+1;j<=n;j++)if(!g[i][j]&&!no[i][j])printf("%d %d\n",i,j);
	}
	return 0;
}
```

# LCIII.[\[CERC2014\]Outer space invaders](https://www.luogu.com.cn/problem/P4766)

一种错误的思路是观察到一定可以构造出一种最优状态使得每次射击都发生在外星人消失的时刻，然后就将所有外星人按照消失时刻排序并设$f[i,j]$表示在第$i$个外星人消失的时刻如果你开了一炮高为（离散化后）$j$的最小费用------但很快就会发现这种DP需要记录下在这之前每一个高度上次被打的时间，于是就DP不了了。

正确的DP是将所有的端点离散化后，观察到如果我们要把被完整的包含在区间$[l,r]$内的所有外星人全部干掉，则其中最远的那个必定要对它开一炮；于是我们便找出这一个外星人，然后枚举这一炮开在哪（设为$p$），就可以将其分作$[l,p-1]$与$[p+1,r]$两截（所有经过$p$的外星人都被干掉了）。

于是就可以区间DP了。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
#define all(v) v.begin(),v.end()
int T,n,m,f[610][610],l[310],r[310],d[310];
vector<int>v;
int main(){
	scanf("%d",&T);
	while(T--){
		scanf("%d",&n),v.clear(),memset(f,0,sizeof(f));
		for(int i=1;i<=n;i++)scanf("%d%d%d",&l[i],&r[i],&d[i]),v.push_back(l[i]),v.push_back(r[i]);
		sort(all(v)),v.resize(m=unique(all(v))-v.begin());
		for(int i=1;i<=n;i++)l[i]=lower_bound(all(v),l[i])-v.begin()+1,r[i]=lower_bound(all(v),r[i])-v.begin()+1;
		for(int i=1;i<=m;i++)for(int j=i;j;j--){
			int id=-1;
			for(int k=1;k<=n;k++)if(j<=l[k]&&r[k]<=i&&(id==-1||d[id]<d[k]))id=k;
			if(id==-1)continue;
			f[j][i]=0x3f3f3f3f;
			for(int k=l[id];k<=r[id];k++)f[j][i]=min(f[j][i],f[j][k-1]+d[id]+f[k+1][i]);
		}
		printf("%d\n",f[1][m]);		
	}
	return 0;
}
```

# LCIV.[\[NOI2005\]瑰丽华尔兹](https://www.luogu.com.cn/problem/P2254)

思路1.$O(N^2T)$暴力DP------设$f[t,i,j]$表示$t$时刻在位置$(i,j)$时的最长路径。显然会T。

思路2.$O(N^2T)$暴力DP------观察到一段长为$len$的时间内向某个方向每时刻移动一格，等价于总共移动$len$格。又因为随时可以停止，所以可以移动$0\\sim len$格中任意长度。暴力枚举转移几格即是上述复杂度。

思路3.$O(N^2K)$暴力DP------因为$len$在一次转移中不变，所以实际上就是经典老题滑动窗口，直接暴力硬套单调队列即可。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int f[2][210][210],n,m,p,sx,sy,res;
char s[210][210];
int main(){
	scanf("%d%d%d%d%d",&n,&m,&sx,&sy,&p),memset(f,0xc0,sizeof(f)),f[0][sx][sy]=0;
	for(int i=1;i<=n;i++)scanf("%s",s[i]+1);
	for(int i=1;i<=n;i++)for(int j=1;j<=m;j++)s[i][j]=(s[i][j]=='.');
	int now=1,las=0;
	for(int len,dir;p--;now^=1,las^=1){
		scanf("%d%d",&len,&dir),len=dir-len+1,scanf("%d",&dir);
//		printf("%d %d\n",len,dir);
		if(dir==1){
			for(int j=1;j<=m;j++){
				deque<int>q;
				for(int i=n;i;i--){
					if(!s[i][j]){q.clear();continue;}
					while(!q.empty()&&(q.front()-i)>len)q.pop_front();
					while(!q.empty()&&(f[las][q.back()][j]+(q.back()-i))<=f[las][i][j])q.pop_back();
					q.push_back(i);
					f[now][i][j]=f[las][q.front()][j]+(q.front()-i);
				}
			}
		}
		if(dir==2){
			for(int j=1;j<=m;j++){
				deque<int>q;
				for(int i=1;i<=n;i++){
					if(!s[i][j]){q.clear();continue;}
					while(!q.empty()&&(i-q.front())>len)q.pop_front();
					while(!q.empty()&&(f[las][q.back()][j]+(i-q.back()))<=f[las][i][j])q.pop_back();
					q.push_back(i);
					f[now][i][j]=f[las][q.front()][j]+(i-q.front());
				}
			}
		}
		if(dir==3){
			for(int i=1;i<=n;i++){
				deque<int>q;
				for(int j=m;j;j--){
					if(!s[i][j]){q.clear();continue;}
					while(!q.empty()&&(q.front()-j)>len)q.pop_front();
					while(!q.empty()&&(f[las][i][q.back()]+(q.back()-j))<=f[las][i][j])q.pop_back();
					q.push_back(j);
					f[now][i][j]=f[las][i][q.front()]+(q.front()-j);
				}
			}
		}
		if(dir==4){
			for(int i=1;i<=n;i++){
				deque<int>q;
				for(int j=1;j<=m;j++){
					if(!s[i][j]){q.clear();continue;}
					while(!q.empty()&&(j-q.front())>len)q.pop_front();
					while(!q.empty()&&(f[las][i][q.back()]+(j-q.back()))<=f[las][i][j])q.pop_back();
					q.push_back(j);
					f[now][i][j]=f[las][i][q.front()]+(j-q.front());
				}
			}
		}
//		for(int i=1;i<=n;i++){for(int j=1;j<=m;j++)printf("%11d ",f[now][i][j]);puts("");}
	}
	for(int i=1;i<=n;i++)for(int j=1;j<=m;j++)res=max(res,f[las][i][j]);
	printf("%d\n",res);
	return 0;
}
```

# LCV.[\[SDOI2008\]山贼集团](https://www.luogu.com.cn/problem/P2465)

[题解](https://www.luogu.com.cn/blog/Troverld/solution-p2465)

# LCVI.[\[HNOI2007\]梦幻岛宝珠](https://www.luogu.com.cn/problem/P3188)

好题。

明显它是01背包的模型，但值域过大。咋办呢？

我们考虑令 $f\_{i,j}$ 表示只考虑 $a\\times 2^i$ 类型的物品，关于 $a$ 做的一个背包。显然，暴力求出这个东西的时空复杂度都是可接受的。

我们再考虑 $g_{i,j}$ 表示有 $j\\times2^i+w\\operatorname{and}(2^i-1)$ 这么多的背包容量时的答案，即只考虑 $w$ 的下 $i$ 位，且第 $i$ 位上选了 $j$ 单位的物品。我们考虑由 $g_{i,j}$ 更新 $g\_{i+1}$。

显然，如果 $w$ 的第 $i$ 位有一个 $1$，在第 $i+1$ 位上，$g\_{i,j}$ 就与一个大小为 $\\left\\lfloor\\dfrac{j}{2}\\right\\rfloor$ 的物品等价；否则，即 $w$ 的第 $i$ 位没有 $1$，它与 $\\left\\lceil\\dfrac{j}{2}\\right\\rceil$ 等价。

于是我们就用 $g_i$ 和 $f_{i+1}$ 即可拼凑出 $g\_{i+1}$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,m;
vector<pair<int,int> >v[40];
int f[40][2000],lim[40],g[40][2000];
void chmx(int &x,int y){if(x<y)x=y;}
int main(){
	while(true){
		scanf("%d%d",&n,&m);
		if(n==-1&&m==-1)break;
		memset(f,0,sizeof(f)),memset(g,0,sizeof(g)),memset(lim,0,sizeof(lim));
		for(int i=0;i<=30;i++)v[i].clear();
		for(int i=1,a,b,c;i<=n;i++){
			scanf("%d%d",&a,&b),c=0;
			while(!(a&1))a>>=1,c++;
			v[c].push_back(make_pair(a,b));
		}
		for(int i=0;i<=30;i++){
			for(auto k:v[i]){
				for(int j=lim[i];j>=0;j--)chmx(f[i][j+k.first],f[i][j]+k.second);
				lim[i]+=k.first;
//				printf("(%d,%d)\n",k.first,k.second);
			}
//			for(int j=0;j<=lim[i];j++)printf("%d ",f[i][j]);puts("");
		}
		for(int i=0;i<=lim[0];i++)g[0][i]=f[0][i];
		for(int i=0;i<=30;i++){
			for(int j=0;j<=lim[i];j++)for(int k=lim[i+1];k>=0;k--)chmx(g[i+1][k+((j+!((m>>i)&1))>>1)],f[i+1][k]+g[i][j]);
			lim[i+1]+=(lim[i]+!((m>>i)&1))>>1;
		}
		printf("%d\n",g[31][0]);
	}
	return 0;
}
```

# LCVII.[\[POI2013\]LUK-Triumphal arch](https://www.luogu.com.cn/problem/P3554)

明显题目具有可二分性。

考虑如何check。

我们发现，一个足够聪明的B，必定不会走回头路。故最终结果一定是一条从根到某个叶子的路径。

我们发现，如果一个父亲已经染掉了它所有儿子，它剩余的操作次数便可以去染儿子，以防到了某个儿子的时候完不成任务。但是儿子的操作却不能反过来贡献父亲。

所以我们可以设计出这样的DP状态：$f_x$表示$x$节点最少需要从父亲那借多少次操作才可以完成任务。设二分的值是$mid$，于是就有

$$f_x=\\max\\Bigg(0,\\Big(\\sum\\limits_{y\\in son_x}(f_y+1)\\Big)-mid\\Bigg)$$

因为一个父亲必须保证它所有的儿子都能在B走过去的时候防的住，所以它必须有足够的操作次数染掉所有的儿子。如果不行，就必须再找爷爷借了。一直借到根，自然根是没地方借去的，所以判断条件就是$f_1$是否为$0$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,f[1001000],mid;
vector<int>v[1001000];
void dfs(int x,int fa){
	f[x]=0;
	for(auto y:v[x])if(y!=fa)dfs(y,x),f[x]+=f[y]+1;
	f[x]-=mid,f[x]=max(f[x],0);
}
bool che(){
	dfs(1,0);
	return f[1]==0; 
}
int main(){
	scanf("%d",&n);
	for(int i=1,x,y;i<n;i++)scanf("%d%d",&x,&y),v[x].push_back(y),v[y].push_back(x);
	int l=0,r=n;
	while(l<r){
		mid=(l+r)>>1;
		if(che())r=mid;
		else l=mid+1;
	}
	printf("%d\n",r);
	return 0;
}
```

# LCVIII.[\[POI2006\]PRO-Professor Szu](https://www.luogu.com.cn/problem/P3436)

我要举报……本题数据与题面不符（事实上我已经举报了……），会有到不了主楼的情形，要特别考虑。

思路很简单，我们跑SCC缩点。假如一个SCC内部有自环，显然可以一直绕自环，故答案是无限；同时，所有可以走到该SCC的其它点答案都是无限。

于是我们反向所有边，从终点开始拓扑排序，传递无限的情形，并进行DP（设$f_i$表示从节点$i$到终点的路径数量即可）。注意要先把所有从到不了的SCC连出的边删去，同时不应该考虑终点自身。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
const int lim=36500;
int n,m,dfn[1001000],low[1001000],tot,f[1001000],col[1001000],c,in[1001000],res,cnt;
bool inf[1001000];
vector<int>v[1001000],u[1001000];
stack<int>s;
void Tarjan(int x){
	dfn[x]=low[x]=++tot,s.push(x);
	for(auto y:v[x]){
		if(!dfn[y])Tarjan(y),low[x]=min(low[x],low[y]);
		else if(!col[y])low[x]=min(low[x],dfn[y]); 
	}
	if(low[x]<dfn[x])return;
	c++;
	int y;
	do y=s.top(),s.pop(),col[y]=c;while(y!=x);
}
queue<int>q;
int main(){
	scanf("%d%d",&n,&m),n++;
	for(int i=1,x,y;i<=m;i++)scanf("%d%d",&x,&y),v[y].push_back(x);
	for(int i=1;i<=n;i++)if(!dfn[i])Tarjan(i); 
	for(int i=1;i<=n;i++)for(auto j:v[i])if(col[i]!=col[j])u[col[i]].push_back(col[j]),in[col[j]]++;else inf[col[i]]=true;
	for(int i=1;i<=c;i++)if(!in[i])q.push(i);
	while(!q.empty()){
		int x=q.front();q.pop();
		if(x==col[n])continue;
		inf[x]=f[x]=0;
		for(auto y:u[x])if(!--in[y])q.push(y);
	}
	f[col[n]]=!inf[col[n]],q.push(col[n]);
	while(!q.empty()){
		int x=q.front();q.pop();
		for(auto y:u[x]){
			if(!inf[y])f[y]+=f[x],inf[y]|=inf[x];
			if(f[y]>lim)f[y]=0,inf[y]=true;
			if(!--in[y])q.push(y);
		}
	}
	for(int i=1;i<=c;i++){
		if(inf[i])res=lim+1;
		else res=max(res,f[i]);
	}
	if(res>lim){
		puts("zawsze");
		for(int i=1;i<n;i++)cnt+=inf[col[i]];
		printf("%d\n",cnt);
		for(int i=1;i<n;i++)if(inf[col[i]])printf("%d ",i);
	}else{
		printf("%d\n",res);
		for(int i=1;i<n;i++)cnt+=(f[col[i]]==res);
		printf("%d\n",cnt);
		for(int i=1;i<n;i++)if(f[col[i]]==res)printf("%d ",i);
	}
	return 0;
}
```

# IC.[\[POI2007\]ATR-Tourist Attractions](https://www.luogu.com.cn/problem/P3451)

这题我一年半之前初学状压DP时就写了份没卡空间的做法，今天终于A了……

首先，思路非常简单------我们可以使用Dijkstra预处理出来$2\\sim k+1$中两两点之间的距离以及它们到$1$和$n$的距离。接着，设$f[i,j]$表示当前访问完了$i$集合中所有东西，且在位置$j$的最小距离。DP很简单，这里就放一个转移式罢：

$$f[i,j]+dis[j,k]\\rightarrow f[i\lor k,k]$$

其中必有$j\\in i,k\\notin i,i\\subseteq mus_k$，其中$mus_k$是$k$之前必选的集合。

但是这题卡空间。按照上述方法，空间大小是$2^{20}\\times20\\times 4B=80MB$，会被卡掉。

我们考虑滚动数组，按照状态中为$1$的位的数量进行DP。此时最大一位的空间消耗是$\\dbinom{20}{10}=184756$，总空间即为$2\\times 184756\\times 20\\times 4B&lt;64MB$，可以通过。

编号直接使用`vector`建立双射即可。

代码 ：

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,p,r,dis[24][20100],d[25][25],d1[25],dn[25],id[(1<<20)+5],f[2][200000][21],mus[25],res=0x3f3f3f3f;
namespace Graph{
	vector<pair<int,int> >v[20100];
	priority_queue<pair<int,int> >q;
	bool vis[20100];
	void Dijkstra(int S){
		memset(dis[S],0x3f,sizeof(dis[S])),memset(vis,false,sizeof(vis)),dis[S][S]=0,q.push(make_pair(0,S));
		while(!q.empty()){
			int x=q.top().second;q.pop();
			if(vis[x])continue;vis[x]=true;
			for(auto y:v[x])if(dis[S][x]+y.second<dis[S][y.first])dis[S][y.first]=dis[S][x]+y.second,q.push(make_pair(-dis[S][y.first],y.first));
		}
	}	
}
vector<int>v[30];
void chmn(int &x,int y){if(x>y)x=y;}
int main(){
	scanf("%d%d%d",&n,&m,&p),memset(f,0x3f3f3f3f,sizeof(f));
	for(int i=1,x,y,z;i<=m;i++)scanf("%d%d%d",&x,&y,&z),Graph::v[x].push_back(make_pair(y,z)),Graph::v[y].push_back(make_pair(x,z));
	scanf("%d",&r);
	for(int i=1,x,y;i<=r;i++)scanf("%d%d",&x,&y),mus[y-2]|=(1<<(x-2));
	if(!p){
		Graph::Dijkstra(1);
		printf("%d\n",dis[1][n]);
		return 0;
	}
	for(int i=2;i<=p+1;i++)Graph::Dijkstra(i);
	for(int i=0;i<p;i++)for(int j=0;j<p;j++)d[i][j]=dis[i+2][j+2];
//	for(int i=0;i<p;i++){for(int j=0;j<p;j++)printf("%d ",d[i][j]);puts("");}
	for(int i=0;i<p;i++)d1[i]=dis[i+2][1],dn[i]=dis[i+2][n];
	for(int i=0;i<(1<<p);i++)id[i]=v[__builtin_popcount(i)].size(),v[__builtin_popcount(i)].push_back(i);
//	for(int i=0;i<=p;i++)printf("%d\n",v[i].size());
	for(int i=0;i<p;i++)if(!mus[i])f[1][id[1<<i]][i]=d1[i]; 
	for(int i=1;i<p;i++)for(int j=0;j<v[i].size();j++)for(int k=0;k<p;k++){
		if(!(v[i][j]&(1<<k)))continue;
		for(int l=0;l<p;l++)if(!(v[i][j]&(1<<l))&&((mus[l]&v[i][j])==mus[l]))chmn(f[!(i&1)][id[v[i][j]|(1<<l)]][l],f[i&1][j][k]+d[k][l]);
		f[i&1][j][k]=0x3f3f3f3f;
	}
	for(int i=0;i<p;i++)chmn(res,f[p&1][id[(1<<p)-1]][i]+dn[i]);
	printf("%d\n",res);
	return 0;
}
```

# C.[\[POI2013\]BAJ-Bytecomputer](https://www.luogu.com.cn/problem/P3558)

本博客的最后一题，献给一道~~大力猜结论~~的题。

首先先说猜想：最终序列中所有数都是$-1,0,1$，且不存在先改后面，后改前面的状态。

有了这个猜想，就可以DP了。我们设$f_{i,j}$表示要使位置$i$出现数$j$，且前$i$个位置单调不降的最小费用。则我们枚举往$a_{i+1}$上加多少个$j$（明显只能加$0\/1\/2$个），判断往$a\_{i+1}$上加上这么多$j$后是否仍满足单调不降，如果可以那就直接转移没问题了。

下面来讲证明。全是$-1,0,1$很好证，因为原本所有数都在此值域内，你要加出这个值域肯定要耗费更多代价。

不存在先改后面，后改前面的状态也很好证------首先，我们观察到执行`a[i]+=a[i-1]`，肯定有一种方案使得要么它在$a_{i-1}$符合要求之前执行，要么它在$a_{i-1}$符合要求之后执行。而两次执行，都是$+1/0/-1$，假如两次相同，那肯定可以看作一端执行两遍；有一个是$0$，不如不执行；则只剩下一次$+1$，一次$-1$的状况，但这样等价于没执行，所以也可以忽略。

则上述解法正确。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,a[1000100],f[1001000][3],res=0x3f3f3f3f;
int main(){
	scanf("%d",&n),memset(f,0x3f,sizeof(f));
	for(int i=1;i<=n;i++)scanf("%d",&a[i]);
	f[1][a[1]+1]=0;
	for(int i=1;i<n;i++)for(int j=-1;j<=1;j++)for(int k=0;k<=2;k++)if(a[i+1]+k*j>=j&&a[i+1]+k*j<=1)f[i+1][a[i+1]+k*j+1]=min(f[i+1][a[i+1]+k*j+1],f[i][j+1]+k);
	for(int i=-1;i<=1;i++)res=min(res,f[n][i+1]);
	if(res==0x3f3f3f3f)puts("BRAK");else printf("%d\n",res);
	return 0;
}
```

* * *

到这里又是50题过去了。本博客又一次卡到敲一个字卡一秒的情形了。更多DP题请参见[下一篇笔记](https://www.luogu.com.cn/blog/Troverld/dp-shua-ti-bi-ji-iii)。

如果觉得本博客帮到了您，不妨点个赞罢！
