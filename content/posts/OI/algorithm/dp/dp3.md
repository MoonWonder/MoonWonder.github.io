---
author: "ybw051114"
author_link: "hugo.ybw051114.cf"
title: "dp3"
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
math: true
lightgallery: true
linkToMarkdown: true
share:
  enable: true
comment: true
---



[笔记I](https:\/\/www.luogu.com.cn\/blog\/Troverld\/dp-shua-ti-bi-ji)（1~50题）

[笔记II](https:\/\/www.luogu.com.cn\/blog\/Troverld\/dp-shua-ti-bi-ji-ii)（51~100题）

现在开始！

# CI.[[IOI2009]salesman](https:\/\/www.luogu.com.cn\/problem\/P5902)

思想非常simple：因为一次从上游往下游的转移，可以被表示成

$f_i+(pos_i-pos_j)\times U\rightarrow f_j\ |\ pos_i<pos_j\land tim_i<tim_j$

拆开括号，即可得到两半互不相关的部分。然后直接使用线段树\/树状数组进行转移即可。

从下游往上游的转移也可以类似地处理。

现在考虑$tim$中可能有相等的情形，并不能确定访问顺序。这个再使用一遍辅助DP过一遍就行了。有一个结论是当$tim$相等时，一次转移中一定不会走回头路——回头路的部分完全可以在上次转移和下次转移处就处理掉了。然后就直接DP过就行了。

3min就能想出的idea，我整整调了3d。主要因为一开始套了两重离散化，后来发现数据范围开的下便删去了离散化；一开始写的是线段树，后来发现线段树debug起来很麻烦，便换成了BIT；一开始也没有想到没有回头路的情形，辅助DP时写的极其憋屈（后来证明就是这个憋屈的DP中有一处$U$和$D$写反了）；同时中文题面翻译还翻译错了，这个“距离”是到上游的距离而非到下游的距离。于是种种因素叠加在一起，debug得精神崩溃。

代码：

```cpp
#include<bits\/stdc++.h>
using namespace std;
const int inf=0xc0c0c0c0;
const int N=1001000;
int n,U,D,S,tim[N],pos[N],bon[N],m=500100,ord[N],f[N],g[N],upper[N],lower[N];\/\/upper:the maximal when go against the wave; lower:vice versa
void modify(int P,int val){
	for(int x=P;x;x-=x&-x)upper[x]=max(upper[x],val-P*U);
	for(int x=P;x<=m;x+=x&-x)lower[x]=max(lower[x],val+P*D);
}
int queryupper(int P){
	int ret=inf;
	for(int x=P;x<=m;x+=x&-x)ret=max(ret,upper[x]+P*U);
	return ret;
}
int querylower(int P){
	int ret=inf;
	for(int x=P;x;x-=x&-x)ret=max(ret,lower[x]-P*D);
	return ret;
}
#define I ord[i]
#define J ord[j]
#define K ord[k]
int main(){
	scanf("%d%d%d%d",&n,&U,&D,&S),memset(upper,0xc0,sizeof(upper)),memset(lower,0xc0,sizeof(lower));
	for(int i=1;i<=n;i++)scanf("%d%d%d",&tim[i],&pos[i],&bon[i]),ord[i]=i;
	sort(ord+1,ord+n+1,[](int x,int y){return tim[x]==tim[y]?pos[x]<pos[y]:tim[x]<tim[y];});
	modify(S,0);
	for(int i=1,j=1;j<=n;){
		while(tim[I]==tim[J])f[J]=g[J]=max(queryupper(pos[J]),querylower(pos[J]))+bon[J],j++;
		for(int k=i+1;k<j;k++)f[K]=max(f[K],f[ord[k-1]]-(pos[K]-pos[ord[k-1]])*D+bon[K]);
		for(int k=j-2;k>=i;k--)g[K]=max(g[K],g[ord[k+1]]-(pos[ord[k+1]]-pos[K])*U+bon[K]);
		while(i<j)modify(pos[I],max(f[I],g[I])),i++;
	}
	printf("%d\n",max(queryupper(S),querylower(S)));
	return 0;
}
```

# CII.[HDU6212 Zuma](http:\/\/acm.hdu.edu.cn\/showproblem.php?pid=6212)

一眼区间DP。

首先，我们将串压缩（即将相同颜色的相邻珠子合并）。记$col_i$为位置$i$的颜色，$sz_i$为位置$i$的珠子数。

我们设$f[i,j]$表示消去区间$[i,j]$中所有东西的最小步数。

则有：

$$f[i,j]=\min\begin{cases}3-sz_i&|i=j\\f[i,k]+f[k+1,j]&|i\leq k<j\\f[i+1,j-1]+\max(0,3-sz_i-sz_j)&|col_i=col_j\\f[i+1,k-1]+f[k+1,j-1]&|col_i=col_j=col_k,(sz_i\neq 2\lor sz_j\neq 2)\land sz_k=1\end{cases}$$

其中，第一条转移是直接补满$3$个球；第二条转移是找个地方切一刀；第三条转移是将$i$和$j$最终合并在一起进行消除；第四条转移是将$i$，$j$，以及区间中某一个$k$合并消除，但需要保证有一种消除顺序可以使得$k$可以先在不与某一边一起消掉的前提下消到那一边，然后再合并两边。

时间复杂度$O(Tn^3)$，需要保证常数。

代码：

```cpp
#include<bits\/stdc++.h>
using namespace std;
int T,n,m,sz[210],f[210][210];
bool col[210];
char s[210];
int main(){
	scanf("%d",&T);
	for(int t=1;t<=T;t++){
		scanf("%s",s+1),m=strlen(s+1),n=0;
		col[1]=s[1]-'0',sz[1]=1,n++;
		for(int i=2;i<=m;i++){
			if(s[i]-'0'==col[n])sz[n]++;
			else n++,col[n]=s[i]-'0',sz[n]=1;
		}
		for(int i=1;i<=n;i++)f[i][i]=3-sz[i];
		for(int l=2;l<=n;l++)for(int i=1,j=i+l-1;j<=n;i++,j++){
			f[i][j]=0x3f3f3f3f;
			for(int k=i;k<j;k++)f[i][j]=min(f[i][j],f[i][k]+f[k+1][j]);
			if(col[i]!=col[j])continue;
			f[i][j]=min(f[i][j],f[i+1][j-1]+max(0,3-sz[i]-sz[j]));
			if(sz[i]==2&&sz[j]==2)continue;
			for(int k=i+1;k<j;k++)if(col[k]==col[i]&&sz[k]==1)f[i][j]=min(f[i][j],f[i+1][k-1]+f[k+1][j-1]);
		}
		printf("Case #%d: %d\n",t,f[1][n]);
	}
	return 0;
} 
```

# CIII.[[APIO2014]连珠线](https:\/\/www.luogu.com.cn\/problem\/P3647)

一般的换根DP题。

明显可以看出，最终的树一定可以通过指定一个根变成一棵有根树，所有的蓝边都可以被分成两两一组，其中每组中两条边深度递增。

于是我们可以设置DP状态。$f_{x,0\/1}$表示节点$x$，它不是\/是某对蓝边的中间节点时，子树中最大的蓝边权和。

简单使用`multiset`维护$f_{x,1}$从哪个儿子转移过来最优即可。

然后换个根即可。

代码：

```cpp
#include<bits\/stdc++.h>
using namespace std;
const int inf=0xc0c0c0c0;
int n,f[200100][2],head[200100],cnt,res;
struct node{
	int to,next,val;
}edge[400100];
void ae(int u,int v,int w){
	edge[cnt].next=head[u],edge[cnt].to=v,edge[cnt].val=w,head[u]=cnt++;
	edge[cnt].next=head[v],edge[cnt].to=u,edge[cnt].val=w,head[v]=cnt++;
}
multiset<int>s[200100];
void dfs1(int x,int fa){
	for(int i=head[x],y;i!=-1;i=edge[i].next){
		if((y=edge[i].to)==fa)continue;
		dfs1(y,x);
		int tmp=max(f[y][0],f[y][1]+edge[i].val);
		f[x][0]+=tmp;
		f[x][1]+=tmp,s[x].insert(f[y][0]+edge[i].val-tmp);
	}
	if(s[x].empty())f[x][1]=inf;
	else f[x][1]+=*s[x].rbegin();
\/\/	printf("%d:%d %d\n",x,f[x][0],f[x][1]);
}
void dfs2(int x,int fa){
	for(int i=head[x],y;i!=-1;i=edge[i].next){
		if((y=edge[i].to)==fa)continue;
		int tmp=max(f[y][0],f[y][1]+edge[i].val);
		int fx0=f[x][0],fx1=f[x][1];
		fx0-=tmp;
		fx1-=tmp;
		fx1-=*s[x].rbegin();
		int pmt=f[y][0]+edge[i].val-tmp;
		s[x].erase(s[x].find(pmt));
		fx1=(s[x].empty()?inf:fx1+*s[x].rbegin());
		s[x].insert(pmt);
		
		int qwq=max(fx0,fx1+edge[i].val);
		f[y][0]+=qwq;
		f[y][1]=(s[y].empty()?0:f[y][1]-*s[y].rbegin());
		f[y][1]+=qwq;
		s[y].insert(fx0+edge[i].val-qwq);
		f[y][1]+=*s[y].rbegin();
		dfs2(y,x);
	}
}
int main(){
	scanf("%d",&n),memset(head,-1,sizeof(head));
	for(int i=1,x,y,z;i<n;i++)scanf("%d%d%d",&x,&y,&z),ae(x,y,z);
	dfs1(1,0),dfs2(1,0);
	for(int i=1;i<=n;i++)res=max(res,f[i][0]);
	printf("%d\n",res);
	return 0;
}
```

# CIV.[[TopCoder 12519]ScotlandYard](https:\/\/vjudge.net\/problem\/TopCoder-12519)

我们考虑一个最原始的DP状态：$f[\mathbb{S}]$表示根据当前给出的信息，猜的人可以推测出当前藏的人一定在且仅在集合$\mathbb{S}$之中时，藏的人最多可以走多少步。

然后考虑枚举藏的人下一步给出走了什么颜色的边，然后取$\mathbb{S}$中所有点当前颜色的出边集合的并集$\mathbb{T}$，则有$f(\mathbb{S})\leftarrow f(\mathbb{T})+1$。边界状态为 $f(\varnothing)=0$，$f(\mathbb{S})=1\text{ when }|\mathbb{S}|=1$。

观察可以发现，猜的人最终可以确定藏的人在哪里的前一刻，$\mathbb{S}$的大小：

1. 如果$\geq3$，显然只判断其中两个亦可；

2. 如果$=2$，显然可以根据此两个一路反推回去，即任意时刻$|\mathbb{S}|$都可以被缩减到$2$。
3. 如果$\leq1$，此状态显然不合法，不可能出现。

故我们发现任意时刻状态中仅需存储$\mathbb{S}$中两个数即可。这样状态数就缩小到$O(n^2)$级别了。则此时就可以直接按照上文所述DP了。采取记忆化搜索的方式DP，如果任意时刻发现搜索到成环了，则答案必为$\infty$。

代码（TC的格式）：

```cpp
#include<bits\/stdc++.h>
using namespace std;
class ScotlandYard{
private:
	const int inf=0x3f3f3f3f;
	int n,f[60][60];
	vector<int>g[60][3];
	bool in[60][60];
	int dfs(int x,int y){
		if(in[x][y])return inf;
		if(f[x][y]!=-1)return f[x][y];
		in[x][y]=true;
		f[x][y]=0;
		for(int i=0;i<3;i++){
			vector<int>v;
			for(auto j:g[x][i])v.push_back(j);
			for(auto j:g[y][i])v.push_back(j);
			sort(v.begin(),v.end()),v.resize(unique(v.begin(),v.end())-v.begin());
			if(v.size()==0){f[x][y]=max(f[x][y],0);continue;}
			if(v.size()==1){f[x][y]=max(f[x][y],1);continue;}
			for(int i=0;i<v.size();i++)for(int j=i+1;j<v.size();j++)f[x][y]=max(f[x][y],min(inf,dfs(v[i],v[j])+1));
		}
		in[x][y]=false;
		return f[x][y];
	}
public:
	int maxMoves(vector<string>taxi,vector<string>bus,vector<string>metro){
		n=taxi.size();
		for(int i=0;i<n;i++)for(int j=0;j<3;j++)g[i][j].clear();
		for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(taxi[i][j]=='Y')g[i][0].push_back(j);
		for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(bus[i][j]=='Y')g[i][1].push_back(j);
		for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(metro[i][j]=='Y')g[i][2].push_back(j);
\/\/		for(int i=0;i<3;i++){for(int j=0;j<n;j++){for(auto k:g[j][i])printf("%d ",k);puts("");}puts("");}
		memset(f,-1,sizeof(f));
		int res=0;
		for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)res=max(res,dfs(i,j));
		return res>=inf?-1:res;
	}
}my;
```

# CV.[[ARC067D] Yakiniku Restaurants](https:\/\/www.luogu.com.cn\/problem\/AT2289)

明显在最优方案中，行走方式一定是从一条线段的一端走到另一端，不回头。

于是设 $f[i,j]$ 表示从 $i$ 走到 $j$ 的最优代价。明显，该代价对于不同的券相互独立。故我们依次考虑每一张券。

我们发现，假设有一张位置 $k$ 的券，则所有 $k\in[l,r]$ 的 $[l,r]$ 都是可以享受到它的。于是，我们建出笛卡尔树来，就可以把它用差分轻松解决了（假设笛卡尔树上有一个节点 $x$，它是区间 $[l,r]$ 中的最大值，则所有区间 $[l,r]$ 中穿过它的区间都会增加 $a_x$，但是它的两个子区间 $[l,x-1]$ 和 $[x+1,r]$ 却享受不到，故在该处再减少 $a_x$，即可实现差分地更新。

则时间复杂度 $O(nm+n^2)$。

代码：

```cpp
#include<bits\/stdc++.h>
using namespace std;
typedef long long ll;
int n,m,a[210][5010],stk[5010],tp,lson[5010],rson[5010];
ll s[5010],f[5010][5010],res;
void solve(int id,int x,int l,int r,int las){
	f[l][r]+=a[id][x]-las;
	if(l==r)return;
	if(lson[x])solve(id,lson[x],l,x-1,a[id][x]);
	if(rson[x])solve(id,rson[x],x+1,r,a[id][x]);
}
int main(){
	scanf("%d%d",&n,&m);
	for(int i=2;i<=n;i++)scanf("%lld",&s[i]),s[i]+=s[i-1];
	for(int i=1;i<=n;i++)for(int j=1;j<=m;j++)scanf("%d",&a[j][i]);
	for(int i=1;i<=m;i++){
		tp=0;
		for(int j=1;j<=n;j++){
			lson[j]=rson[j]=0;
			while(tp&&a[i][stk[tp]]<=a[i][j])lson[j]=stk[tp--];
			if(stk[tp])rson[stk[tp]]=j;
			stk[++tp]=j;
		}
		solve(i,stk[1],1,n,0);
	}
	for(int i=1;i<=n;i++)for(int j=n;j>=i;j--)f[i][j]+=f[i-1][j]+f[i][j+1]-f[i-1][j+1];
	for(int i=1;i<=n;i++)for(int j=i;j<=n;j++)res=max(res,f[i][j]-(s[j]-s[i]));
	printf("%lld\n",res);
	return 0;
}
```

# CVI.[[CSACADEMY]Root Change](https:\/\/csacademy.com\/contest\/archive\/task\/root-change\/)

常规换根DP。设 $f_i$ 表示 $i$ 子树中以 $i$ 为起点的最长路径长度，设 $sz_i$ 表示 $i$ 子树中**边**的数量，再设 $g_i$ 表示 $i$ 子树的答案。

则 $f$ 和 $sz$ 显然很好转移。考虑 $g$，则有

$$g_i=\begin{cases}sz_i&(\text{存在两个以上的儿子具有最长路径})\\sz_i+\Big(g_j-(sz_j+1)\Big)&(\text{具有最长路径的儿子}j\text{唯一})\end{cases}$$

于是直接上 `multiset` 暴力换根即可。时间复杂度 $O(n\log n)$。

代码：

```cpp
#include<bits\/stdc++.h>
using namespace std;
int n,f[100100],g[100100],sz[100100];
vector<int>v[100100];
multiset<pair<int,int> >s[100100];
multiset<int>t[100100];
void dfs1(int x,int fa){
	for(auto y:v[x])if(y!=fa)dfs1(y,x),f[x]=max(f[x],f[y]+1),sz[x]+=sz[y]+1,s[x].insert(make_pair(f[y]+1,g[y]-(sz[y]+1))),t[x].insert(f[y]+1);
	g[x]=sz[x];
	if(s[x].size()==1||s[x].size()>=2&&s[x].rbegin()->first!=(++s[x].rbegin())->first)g[x]+=s[x].rbegin()->second;
}
void dfs2(int x,int fa){
	for(auto y:v[x]){
		if(y==fa)continue;
		int fx=0,szx=sz[x]-sz[y]-1;
		t[x].erase(t[x].find(f[y]+1));
		if(!t[x].empty())fx=*t[x].rbegin();
		t[x].insert(f[y]+1);
		int gx=szx;
		s[x].erase(s[x].find(make_pair(f[y]+1,g[y]-(sz[y]+1))));
		if(s[x].size()==1||s[x].size()>=2&&s[x].rbegin()->first!=(++s[x].rbegin())->first)gx+=s[x].rbegin()->second;
		s[x].insert(make_pair(f[y]+1,g[y]-(sz[y]+1)));
		
		t[y].insert(fx+1);
		s[y].insert(make_pair(fx+1,gx-(szx+1)));
		sz[y]+=szx+1;
		f[y]=*t[y].rbegin();
		g[y]=sz[y];
		if(s[y].size()==1||s[y].size()>=2&&s[y].rbegin()->first!=(++s[y].rbegin())->first)g[y]+=s[y].rbegin()->second;
		dfs2(y,x);
	}
}
int main(){
	scanf("%d",&n);
	for(int i=1,x,y;i<n;i++)scanf("%d%d",&x,&y),v[x].push_back(y),v[y].push_back(x);
	dfs1(1,0),dfs2(1,0);
	for(int i=1;i<=n;i++)printf("%d\n",g[i]);
	return 0;
}
```

# CVII.[[NOI2009]二叉查找树](https:\/\/www.luogu.com.cn\/problem\/P1864)

首先该树的中序遍历是唯一可以确定的（直接按照数据值排序即可）。

然后，因为权值可以被修改成一切实数，故我们完全可以把权值离散化掉。

于是我们现在可以设置一个DP状态$f[l,r,lim]$表示：

区间$[l,r]$中的所有东西构成了一棵子树，且树中最小权值不小于$lim$的最优方案。

然后就枚举根转移即可。转移的时候就可以看作是子树内所有东西被整体提高了一层，所以直接增加$sum[l,r]$（意为区间$[l,r]$中的所有数据值之和）即可。同时，如果有当前枚举的根的权值不小于$lim$，显然就可以不修改，但是两边儿子的权值就必须比它大；否则则必须修改，两边儿子的权值下限还是$lim$（因为根的权值可以被修改成一个略大于$lim$的实数）。

则时间复杂度$O(n^4)$。

代码：

```cpp
#include<bits\/stdc++.h>
using namespace std;
int n,m,sum[110],f[110][110][110];
struct dat{
	int val,key,lam;
}a[100];
int dfs(int l,int r,int lim){
	if(l>r)return 0;
	if(f[l][r][lim]!=-1)return f[l][r][lim];
	int &now=f[l][r][lim];now=0x3f3f3f3f;
	for(int i=l;i<=r;i++){\/\/assume that i is the root in the section [l,r].
		if(a[i].key>=lim)now=min(now,dfs(l,i-1,a[i].key)+dfs(i+1,r,a[i].key)+sum[r]-sum[l-1]);\/\/do not modify, the height simply increased by one.
		now=min(now,dfs(l,i-1,lim)+dfs(i+1,r,lim)+m+sum[r]-sum[l-1]);\/\/modify i to any real number a little greater than lim.
	}
	return now;
}
int main(){
	scanf("%d%d",&n,&m),memset(f,-1,sizeof(f));
	for(int i=1;i<=n;i++)scanf("%d",&a[i].val);
	for(int i=1;i<=n;i++)scanf("%d",&a[i].key);
	for(int i=1;i<=n;i++)scanf("%d",&a[i].lam);
	sort(a+1,a+n+1,[](dat u,dat v){return u.key<v.key;});
	for(int i=1;i<=n;i++)a[i].key=i;
	sort(a+1,a+n+1,[](dat u,dat v){return u.val<v.val;});
	for(int i=1;i<=n;i++)sum[i]=sum[i-1]+a[i].lam;
	printf("%d\n",dfs(1,n,1));
	return 0;
}
```

# CVIII.[[POI2014]MRO-Ant colony](https:\/\/www.luogu.com.cn\/problem\/P3576)

根据下取整除法的性质（$\left\lfloor\dfrac{\left\lfloor\dfrac{x}{y}\right\rfloor}{z}\right\rfloor=\left\lfloor\dfrac{x}{yz}\right\rfloor$），我们可以反向考虑，即从特殊边开始，计算出从每个叶子到特殊边的路径上，要除以的那个分母是什么。

这个可以直接一遍dfs就出来了（可以把它当成DP）。注意，当一段路径的分母已经爆$10^9$时就可以直接退出了，因为这样子不会有蚂蚁到得了特殊边。

然后，对于一个分母$d$，所有$\in\Big[dk,d(k+1)\Big)$的蚁群数量都是合法的；故我们直接对蚁群数量排序然后二分再差分即可。

时间复杂度$O(n\log n)$。

代码：

```cpp
#include<bits\/stdc++.h>
using namespace std;
typedef long long ll;
const int LIM=1e9;
int n,m,k,sp[1001000],U,V;
ll dif[1001000],res;
vector<int>v[1001000],u;
void dfs(int x,int fa,int lam){
	if(v[x].size()==1){u.push_back(lam);return;}
	if(1ll*lam*(v[x].size()-1)>LIM)return;
	lam*=(v[x].size()-1);
	for(auto y:v[x])if(y!=fa)dfs(y,x,lam);
}
int main(){
	scanf("%d%d%d",&n,&m,&k);
	for(int i=1;i<=m;i++)scanf("%d",&sp[i]);
	scanf("%d%d",&U,&V),v[U].push_back(V),v[V].push_back(U);
	for(int i=1,x,y;i+1<n;i++)scanf("%d%d",&x,&y),v[x].push_back(y),v[y].push_back(x);
	dfs(U,V,1),dfs(V,U,1);
	sort(sp+1,sp+m+1);
	for(auto i:u){
		ll l=1ll*k*i,r=1ll*(k+1)*i;
		if(l>LIM)continue;
		dif[lower_bound(sp+1,sp+m+1,l)-sp]++;
		dif[lower_bound(sp+1,sp+m+1,r)-sp]--;
	}
	for(int i=1;i<=m;i++)dif[i]+=dif[i-1],res+=dif[i]; 
	printf("%lld\n",res*k);
	return 0;
}
```

# CIX.[[NOI Online #1 入门组]魔法](https:\/\/www.luogu.com.cn\/problem\/P6190)

我们可以构造出原图的转移矩阵 $A$，表示只走原图的边的代价。这个直接暴力上Floyd即可。

我们还可以构造出魔法的转移矩阵$B$。

则，可以想到，答案一定是

$$ABABABABAB\dots ABA$$

这种样子。

故我们用$B$左乘$A$得到$C=(BA)$。则计算$AC^k$，即为答案。

时间复杂度$O(n^3\log k)$。

代码：

```cpp
#include<bits\/stdc++.h>
using namespace std;
typedef long long ll;
int n,m,p;
struct Matrix{
	ll a[110][110];
	void init(){memset(a,0x3f,sizeof(a));for(int i=1;i<=n;i++)a[i][i]=0;}
	ll* operator[](int x){return a[x];}
	friend Matrix operator *(Matrix &u,Matrix &v){
		Matrix w;w.init();
		for(int i=1;i<=n;i++)for(int j=1;j<=n;j++)for(int k=1;k<=n;k++)w[i][j]=min(w[i][j],u[i][k]+v[k][j]);
		return w;
	}
}a,b;
int main(){
	scanf("%d%d%d",&n,&m,&p);
	a.init(),b.init();
	for(int i=1,x,y,z;i<=m;i++)scanf("%d%d%d",&x,&y,&z),a[x][y]=min(a[x][y],1ll*z),b[x][y]=min(b[x][y],-1ll*z);
	for(int k=1;k<=n;k++)for(int i=1;i<=n;i++)for(int j=1;j<=n;j++)a[i][j]=min(a[i][j],a[i][k]+a[k][j]);
\/\/	for(int i=1;i<=n;i++){for(int j=1;j<=n;j++)printf("%d ",a[i][j]);puts("");}
	b=b*a;
\/\/	for(int i=1;i<=n;i++){for(int j=1;j<=n;j++)printf("%d ",b[i][j]);puts("");}
	for(;p;p>>=1,b=b*b)if(p&1)a=a*b;
	printf("%lld\n",a[1][n]);
	return 0;
}
```

# CX.[[POI2015]MOD](https:\/\/www.luogu.com.cn\/problem\/P3596)

比较恶心的题目。

首先，有一个结论，即如果把两棵树通过某种方式连接起来，新树的直径的端点一定来自于原本两棵树的直径端点集合。

则考虑新树的最大直径，明显就是把两棵树的直径直接连一块，就是两棵树的直径之和再加一。

考虑新树的最小直径，则应该选择两树直径的中点（如果直径长度为奇数则随便选一个）连一块，这样新树的直径就是 $\left\lceil\dfrac{\text{直径一}}{2}\right\rceil+\left\lceil\dfrac{\text{直径二}}{2}\right\rceil+1$。当然，还得与两条直径本身取一个$\max$。

于是我们就用换根DP求出$g_x$表示$x$子树内的直径，$h_x$求出其子树外的直径（这里换根DP我一开始用的是```multiset```维护，但是会莫名其妙`MLE`。故最后不得不全面换成```vector```才不出问题）。然后两个拼一块就能找出所有新树的直径的最大值\/最小值。

代码（非常丑陋）：

```cpp
#include<bits\/stdc++.h>
using namespace std;
int n,f[500100],g[500100],h[500100],FA[500100],mx,mn=0x3f3f3f3f;
\/\/f[i]:the maximal length starting from i; g[i]: the maximal length in i's subtree; h[i]:the maximal length outside that.
vector<int>v[500100],s[500100],t[500100];
void dfs1(int x,int fa){
	for(auto y:v[x]){
		if(y==fa)continue;
		FA[y]=x;
		dfs1(y,x);
		f[x]=max(f[x],f[y]+1);
		s[x].push_back(f[y]+1);
		t[x].push_back(g[y]);
		g[x]=max(g[x],g[y]);
	}
	sort(s[x].rbegin(),s[x].rend());while(s[x].size()>3)s[x].pop_back();
	sort(t[x].rbegin(),t[x].rend());while(t[x].size()>2)t[x].pop_back();
	if(s[x].size()>=2)g[x]=max(g[x],s[x][0]+s[x][1]);
	else if(s[x].size()>=1)g[x]=max(g[x],s[x][0]);
}
void dfs2(int x,int fa){
	int alls=0;
	for(auto i:s[x])alls+=i;
\/\/	printf("%dS",x);for(auto i:s[x])printf("%d ",i);puts("");
\/\/	printf("%dT",x);for(auto i:t[x])printf("%d ",i);puts("");
	for(auto y:v[x]){
		if(y==fa)continue;
		if(f[y]+1>=s[x].back())h[y]=alls-(f[y]+1);
		else if(s[x].size()<=2)h[y]=alls;
		else h[y]=s[x][0]+s[x][1];
		
		if(t[x][0]!=g[y])h[y]=max(h[y],t[x][0]);
		else if(t[x].size()>=2)h[y]=max(h[y],t[x][1]);
		
		t[y].push_back(h[y]);
		sort(t[y].rbegin(),t[y].rend());while(t[y].size()>2)t[y].pop_back();
		
		if(s[x][0]!=f[y]+1)s[y].push_back(s[x][0]+1);
		else if(s[x].size()>=2)s[y].push_back(s[x][1]+1);
		else s[y].push_back(1);
		sort(s[y].rbegin(),s[y].rend());while(s[y].size()>3)s[y].pop_back();
		
		dfs2(y,x);
	}
}
int S,dp,inva,nd,rt;
void dfs3(int x,int fa,int dep){
	if(dep>dp)S=x,dp=dep;
	for(auto y:v[x])if(y!=fa&&y!=inva)dfs3(y,x,dep+1);
}
bool dfs4(int x,int fa){
	if(x==S){
		nd--;
		if(nd==0)rt=x;
		return true;	
	}
	for(auto y:v[x]){
		if(y==fa)continue;
		if(!dfs4(y,x))continue;
		nd--;
		if(nd==0)rt=x;
		return true;
	}
	return false;
}
int main(){
	scanf("%d",&n);
	for(int i=1,x,y;i<n;i++)scanf("%d%d",&x,&y),v[x].push_back(y),v[y].push_back(x);
	dfs1(1,0),dfs2(1,0);
\/\/	for(int i=1;i<=n;i++)printf("%d:%d %d %d\n",i,f[i],g[i],h[i]);
	for(int i=2;i<=n;i++)mx=max(mx,g[i]+h[i]+1),mn=min(mn,max({(g[i]+1)\/2+(h[i]+1)\/2+1,g[i],h[i]}));
	for(int i=2;i<=n;i++){
		if(mn!=max({(g[i]+1)\/2+(h[i]+1)\/2+1,g[i],h[i]}))continue;
		printf("%d %d %d ",mn,i,FA[i]);
		inva=FA[i];
		S=0,dp=-1;
		dfs3(i,FA[i],0);
		int T=S;
		S=0,dp=-1;
		dfs3(T,0,0);
		nd=(g[i]+2)\/2;
		dfs4(T,0);
		printf("%d ",rt);
		
		inva=i;
		S=0,dp=-1;
		dfs3(FA[i],i,0);
		T=S;
		S=0,dp=-1;
		dfs3(T,0,0);
		nd=(h[i]+2)\/2,dfs4(T,0);
		printf("%d\n",rt);
		break;
	}
	for(int i=2;i<=n;i++){
		if(mx!=g[i]+h[i]+1)continue;
		inva=0;
		printf("%d %d %d ",mx,i,FA[i]);
		S=0,dp=-1;
		dfs3(i,FA[i],0);
		printf("%d ",S);
		S=0,dp=-1;
		dfs3(FA[i],i,0);
		printf("%d\n",S);
		break;
	}
	return 0;
}
```

# CXI.[[九省联考2018]一双木棋chess](https:\/\/www.luogu.com.cn\/problem\/P4363)

一下子就想到了LXX.[[USACO5.5]贰五语言Two Five](https:\/\/www.luogu.com.cn\/problem\/P2750)（可见刷题笔记II），因为同是阶梯型的图样。然后稍微想一想就发现总方案数可以用隔板法证得是$\dbinom{n+m}{m}$的，代入一看发现才$2\times10^5$都不到。于是就果断DP了。

首先先用爆搜搜出所有图案的分布（实现从编号到图案的映射），然后再预处理一个辅助的DP来实现从图案到编号的映射。然后就直接分当前是谁操作进行不同的转移即可。

时间复杂度，如上所述，是$\dbinom{n+m}{m}\times\text{转移复杂度}$的。我采取的转移是$O(n^2)$的，还可以被优化为最终$O(n)$转移，但是没有必要。

代码：

```cpp
#include<bits\/stdc++.h>
using namespace std;
int n,m,cnt,f[20][20],a[20][20],b[20][20],g[200000];
vector<int>v[200100];
vector<int>u;
void dfs(int pos,int lim){
	if(pos==n){v[++cnt]=u;return;}
	for(int i=0;i<=lim;i++){
		u.push_back(i);
		dfs(pos+1,i);
		u.pop_back();
	}
}
int deco(vector<int>&ip){
	int ret=1;
	for(int i=0;i<n;i++)if(ip[i])ret+=f[i][ip[i]-1];
	return ret;
}
int dp(int ip,bool sd){
	if(ip==cnt)return 0;
	if(g[ip]!=-1)return g[ip];
	if(sd==0){\/\/first player
		g[ip]=0xc0c0c0c0;
		vector<int>tmp=v[ip];
		for(int i=0;i<n;i++){
			if(i==0&&tmp[i]==m||i>0&&tmp[i]==tmp[i-1])continue;
			tmp[i]++;
			g[ip]=max(g[ip],dp(deco(tmp),sd^1)+a[i][tmp[i]]);
			tmp[i]--;
		}
		return g[ip];
	}else{
		g[ip]=0x3f3f3f3f;
		vector<int>tmp=v[ip];
		for(int i=0;i<n;i++){
			if(i==0&&tmp[i]==m||i>0&&tmp[i]==tmp[i-1])continue;
			tmp[i]++;
			g[ip]=min(g[ip],dp(deco(tmp),sd^1)-b[i][tmp[i]]);
			tmp[i]--;
		}
		return g[ip];		
	}
}
int main(){
	scanf("%d%d",&n,&m),memset(g,-1,sizeof(g));
	dfs(0,m);
	for(int i=0;i<=m;i++)f[n-1][i]=i+1;
	for(int i=n-2;i>=0;i--)for(int j=0;j<=m;j++)for(int k=0;k<=j;k++)f[i][j]+=f[i+1][k];
	for(int i=0;i<n;i++)for(int j=1;j<=m;j++)scanf("%d",&a[i][j]);
	for(int i=0;i<n;i++)for(int j=1;j<=m;j++)scanf("%d",&b[i][j]);
	printf("%d\n",dp(1,0));
	return 0;
} 
```


