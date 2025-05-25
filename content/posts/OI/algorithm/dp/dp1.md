---
author: "MoonWonder"
author_link: "moonwonder.top"
title: "dp1"
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



发现自己DP学的很糟糕……难一点的DP根本不会做……因此决定不管三七二十一先刷上百十来道再说……

# O. 前提

本笔记的重点是**状态的设计**，在转移简单的时候就会一笔带过。

当然，如果转移也比较恶心，会提到的。

# I.[[JSOI2010]快递服务](https://www.luogu.com.cn/problem/P4046)

我们约定共有$n$个地点，依次登记了$m$家公司。

思路1.

设$f[l][i][j][k]$表示：当前某一个司机在第$i$家公司（注意是公司！$1000$家那个！），第二个司机在第$j$家，第三个司机在第$k$家，当前我们遍历到了第$l$家公司。依次转移即可。

复杂度$O(m^4)$。

思路2. 观察到$i, j, k$中必有一个等于$l$（不然你位置$l$的货是哪辆车发的？），因此我们可以省掉一维。设$f[i][j][k]$即可。

复杂度$O(m^3)$。

明显第一维可以滚动掉，因此空间复杂度便可以通过。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,dis[210][210],f[2][1010][1010],pos[1010],m,res=0x3f3f3f3f;
int main(){
	scanf("%d",&n);
	for(int i=1;i<=n;i++)for(int j=1;j<=n;j++)scanf("%d",&dis[i][j]);
	memset(f,0x3f3f3f3f,sizeof(f)),f[1][2][1]=0;
	pos[++m]=1,pos[++m]=2,pos[++m]=3;
	while(scanf("%d",&pos[++m])!=EOF);
	for(int i=3;i<m;i++){
		for(int j=1;j<=i;j++)for(int k=1;k<j;k++)f[!(i&1)][j][k]=0x3f3f3f3f;
		for(int j=1;j<i;j++)for(int k=1;k<j;k++){
			f[!(i&1)][j][k]=min(f[!(i&1)][j][k],f[i&1][j][k]+dis[pos[i]][pos[i+1]]);
			f[!(i&1)][i][k]=min(f[!(i&1)][i][k],f[i&1][j][k]+dis[pos[j]][pos[i+1]]);
			f[!(i&1)][i][j]=min(f[!(i&1)][i][j],f[i&1][j][k]+dis[pos[k]][pos[i+1]]);
		}
//		for(int j=1;j<=i;j++){for(int k=1;k<j;k++)printf("%d ",f[!(i&1)][j][k]);puts("");}puts("");
	}
	for(int j=1;j<m;j++)for(int k=1;k<j;k++)res=min(res,f[m&1][j][k]);
	printf("%d\n",res);
	return 0;
} 
```

思路3. 发现$O(m^3)$只能拿到$50\%$。似乎只有最后两维可以优化成$n^2$的。

我们设$f[i][j][k]$表示：当前某一辆车在第$i$家**公司**（还是$1000$家那个！）剩下两辆车分别在第$j$和第$k$个**收件地点**（是$200$家那个！）。

复杂度为$O(mn^2)$。

这是正解~~尽管出题人丧心病狂卡长只有$70\%$但是开个$O3$然后卡卡长就过了~~。

代码：

``` cpp
#pragma GCC optimize(3)
#include<bits/stdc++.h>
using namespace std;
int n,dis[210][210],f[2][1010][1010],pos[1010],m,res=0x3f3f3f3f;
inline void read(int &x){
	x=0;
	register char c=getchar();
	while(c>'9'||c<'0')c=getchar();
	while(c>='0'&&c<='9')x=(x<<3)+(x<<1)+(c^48),c=getchar();
}
inline void print(int x){
	if(x<=9)putchar('0'+x);
	else print(x/10),putchar('0'+x%10);
}
int main(){
	read(n);
	for(register int i=1;i<=n;i++)for(register int j=1;j<=n;j++)read(dis[i][j]);
	memset(f,0x3f3f3f3f,sizeof(f)),f[1][2][1]=0;
	pos[++m]=1,pos[++m]=2,pos[++m]=3;
	while(scanf("%d",&pos[++m])!=EOF);
	for(register int i=3;i<m;i++){
		for(register int j=1;j<=n;j++)for(register int k=1;k<=n;k++)f[!(i&1)][j][k]=0x3f3f3f3f;
		for(register int j=1;j<=n;j++)for(register int k=1;k<=n;k++){
			f[!(i&1)][j][k]=min(f[!(i&1)][j][k],f[i&1][j][k]+dis[pos[i]][pos[i+1]]);
			f[!(i&1)][pos[i]][k]=min(f[!(i&1)][pos[i]][k],f[i&1][j][k]+dis[j][pos[i+1]]);
			f[!(i&1)][pos[i]][j]=min(f[!(i&1)][pos[i]][j],f[i&1][j][k]+dis[k][pos[i+1]]);
		}
//		for(int j=1;j<=i;j++){for(int k=1;k<j;k++)printf("%d ",f[!(i&1)][j][k]);puts("");}puts("");
	}
	for(register int j=1;j<=n;j++)for(register int k=1;k<=n;k++)res=min(res,f[m&1][j][k]);
	print(res);
	return 0;
} 
```

# II.[[HAOI2010]计数](https://www.luogu.com.cn/problem/P2518)

我不得不吐槽出题人的语文实在太……那个了。

翻译一下：给你一个数，求它是全排列中第几个。

为什么呢？我们看一下给定的那个$\{1, 2\}$的例子。显然，在任何合法的数中，所有的非零数的出现次数，在每个数中都是相同的。如果我们允许前导零，那么所有的$0$的出现次数也都相同了。（删去$0$可以看作将$0$移到了开头）

我们考虑借鉴数位DP的思想：从高位向低位枚举，并考虑当前这位填入比原数小的数还是和原数相同的数。

如果填入一个比它小的数，那么后面的位就可以全排列了。

考虑每个数$i$共出现了$cnt_i$次，所有数总共出现了$tot$次。

数字$0$可以在这$tot$个位置里面随便填，共$C_{tot}^{cnt_0}$种方案。

数字$1$可以在剩下$tot-cnt_0$个位置里面随便填，共$C_{tot-cnt_0}^{cnt_1}$种方案。

以此类推。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int n,num[100],cnt[10],C[100][100],res;
char s[100];
int calc(int tot){
	int ans=1;
	for(int i=0;i<10;i++)ans*=C[tot][cnt[i]],tot-=cnt[i];
	return ans;
}
signed main(){
	scanf("%s",s+1),n=strlen(s+1);
	for(int i=0;i<=n;i++)C[i][0]=1;
	for(int i=1;i<=n;i++)for(int j=1;j<=i;j++)C[i][j]=C[i-1][j-1]+C[i-1][j];
//	for(int i=0;i<=n;i++){for(int j=0;j<=i;j++)printf("%d ",C[i][j]);puts("");}
	for(int i=1;i<=n;i++)num[i]=s[i]-'0',cnt[num[i]]++;
	for(int i=1;i<=n;i++){
		for(int j=0;j<num[i];j++){
			if(!cnt[j])continue;
			cnt[j]--;
			res+=calc(n-i);
			cnt[j]++;
		}
		cnt[num[i]]--;
	}
	printf("%lld\n",res);
	return 0;
}
```

# III.[[SCOI2009]粉刷匠](https://www.luogu.com.cn/problem/P4158)

所有的DP，只要式子一推出来（不管复杂度），那就很简单了，因为优化是成千上万种的……

思路1. 我们考虑设$f[i][j][k]$表示：当前DP到第$i$块木板的第$j$个位置，共涂了$k$次，所能获得的最大收益。因为还要枚举当前这次涂是从哪到哪的，因此复杂度为$O(NM^2T)$，实际$90\%$。在实际操作中，第一维可以省略。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,t,f[100][5000],res[100][100][2],ans;
char s[100];
int main(){
	scanf("%d%d%d",&n,&m,&t);
	for(int l=1;l<=n;l++){
		scanf("%s",s+1);
		for(int i=1;i<=m;i++)for(int j=i;j<=m;j++)res[i][j][0]=res[i][j-1][0]+(s[j]=='0'),res[i][j][1]=res[i][j-1][1]+(s[j]=='1');
		for(int i=0;i<=t;i++)f[0][i]=f[m][i];
		for(int i=1;i<=m;i++){
			for(int j=1;j<=t;j++){
				f[i][j]=0;
				for(int k=0;k<i;k++)f[i][j]=max(f[i][j],f[k][j-1]+max(res[k+1][i][0],res[k+1][i][1]));
			}
		}
	}
	for(int i=1;i<=t;i++)ans=max(ans,f[m][i]);
	printf("%d\n",ans);
	return 0;
}
```

虽然开个$O2$甚至只是单纯卡卡长也一样能过，但是介于十年前评测姬的蜜汁速度，我们思考还有没有优化复杂度的余地。

思路2. 我们考虑设$f[i][j][k][0/1/2]$表示：

当前DP到第$i$块木板的第$j$个位置，共涂了$k$次，当前这个位置的状态是$0/1/2$。

其中，状态$0$意为涂上了颜色$0$，状态$1$意为涂上了颜色$1$，状态$2$意为啥也没涂。

因为这种方法不需要枚举上一次的断点，因此复杂度是$O(NMT)$的。老样子，第一维可以砍掉。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,t,f[100][5000][3],res;
char s[100];
int main(){
	scanf("%d%d%d",&n,&m,&t);
	for(int l=1;l<=n;l++){
		scanf("%s",s+1);
		for(int i=0;i<=t;i++)f[0][i][2]=max(max(f[m][i][0],f[m][i][1]),f[m][i][2]);
		for(int i=1;i<=m;i++){
			for(int j=1;j<=t;j++){
				f[i][j][2]=max(max(f[i-1][j][0],f[i-1][j][1]),f[i-1][j][2]);
				f[i][j][1]=max(max(f[i-1][j-1][0],f[i-1][j][1]),f[i-1][j-1][2])+(s[i]=='0');
				f[i][j][0]=max(max(f[i-1][j][0],f[i-1][j-1][1]),f[i-1][j-1][2])+(s[i]=='1');
			}
		}
	}
	for(int i=1;i<=t;i++)res=max(max(res,f[m][i][2]),max(f[m][i][0],f[m][i][1]));
	printf("%d\n",res);
	return 0;
}
```

# IV.[[SCOI2003]字符串折叠](https://www.luogu.com.cn/problem/P4302)

一眼区间DP。

设$f[i][j]$表示：将区间$[i, j]$内的所有东西压一起的最短长度。

显然，有两种方法：

1. 在中间一刀劈开，然后拼一起。

2. 找到它的循环节，然后把整个串压一起。

至于找循环节吗……枚举循环节长度，然后无脑哈希一下。

注意，你可能会压出类似于$10(AB)$这种东西，记得$10$是两位数！！！

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
typedef unsigned long long ull;
char s[110];
int n,f[110][110];
ull sd1=998244353,sd2=666623333,pov1[2001000],pov2[2001000];
struct HASH{
	ull val1,val2;
	int len;
	HASH(){
		val1=val2=0ull;
		len=0;
	}
	HASH(char ip){
		val1=val2=ip;
		len=1;
	}
	friend HASH operator +(const HASH &x,const HASH &y){
		HASH z;
		z.val1=x.val1*pov1[y.len]+y.val1;
		z.val2=x.val2*pov2[y.len]+y.val2;
		z.len=x.len+y.len;
		return z;
	}
	friend HASH operator -(const HASH &x,const HASH &y){
		HASH z;
		z.val1=x.val1-y.val1*pov1[x.len-y.len];
		z.val2=x.val2-y.val2*pov2[x.len-y.len];
		z.len=x.len-y.len;
		return z;
	}
	friend bool operator ==(const HASH &x,const HASH &y){
		if(x.len!=y.len)return false;
		if(x.val1!=y.val1)return false;
		if(x.val2!=y.val2)return false;
		return true;
	}
}hs[110];
int calc(int x){
	int res=0;
	while(x)res++,x/=10;
	return res;
}
int main(){
	scanf("%s",s+1),memset(f,0x3f3f3f3f,sizeof(f)),n=strlen(s+1);
	pov1[0]=pov2[0]=1;
	for(int i=1;i<=n;i++)pov1[i]=pov1[i-1]*sd1,pov2[i]=pov2[i-1]*sd2;
	for(int i=1;i<=n;i++)hs[i]=hs[i-1]+HASH(s[i]),f[i][i]=1;
	for(int l=2;l<=n;l++){
		for(int i=1,j=i+l-1;j<=n;i++,j++){
			for(int k=i;k<j;k++)f[i][j]=min(f[i][j],f[i][k]+f[k+1][j]);
			for(int k=1;k<l;k++){
				if(l%k)continue;
				if((hs[j]-hs[i+k-1])==(hs[j-k]-hs[i-1]))f[i][j]=min(f[i][j],f[i][i+k-1]+2+calc(l/k));
			}
		}
	}
//	for(int i=1;i<=n;i++){for(int j=i;j<=n;j++)printf("%d ",f[i][j]);puts("");}
	printf("%d\n",f[1][n]);
	return 0;
}
```

# V.[[SCOI2007]压缩](https://www.luogu.com.cn/problem/P2470)

这种DP状态需要考虑到各种状态的题最讨厌了……

思路1. 设$f[i][j]$表示将区间$[i, j]$里面所有东西压一起的最小代价

有两种转移：

1. 砍成两段拼一起

2. 样例里面这种方法，```MaRR=aaaa``` 这种倍增法

然后我就写出了这样的代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
typedef unsigned long long ull;
char s[110];
int n,f[110][110];
ull sd1=998244353,sd2=666623333,pov1[2001000],pov2[2001000];
struct HASH{
	ull val1,val2;
	int len;
	HASH(){
		val1=val2=0ull;
		len=0;
	}
	HASH(char ip){
		val1=val2=ip;
		len=1;
	}
	friend HASH operator +(const HASH &x,const HASH &y){
		HASH z;
		z.val1=x.val1*pov1[y.len]+y.val1;
		z.val2=x.val2*pov2[y.len]+y.val2;
		z.len=x.len+y.len;
		return z;
	}
	friend HASH operator -(const HASH &x,const HASH &y){
		HASH z;
		z.val1=x.val1-y.val1*pov1[x.len-y.len];
		z.val2=x.val2-y.val2*pov2[x.len-y.len];
		z.len=x.len-y.len;
		return z;
	}
	friend bool operator ==(const HASH &x,const HASH &y){
		if(x.len!=y.len)return false;
		if(x.val1!=y.val1)return false;
		if(x.val2!=y.val2)return false;
		return true;
	}
	friend bool operator !=(const HASH &x,const HASH &y){
		return !(x==y);
	}
}hs[110];
bool che(int ip){
	return ip==(ip&-ip);
}
int main(){
	scanf("%s",s+1),memset(f,0x3f3f3f3f,sizeof(f)),n=strlen(s+1);
	pov1[0]=pov2[0]=1;
	for(int i=1;i<=n;i++)pov1[i]=pov1[i-1]*sd1,pov2[i]=pov2[i-1]*sd2;
	for(int i=1;i<=n;i++)hs[i]=hs[i-1]+HASH(s[i]),f[i][i]=1;
	for(int l=2;l<=n;l++){
		for(int i=1,j=i+l-1;j<=n;i++,j++){
			for(int k=i;k<j;k++)f[i][j]=min(f[i][j],f[i][k]+f[k+1][j]);
			for(int k=1;k<l;k++){
				if(l%k)continue;
				if((hs[j]-hs[i+k-1])!=(hs[j-k]-hs[i-1]))continue;
				if(!che(l/k))continue;
//				printf("%d %d %d\n",i,j,l/k);
				f[i][j]=min(f[i][j],f[i][i+k-1]+__builtin_ctz(l/k)+(i!=1));
			}
		}
	}
//	for(int l=1;l<=n;l++){for(int i=1,j=i+l-1;j<=n;i++,j++)printf("%d ",f[i][j]);puts("");}
	printf("%d\n",f[1][n]);
	return 0;
}
```

一交，WA，$40\%$。

怎么回事？

我费尽千辛万苦，找到一组hack数据：

```xabababababab

```

按照我之前的这种压法，会压出来```xMMabRabR```这种东西。因为这时区间DP，按照我之前的思路，是按照括号的顺序压的：

```x(M(MabR)abR)```

因此，相同的左端点，如果已经有了一个`` `M` ` `，就不用重复有` ` `M` ``了。

我们设一个新状态$f[i][j][0/1]$表示：将区间$[i, j]$压一起，左端点有无`` `M` ``的状态是$[0/1]$。

然后写出来这样的东西：

``` cpp
#include<bits/stdc++.h>
using namespace std;
typedef unsigned long long ull;
char s[110];
int n,f[110][110][2];
ull sd1=998244353,sd2=666623333,pov1[2001000],pov2[2001000];
struct HASH{
	ull val1,val2;
	int len;
	HASH(){
		val1=val2=0ull;
		len=0;
	}
	HASH(char ip){
		val1=val2=ip;
		len=1;
	}
	friend HASH operator +(const HASH &x,const HASH &y){
		HASH z;
		z.val1=x.val1*pov1[y.len]+y.val1;
		z.val2=x.val2*pov2[y.len]+y.val2;
		z.len=x.len+y.len;
		return z;
	}
	friend HASH operator -(const HASH &x,const HASH &y){
		HASH z;
		z.val1=x.val1-y.val1*pov1[x.len-y.len];
		z.val2=x.val2-y.val2*pov2[x.len-y.len];
		z.len=x.len-y.len;
		return z;
	}
	friend bool operator ==(const HASH &x,const HASH &y){
		if(x.len!=y.len)return false;
		if(x.val1!=y.val1)return false;
		if(x.val2!=y.val2)return false;
		return true;
	}
	friend bool operator !=(const HASH &x,const HASH &y){
		return !(x==y);
	}
}hs[110];
bool che(int ip){
	return ip==(ip&-ip);
}
int main(){
	scanf("%s",s+1),memset(f,0x3f3f3f3f,sizeof(f)),n=strlen(s+1);
	pov1[0]=pov2[0]=1;
	for(int i=1;i<=n;i++)pov1[i]=pov1[i-1]*sd1,pov2[i]=pov2[i-1]*sd2;
	for(int i=1;i<=n;i++){
		hs[i]=hs[i-1]+HASH(s[i]);
		f[i][i][0]=1;
		f[i][i][1]=1+(i!=1);
	}
	for(int l=2;l<=n;l++){
		for(int i=1,j=i+l-1;j<=n;i++,j++){
			for(int k=i;k<j;k++)f[i][j][0]=min(f[i][j][0],f[i][k][0]+min(f[k+1][j][0],f[k+1][j][1])),f[i][j][1]=min(f[i][j][1],f[i][k][1]+min(f[k+1][j][0],f[k+1][j][1]));
			for(int k=1;k<l;k++){
				if(l%k)continue;
				if((hs[j]-hs[i+k-1])!=(hs[j-k]-hs[i-1]))continue;
				if(!che(l/k))continue;
//				printf("%d %d %d\n",i,j,l/k);
				f[i][j][1]=min(f[i][j][1],min(f[i][i+k-1][0]+1,f[i][i+k-1][1])+__builtin_ctz(l/k));
			}
		}
	}
//	for(int l=1;l<=n;l++){for(int i=1,j=i+l-1;j<=n;i++,j++)printf("%d ",f[i][j]);puts("");}
	printf("%d\n",f[1][n][1]);
	return 0;
}
//xabababababab
```

一交，WA，$70\%$。

然后我想了想，那种倍增的合并法也可以并入（左端点已经有了`` `M` ``）的情形。

然后我改成了这样的代码（这种情形实际上哈希都没必要了）

``` cpp
#include<bits/stdc++.h>
using namespace std;
typedef unsigned long long ull;
char s[110];
int n,f[110][110][2];
ull sd1=998244353,sd2=666623333,pov1[2001000],pov2[2001000];
struct HASH{
	ull val1,val2;
	int len;
	HASH(){
		val1=val2=0ull;
		len=0;
	}
	HASH(char ip){
		val1=val2=ip;
		len=1;
	}
	friend HASH operator +(const HASH &x,const HASH &y){
		HASH z;
		z.val1=x.val1*pov1[y.len]+y.val1;
		z.val2=x.val2*pov2[y.len]+y.val2;
		z.len=x.len+y.len;
		return z;
	}
	friend HASH operator -(const HASH &x,const HASH &y){
		HASH z;
		z.val1=x.val1-y.val1*pov1[x.len-y.len];
		z.val2=x.val2-y.val2*pov2[x.len-y.len];
		z.len=x.len-y.len;
		return z;
	}
	friend bool operator ==(const HASH &x,const HASH &y){
		if(x.len!=y.len)return false;
		if(x.val1!=y.val1)return false;
		if(x.val2!=y.val2)return false;
		return true;
	}
	friend bool operator !=(const HASH &x,const HASH &y){
		return !(x==y);
	}
}hs[110];
int main(){
	scanf("%s",s+1),memset(f,0x3f3f3f3f,sizeof(f)),n=strlen(s+1);
	pov1[0]=pov2[0]=1;
	for(int i=1;i<=n;i++)pov1[i]=pov1[i-1]*sd1,pov2[i]=pov2[i-1]*sd2;
	for(int i=1;i<=n;i++){
		hs[i]=hs[i-1]+HASH(s[i]);
		f[i][i][0]=1;
		f[i][i][1]=1+(i!=1);
	}
	for(int l=2;l<=n;l++){
		for(int i=1,j=i+l-1;j<=n;i++,j++){
			for(int k=i;k<j;k++)f[i][j][0]=min(f[i][j][0],f[i][k][0]+min(f[k+1][j][0],f[k+1][j][1])),f[i][j][1]=min(f[i][j][1],f[i][k][1]+min(f[k+1][j][0],f[k+1][j][1]));
			if(l&1)continue;
			int k=l>>1;
			if((hs[j]-hs[i+k-1])!=(hs[j-k]-hs[i-1]))continue;
			f[i][j][1]=min(f[i][j][1],min(f[i][i+k-1][0]+1,f[i][i+k-1][1])+1);
		}
	}
//	for(int l=1;l<=n;l++){for(int i=1,j=i+l-1;j<=n;i++,j++)printf("%d ",f[i][j]);puts("");}
	printf("%d\n",f[1][n][1]);
	return 0;
}
//xabababababab
//xabcabcxabcabc
```

一交，WA，还是$70\%$。

我费劲千辛万苦，终于找到另一组hack数据：

```xabcabcxabcabc

```

按照我之前的思路，会压出来这样的东西：

```xMabcRR```

因为我的程序是这样考虑的：

`` `x(MabcR)R` ``，根本没有考虑内部的情况

因此还要额外再加一维，表示该串内部有无`` `M` ``：

我们现在得到的是状态$f[i][j][0/1][0/1]$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
typedef unsigned long long ull;
char s[110];
int n,f[110][110][2][2];
ull sd1=998244353,sd2=666623333,pov1[2001000],pov2[2001000];
struct HASH{
	ull val1,val2;
	int len;
	HASH(){
		val1=val2=0ull;
		len=0;
	}
	HASH(char ip){
		val1=val2=ip;
		len=1;
	}
	friend HASH operator +(const HASH &x,const HASH &y){
		HASH z;
		z.val1=x.val1*pov1[y.len]+y.val1;
		z.val2=x.val2*pov2[y.len]+y.val2;
		z.len=x.len+y.len;
		return z;
	}
	friend HASH operator -(const HASH &x,const HASH &y){
		HASH z;
		z.val1=x.val1-y.val1*pov1[x.len-y.len];
		z.val2=x.val2-y.val2*pov2[x.len-y.len];
		z.len=x.len-y.len;
		return z;
	}
	friend bool operator ==(const HASH &x,const HASH &y){
		if(x.len!=y.len)return false;
		if(x.val1!=y.val1)return false;
		if(x.val2!=y.val2)return false;
		return true;
	}
	friend bool operator !=(const HASH &x,const HASH &y){
		return !(x==y);
	}
}hs[110];
int main(){
	scanf("%s",s+1),memset(f,0x3f3f3f3f,sizeof(f)),n=strlen(s+1);
	pov1[0]=pov2[0]=1;
	for(int i=1;i<=n;i++)pov1[i]=pov1[i-1]*sd1,pov2[i]=pov2[i-1]*sd2;
	for(int i=1;i<=n;i++){
		hs[i]=hs[i-1]+HASH(s[i]);
		f[i][i][0][0]=1;
		f[i][i][1][0]=1+(i!=1);
	}
	for(int l=2;l<=n;l++){
		for(int i=1,j=i+l-1;j<=n;i++,j++){
			for(int k=i;k<j;k++){
				f[i][j][0][0]=min(f[i][j][0][0],f[i][k][0][0]+f[k+1][j][0][0]);
				f[i][j][1][0]=min(f[i][j][1][0],f[i][k][1][0]+f[k+1][j][0][0]);
				f[i][j][0][1]=min(f[i][j][0][1],min(f[i][k][0][1],f[i][k][0][0])+min(min(f[k+1][j][0][0],f[k+1][j][0][1]),min(f[k+1][j][1][0],f[k+1][j][1][1])));
				f[i][j][1][1]=min(f[i][j][1][1],min(f[i][k][1][1],f[i][k][1][0])+min(min(f[k+1][j][0][0],f[k+1][j][0][1]),min(f[k+1][j][1][0],f[k+1][j][1][1])));
			}
			if(l&1)continue;
			int k=l>>1;
			if((hs[j]-hs[i+k-1])!=(hs[j-k]-hs[i-1]))continue;
			f[i][j][1][0]=min(f[i][j][1][0],min(f[i][i+k-1][0][0]+1,f[i][i+k-1][1][0])+1);
		}
	}
//	for(int l=1;l<=n;l++){for(int i=1,j=i+l-1;j<=n;i++,j++)printf("%d ",f[i][j]);puts("");}
	printf("%d\n",min(f[1][n][1][0],f[1][n][1][1]));
	return 0;
}
//xabababababab
//xabcabcxabcabc
```

# VI.[[HAOI2008]玩具取名](https://www.luogu.com.cn/problem/P4290)

状压一下。

我们令$f[i][j]$为：区间$[i, j]$的串，能转移到字母的状态（是个 `` `bitmask` `` ）

至于转移吗……劈开拼一起即可。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int m[4],n,tr[4][4],f[210][210];
int tran(char ip){
	if(ip=='W')return 0;
	if(ip=='I')return 1;
	if(ip=='N')return 2;
	if(ip=='G')return 3;
}
char s[210];
int main(){
	for(int i=0;i<4;i++)scanf("%d",&m[i]);
	for(int i=0;i<4;i++)for(int j=0;j<m[i];j++)scanf("%s",s),tr[tran(s[0])][tran(s[1])]|=(1<<i);
	scanf("%s",s+1),n=strlen(s+1);
	for(int i=1;i<=n;i++)f[i][i]=(1<<tran(s[i]));
	for(int l=2;l<=n;l++)for(int i=1,j=i+l-1;j<=n;i++,j++)for(int k=i;k<j;k++)for(int a=0;a<4;a++)for(int b=0;b<4;b++){
		if(!(f[i][k]&(1<<a)))continue;
		if(!(f[k+1][j]&(1<<b)))continue;
		f[i][j]|=tr[a][b];
	}
	if(f[1][n]&(1<<0))putchar('W');
	if(f[1][n]&(1<<1))putchar('I');
	if(f[1][n]&(1<<2))putchar('N');
	if(f[1][n]&(1<<3))putchar('G');
	if(!f[1][n])puts("The name is wrong!");
	return 0;
}
```

# VII.[[SDOI2009]Bill的挑战](https://www.luogu.com.cn/problem/P2167)

第一眼看上去不会做。第二眼发现$n\leq 15$直觉状压。第三眼算算复杂度发现OK，然后就没问题了。

我们设$f[i][j]$表示：

当前DP到了第$i$位，

所有串的匹配成功的状态是$j$，

的方案数。

通过预处理一个状压数组$mat[i][j]$表示第$i$位填入字符$j$的匹配结果，我们可以在复杂度$O(TAlen2^n)$范围内跑过。其中$T$是数据组数，$A$是字符集大小（$26$），$len$是串长，$n$是串数。

这是正解，只是毒瘤出题人卡长，不得不吸个臭氧才卡过。

代码：

``` cpp
#pragma GCC optimize(3)
#include<bits/stdc++.h>
using namespace std;
const int mod=1000003;
int T,n,m,S,f[100][1<<15],mat[100][26],MAXN,res;
char s[15][100];
int main(){
	scanf("%d",&T);
	while(T--){
		scanf("%d%d",&n,&m),MAXN=1<<n,res=0,memset(f,0,sizeof(f)),memset(mat,0,sizeof(mat));
		for(register int i=0;i<n;i++)scanf("%s",s[i]+1);
		S=strlen(s[0]+1);
		for(register int i=1;i<=S;i++)for(register int j=0;j<26;j++)for(register int k=0;k<n;k++)if(s[k][i]=='?'||s[k][i]==j+'a')mat[i][j]|=1<<k;
		f[0][MAXN-1]=1;
		for(register int i=0;i<S;i++)for(register int j=0;j<MAXN;j++)for(register int k=0;k<26;k++)(f[i+1][j&mat[i+1][k]]+=f[i][j])%=mod;
		for(register int i=0;i<MAXN;i++)if(__builtin_popcount(i)==m)(res+=f[S][i])%=mod;
		printf("%d\n",res);
	}
	return 0;
}
```

# VIII.[CF149D Coloring Brackets](https://www.luogu.com.cn/problem/CF149D)

考虑设$f[i][j][k=0/1/2][l=0/1/2]$表示：将区间$[i, j]$里的东西染色，左端染上颜色$k$，右端染上颜色$l$（$0$为红，$1$为蓝，$2$不染）的方案数。

因为这个$n$是$700$，$n^3$似乎过不了，考虑$n^2$的区间DP。

我们首先关于每个括号找出它匹配的位置。然后，约定只有合法的子串（连续的）的DP值是有效的，不合法的子串的DP值都为$0$。

当我们要求出$[i, j]$的DP值时，

1. 如果在位置$[i,j]$上的括号本身就是匹配的，直接从$[i+1,j-1]$转移过来；

2. 否则，既然这个子串是合法的，那唯一的构成方式就是拼接（例如```()()```）。直接从某个位置断开（比如说从右边界的匹配位置那边断开）拼一起即可。

复杂度为$O((C+1)^4*n^2)$，其中$C$是颜色数（本题中为$2$）。

代码:

``` cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int mat[710],n,f[710][710][3][3],res;
char s[710];
stack<int>stk;
int main(){
	scanf("%s",s+1),n=strlen(s+1);
	for(int i=1;i<=n;i++){
		if(s[i]=='(')stk.push(i);
		else mat[stk.top()]=i,mat[i]=stk.top(),stk.pop();
	}
	for(int i=1;i<n;i++)if(mat[i]==i+1)f[i][i+1][0][2]=f[i][i+1][2][0]=f[i][i+1][1][2]=f[i][i+1][2][1]=1;
	for(int l=4;l<=n;l+=2)for(int i=1,j=i+l-1;j<=n;i++,j++){
		if(s[i]!='('||s[j]!=')')continue;
		if(mat[i]==j){
			for(int a=0;a<3;a++)for(int b=0;b<3;b++){
				if(a==b)continue;
				if(a!=2&&b!=2)continue;
				for(int c=0;c<3;c++)for(int d=0;d<3;d++){
					if(a!=2&&c!=2&&a==c)continue;
					if(b!=2&&d!=2&&b==d)continue;
					(f[i][j][a][b]+=f[i+1][j-1][c][d])%=mod;
				}
			}
		}else{
			int k=mat[j];
			for(int a=0;a<3;a++)for(int b=0;b<3;b++)for(int c=0;c<3;c++)for(int d=0;d<3;d++){
				if(b!=2&&c!=2&&b==c)continue;
				f[i][j][a][d]=(1ll*f[i][k-1][a][b]*f[k][j][c][d]+f[i][j][a][d])%mod;
			}		
		}
	}
	for(int i=0;i<3;i++)for(int j=0;j<3;j++)(res+=f[1][n][i][j])%=mod;
	printf("%d\n",res);
	return 0;
} 
```

# IX.[[AHOI2018初中组]球球的排列](https://www.luogu.com.cn/problem/P4448)

~~论DP的百种用法之一~~

因为DP必须有一种全面的状态，但是这道题……似乎排列等等问题都不是DP擅长处理的地方。

首先分析性质。我们发现，这种不能放在一起的关系**具有传递性**。因为如果$xy=a^2, xz=b^2$，那么$yz=\dfrac{(xy)(yz)}{x^2}=\dfrac{a^2b^2}{x^2}=\Big(\dfrac{ab}{x}\Big)^2$。

具有传递性的话，我们就会发现，所有不能放在一起的位置，构成了多个**团（完全图）**。

我们就想着把每个团里的所有球都染上同一种颜色，则相同颜色的球不能紧贴在一起。

则我们现在将问题转换为：给你$n$个染了色的球，相同的球不能放一起，求排列数。

考虑将这些球按照颜色排序，这样便有了一个合理的（可以抽象出状态的）DP顺序。

我们设$f[i][j][k]$表示：

当前DP到第$i$位，

有两个球放在一起，它们的颜色相同，并且颜色与第$i$位的球**不同**，这样的对共有$j$个，

有两个球放在一起，它们的颜色相同，并且颜色与第$i$位的球**相同**，这样的对共有$k$个，

的方案数。

因为我们已经排过序，因此颜色相同的球必定紧贴。

### 1. 第 $i$ 位的球和第 $i-1$ 位的球颜色不同。

则DP状态的第三维（即$k$）必为$0$，因为不存在在它之前并且和它颜色相同的球。我们只需要枚举第二维$j$。

#### 1.1. 我们将这个球放在两个颜色不同的球之间。

我们枚举一个$k'$，表示**上一个球所代表的颜色中**颜色相同且紧贴的对共有$k'$个（$k'\in[0, j]$）。

则有`` `f[i][j][0]+=f[i-1][j-k'][k']*(i-j)` ` `，因为共有` ` `j-k'` ` `个相邻且相同且和上一个球的颜色不同的位置，并且共有` ` `i-j` ``个可以放球的位置。

#### 1.2. 我们将这个球放在两个颜色相同的球之间。

我们仍然枚举一个$k'$，意义相同。这时，$k'\in[0, j+1]$。

则有`` `f[i][j][0]+=f[i-1][j-k'+1][k']*(j+1)` ``。因为放入这个球后就拆开了一对球，因此原来共有 $j+1$ 对这样的球。

### 2. 第 $i$ 位的球和第 $i-1$ 位的球颜色相同。

我们需要枚举剩余两维$j, k$。并且，设在第$i$位之前，有$cnt$个和第$i$位相同的位置。

#### 2.1. 我们将这个球放在某个和这个球颜色相同的球旁边。

则共有$2*cnt-(k-1)$个这样的位置。

因此有`` `f[i][j][k]+=f[i-1][j][k-1]*(2*cnt-(k-1))` ``。

#### 2.2. 我们将这个球放在两个颜色相同的球之间。

同1.2，有`` `f[i][j][k]+=f[i-1][j+1][k]*(j+1)` ``。

#### 2.3. 我们将这个球放在两个颜色不同且与这个球颜色不同的球之间。

这次操作没有添加或删除任何对，并且共有$i-(2*cnt-k)-j$个位置。

因此有`` `f[i][j][k]+=f[i-1][j][k]*(i-(cnt*2-k)-j)` ``。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
typedef long long ll;
int n,num[310],dsu[310],f[2][310][310];
vector<int>v;
int find(int x){
	return dsu[x]==x?x:dsu[x]=find(dsu[x]);
}
void merge(int x,int y){
	x=find(x),y=find(y);
	if(x==y)return;
	dsu[x]=y;
}
bool che(ll ip){
	ll tmp=sqrt(ip)+0.5;
	return tmp*tmp==ip;
}
int main(){
	scanf("%d",&n);
	for(int i=1;i<=n;i++)scanf("%d",&num[i]),dsu[i]=i;
	for(int i=1;i<=n;i++)for(int j=1;j<=n;j++)if(che(1ll*num[i]*num[j]))merge(i,j);
	for(int i=1;i<=n;i++)dsu[i]=find(i);
	sort(dsu+1,dsu+n+1);
	f[0][0][0]=1;
	for(int i=1,cnt;i<=n;i++){
		memset(f[i&1],0,sizeof(f[i&1]));
		if(dsu[i]!=dsu[i-1]){
			cnt=0;
			for(int j=0;j<i;j++){
				for(int k=0;k<=j;k++)f[i&1][j][0]=(1ll*f[!(i&1)][j-k][k]*(i-j)+f[i&1][j][0])%mod;//if we put it between two balls of different colours
				for(int k=0;k<=j+1;k++)f[i&1][j][0]=(1ll*f[!(i&1)][j-k+1][k]*(j+1)+f[i&1][j][0])%mod;//if we put it between two balls of the same colours
			}
		}else{
			for(int j=0;j<i;j++){
				for(int k=1;k<=cnt;k++)f[i&1][j][k]=(1ll*f[!(i&1)][j][k-1]*(cnt*2-(k-1))+f[i&1][j][k])%mod;//if we put it next to a ball of the same colour
				for(int k=0;k<=cnt;k++)f[i&1][j][k]=(1ll*f[!(i&1)][j+1][k]*(j+1)+f[i&1][j][k])%mod;//if we put it between two balls of the same colours
				for(int k=0;k<=cnt;k++)f[i&1][j][k]=(1ll*f[!(i&1)][j][k]*(i-(cnt*2-k)-j)+f[i&1][j][k])%mod;//if we put it between two balls of different colours
			}
		}
		cnt++;
	}
	printf("%d\n",f[n&1][0][0]);
	return 0;
}
```

# X.[[SCOI2008]着色方案](https://www.luogu.com.cn/problem/P2476)

~~双倍经验，双倍快乐~~

~~可以看出这题直接是上一题的无编号版，直接套上一题的板子，乘上逆元的倒数直接水过，还轻轻松松完虐正解（五维暴力DP）~~

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
typedef long long ll;
int n,m,num[310],dsu[310],f[2][310][310],res,fac[310];
int ksm(int x,int y){
	int z=1;
	for(;y;x=(1ll*x*x)%mod,y>>=1)if(y&1)z=(1ll*x*z)%mod;
	return z;
}
int main(){
	scanf("%d",&m);
	for(int i=1,x;i<=m;i++){
		scanf("%d",&num[i]);
		for(int j=1;j<=num[i];j++)dsu[++n]=i;
	}
	fac[0]=1;
	for(int i=1;i<=n;i++)fac[i]=(1ll*fac[i-1]*i)%mod;
	f[0][0][0]=1;
	for(int i=1,cnt;i<=n;i++){
		memset(f[i&1],0,sizeof(f[i&1]));
		if(dsu[i]!=dsu[i-1]){
			cnt=0;
			for(int j=0;j<i;j++){
				for(int k=0;k<=j;k++)f[i&1][j][0]=(1ll*f[!(i&1)][j-k][k]*(i-j)+f[i&1][j][0])%mod;//if we put it between two balls of different colours
				for(int k=0;k<=j+1;k++)f[i&1][j][0]=(1ll*f[!(i&1)][j-k+1][k]*(j+1)+f[i&1][j][0])%mod;//if we put it between two balls of the same colours
			}
		}else{
			for(int j=0;j<i;j++){
				for(int k=1;k<=cnt;k++)f[i&1][j][k]=(1ll*f[!(i&1)][j][k-1]*(cnt*2-(k-1))+f[i&1][j][k])%mod;//if we put it next to a ball of the same colour
				for(int k=0;k<=cnt;k++)f[i&1][j][k]=(1ll*f[!(i&1)][j+1][k]*(j+1)+f[i&1][j][k])%mod;//if we put it between two balls of the same colours
				for(int k=0;k<=cnt;k++)f[i&1][j][k]=(1ll*f[!(i&1)][j][k]*(i-(cnt*2-k)-j)+f[i&1][j][k])%mod;//if we put it between two balls of different colours
			}
		}
		cnt++;
	}
	res=f[n&1][0][0];
	for(int i=1;i<=m;i++)res=(1ll*res*ksm(fac[num[i]],mod-2))%mod;
	printf("%d\n",res);
	return 0;
}
```

~~当然这么就水过一道题好像有点不好意思哈~~

因此额外再介绍一种方法，复杂度最劣应该是$O(n^3)$的，其中$n$是木块数量。

我们设$num[i]$表示第$i$种颜色有多少个，$sum[i]$为前$i$种颜色有多少个。

因为这题无编号，我们可以考虑简化一维：设$f[i][j]$表示：

前$i$种**颜色**（！！！）

涂了前$sum[i]$块，

并且有$j$对相邻同色对的方案数。

我们采取刷表法进行DP。

考虑由$f[i][j]$推出$f[i+1][?]$。

我们枚举一个$k\in\Big[1, num[i+1]\Big]$，表示我们将$num[i+1]$分成$k$段连续的同色木块。

我们再枚举一个$l\in\Big[0, \min(j, k)\Big]$，表示我们从这$k$段木块中，抽出$l$段木块塞在两段**颜色相同**但相邻的木块中。

首先，依据隔板法（~~小学奥数~~），共有$\large C_{num[i+1]-1}^{k-1}$中合法的分割方案；

一共有$sum[i]-j+1$个颜色不同的相邻位置，因此这$j-l$段放入颜色相同的位置的木块共有$\large C_{sum[i]-j+1}^{j-l}$种放法。

一共有$j$个颜色相同的相邻位置，共有$C_j^l$种放法。

则总方案数为$\large C_{num[i+1]-1}^{k-1}*C_{sum[i]-j+1}^{j-l}*C_j^l*f[i][j]$。

等等，这一大坨是往哪里更新去的？

是往$f\Big[i+1\Big]\Big[j+num[i+1]-k-l\Big]$更新的。原本应该增加$num[i+1]-1$段相邻的，现在聚合成了$k$段，减少了$k-1$段；有$l$段放偏了，又减少了$l$段。

代码（~~压 行 带 师~~）：

``` cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int f[20][100],n,num[20],sum[20],C[100][100];
int main(){
	scanf("%d",&n);
	for(int i=1;i<=n;i++)scanf("%d",&num[i]),sum[i]=sum[i-1]+num[i];
	for(int i=0;i<=sum[n];i++)C[i][0]=1;
	for(int i=1;i<=sum[n];i++)for(int j=1;j<=i;j++)C[i][j]=(C[i-1][j-1]+C[i-1][j])%mod;
	f[1][num[1]-1]=1;
	for(int i=1;i<n;i++)for(int j=0;j<sum[i];j++)for(int k=1;k<=num[i+1];k++)for(int l=0;l<=min(k,j);l++)f[i+1][j-k+num[i+1]-l]=(1ll*f[i][j]*C[num[i+1]-1][k-1]%mod*C[sum[i]-j+1][k-l]%mod*C[j][l]%mod+f[i+1][j-k+num[i+1]-l])%mod;
	printf("%d\n",f[n][0]);
	return 0;
}
```

# XI.[[SHOI2007]书柜的尺寸](https://www.luogu.com.cn/problem/P2160)

**排序**是各类DP题中只要出现了**物品**这个意象后的常客。

我们首先将书按照高度**递减**排序。这样，一个书柜的高度，就是第一本被放进来的书的高度。

设$f[i][j][k]$表示：DP到第$i$本书，第一层书架的长度为$j$，第二层书架的长度为$k$时，整个书柜的最小高度。设$sum[i]$表示所有书厚度的前缀和。

我们枚举这本书到底是放入第一层、第二层还是第三层（第三层长度为$sum[i]-j-k$）。

转移分几种情况：

1. 当$j=0$，即第一层为空时，应该加上$h[i]$。

2. 当$k=0$，应该加上$h[i]$。

3. 当$j+k=sum[i]$，应该加上$h[i]$。

答案就是枚举$f[n][?][?]$统计答案即可。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int f[2][2110][2110],n,sum[110];
typedef long long ll;
ll res=0x3f3f3f3f3f3f3f3f;
pair<int,int>p[100];
bool cmp(pair<int,int>x,pair<int,int>y){
	return x.first>y.first;
}
int main(){
	scanf("%d",&n),memset(f,0x3f3f3f3f,sizeof(f));
	for(int i=1;i<=n;i++)scanf("%d%d",&p[i].first,&p[i].second);
	sort(p+1,p+n+1,cmp);
	for(int i=1;i<=n;i++)sum[i]=sum[i-1]+p[i].second;
	f[0][0][0]=0;
	for(int i=0;i<n;i++){
		memset(f[!(i&1)],0x3f3f3f3f,sizeof(f[!(i&1)]));
		for(int j=0;j<=sum[i];j++)for(int k=0;j+k<=sum[i];k++){
			f[!(i&1)][j+p[i+1].second][k]=min(f[!(i&1)][j+p[i+1].second][k],f[i&1][j][k]+p[i+1].first*(!j));
			f[!(i&1)][j][k+p[i+1].second]=min(f[!(i&1)][j][k+p[i+1].second],f[i&1][j][k]+p[i+1].first*(!k));
			f[!(i&1)][j][k]=min(f[!(i&1)][j][k],f[i&1][j][k]+p[i+1].first*(!(sum[i]-j-k)));
		}
	}
	for(int i=1;i<sum[n];i++)for(int j=1;i+j<sum[n];j++)res=min(res,1ll*max(max(i,j),sum[n]-i-j)*f[n&1][i][j]);
	printf("%d\n",res);
	return 0;
}
```

# XII.[任务安排](https://www.luogu.com.cn/problem/P2365)

斜率优化真$\color{black}\colorbox{black}{XX}$有意思！！

设$t[i]$表示原题中的$t_i$的前缀和，$c[i]$表示原题中$f_i$的前缀和，$m$表示启动时间$s$。

思路1：$n^3$DP：

设$f[i][j]$表示：前$i$个位置，分成$j$组，的最快时间。

则有$f[i][j]=\min\limits_{k=0}^{i-1}\{f[k][j-1]+(t[i]+m*j)*(c[i]-c[k])\}$。

思路2：$n^2$DP：

观察到我们每在第$i$个点前多分出一组，则在$i$后面所有东西的时间都会向后拖$m$时刻，共计造成$m*(c[n]-c[i])$点费用，

因此我们可以设$f[i]$表示前$i$个位置的最短时间，

则有$f[i]=\min\limits_{j=0}^{i-1}\{f[j]+m*(c[n]-c[j])+t[i]*(c[i]-c[j])\}$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,f[10010],t[10010],c[10010];
int main(){
	scanf("%d%d",&n,&m),memset(f,0x3f3f3f3f,sizeof(f)),f[0]=0;
	for(int i=1;i<=n;i++)scanf("%d%d",&t[i],&c[i]),t[i]+=t[i-1],c[i]+=c[i-1];
	for(int i=1;i<=n;i++)for(int j=0;j<i;j++)f[i]=min(f[i],f[j]+m*(c[n]-c[j])+t[i]*(c[i]-c[j]));
	printf("%d\n",f[n]);
	return 0;
}
```

思路3：考虑斜率优化。

设$j<k<i$，且$j$比$k$更优。

则有

$f[j]+m*(c[n]-c[j])+t[i]*(c[i]-c[j])<f[k]+m*(c[n]-c[k])+t[i]*(c[i]-c[k])$

拆括号

$f[j]+m*c[n]-m*c[j]+t[i]*c[i]-t[i]*c[j]<f[k]+m*c[n]-m*c[k]+t[i]*c[i]-t[i]*c[k]$

消元

$f[j]-m*c[j]-t[i]*c[j]<f[k]-m*c[k]-t[i]*c[k]$

移项并合并

$f[j]-f[k]-(m+t[i])*(c[j]-c[k])<0$

再移

$f[j]-f[k]<(m+t[i])*(c[j]-c[k])$

注意因为$j<k$，且$c$是前缀和，则$c[j]<c[k]$。不等式两边除以负数，应该换方向。

最终得到

$\dfrac{f[j]-f[k]}{c[j]-c[k]}>m+t[i]$

左边的东西仅与$j$和$k$有关；右边的东西是单调的（$t$也是前缀和）；

因此就可以斜率优化辣。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,t[10100],c[10100],f[10100],q[10100],l,r;
int main(){
	scanf("%d%d",&n,&m);
	for(int i=1;i<=n;i++)scanf("%d%d",&t[i],&c[i]),t[i]+=t[i-1],c[i]+=c[i-1];
	for(int i=1;i<=n;i++){
		while(r-l&&(f[q[l]]-f[q[l+1]])>=(c[q[l]]-c[q[l+1]])*(m+t[i]))l++;
		f[i]=f[q[l]]+m*(c[n]-c[q[l]])+t[i]*(c[i]-c[q[l]]);
		while(r-l&&(f[q[r-1]]-f[q[r]])*(c[q[r]]-c[i])>=(f[q[r]]-f[i])*(c[q[r-1]]-c[q[r]]))r--;
		q[++r]=i;
	}
	printf("%d\n",f[n]);
	return 0;
}
```

# XII.[[SDOI2012]任务安排](https://www.luogu.com.cn/problem/P5785)

同上一题一样，不过，这题的$t_i$可能有负数，这就意味着前缀和不再是单调增的！

我们不能再像前一题一样用单调队列维护了——但是因为队尾的单调性仍然存在，我们仍然可以维护上凸包。这就启发我们使用单调栈来维护斜率，并且在单调栈中二分。

我们不妨想一想，如果这个$c$也有可能是负数怎么办？

$c$是负数就意味着不再具有一个明确的凸壳——我们在两边同除时不知道$c[j]-c[k]$是正是负。因此，我们可以采用平衡树来支持插入斜率和查询，复杂度$O(n\log n)$。（该方法纯属口胡，请勿当真）

本题代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int n,m,t[300100],c[300100],f[300100],s[300100],tp;
signed main(){
	scanf("%lld%lld",&n,&m);
	for(int i=1;i<=n;i++)scanf("%lld%lld",&t[i],&c[i]),t[i]+=t[i-1],c[i]+=c[i-1];
	for(int i=1;i<=n;i++){
		int L=0,R=tp;
		while(L<R){
			int mid=(L+R)>>1;
			if((f[s[mid]]-f[s[mid+1]])>=(c[s[mid]]-c[s[mid+1]])*(m+t[i]))L=mid+1;
			else R=mid;
		}
		f[i]=f[s[L]]+m*(c[n]-c[s[L]])+t[i]*(c[i]-c[s[L]]);
		while(tp&&(f[s[tp-1]]-f[s[tp]])*(c[s[tp]]-c[i])>=(f[s[tp]]-f[i])*(c[s[tp-1]]-c[s[tp]]))tp--;
		s[++tp]=i;
	}
	printf("%lld\n",f[n]);
	return 0;
}
```

# XIII.[[SDOI2016]征途](https://www.luogu.com.cn/problem/P4072)

这题已经在我的任务列表里吃了大半年的灰了……（去年7月加进来的，到现在已经8个月了）

开始推式子。

我们设第$i$天的路程是$l_i$，

则我们的目的是最小化

$s^2=\sum\limits_{i=1}^m\dfrac{(\overline{l}-l_i)^2}{m}$

代入平均值的定义

$s^2=\dfrac{\sum\limits_{i=1}^m\bigg(\tfrac{\sum\limits_{j=1}^ml_j}{m}-l_i\bigg)^2}{m}$

暴力展开平方项

$s^2=\dfrac{\sum\limits_{i=1}^m\bigg(\dfrac{\sum\limits_{j=1}^ml_j}{m}\bigg)^2-2*l_i*\dfrac{\sum\limits_{j=1}^ml_j}{m}+l_i^2}{m}$

分离$\Sigma$

$s^2=\dfrac{m\bigg(\dfrac{\sum\limits_{j=1}^ml_j}{m}\bigg)^2-2*\sum\limits_{i=1}^ml_i*\dfrac{\sum\limits_{j=1}^ml_j}{m}+\sum\limits_{i=1}^ml_i^2}{m}$

稍作整合

$s^2=\dfrac{\dfrac{(\sum\limits_{j=1}^ml_j)^2}{m}-2*\dfrac{(\sum\limits_{j=1}^ml_j)^2}{m}+\sum\limits_{i=1}^ml_i^2}{m}$

合并

$s^2=\dfrac{-\dfrac{(\sum\limits_{j=1}^ml_j)^2}{m}+\sum\limits_{i=1}^ml_i^2}{m}$

乘以$m^2$

$s^2m^2=-(\sum\limits_{j=1}^ml_j)^2+m\sum\limits_{i=1}^ml_i^2$

右边的等式中，左边是定值（等于总路程的平方）；右边则要我们最小化$\sum\limits_{i=1}^ml_i^2$。

设$f[i][j]$表示：前$i$天内分成了$j$段的最小平方和。再设$s_i$表示路程的前缀和。

则有$f[i][j]=\min\limits_{k=0}^{i-1}\{f[k][j-1]+(s_i-s_k)^2\}$

可以$n^2m$的进行暴力DP，能拿到$60\%$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,s[3010],f[3010][3010];
int main(){
	scanf("%d%d",&n,&m),memset(f,0x3f3f3f3f,sizeof(f));
	for(int i=1;i<=n;i++)scanf("%d",&s[i]),s[i]+=s[i-1];
	f[0][0]=0;
	for(int i=1;i<=n;i++)for(int j=1;j<=min(i,m);j++)for(int k=0;k<i;k++)f[i][j]=min(f[i][j],f[k][j-1]+(s[i]-s[k])*(s[i]-s[k]));
	printf("%d\n",m*f[n][m]-s[n]*s[n]);
	return 0;
} 
```

我们尝试按段数DP，而不是按天数DP。即，在$f[i][j]$中，优先枚举$j$。

在枚举$j$后，我们就可以暂时忽略$j$这一维了。

我们有$f[i]=\min\limits_{j=0}^{i-1}\{F[j]+(s_i-s_j)^2\}$。其中，这个$F[j]$是上一轮DP时的$f$值，即原本的$f[i][j-1]$（注意这个$j$和上面递推式里面的枚举的$j$不是同一个$j$）

假设$j<k<i$，且$j$比$k$优，

则有

$F[j]+(s_i-s_j)^2<F[k]+(s_i-s_k)^2$

暴力展开

$F[j]+s_i^2-s_is_j+s_j^2<F[k]+s_i^2-s_is_k+s_k^2$

合并同类项

$F[j]-s_is_j+s_j^2<F[k]-s_is_k+s_k^2$

移项

$F[j]-F[k]+s_j^2-s_k^2<s_is_j-s_is_k$

提一下

$F[j]-F[k]+s_j^2-s_k^2<s_i(s_j-s_k)$

除过去（注意$s_j-s_k$是负的！！！）

$\dfrac{F[j]-F[k]+s_j^2-s_k^2}{s_j-s_k}>s_i$

左边的东西与$i$无关；右边的东西单调增；

那不就可以了吗！！！

维护下凸壳，直接斜率优化硬套，完事。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,s[3010],f[3010][3010],q[3010],l,r;
int main(){
	scanf("%d%d",&n,&m),memset(f,0x3f3f3f3f,sizeof(f));
	for(int i=1;i<=n;i++)scanf("%d",&s[i]),s[i]+=s[i-1];
	f[0][0]=0;
	for(int j=1;j<=m;j++){
		l=r=0;
		for(int i=1;i<=n;i++){
			while(r-l&&f[q[l]][j-1]-f[q[l+1]][j-1]+s[q[l]]*s[q[l]]-s[q[l+1]]*s[q[l+1]]>=2*s[i]*(s[q[l]]-s[q[l+1]]))l++;
			f[i][j]=f[q[l]][j-1]+(s[i]-s[q[l]])*(s[i]-s[q[l]]);
			while(r-l&&(f[q[r-1]][j-1]-f[q[r]][j-1]+s[q[r-1]]*s[q[r-1]]-s[q[r]]*s[q[r]])*(s[q[r]]-s[i])>=(f[q[r]][j-1]-f[i][j-1]+s[q[r]]*s[q[r]]-s[i]*s[i])*(s[q[r-1]]-s[q[r]]))r--;
			q[++r]=i; 
		}
	}
	printf("%d\n",m*f[n][m]-s[n]*s[n]);
	return 0;
} 
```

# XIV.[[SDOI2013]保护出题人](https://www.luogu.com.cn/problem/P3299)

这题好像不算DP……~~但是涉及到斜率和凸包的题都是好题~~

因为这题要求是确保没有任何一个姜丝能活着走到门口，

所以设血量的前缀和为$s$，每两只姜丝间距离为$m$，

则对于 $\forall i$ ，

都应有$ans_i=\max\limits_{j=0}^{i-1}\{\dfrac{s_i-s_j}{x_i+(i-j-1)*m}\}$

其中，分母是第 $j+1$ 只姜丝距离门的距离，分子是第$i$到第$j+1$姜丝的总血量。

这样便能拿到$50\%$！！

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int n,m,s[100100];
double res,ans;
signed main(){
	scanf("%lld%lld",&n,&m);
	for(int i=1,x;i<=n;i++){
		scanf("%lld%lld",&s[i],&x),s[i]+=s[i-1],res=0;
		for(int j=0;j<i;j++)res=max(res,1.0*(s[i]-s[j])/(x+(i-j-1)*m));
		ans+=res;
	}
	printf("%.0lf\n",ans);
	return 0;
}
```

我们将这个东西变成斜率的形式：

$ans_i=\max\limits_{j=0}^{i-1}\{\dfrac{\{s_i\}-\{s_j\}}{\{x_i+im\}-\{m(j+1)\}}\}$

可以将其看作是$\Big(s_i, x_i+im\Big)$与$\Big(s_j, m(j+1)\Big)$的斜率。

即

$ans_i=\max\limits_{j=0}^{i-1}\{\operatorname{slope}\{\Big(s_i, x_i+im\Big), \Big(s_j, m(j+1)\Big)\}\}$

前者我们没法管它；但是后者，我们是可以维护下凸壳的（因为对于不同的$i$，后面的东西是相同的）。用单调栈维护并二分查找出斜率的最大值（实际上对于这种单峰函数应该写三分来着的……但是如果三分分的那两个点都在一起那不就是二分吗），并统计答案即可。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
#define pii pair<int,int>
#define x first
#define y second
#define mp make_pair 
int n,m,s[100100],tp;
double res,ans;
double slope(pii u,pii v){//ask for the slope from u to v
	return 1.0*(v.y-u.y)/(v.x-u.x);
}
pii stk[100100];
signed main(){
	scanf("%lld%lld",&n,&m),stk[0]=mp(m,0);
	for(int i=1,x;i<=n;i++){
		scanf("%lld%lld",&s[i],&x),s[i]+=s[i-1];
		int l=0,r=tp,qwq=0;
		pii tmp=mp(x+i*m,s[i]);
		while(l<=r){
			int mid=(l+r)>>1;
			if(slope(stk[mid],tmp)<slope(stk[mid-1],tmp))r=mid-1;
			else qwq=mid,l=mid+1;
		}
		res=slope(stk[qwq],tmp);
		tmp=mp((i+1)*m,s[i]);
		while(tp&&slope(stk[tp-1],tmp)>=slope(stk[tp],tmp))tp--;
		stk[++tp]=tmp;
		ans+=res;
	}
	printf("%.0lf\n",ans);
	return 0;
}
```

# XV.[[JSOI2009]火星藏宝图](https://www.luogu.com.cn/problem/P4056)

一个非常显然的结论：在最优方案中，路径上的任意两个点所构成的矩形内部一定不存在其它点。不然的化，在这个其它的点多停留一下一定不会更差。

因为$a^2+b^2<(a+b)^2$。

~~但是，就算想到这个，我也得不出什么好的转移方式~~

考虑将所有岛屿按照行优先，如果行相同就按列优先进行排序。这样，对于任何一个岛$i$，所有编号小于$i$的且列比它小的岛都是可转移的。

而在所有列相同的岛中，行最大的那个一定是最优的。

因此我们可以针对每行维护一个列数最大的点（类似于桶），每次只需要遍历这些桶进行转移即可。

复杂度$O(nm)$，卡卡就卡过去了。

代码：

``` cpp
#pragma GCC optimize(3)
#include<bits/stdc++.h>
using namespace std;
int n,m,tri[1010],f[200100];
struct node{
	int x,y,v;
	friend bool operator <(const node &x,const node &y){
		if(x.x!=y.x)return x.x<y.x;
		return x.y<y.y;
	}
}is[200100];
inline void read(int &x){
	x=0;
	char c=getchar();
	while(c>'9'||c<'0')c=getchar();
	while(c>='0'&&c<='9')x=(x<<3)+(x<<1)+(c^48),c=getchar();
}
inline void print(int x){
	if(x<0)putchar('-'),x=-x;
	if(x<=9)putchar('0'+x);
	else print(x/10),putchar('0'+x%10);
}
int main(){
	read(n),read(m);
	for(register int i=1;i<=n;i++)read(is[i].x),read(is[i].y),read(is[i].v);
	sort(is+1,is+n+1);
	tri[1]=1;
	f[1]=is[1].v;
	for(register int i=2;i<=n;i++){
		f[i]=f[1]-(is[i].x-1)*(is[i].x-1)-(is[i].y-1)*(is[i].y-1);
		for(register int j=1;j<=is[i].y;j++)if(tri[j])f[i]=max(f[i],f[tri[j]]-(is[i].x-is[tri[j]].x)*(is[i].x-is[tri[j]].x)-(is[i].y-is[tri[j]].y)*(is[i].y-is[tri[j]].y));
		f[i]+=is[i].v;
		tri[is[i].y]=i;
	}
	print(f[n]);
	return 0;
}
```

# XVI.[[HDU3507]Print Article](http://acm.hdu.edu.cn/showproblem.php?pid=3507)

没什么好说的，这题比任务安排还水，随便推推完事。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int n,m,s[500100],f[500100],q[500100],l,r;
signed main(){
	while(scanf("%lld%lld",&n,&m)!=EOF){
		for(int i=1;i<=n;i++){
			scanf("%lld",&s[i]);
			if(!s[i]){i--,n--;continue;}
			s[i]+=s[i-1];
		}
//		for(int i=1;i<=n;i++)printf("%d ",s[i]);puts("");
		l=r=0;
		for(int i=1;i<=n;i++){
			while(r-l&&f[q[l]]-f[q[l+1]]+s[q[l]]*s[q[l]]-s[q[l+1]]*s[q[l+1]]>=2*s[i]*(s[q[l]]-s[q[l+1]]))l++;
			f[i]=f[q[l]]+m+(s[i]-s[q[l]])*(s[i]-s[q[l]]);
			while(r-l&&(f[q[r-1]]-f[q[r]]+s[q[r-1]]*s[q[r-1]]-s[q[r]]*s[q[r]])*(s[q[r]]-s[i])>=(f[q[r]]-f[i]+s[q[r]]*s[q[r]]-s[i]*s[i])*(s[q[r-1]]-s[q[r]]))r--;
			q[++r]=i;
		}
		printf("%lld\n",f[n]);
	}
	return 0;
}
```

# XVII.[CF311B Cats Transport](https://www.luogu.com.cn/problem/CF311B)

推式子时间到~~~

我们首先对题目中的$d_i$做前缀和，求出每座山距离原点距离；

然后对于第$i$只猫，如果一个饲养员在$t_i-d_{h_i}$时刻以后出发就可以接到它；

注意，饲养员可以在负时刻就出发！！！~~我之前想多了以为只能在非负时刻出发而纳闷了好半天~~

我们设$t_i-d_{h_i}$为新的$t_i$，然后将所有的$t_i$排序。

然后开始DP：

设$f[i][j]$表示：前$i$只猫，派出$j$个人，的最优时间。再设$s_i$表示$t_i$的前缀和。

则有$f[i][j]=\min\limits_{k=0}^{i-1}\{f[k][j-1]+t_i*(i-k)-(s_i-s_k)\}$

我们这样就可以写出$O(m^2p)$的代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int n,m,p,d[100100],t[100100],s[100100],f[100100][110],qwq=0x3f3f3f3f3f3f3f3f;
signed main(){
	scanf("%lld%lld%lld",&n,&m,&p),memset(f,0x3f3f3f3f,sizeof(f));
	for(int i=2;i<=n;i++)scanf("%lld",&d[i]),d[i]+=d[i-1];
//	for(int i=1;i<=n;i++)printf("%lld ",d[i]);puts("");
	for(int i=1,x,y;i<=m;i++)scanf("%lld%lld",&x,&y),t[i]=y-d[x];
//	printf("%lld\n",res);
//	for(int i=1;i<=m;i++)printf("%lld ",t[i]);puts("");
	sort(t+1,t+m+1);
	for(int i=1;i<=m;i++)s[i]=s[i-1]+t[i];
//	for(int i=1;i<=m;i++)printf("%lld ",t[i]);puts("");
	f[0][0]=0;
	for(int j=1;j<=p;j++)for(int i=1;i<=m;i++)for(int k=0;k<i;k++)f[i][j]=min(f[i][j],f[k][j-1]+(i-k)*t[i]-(s[i]-s[k]));
	for(int i=1;i<=p;i++)qwq=min(qwq,f[m][i]);
	printf("%lld\n",qwq);
	return 0;
}
```

然后考虑斜率优化一下：

在$f[i][j]$中，我们按照列优先（先枚举$j$）的顺序进行DP；并且，设$f[i][j-1]$为$F[i]$。

设$j<k<i$（不是同一个$j$）。则如果$j$比$k$优，则有：

$F_j+t_i*(i-j)-(s_i-s_j)<F_k+t_i*(i-k)-(s_i-s_k)$

拆开

$F_j+i*t_i-j*t_i-s_i+s_j<F_k+i*t_i-k*t_i-s_i-s_k$

抵消

$F_j-j*t_i+s_j<F_k-k*t_i+s_k$

移项

$F_j-F_k+s_j-s_k<(j-k)*t_i$

除过去（注意$j-k$是负数）

$\dfrac{F_j-F_k+s_j-s_k}{j-k}>t_i$

右边的$t_i$是递增的（排过序了），因此可以采用单调队列维护斜率；然后维护一个下凸壳即可。复杂度$O(mp)$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int n,m,p,d[100100],t[100100],s[100100],f[100100][110],qwq=0x3f3f3f3f3f3f3f3f,l,r,q[100100];
signed main(){
	scanf("%lld%lld%lld",&n,&m,&p),memset(f,0x3f3f3f3f,sizeof(f));
	for(int i=2;i<=n;i++)scanf("%lld",&d[i]),d[i]+=d[i-1];
//	for(int i=1;i<=n;i++)printf("%lld ",d[i]);puts("");
	for(int i=1,x,y;i<=m;i++)scanf("%lld%lld",&x,&y),t[i]=y-d[x];
//	printf("%lld\n",res);
//	for(int i=1;i<=m;i++)printf("%lld ",t[i]);puts("");
	sort(t+1,t+m+1);
	for(int i=1;i<=m;i++)s[i]=s[i-1]+t[i];
//	for(int i=1;i<=m;i++)printf("%lld ",t[i]);puts("");
	f[0][0]=0;
	for(int j=1;j<=p;j++){
		l=r=0;
		for(int i=1;i<=m;i++){
			while(r-l&&(f[q[l]][j-1]-f[q[l+1]][j-1]+s[q[l]]-s[q[l+1]])>=(q[l]-q[l+1])*t[i])l++;
			f[i][j]=f[q[l]][j-1]+(i-q[l])*t[i]-(s[i]-s[q[l]]);
			while(r-l&&(f[q[r-1]][j-1]-f[q[r]][j-1]+s[q[r-1]]-s[q[r]])*(q[r]-i)>=(f[q[r]][j-1]-f[i][j-1]+s[q[r]]-s[i])*(q[r-1]-q[r]))r--;
			q[++r]=i;
		}
	}
	for(int i=1;i<=p;i++)qwq=min(qwq,f[m][i]);
	printf("%lld\n",qwq);
	return 0;
}
```

# XVIII.[[HAOI2010]软件安装](https://www.luogu.com.cn/problem/P2515)

不知道大家有没有做过这道题[[CTSC1997]选课](https://www.luogu.com.cn/problem/P2014)啊，反正我一看到这道题，就想起了它——都是树上背包。所以我便高高兴兴的敲了一发背包交上去。

然后呢？光荣的WA掉了。

为什么呢？

因为这道题和选课不一样；选课是你没有修完前一节课就不能修这节；但是本题是你装软件是可以随便装，想咋装就咋装的——只不过会不会起效就不知道了。因此，如果成环的话，只要整个环全装上就行了。

那么我们就SCC缩个点，在缩出来的树上背包一下就行了（实际上数据还可以加强成DAG的……）

代码：

``` 
#include<bits/stdc++.h>
using namespace std;
int n,m,w[110],v[110],f[110][510],g[510],res,col[110],val[110],sz[110],in[110],c;
namespace SCC{
	int tot,dfn[310],low[310],head[310],cnt;
	struct node{
		int to,next;
	}edge[200100];
	void ae(int u,int v){
	//	cout<<u<<" "<<v<<endl;
		edge[cnt].next=head[u],edge[cnt].to=v,head[u]=cnt++;
	}
	stack<int>stk;
	void Tarjan(int x){
		dfn[x]=low[x]=++tot,stk.push(x);
		for(int i=head[x];i!=-1;i=edge[i].next){
			if(!dfn[edge[i].to])Tarjan(edge[i].to),low[x]=min(low[x],low[edge[i].to]);
			if(!col[edge[i].to])low[x]=min(low[x],dfn[edge[i].to]);
		}
		if(low[x]<dfn[x])return;
		c++;
		while(stk.top()!=x)col[stk.top()]=c,val[c]+=v[stk.top()],sz[c]+=w[stk.top()],stk.pop();
		col[stk.top()]=c,val[c]+=v[stk.top()],sz[c]+=w[stk.top()],stk.pop();
	}
}
namespace DP{
	int head[110],cnt;
	struct node{
		int to,next;
	}edge[110];
	void ae(int u,int v){
//		printf("%d %d\n",u,v);
		edge[cnt].next=head[u],edge[cnt].to=v,head[u]=cnt++;
	}
	void dfs(int x){
		if(sz[x]<=m)f[x][sz[x]]=val[x];
		for(int i=head[x];i!=-1;i=edge[i].next){
			dfs(edge[i].to);
			for(int j=0;j<=m;j++)g[j]=f[x][j];
			for(int j=0;j<=m;j++)for(int k=0;j+k<=m;k++)if(f[x][j]!=-1&&f[edge[i].to][k]!=-1)g[j+k]=max(g[j+k],f[x][j]+f[edge[i].to][k]);
			for(int j=0;j<=m;j++)f[x][j]=g[j];
		}
	}	
}
int main(){
	scanf("%d%d",&n,&m),memset(f,-1,sizeof(f)),memset(SCC::head,-1,sizeof(SCC::head)),memset(DP::head,-1,sizeof(DP::head));
	for(int i=1;i<=n;i++)scanf("%d",&w[i]);
	for(int i=1;i<=n;i++)scanf("%d",&v[i]);
	for(int i=1,x;i<=n;i++){
		scanf("%d",&x);
		if(x)SCC::ae(x,i);
	}
	for(int i=1;i<=n;i++)if(!SCC::dfn[i])SCC::Tarjan(i);
//	for(int i=1;i<=c;i++)printf("%d %d\n",val[i],sz[i]);
	for(int i=1;i<=n;i++)for(int j=SCC::head[i];j!=-1;j=SCC::edge[j].next)if(col[i]!=col[SCC::edge[j].to])DP::ae(col[i],col[SCC::edge[j].to]),in[col[SCC::edge[j].to]]++;
	for(int i=1;i<=c;i++)if(!in[i])DP::ae(0,i);
	DP::dfs(0);
	for(int i=0;i<=m;i++)res=max(res,f[0][i]);
	printf("%d\n",res);
	return 0;
}
```

# IXX.[[HNOI2005]星际贸易](https://www.luogu.com.cn/problem/P2317)

第一问直接背包一下就行，是模板。

然后，因为题面中的一句话：

**……并使得只有一种获得最大贸易值的方法。**

因此我们可以直接根据各状态是从哪个前驱状态转移而来直接得出那些必须要访问的星球。

注意，你所规定的这条路径必须满足贸易值最大（不管合不合法（走不走的完），但贸易值必须最大），不然你就会像我一样死活看不懂第二组样例……

我们考虑DP。

设$f[i][j]$表示：当前在位置$i$，已经进行了所有的操作随时可以起飞，并且当前舰上还有$j$份燃料的最小代价。

思路1. 暴力DP：

我们有

$f[i][j]=\min\limits_{k=\max(i\text{之前距离}i\text{最近的那个必须访问的星球}, i\text{之前飞船不维修最远能到的那个星球})}^{i-1}\{\min\limits_{l=2}^{\min(r, j+2)}f[k][l]+(j-l+2)*p[i]+fx[i]\}$

其中，$p[i]$是$i$星球一份暗物质的费用，$fx[i]$是$i$位置修船的费用。

复杂度$O(n^4)$，可以拿到$55\%$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,r,l,a[2010],b[2010],dis[2010],p[2010],fx[2010],f[2010][4010],mp,mn=0x3f3f3f3f;
bool cho[2010];
int main(){
	scanf("%d%d%d%d",&n,&m,&r,&l),memset(f,0x80,sizeof(f)),r=min(r,2*n);
	if(r<2){puts("Poor Coke!");return 0;}
	for(int i=1;i<=n;i++)scanf("%d%d%d%d%d",&a[i],&b[i],&dis[i],&p[i],&fx[i]);
	for(int i=1;i<=n;i++)if(dis[i]-dis[i-1]>l){puts("Poor Coke!");return 0;}
	f[0][0]=0;
	for(int i=1;i<=n;i++){
		for(int j=0;j<a[i];j++)f[i][j]=f[i-1][j];
		for(int j=a[i];j<=m;j++)f[i][j]=max(f[i-1][j],f[i-1][j-a[i]]+b[i]);
	}
	for(int i=0;i<=m;i++)if(f[n][mp]<f[n][i])mp=i;
	for(int i=n,j=mp;i;i--){
		if(f[i][j]==f[i-1][j])continue;
		cho[i]=true,j-=a[i];
	}
//	for(int i=1;i<=n;i++)printf("%d ",cho[i]);puts("");
	mp=f[n][mp];
	memset(f,0x3f,sizeof(f));
	f[0][r]=0;
	for(int i=1;i<=n;i++)for(int j=0;j<=r;j++){
		for(int k=i-1;k>=0;k--){
			if(dis[i]-dis[k]>l)break;
			if(!p[i]){
				if(j>=2)f[i][j]=min(f[i][j],f[k][j+2]+fx[i]);
				else f[i][j]=0x3f3f3f3f;
			}
			else for(int l=2;l<=min(j+2,r);l++)f[i][j]=min(f[i][j],f[k][l]+(j-l+2)*p[i]+fx[i]);
			if(cho[k])break;
		}
//		printf("%d %d:%d\n",i,j,f[i][j]);
	}
	for(int i=0;i<=r;i++)mn=min(mn,f[n][i]);
	if(mn==0x3f3f3f3f){puts("Poor Coke!");return 0;}
	printf("%d %d\n",mp,mp-mn);
	return 0;
} 
```

思路2. 背包

因为在位置$i$买暗物质的操作实际上就是一个完全背包的效果，所以我们完全可以不枚举$l$，转而采用完全背包的形式在$O(n^3)$解决它。可以拿到$65\%$。

即：$f[i][j]=\min(f[k][j+2]+f[i], f[i][j-1]+p[i])$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,r,l,a[2010],b[2010],dis[2010],p[2010],fx[2010],f[2010][4010],mp,mn=0x3f3f3f3f;
bool cho[2010];
int main(){
	scanf("%d%d%d%d",&n,&m,&r,&l),memset(f,0x80,sizeof(f)),r=min(r,2*n);
	if(r<2){puts("Poor Coke!");return 0;}
	for(int i=1;i<=n;i++)scanf("%d%d%d%d%d",&a[i],&b[i],&dis[i],&p[i],&fx[i]);
	for(int i=1;i<=n;i++)if(dis[i]-dis[i-1]>l){puts("Poor Coke!");return 0;}
	f[0][0]=0;
	for(int i=1;i<=n;i++){
		for(int j=0;j<a[i];j++)f[i][j]=f[i-1][j];
		for(int j=a[i];j<=m;j++)f[i][j]=max(f[i-1][j],f[i-1][j-a[i]]+b[i]);
	}
	for(int i=0;i<=m;i++)if(f[n][mp]<f[n][i])mp=i;
	for(int i=n,j=mp;i;i--){
		if(f[i][j]==f[i-1][j])continue;
		cho[i]=true,j-=a[i];
	}
//	for(int i=1;i<=n;i++)printf("%d ",cho[i]);puts("");
	mp=f[n][mp];
	memset(f,0x3f,sizeof(f));
	f[0][r]=0;
	for(int i=1;i<=n;i++)for(int j=0;j<=r;j++){
		for(int k=i-1;k>=0;k--){
			if(dis[i]-dis[k]>l)break;
			f[i][j]=min(f[i][j],f[k][j+2]+fx[i]);
			if(cho[k])break;
		}
		if(p[i]&&j)f[i][j]=min(f[i][j],f[i][j-1]+p[i]);
//		printf("%d %d:%d\n",i,j,f[i][j]);
	}
	for(int i=0;i<=r;i++)mn=min(mn,f[n][i]);
	if(mn==0x3f3f3f3f){puts("Poor Coke!");return 0;}
	printf("%d %d\n",mp,mp-mn);
	return 0;
} 
```

思路3. 单调队列

因为$f[k][j+2]$这个东西随着$i$的增加，每个$i$都要枚举一下，因此可以采用单调队列来保存每个暗物质数量$j$可以转移的最优位置，并且按照距离及时弹出已经距离$i$太远的位置。复杂度$O(n^2)$，期望得分$100\%$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,r,l,a[2010],b[2010],dis[2010],p[2010],fx[2010],f[2010][4010],mp,mn=0x3f3f3f3f;
deque<int>q[2010];
bool cho[2010];
int main(){
	scanf("%d%d%d%d",&n,&m,&r,&l),memset(f,0x80,sizeof(f)),r=min(r,2*n);
	if(r<2){puts("Poor Coke!");return 0;}
	for(int i=1;i<=n;i++)scanf("%d%d%d%d%d",&a[i],&b[i],&dis[i],&p[i],&fx[i]);
	for(int i=1;i<=n;i++)if(dis[i]-dis[i-1]>l){puts("Poor Coke!");return 0;}
	f[0][0]=0;
	for(int i=1;i<=n;i++){
		for(int j=0;j<a[i];j++)f[i][j]=f[i-1][j];
		for(int j=a[i];j<=m;j++)f[i][j]=max(f[i-1][j],f[i-1][j-a[i]]+b[i]);
	}
	for(int i=0;i<=m;i++)if(f[n][mp]<f[n][i])mp=i;
	for(int i=n,j=mp;i;i--){
		if(f[i][j]==f[i-1][j])continue;
		cho[i]=true,j-=a[i];
	}
//	for(int i=1;i<=n;i++)printf("%d ",cho[i]);puts("");
	mp=f[n][mp];
	memset(f,0x3f,sizeof(f));
	f[0][r]=0;
	for(int i=1;i<=n;i++)for(int j=0;j<=r;j++){
		while(!q[j+2].empty()&&dis[i]-dis[q[j+2].front()]>l)q[j+2].pop_front();
		while(!q[j+2].empty()&&f[q[j+2].back()][j+2]>=f[i-1][j+2])q[j+2].pop_back();
		q[j+2].push_back(i-1);
		f[i][j]=min(f[i][j],f[q[j+2].front()][j+2]+fx[i]);
		if(p[i]&&j)f[i][j]=min(f[i][j],f[i][j-1]+p[i]);
		if(cho[i])q[j+2].clear();
//		printf("%d %d:%d\n",i,j,f[i][j]);
	}
	for(int i=0;i<=r;i++)mn=min(mn,f[n][i]);
	if(mn==0x3f3f3f3f){puts("Poor Coke!");return 0;}
	printf("%d %d\n",mp,mp-mn);
	return 0;
} 
```

# XX.[[SCOI2010]股票交易](https://www.luogu.com.cn/problem/P2569)

这题状态很好想：设$f[i][j]$表示：第$i$天，持有$j$支股票，的最大收益。

然后我就脑残了，想了个$O(n^2m^2)$的弱智初始DP，然后就WA掉惹。

实际上转移也挺简单的。设第$i$天买股票花$a_i$元，卖股票花$b_i$元，可以买$A_i$次，卖$B_i$次。

1. 从起始状态转移。即，如果有$j\leq A_i$，$f[i][j]=-j*a_i$。

2. 这一时刻不买。即，$f[i][j]=f[i-1][j]$。

3. 从$i-w-1$时刻买。即，$f[i][j]=\max\{f[i-w-1][l]+\text{买或卖的费用}\}$

然后1和2都是$nm$的；3套上单调队列也是$nm$的；总复杂度$O(nm)$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
int n,m,w,a[2010],b[2010],A[2010],B[2010];
ll f[2010][2010];
deque<int>q;
int main(){
	scanf("%d%d%d",&n,&m,&w),w++,memset(f,0x80,sizeof(f));
	for(int i=1;i<=n;i++)scanf("%d%d%d%d",&a[i],&b[i],&A[i],&B[i]);
	for(int i=1;i<=n;i++){
		for(int j=0;j<=m;j++){
			if(j<=A[i])f[i][j]=-j*a[i];
			f[i][j]=max(f[i][j],f[i-1][j]);	
		}
		if(i-w<=0)continue;
		int k=i-w;
		q.clear();
		for(int j=0;j<=m;j++){
			while(!q.empty()&&j-q.front()>A[i])q.pop_front();
			while(!q.empty()&&f[k][q.back()]-(j-q.back())*a[i]<=f[k][j])q.pop_back();
			q.push_back(j);
			f[i][j]=max(f[i][j],f[k][q.front()]-(j-q.front())*a[i]);
		}
		q.clear();
		for(int j=m;j>=0;j--){
			while(!q.empty()&&q.front()-j>B[i])q.pop_front();
			while(!q.empty()&&f[k][q.back()]+(q.back()-j)*b[i]<=f[k][j])q.pop_back();
			q.push_back(j);
			f[i][j]=max(f[i][j],f[k][q.front()]+(q.front()-j)*b[i]);
		}
	}
//	for(int i=1;i<=n;i++){for(int j=0;j<=m;j++)printf("%d ",f[i][j]);puts("");}
	printf("%lld\n",f[n][0]);
	return 0;
}
```

# XXI.[[HAOI2011]Problem c](https://www.luogu.com.cn/problem/P2523)

这题还是挺简单的~~~

关于每个位置$i$，在一种合法的方案 $a$ 中，必有

$(\sum\limits_{j=1}^n[a_j\geq i])\leq n-i+1$。

因为，每一个$a_j\geq i$都会占据$i$以后的某个位置，而$i$后面共有$n-i+1$个位置，因此这是充分必要条件。

因此我们发现，这个入座的顺序对答案并无影响——因为上面的判别式并没有对下标的操作。因此，对于那贿赂上司的$m$个人，我们只需要关注那个$q_i$即可。

我们设$num_i=(n-i+1)-\sum\limits_{j=1}^m[q_j\geq i]$，即先减去已经确定的部分。

然后，我们从后往前确认每个位置填什么。

设$f[i][j]$表示：

后$i$个位置，

还有$j$个$a$没有确定，

的方案数。

初始状态为$f[n+1][n-m]=1$，其它都为$0$。

则有$f[i][j-k]=\sum f[i+1][j]*C_{j}^{k}$。

状态的含义：我们从$i+1$位置剩下的$j$个人中，挑选出$k$个人令他们的$a_x=i$。因为顺序无关，所以是$C_j^k$。

至于这个$k$，$k\in\Big[0, \min\big(num_i-(n-m-j), j\big)\Big]$，因为在位置$i$前面已经填入的$(n-m-j)$个人也会对$i$造成影响。

我们最后要判断$f[1][0]$是否**被更新过**，而不是判断它是否非$0$，因为可能会出现答案是模数倍数的情况。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,T,mod,num[310],f[310][310],C[310][310];
bool upd[310][310];
int main(){
	scanf("%d",&T);
	while(T--){
		scanf("%d%d%d",&n,&m,&mod),memset(f,0,sizeof(f)),memset(upd,0,sizeof(upd)),memset(C,0,sizeof(C)),memset(num,0,sizeof(num));
		for(int i=1;i<=n;i++)num[i]=n-i+1;
		for(int i=0;i<=n;i++)C[i][0]=1;
		for(int i=1;i<=n;i++)for(int j=1;j<=i;j++)C[i][j]=(C[i-1][j-1]+C[i-1][j])%mod;
		for(int i=1,x,y;i<=m;i++){
			scanf("%d%d",&x,&y);
			for(int j=1;j<=y;j++)num[j]--;
		}
		f[n+1][n-m]=upd[n+1][n-m]=1;
		for(int i=n;i>=1;i--)for(int j=0;j<=n-m;j++){
			if(num[i]-((n-m)-j)<0)continue;
			for(int k=0;k<=min(num[i]-((n-m)-j),j);k++)upd[i][j-k]|=upd[i+1][j],f[i][j-k]=(1ll*f[i+1][j]*C[j][k]+f[i][j-k])%mod;
		}
		if(!upd[1][0])puts("NO");
		else printf("YES %d\n",f[1][0]);
	}
	return 0;
}
```

# XXII.[[ZJOI2010]排列计数](https://www.luogu.com.cn/problem/P2606)

按照这个关系可以建出一棵树出来；然后一组合法的排列就是这棵树的一组拓扑序。

设$f_x$表示以$x$为根的子树的拓扑序种数，$sz_x$表示以$x$为根的子树的大小，

则有$f_x=\prod\limits_{y\in Son_x}f_y*C_{(sz_x-1-\sum\limits_{z\in Son_x, z<y}sz_z)}^{sz_y}$

因为这个可以看作是把所有$x$的儿子所代表的拓扑序列归并到一起，所以直接$C$一下找出要填的位置即可。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,f[1001000],sz[1001000],fac[1001000],inv[1001000];
int ksm(int x,int y){
	int z=1;
	for(;y;x=(1ll*x*x)%m,y>>=1)if(y&1)z=(1ll*z*x)%m;
	return z;
}
int C(int x,int y){
	return 1ll*fac[x]*inv[y]%m*inv[x-y]%m;
}
int main(){
	scanf("%d%d",&n,&m),fac[0]=1;
	for(int i=1;i<=n;i++)fac[i]=(1ll*fac[i-1]*i)%m;
	inv[n]=ksm(fac[n],m-2);
	for(int i=n-1;i>=0;i--)inv[i]=1ll*inv[i+1]*(i+1)%m;
	for(int i=1;i<=n;i++)f[i]=1;
	for(int i=n;i>1;i--){
		sz[i]++;
		f[i>>1]=(1ll*f[i>>1]*C(sz[i>>1]+sz[i],sz[i])%m*f[i])%m;
		sz[i>>1]+=sz[i];
	} 
	printf("%d\n",f[1]);
	return 0;
}
```

# XXIII.[[HNOI2010]公交线路](https://www.luogu.com.cn/problem/P3204)

状压+矩乘的好题。

因为每$p$个位置中，每辆车就至少有$1$个位置，

所以我们可以状压一下。

设$f[i][j]$表示：

区间$[i, i+p-1]$内的车站现在的规划情况是$j$的方案数。

显然，必有$j$的第$p$位是$1$，且$j$共有$k$位是$1$（$j$的第$p$位对应着$i$）。

则$f[i][j]=\sum f[i-1][k]$，其中$k$能转移到$j$。

那什么样的$k$能转移到$j$呢？

我们将$k$左移一位（即增加了 $i+p-1$ 一位），然后删去第$p$位的数（即删去第 $i-1$ 位），得到了一个$k'$。

如果$k'$和$j$只相差**恰好$1$位**，那么$k$就可以转移到$j$（第$i-1$位的车刚好跑到了着相差的一位）。

然后发现，对于每个$f[i][j]$，它的祖先的$k$都是完全一致的；因此可以矩乘优化，建立转移矩阵$T[k][j]$，如果状态$k$可以转移到$j$，则$T[k][j]=1$，否则为$0$。

则复杂度为$S^3\log n$，其中$S$是合法状态数量（即符合$j$的第$p$位是$1$，且$j$共有$k$位是$1$的$j$的数量）。我们有$S=C_{p-1}^{k-1}$，当$p=10, k=5\ \operatorname{or}\ 6$时取得最大值，有$S=C_9^4\ \operatorname{or}\ C_9^5=126$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=30031;
int n,m,p,len,sta[150];
struct mat{
	int g[150][150];
	mat(){memset(g,0,sizeof(g));}
	friend mat operator *(const mat &x,const mat &y){
		mat z;
		for(int i=0;i<len;i++)for(int j=0;j<len;j++)for(int k=0;k<len;k++)(z.g[i][j]+=x.g[i][k]*y.g[k][j])%=mod;
		return z;
	}
}X,I;
bool che(int x,int y){
	x<<=1,x-=(1<<p);
	return __builtin_popcount(x^y)<=1;
}
void ksm(int y){
	for(;y;X=X*X,y>>=1)if(y&1)I=I*X;
}
int main(){
	scanf("%d%d%d",&n,&m,&p);
	for(int i=(1<<(p-1));i<(1<<p);i++)if(__builtin_popcount(i)==m)sta[len++]=i;
	for(int i=0;i<len;i++)I.g[i][i]=1;
	for(int i=0;i<len;i++)for(int j=0;j<len;j++)X.g[i][j]=che(sta[i],sta[j]);
	ksm(n-m);
	printf("%d\n",I.g[len-1][len-1]);
	return 0;
} 
```

# XXIV.[[HEOI2013]SAO](https://www.luogu.com.cn/problem/P4099)

这题思路和我们之前的XXII.[[ZJOI2010]排列计数](https://www.luogu.com.cn/problem/P2606)类似，也是一棵树的拓扑序数。但是，那题边只有一种情况（相当于这题的第三组$20\%$的特殊限制），这题情况就比较复杂。

我们先忽略边方向的限制，把整张图看作一棵无向树。不妨令$0$号节点为根。

发现只维护一维信息并不能准确地合并状态。此题的数据访问暗示我们采用$n^2$算法，因此考虑二维DP。

设$f[i][j]$表示：在以$i$为根的子树中，$i$的拓扑序为$j$的方案数。则答案为$\sum f[0][i]$。

我们考虑将$x$同它的某个儿子$y$合并。设它们的**当前**大小分别为$sz_x$和$sz_y$。

假设我们现在要合并$f[x][i]$和$f[y][j](i\leq sz_x, j\leq sz_y)$。我们枚举一个$k$，表示最终合并后，有$k$个位于$y$子树内的点排在了$x$前面。

1. $y$应该放在$x$前面。

这时，必有$k\geq j$，因为那$k$个排在$y$前面的点都必定放在$x$前面。

则这次枚举贡献给了$f[x][i+k]$。

那么具体贡献了多少呢？

首先一定有$f[x][i]$和$f[y][j]$。

然后，前$i+k-1$个位置中，有$k$个位置是来自$y$的，有$C_{i+k-1}^k$。

后$sz_x+sz_y-i-k$个位置中，有$sz_x-i$个位置是来自$x$的，有$C_{sz_x+sz_y-i-k}^{sz_x-i}$。

然后最后的贡献就是这四个东西的乘积。

2. $y$应该放在$x$后面。

唯一有区别的是$k$的枚举范围变成$k<j$。

复杂度$O(n^3)$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int T,n,f[1010][1010],head[1010],cnt,sz[1010],C[1010][1010],res,g[1010];
struct node{
	int to,next,val;
}edge[2010];
void ae(int u,int v,int w){
	edge[cnt].next=head[u],edge[cnt].to=v,edge[cnt].val= w,head[u]=cnt++;
	edge[cnt].next=head[v],edge[cnt].to=u,edge[cnt].val=-w,head[v]=cnt++;
}
void dfs(int x,int fa){
	sz[x]=1,f[x][1]=1;
	for(int e=head[x],y;e!=-1;e=edge[e].next){
		if((y=edge[e].to)==fa)continue;
		dfs(y,x);
		for(int i=1;i<=sz[x]+sz[y];i++)g[i]=0;
		if(edge[e].val==-1)for(int i=1;i<=sz[x];i++)for(int j=1;j<=sz[y];j++)for(int k=j;k<=sz[y];k++)g[i+k]=(1ll*f[y][j]*C[i+k-1][k]%mod*f[x][i]%mod*C[sz[x]+sz[y]-i-k][sz[x]-i]%mod+g[i+k])%mod;
		if(edge[e].val== 1)for(int i=1;i<=sz[x];i++)for(int j=1;j<=sz[y];j++)for(int k=0;k<     j;k++)g[i+k]=(1ll*f[y][j]*C[i+k-1][k]%mod*f[x][i]%mod*C[sz[x]+sz[y]-i-k][sz[x]-i]%mod+g[i+k])%mod;
		for(int i=1;i<=sz[x]+sz[y];i++)f[x][i]=g[i];
		sz[x]+=sz[y];
	}
}
int gt(){
	char c=getchar();
	while(c!='>'&&c!='<')c=getchar();
	return c=='>'?1:-1;
}
int main(){
	scanf("%d",&T);
	while(T--){
		scanf("%d",&n),memset(head,-1,sizeof(head)),memset(f,0,sizeof(f)),cnt=0;
		for(int i=0;i<=n;i++)C[i][0]=1;
		for(int i=1;i<=n;i++)for(int j=1;j<=i;j++)C[i][j]=(C[i-1][j-1]+C[i-1][j])%mod;
		for(int i=1;i<n;i++){
			int x,y,z;
			scanf("%d",&x);
			z=gt();
			scanf("%d",&y);
			ae(x,y,z);
		}
		dfs(0,-1),res=0;
		for(int i=1;i<=n;i++)(res+=f[0][i])%=mod;
		printf("%d\n",res);
	}
	return 0;
}
```

考虑优化。

我们看到这四个东西：

$f[x][i]*f[y][j]*C_{i+k-1}^k*C_{sz_x+sz_y-i-k}^{sz_x-i}$

发现，只有$f[y][j]$一个是与$j$有关的！

于是，我们可以改变枚举顺序，枚举$k$，然后直接用$f[y]$的前缀和就可以了。

因为少了一重循环，复杂度$O(n^2)$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int T,n,f[1010][1010],head[1010],cnt,sz[1010],C[1010][1010],res,g[1010],s[1010][1010];
struct node{
	int to,next,val;
}edge[2010];
void ae(int u,int v,int w){
	edge[cnt].next=head[u],edge[cnt].to=v,edge[cnt].val= w,head[u]=cnt++;
	edge[cnt].next=head[v],edge[cnt].to=u,edge[cnt].val=-w,head[v]=cnt++;
}
void dfs(int x,int fa){
	sz[x]=1,f[x][1]=1;
	for(int e=head[x],y;e!=-1;e=edge[e].next){
		if((y=edge[e].to)==fa)continue;
		dfs(y,x);
		for(int i=1;i<=sz[x]+sz[y];i++)g[i]=0;
		if(edge[e].val==-1)for(int i=1;i<=sz[x];i++)for(int k=1;k<=sz[y];k++)g[i+k]=(1ll*s[y][k]*C[i+k-1][k]%mod*f[x][i]%mod*C[sz[x]+sz[y]-i-k][sz[x]-i]%mod+g[i+k])%mod;
		if(edge[e].val== 1)for(int i=1;i<=sz[x];i++)for(int k=0;k<=sz[y];k++)g[i+k]=(1ll*(s[y][sz[y]]-s[y][k]+mod)%mod*C[i+k-1][k]%mod*f[x][i]%mod*C[sz[x]+sz[y]-i-k][sz[x]-i]%mod+g[i+k])%mod;
		for(int i=1;i<=sz[x]+sz[y];i++)f[x][i]=g[i];
		sz[x]+=sz[y];
	}
	for(int i=1;i<=sz[x];i++)s[x][i]=(s[x][i-1]+f[x][i])%mod;
}
int gt(){
	char c=getchar();
	while(c!='>'&&c!='<')c=getchar();
	return c=='>'?1:-1;
}
int main(){
	scanf("%d",&T);
	while(T--){
		scanf("%d",&n),memset(head,-1,sizeof(head)),memset(f,0,sizeof(f)),cnt=0;
		for(int i=0;i<=n;i++)C[i][0]=1;
		for(int i=1;i<=n;i++)for(int j=1;j<=i;j++)C[i][j]=(C[i-1][j-1]+C[i-1][j])%mod;
		for(int i=1;i<n;i++){
			int x,y,z;
			scanf("%d",&x);
			z=gt();
			scanf("%d",&y);
			ae(x,y,z);
		}
		dfs(0,-1),res=0;
		for(int i=1;i<=n;i++)(res+=f[0][i])%=mod;
		printf("%d\n",res);
	}
	return 0;
}
```

# XXV.[[CQOI2017]老C的键盘](https://www.luogu.com.cn/problem/P3757)

和前一题 完 全 一 致。

那就不讲了，双倍经验水过。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int n,f[1010][1010],head[1010],cnt,sz[1010],C[1010][1010],res,g[1010],s[1010][1010];
struct node{
	int to,next,val;
}edge[2010];
void ae(int u,int v,int w){
//	printf("%d %d %d\n",u,v,w);
	edge[cnt].next=head[u],edge[cnt].to=v,edge[cnt].val=w,head[u]=cnt++;
}
void dfs(int x){
	sz[x]=1,f[x][1]=1;
	for(int e=head[x],y;e!=-1;e=edge[e].next){
		y=edge[e].to;
		dfs(y);
		for(int i=1;i<=sz[x]+sz[y];i++)g[i]=0;
		if(edge[e].val==-1)for(int i=1;i<=sz[x];i++)for(int k=1;k<=sz[y];k++)g[i+k]=(1ll*s[y][k]*C[i+k-1][k]%mod*f[x][i]%mod*C[sz[x]+sz[y]-i-k][sz[x]-i]%mod+g[i+k])%mod;
		if(edge[e].val== 1)for(int i=1;i<=sz[x];i++)for(int k=0;k<=sz[y];k++)g[i+k]=(1ll*(s[y][sz[y]]-s[y][k]+mod)%mod*C[i+k-1][k]%mod*f[x][i]%mod*C[sz[x]+sz[y]-i-k][sz[x]-i]%mod+g[i+k])%mod;
		for(int i=1;i<=sz[x]+sz[y];i++)f[x][i]=g[i];
		sz[x]+=sz[y];
	}
	for(int i=1;i<=sz[x];i++)s[x][i]=(s[x][i-1]+f[x][i])%mod;
}
char str[1010];
int main(){
	scanf("%d",&n),memset(head,-1,sizeof(head));
	for(int i=0;i<=n;i++)C[i][0]=1;
	for(int i=1;i<=n;i++)for(int j=1;j<=i;j++)C[i][j]=(C[i-1][j-1]+C[i-1][j])%mod;
	scanf("%s",str+2);
	for(int i=2;i<=n;i++)ae(i>>1,i,str[i]=='>'?1:-1);
	dfs(1);
	for(int i=1;i<=n;i++)(res+=f[1][i])%=mod;
	printf("%d\n",res);
	return 0;
}
```

# XXVI.[[FJOI2007]轮状病毒](https://www.luogu.com.cn/problem/P2144)

~~论此题的一百种不同解法~~

首先，这题是有通项公式的——

$f[i]=3f[i-1]-f[i-2]+2$，

或$f[i]=i^2-4*[i|2]$。

当然这并不是我们DP笔记的讨论内容。

可以观察到，答案相当于：

将$1$到$n$共$n$个物品分成一些相邻的组，每组选出一个点，求分组方案数。（注意$1$和$n$可以在一起）。

我们设$f[i]$表示不考虑$1$和$n$可以在一起的方案数。

则有

$f[i]=\sum\limits_{j=1}^i f[i-j]*j$

我们让$f[i]$中后$j$个数单独分一组，则剩下的是$f[i-j]$；这$j$个数选出一个点，$j$种选法。

现在我们强制$1$和$n$在一起；

方案数为

$num=\sum\limits_{i=2}^{n}f[n-i]*i*(i-1)$

我们选出$i$个节点放在两边，共有$i-1$种放法；

从中选出一个连到中间，共有$i$种选法；

剩下的部分是$f[n-i]$。

然后答案即为$num+f[n]$。

加上高精度，复杂度$O(n^3)$。

另外这个$f$是可以通过差分达到线性递推的（当然加上高精度还是$O(n^2)$）。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n;
struct Wint:vector<int>{
    Wint(int n=0)
    {
        push_back(n);
        check();
    }
    Wint& check(){
        while(!empty()&&!back())pop_back();
        if(empty())return *this;
        for(int i=1; i<size(); ++i)(*this)[i]+=(*this)[i-1]/10,(*this)[i-1]%=10;
        while(back()>=10)push_back(back()/10),(*this)[size()-2]%=10;
        return *this;
    }
}f[110],res;
Wint& operator+=(Wint &a,const Wint &b){
	if(a.size()<b.size())a.resize(b.size());
    for(int i=0; i!=b.size(); ++i)a[i]+=b[i];
    return a.check();
}
Wint operator+(Wint a,const Wint &b){
    return a+=b;
}
Wint& operator*=(Wint &a,const int &b){
	for(int i=0;i<a.size();i++)a[i]*=b;
	return a.check();
}
Wint operator*(Wint a,const int &b){
	return a*=b;
}
void print(Wint a){
	for(int i=a.size()-1;i>=0;i--)putchar(a[i]+'0');
}
int main(){
	scanf("%d",&n);
	f[0]=Wint(1),f[1]=Wint(1);
	for(int i=2;i<=n;i++)for(int j=1;j<=i;j++)f[i]+=f[i-j]*j;
	res=f[n];
	for(int i=2;i<=n;i++)res+=f[n-i]*(i*(i-1));
	print(res);
	return 0;
}
```

# XXVII.[[SHOI2012]随机树](https://www.luogu.com.cn/problem/P3830)

$q=1$：

考虑令$f_i$表示：一棵有$i$个叶节点的树，叶节点平均深度的期望值。

则$f_i=f_{i-1}+\dfrac{2}{i}$。

证明：

我们随便从$i-1$个叶子中选一个出来，展开它，

则这次展开期望能为叶子的深度和增加$2*(f_{i-1}+1)-f_{i-1}$。

但是还要重新取平均；

于是

$f_i=\dfrac{f_{i-1}*(i-1)+2*(f_{i-1}+1)-f_{i-1}}{i}$

化简就得到了

$f_i=f_{i-1}+\dfrac{2}{i}$

$q=2$：

考虑令$f[i][j]$表示：

一棵有$i$个叶节点的树，深度$\geq j$的概率。

显然，有$f[i][j]=\sum\limits_{k=1}^{i-1}\dfrac{f[k][j-1]+f[i-k][j-1]-f[k][j-1]*f[i-k][j-1]}{?}$

释义：我们枚举左子树中放进去$k$个子节点。则左/右节点至少有一个深度$\geq j-1$的状态都是合法的。但是，左右节点深度都$\geq j-1$的情况在两个中都被算进去了；因此需要减去这种可能。

这个分母上的$?$，就是出现这种左右子树$size$分配的可能性。

考虑这种可能性的大小。

我们设$g_i$表示构成一棵有$i$个叶节点的树的方案数。则有$g_i=(i-1)!$，因为每“扩展”一个点就相当于从$i$个叶子中选了一个叶子出来，有$i$种选法；则有$g_i=\prod\limits_{j=1}^{i-1}j=(i-1)!$。

显然，这种可能性应该等于$g_{k}*g_{i-k}*?$（这个$?$是一个新的$?$）。我们将两棵子树合并，首先两棵子树自己内部扩展的顺序已经被$g$决定了；但是合并的顺序可是可以随便指定的；合并顺序的种数等于$C_{i-2}^{k-1}$，因为$i$个叶节点就意味着$i-2$次合并（当前节点自己本身就占用一次合并），这$i-2$次合并选出$k-1$次合并在左子树上。

则可能性的大小为$g_{k}*g_{i-k}*C_{i-2}^{k-1}=(k-1)!*(i-k-1)!*\dfrac{(i-2)!}{(k-1)!*(i-2-k+1)!}=(i-2)!$

然后分母上的$?$就是$\dfrac{g_i}{(i-2)!}=\dfrac{(i-1)!}{(i-2)!}=(i-1)$。

于是我们现在有

$f[i][j]=\sum\limits_{k=1}^{i-1}\dfrac{f[k][j-1]+f[i-k][j-1]-f[k][j-1]*f[i-k][j-1]}{i-1}$

有一个式子：

$E(x)=\sum\limits_{i=1}^{\infty}P(i)$

其中$E(x)$表示$x$的期望，$P(i)$表示$i\leq x$的概率。

证明：

设$p(i)$表示$i=x$的概率，$P(i)$表示$i\leq x$的概率，

则$E(x)=\sum\limits_{i=1}^{\infty}p(i)*i$

而$P(i)=\sum\limits_{j=i}^{\infty}p(j)$

则

$\begin{aligned}\sum\limits_{i=1}^{\infty}P(i)&=\sum\limits_{i=1}^{\infty}\sum\limits_{j=i}^{\infty}p(j)\\&=\sum\limits_{i=1}^{\infty}p(i)*i\\&=E(x)\end{aligned}$

证毕。

依据此式，则答案为$\sum\limits_{i=1}^{n-1}f[n][i]$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,m;
namespace T1{
	double f[110];
	double work(){
		f[1]=0;
		for(int i=2;i<=n;i++)f[i]=f[i-1]+2.0/i;
		return f[n];
	}
}
namespace T2{
	double f[110][110];
	double work(){
		for(int i=1;i<=n;i++)f[i][0]=1;
		for(int i=2;i<=n;i++)for(int j=1;j<i;j++){
			for(int k=1;k<i;k++)f[i][j]+=f[i-k][j-1]+f[k][j-1]-f[i-k][j-1]*f[k][j-1];
			f[i][j]/=i-1;
		}
		double res=0;
		for(int i=1;i<n;i++)res+=f[n][i];
		return res;
	}
} 
int main(){
	scanf("%d%d",&m,&n);
	if(m==1)printf("%lf\n",T1::work());
	if(m==2)printf("%lf\n",T2::work());
	return 0;
}
```

# XXVIII.[[HAOI2006]数字序列](https://www.luogu.com.cn/problem/P2501)

第一问：

正难则反。我们考虑从这个序列中找出最多可以保留的数。

如果两个下标$i, j(i<j)$都是要保留的，那么保留的充要条件就是

$a_j-a_i\geq j-i$

因为$(i, j)$开区间中的其它数要保证仍然有可以修改到的位置。例如 `` `10 4 3 12` ` ` 这组数据中，` ` `10` ` `和` ` `12` ` `便不能同时选择，因为` ` `4` ` `和` ` `3` ``要有修改的位置。

上面式子调换一下，便是

$a_j-j\geq a_i-i$

设$a_i-i=b_i$，则

$b_j\geq b_i$便是充要条件。

当我们找出了完整的$b$数组后，发现$b$中的最长不降子序列便是可以保留的位置。

然后第一问答案就是$n-\text{b中LIS的长度}$。

第二问：

实际上就是让$b$中LIS的长度为$n$。

考虑在第一问中找出的一条LIS上修改（注意LIS很有可能不止一条）。

我们在LIS中找出相邻的两个下标$j, i(j<i)$

则一组合法的修改结果肯定是一个“台阶”形。

![](https://cdn.luogu.com.cn/upload/image_hosting/jt7ts2f7.png)

我们发现，对于一段“台阶”：

如果它向下的箭头比向上的箭头要多，那么台阶上移一定不会更劣。反之亦然。

比如上图最左端那级台阶，就是上移下移都可以；中间的台阶，向上移更优；右面的台阶，向下移最好。

这样我们就可以构思出一种移台阶的方法：

对于一段台阶，如果它向上最好，则一直向上移直到和右边的下一段台阶齐平。然后合并两段台阶，再对新生成的这段台阶进行类似的操作。这种操作一定不会使答案变差。

则全部移完后，我们发现原本一小段一小段的台阶，要么同左边合并了，要么同右边合并了，反正最后一定是左边与左端点有一段台阶，右边与右端点有一段台阶。我们可以枚举左右台阶间的断点取$\min$。

这样我们就可以DP了。设$f_i$表示以$i$结尾的LIS的长度，$g_i$表示将$[1, i]$中所有台阶全都移完，且$i$是某条LIS中的一个位置时的最小代价。显然，$g_i$能从所有$j<i, b_j<b_i, f_j=f_i-1$的$j$转移过来。如果令$b_0=-\infty, b_{n+1}=+\infty, f_0=0, f_{n+1}=\max\limits_{i=1}^{n}\{f_i\}+1$的话，则答案为$g_{n+1}$。

在极端数据下，这种暴力转移复杂度是$O(n^3)$的（枚举$i$是$O(n)$的，枚举$j$在极端数据下是$O(n)$的，枚举断点也是$O(n)$的）。但是，“数据随机”让这个算法的期望复杂度优化成了$O(n\log^2n)$，轻松通过。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
const int INF=1e6;
int n,a[50100],b[50100],f[50100],t[50100],lim,mx,g[50100],pre[50100],suf[50100];
vector<int>v;
void add(int x,int val){
	while(x<=lim)t[x]=max(t[x],val),x+=x&-x;
}
int ask(int x){
	int qwq=0;
	while(x)qwq=max(qwq,t[x]),x-=x&-x;
	return qwq;
}
vector<int>q[50100];
int main(){
	scanf("%d",&n);
	for(int i=1;i<=n;i++)scanf("%d",&a[i]);
	for(int i=1;i<=n;i++)b[i]=a[i]-i,v.push_back(b[i]);
	sort(v.begin(),v.end()),v.resize(unique(v.begin(),v.end())-v.begin()),lim=v.size();
	for(int i=1;i<=n;i++)b[i]=lower_bound(v.begin(),v.end(),b[i])-v.begin()+1;
	for(int i=1;i<=n;i++)f[i]=ask(b[i])+1,add(b[i],f[i]),mx=max(mx,f[i]);
	for(int i=1;i<=n;i++)b[i]=a[i]-i;
	printf("%d\n",n-mx);
	q[0].push_back(0);
	memset(g,0x3f3f3f3f,sizeof(g));
	b[0]=-INF;
	b[n+1]=INF;
	g[0]=0;
	f[n+1]=mx+1;
	for(int i=1;i<=n+1;i++){
		q[f[i]].push_back(i);
		for(auto j:q[f[i]-1]){
			if(b[j]>b[i])continue;
//			printf("%d %d:\n",j,i);
			pre[j]=suf[i]=0;
			for(int k=j+1;k<i;k++)pre[k]=pre[k-1]+abs(b[k]-b[j]);
			for(int k=i-1;k>j;k--)suf[k]=suf[k+1]+abs(b[k]-b[i]);
//			for(int k=j;k<i;k++)printf("%d ",pre[k]);puts("");
//			for(int k=j+1;k<=i;k++)printf("%d ",suf[k]);puts("");
			for(int k=j;k<i;k++)g[i]=min(g[i],g[j]+pre[k]+suf[k+1]);
		}		
	}
//	for(int i=0;i<=n+1;i++)printf("%9d ",f[i]);puts("");
//	for(int i=0;i<=n+1;i++)printf("%9d ",b[i]);puts("");
//	for(int i=0;i<=n+1;i++)printf("%9d ",g[i]);puts("");
	printf("%d\n",g[n+1]);
	return 0;
} 
```

# XXIX.[[SDOI2008]Sue的小球](https://www.luogu.com.cn/problem/P2466)

DP做多了，手感自然就出来了。

~~话说这题打着“小球”的名字题目中却是“彩蛋”是怎么回事~~

首先，这个下落速度$v$，尽管题面中说它可能为负数，但我们想一想，这可能吗？如果是负数答案就是正无穷（可以等着这个球一直向上飞），因此排除球速为负的可能。

如果是这样的话，那么，当我们经过一个球时，随手将它射爆明显是更好的行为。因此，无论何时，我们球已经被射下的位置一定是一个包含起始点$x_0$的区间。

我们将所有球按照位置在$x_0$左边还是右边压进两个`` `vector` ` `中（下标从$0$开始）。在左边的` ` `vector` ``（设为$v1$）中，我们按照$x$值从大到小排序并处理；在右边（设为$v2$），我们从小到大排序。同时，我们在$v1$和$v2$中都压入一个$x=x_0$的球，方便初始化。

我们设$f[i][j][0/1]$表示：当前进行到$v1$的第$i$位，$v2$的第$j$位，同时位于这个区间的左/右端点的情况。我们可以提前计算出所有小球初始$y$值的和，这样我们只需要最小化捡球过程中球下落的距离即可。

我们设$s[i][j]$表示：除了$v1$前$i$位和$v2$前$j$位外，其它球$1s$内下落的距离之和（这借鉴了XII.[任务安排](https://www.luogu.com.cn/problem/P2365)中**费用提前计算**的经典思想）。在实现中，这个可以直接通过前缀和做出。设$x1[i]$表示$v1$的$x$值，$x2[j]$表示$v2$的$x$值。

我们有

$f[i][j][0]=f[i-1][j][0]+\Big|x1[i-1]-x1[i]\Big|*(s[i-1][j])$

$f[i][j][1]=f[i][j-1][0]+\Big|x2[j-1]-x2[j]\Big|*(s[i][j-1])$

然后因为两边可以互相走，所以还有

$f[i][j][0]=f[i][j][1]+\Big|x2[j]-x1[i]\Big|*s[i][j]$

$f[i][j][1]=f[i][j][0]+\Big|x1[i]-x2[j]\Big|*s[i][j]$

两种转移取$\min$即可。

复杂度$O(n^2)$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,X,s1[1010],s2[1010],sy,f[1010][1010][2],sv;
struct node{
	int x,y,v;
	node(int a=0,int b=0,int c=0){x=a,y=b,v=c;}
}b[1010];
vector<node>v1,v2;
bool cmp1(const node &x,const node &y){
	return x.x<y.x;
}
bool cmp2(const node &x,const node &y){
	return x.x>y.x;
}
int main(){
	scanf("%d%d",&n,&X),memset(f,0x3f3f3f3f,sizeof(f));
	for(int i=1;i<=n;i++)scanf("%d",&b[i].x);
	for(int i=1;i<=n;i++)scanf("%d",&b[i].y),sy+=b[i].y;
	for(int i=1;i<=n;i++)scanf("%d",&b[i].v);
	for(int i=1;i<=n;i++){
		if(b[i].x<X)v1.push_back(b[i]);
		if(b[i].x>X)v2.push_back(b[i]);
	}
	v1.push_back(node(X,0,0)),v2.push_back(node(X,0,0));
	sort(v1.begin(),v1.end(),cmp2);
	sort(v2.begin(),v2.end(),cmp1);
	for(int i=1;i<v1.size();i++)s1[i]=s1[i-1]+v1[i].v;
	for(int i=1;i<v2.size();i++)s2[i]=s2[i-1]+v2[i].v;
//	for(int i=0;i<v1.size();i++)printf("%d %d %d\n",v1[i].x,v1[i].y,v1[i].v);puts("");
//	for(int i=0;i<v2.size();i++)printf("%d %d %d\n",v2[i].x,v2[i].y,v2[i].v);puts("");
	sv=s1[v1.size()-1]+s2[v2.size()-1];
	f[0][0][0]=f[0][0][1]=0;
	for(int i=0;i<v1.size();i++)for(int j=0;j<v2.size();j++){
		if(i)f[i][j][0]=f[i-1][j][0]+abs(v1[i].x-v1[i-1].x)*(sv-s1[i-1]-s2[j]);
		if(j)f[i][j][1]=f[i][j-1][1]+abs(v2[j].x-v2[j-1].x)*(sv-s1[i]-s2[j-1]);
		f[i][j][0]=min(f[i][j][0],f[i][j][1]+abs(v2[j].x-v1[i].x)*(sv-s1[i]-s2[j]));
		f[i][j][1]=min(f[i][j][1],f[i][j][0]+abs(v1[i].x-v2[j].x)*(sv-s1[i]-s2[j]));
	}
	double res=sy-min(f[v1.size()-1][v2.size()-1][0],f[v1.size()-1][v2.size()-1][1]);
	res/=1000;
	printf("%.3lf\n",res);
	return 0;
}
```

# XXX.[[SDOI2007]游戏](https://www.luogu.com.cn/problem/P2462)

~~论`` `STL` ``的百种用法~~

可以观察到可以接龙的对构成一张DAG。因此我们要找到DAG中最长路。这个随便DP就可以了。

关键是找到可以互相转移的位置。

$n^2$枚举非常危险，因为还有一个$26$判断的常数，没试，估计过不了。

我们必须寻找复杂度更低的算法。

发现一个串只与组成它的每个字符的数量有关。那么我们可以把这每个字符的数量压到一个`` `vector` ` `里面，然后用` ` `map<vector<int>,int>` ` `来找可以转移的位置。或者因为串长$\leq 100$，因此` ` `vector` ` `中每个数必定不超过$100$，然后可以化成一个` ` `string` ` `。当然，` ` `string` ``也可以哈希（虽然答案就不一定正确了）。

当然，无论怎么搞，都有一个$26$的常数（似乎哈希一下复杂度是$26n\log n$，而不哈希复杂度是$26^2\log n$）。但不管怎么说，能过。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
string s[10010];
map<vector<int>,int>m;
int S,n,f[10010],pre[10010],mp;
void print(int i){
	if(!i)return;
	print(pre[i]);
	cout<<s[i]<<endl;
}
int main(){
	n++;
	while(cin>>s[n])n++;
	sort(s+1,s+n);
	for(int i=1;i<n;i++){
		f[i]=1;
		vector<int>v;
		v.resize(26);
		for(auto j:s[i])v[j-'a']++;
		m[v]=i;
	}
	for(auto i:m){
		vector<int>v=i.first;
		for(int k=0;k<26;k++){
			v[k]++;
			if(m.find(v)!=m.end()){
				int j=m[v];
				if(f[j]<f[i.second]+1)f[j]=f[i.second]+1,pre[j]=i.second;
			}
			v[k]--;
		}
	}
	for(int i=1;i<n;i++)if(f[i]>f[mp])mp=i;
	printf("%d\n",f[mp]);
	print(mp);
	return 0;
}
```

# XXXI.[[CQOI2018]解锁屏幕](https://www.luogu.com.cn/problem/P4460)

$n\leq 20$一眼状压。

设$f[i][j]$表示：访问状态为$i$，当前在$j$点的方案数。

我们枚举一个$k$，表示下一个要去的地方；要判断$j$能不能转移到$k$，还要枚举$l$，判断$j, k, l$是否共线。判断共线是基础向量，一次点积+一次叉积带走。

这样复杂度$O(n^32^n)$，期望得分$30\%$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
#define pii pair<int,int>
#define mp make_pair
#define x first
#define y second
const int mod=1e8+7;
int n,f[1<<20][20],lim,res;
pii p[20];
pii operator-(const pii &u,const pii &v){
	return mp(u.x-v.x,u.y-v.y);
}
int operator*(const pii &u,const pii &v){
	return u.x*v.x+u.y*v.y;
}
int operator^(const pii &u,const pii &v){
	return u.x*v.y-u.y*v.x;
}
int main(){
	scanf("%d",&n),lim=1<<n;
	for(int i=0;i<n;i++)scanf("%d%d",&p[i].first,&p[i].second);
	for(int i=0;i<n;i++)f[1<<i][i]=1;
	for(int i=0;i<lim;i++)for(int j=0;j<n;j++){
		if(!(i&(1<<j)))continue;
//		printf("%d %d:\n",i,j);
		for(int k=0;k<n;k++){
			if(i&(1<<k))continue;
//			printf("%d:\n",k);
			bool ok=true;
			for(int l=0;l<n;l++){
				if(i&(1<<l))continue;
				if(k==l)continue;
				if(((p[k]-p[j])^(p[l]-p[j]))!=0)continue;
				if(((p[k]-p[l])*(p[j]-p[l]))>0)continue;
				ok=false;break;
			}
//			printf("%d\n",ok);
			(f[i|(1<<k)][k]+=f[i][j]*ok)%=mod;	
		}
	}
	for(int i=0;i<lim;i++)if(__builtin_popcount(i)>=4)for(int j=0;j<n;j++)(res+=f[i][j])%=mod;
	printf("%d\n",res);
	return 0;
}
```

考虑$O(n^3)$预处理出如果能从$j$转移到$k$需要选择的子集。这样子就可以$O(1)$在DP时判断（即判断该子集是否是$i$的子集）。复杂度$O(n^22^n)$。期望得分$100\%$。

另：本题卡常，请随手吸氧。

代码：

``` cpp
#pragma GCC optimize(3)
#include<bits/stdc++.h>
using namespace std;
#define pii pair<int,int>
#define mp make_pair
#define x first
#define y second
const int mod=1e8+7;
int n,f[1<<20][20],lim,res,blk[20][20];
pii p[20];
pii operator-(const pii &u,const pii &v){
	return mp(u.x-v.x,u.y-v.y);
}
int operator*(const pii &u,const pii &v){
	return u.x*v.x+u.y*v.y;
}
int operator^(const pii &u,const pii &v){
	return u.x*v.y-u.y*v.x;
}
int main(){
	scanf("%d",&n),lim=1<<n;
	for(int i=0;i<n;i++)scanf("%d%d",&p[i].first,&p[i].second);
	for(int i=0;i<n;i++)for(int j=0;j<n;j++){
		if(i==j)continue;
		for(int k=0;k<n;k++){
			if(i==k||j==k)continue;
			if(((p[j]-p[i])^(p[k]-p[i]))!=0)continue;
			if(((p[i]-p[k])*(p[j]-p[k]))>0)continue;
			blk[i][j]|=(1<<k);
		}
	}
	for(int i=0;i<n;i++)f[1<<i][i]=1;
	for(int i=0;i<lim;i++)for(int j=0;j<n;j++){
		if(!(i&(1<<j)))continue;
//		printf("%d %d:\n",i,j);
		for(int k=0;k<n;k++){
			if(i&(1<<k))continue;
			if((i&blk[j][k])!=blk[j][k])continue;
			(f[i|(1<<k)][k]+=f[i][j])%=mod;	
		}
	}
	for(int i=0;i<lim;i++)if(__builtin_popcount(i)>=4)for(int j=0;j<n;j++)(res+=f[i][j])%=mod;
	printf("%d\n",res);
	return 0;
}
```

# XXXII.[[HNOI2009]双递增序列](https://www.luogu.com.cn/problem/P4728)

~~某科学的消减维数~~

思路1. 暴力五维DP：

设$f[h][i][j][k][l]$表示：前$h$位中，$U$有$i$位，$V$有$j$位，$U$以$k$结尾，$V$以$l$结尾是否合法。

显然过不去。

思路2. 暴力四维DP：

发现必有$i+j=h$，因此我们可以消掉$i$或$j$。

则有设$f[i][j][k][l]$表示：前$i$位中，$U$有$j$位，$U$以$k$结尾，$V$以$l$结尾是否合法。

思路3. 暴力三维DP：

发现$U$和$V$中必有一个以位置$i$为结尾。那么我们可以令「序列1」表示以$i$为结尾的那个串，「序列2」表现另一个串。

设$f[i][j][k]$表示：前$i$位中，「序列1」有$j$位，「序列2」以$k$结尾是否合法。

思路4. 正解二维DP：

当$f$数组是一个`` `bool` ``数组时，便有优化的空间。

明显这个$k$越小越好。因此我们可以设$f[i][j]$表示：前$i$位中，「序列1」有$j$位，此时「序列2」的结尾最小为$f[i][j]$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,T,f[2010][2010],num[2010];
int main(){
	scanf("%d",&T);
	while(T--){
		scanf("%d",&n),num[0]=-1;
		for(int i=1;i<=n;i++)scanf("%d",&num[i]);
		for(int i=1;i<=n;i++)for(int j=1;j<=min(i,n>>1);j++)f[i][j]=0x3f3f3f3f;
//		for(int i=1;i<=n;i++){for(int j=1;j<=min(i,n>>1);j++)printf("%d ",f[i][j]);puts("");}
		for(int i=1;i<=n/2;i++){
			if(num[i]>num[i-1])f[i][i]=-1;
			else break;
		}
		for(int i=1;i<n;i++)for(int j=1;j<=min(i,n/2);j++){
			if(num[i+1]>num[i])f[i+1][j+1]=min(f[i+1][j+1],f[i][j]);
			if(num[i+1]>f[i][j])f[i+1][i+1-j]=min(f[i+1][i+1-j],num[i]);
		}
//		for(int i=1;i<=n;i++){for(int j=1;j<=min(i,n>>1);j++)printf("%d ",f[i][j]);puts("");}
		puts(f[n][n/2]!=0x3f3f3f3f?"Yes!":"No!");
	}
	return 0;
}
```

# XXXIII.[[HAOI2018]奇怪的背包](https://www.luogu.com.cn/problem/P4495)

神题。

1. 对于某个大小为$v$的物品，它所能表示出的位置的集合等于$\gcd(v,P)$所能表示的集合。

2. 对于某些大小为$v_1,\dots,v_k$的物品，位置集合为$\gcd\{v_1,\dots,v_k,P\}$。

因此考虑DP。

我们找出所有$P$的约数，存入`` `vector` ``。（这个个数的级别设为$L$，则$L$最大只到$768$。）设$P$的第$i$个约数为$p_i$。

则对于所有的$v_i$，我们找出$\gcd(P, v_i)$。设新的$v_i=\gcd(P, v_i)$。

对于每个$p_i$，统计它在$v_1, \dots, v_n$中出现了多少次，设为$s_i$。

我们设$f[i][j]$表示：在$P$前$i$个约数中，选择一些数，使得他们的$\gcd$等于$P$的第$j$个约数的方案数。

则有

$f[i][j]=f[i-1][j]+\Bigg(\small{\begin{cases}1(i=j)\\0(i\neq j)\end{cases}}+\sum\limits_{\gcd(p_k, p_i)=p_j}f[i-1][k]\Bigg)*(2^{s_i}-1)$

释义：

首先，答案是可以从前一位继承来的。

然后，因为对于每个$i$，选任何数量的$v_k=p_i$的$k$都是等价的，因此共有$2^{s_i}-1$中选法；

当$i=j$时，可以之前一个数也不选，就选$i$一个数，因此要加上$1$。

然后，因为$\gcd$具有结合律和交换律，所有$\gcd(p_k, p_i)=p_j$的状态也是可继承的。

则$f[n][j]$的状态是最终状态。

对于每个$w_i$，答案为$\sum\limits_{v_j|w_i}f[n][j]$。这个可以通过一个$L^2$的预处理求出$g[i]=\sum\limits_{v_j|v_i}f[n][j]$算出。

复杂度$O(\sqrt{P}+L^2\log L+q)$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int n,m,p,s[1001000],f[2][1001000],g[1001000],two[1001000];
vector<int>v; 
int main(){
	scanf("%d%d%d",&n,&m,&p);
	two[0]=1;
	for(int i=1;i<=n;i++)two[i]=(two[i-1]<<1)%mod;
	for(int i=0;i<=n;i++)two[i]=(two[i]-1+mod)%mod;
//	for(int i=0;i<=n;i++)printf("%d ",two[i]);puts("");
	for(int i=1;i*i<=p;i++){
		if(p%i)continue;
		v.push_back(i);
		if(i*i!=p)v.push_back(p/i);
	}
	sort(v.begin(),v.end());
//	for(auto i:v)printf("%d ",i);puts("");
	for(int i=1,x;i<=n;i++)scanf("%d",&x),x=__gcd(x,p),s[lower_bound(v.begin(),v.end(),x)-v.begin()]++;
//	for(int i=0;i<v.size();i++)printf("%d ",s[i]);puts("");puts("");
	for(int i=0;i<v.size();i++){
		for(int j=0;j<=i;j++)f[i&1][j]=0;
		f[i&1][i]=1;
		for(int j=0;j<i;j++){
			int gcd=__gcd(v[i],v[j]);
			gcd=lower_bound(v.begin(),v.end(),gcd)-v.begin();
			(f[i&1][gcd]+=f[!(i&1)][j])%=mod;
		}
		for(int j=0;j<=i;j++)f[i&1][j]=(1ll*f[i&1][j]*two[s[i]]+f[!(i&1)][j])%mod;
//		for(int j=0;j<=i;j++)printf("%d ",f[i&1][j]);puts("");
	}
	for(int i=0;i<v.size();i++)for(int j=0;j<=i;j++)if(!(v[i]%v[j]))(g[i]+=f[n&1][j])%=mod;
	for(int i=1,w;i<=m;i++)scanf("%d",&w),w=__gcd(w,p),printf("%d\n",g[lower_bound(v.begin(),v.end(),w)-v.begin()]);
	return 0;
} 
```

# XXXIV.[[SCOI2008]奖励关](https://www.luogu.com.cn/problem/P2473)

$n\leq 15$就是一眼状压。但这题难点不是状压，而是期望。

应该很容易就能想到，设$f[i][j]$表示前$i$次操作后，状态为$j$的期望收益。但这有个问题——我们不知道如果刷到一个负数收益应不应该选，因为我们不知道这个负数收益在后面会带给我们怎样的期望收益。

因为必须要直到后面的内容，所以考虑倒序DP：设$f[i][j]$表示前$i$次操作后状态为$j$，在后$K-i$次操作中的期望收益。这样期望就可以直接取$\max$了——对后面的影响已经确定。

对于$f[i][j]$，我们枚举一个$k$，表示刷到第$k$个物品。如果$k$不可以选，有 `` `f[i][j]+=f[i+1][j]` ` ` ；否则，即$k$可以选，有` ` `f[i][j]+=max(f[i+1][j],f[i+1][j|(1<<k)]+val[k])` ``。

这时期望就可以正常除以$n$了，因为刷到所有物品的概率是均等的。

复杂度$O(k^22^n)$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,lim,val[16],sta[16];
double f[110][1<<16];
int main(){
	scanf("%d%d",&m,&n),lim=(1<<n);
	for(int i=0,x;i<n;i++){
		scanf("%d",&val[i]);
		scanf("%d",&x);
		while(x)sta[i]|=(1<<(x-1)),scanf("%d",&x);
	}
	for(int i=m;i;i--)for(int j=0;j<lim;j++){
		for(int k=0;k<n;k++)if((j&sta[k])==sta[k])f[i][j]+=max(f[i+1][j],f[i+1][j|(1<<k)]+val[k]);else f[i][j]+=f[i+1][j];
		f[i][j]/=n;
	}
	printf("%lf\n",f[1][0]);
	return 0;
}
```

# XXXV.[[GDOI2014]拯救莫莉斯](https://www.luogu.com.cn/problem/P3888)

因为$nm\leq 50, m\leq n$，

所以$m$最大只会到$7$，可以状压。

考虑设$f[i][j][k]$表示：

在前$i-1$行已经填好的情况下，第$i-1$行状态为$j$，第$i$行状态为$k$的最小代价和最小数量（是个`` `std::pair` ``）。

转移时枚举$i-2$行的状态。复杂度$O(n2^{3m})$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
#define bp __builtin_popcount
#define pii pair<int,int>
#define x first
#define y second
#define mp make_pair
int n,m,c[100][100],lim,s[100][1<<8];
pii f[100][1<<8][1<<8],res=mp(0x3f3f3f3f,0x3f3f3f3f);
pii operator+(const pii &u,const pii &v){
	return mp(u.x+v.x,u.y+v.y);
}
bool che(int i,int j,int k){
	int jj=j;
	jj|=(j>>1)&(lim-1);
	jj|=(j<<1)&(lim-1);
	jj|=i;
	jj|=k;
	return jj==(lim-1);
}
int main(){
	scanf("%d%d",&n,&m),memset(f,0x3f3f3f3f,sizeof(f)),lim=(1<<m);
	for(int i=0;i<n;i++){
		for(int j=0;j<m;j++)scanf("%d",&c[i][j]);
		for(int j=0;j<lim;j++)for(int k=0;k<m;k++)if(j&(1<<k))s[i][j]+=c[i][k];
	}
	if(n==1){printf("%d %d\n",1,c[0][0]);return 0;}
	for(int i=0;i<lim;i++)for(int j=0;j<lim;j++)if(che(0,i,j))f[1][i][j]=make_pair(s[0][i]+s[1][j],bp(i)+bp(j));
	for(int i=2;i<n;i++)for(int j=0;j<lim;j++)for(int k=0;k<lim;k++)for(int l=0;l<lim;l++)if(che(l,j,k))f[i][j][k]=min(f[i][j][k],f[i-1][l][j]+mp(s[i][k],bp(k)));
	for(int i=0;i<lim;i++)for(int j=0;j<lim;j++)if(che(0,j,i))res=min(res,f[n-1][i][j]);
	printf("%d %d\n",res.y,res.x);
	return 0;
}
```

# XXXVI.[[BJOI2017]喷式水战改](https://www.luogu.com.cn/problem/P3991)

这题类似于毒瘤数据结构题，想起来非常简单，但是写起来……

平衡树是必须写的——这种毒瘤的维护肯定要写平衡树。

然后说一下怎么DP吧。在每个节点上维护$f[i][j]$，表示在以该节点为根的子树上，阶段$i$到阶段$j$的最大收益。

直接在`` `pushup` ``时维护即可。

主要是这个插入难，要分裂某个节点。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
#define lson t[x].ch[0]
#define rson t[x].ch[1] 
#define ROOT t[0].ch[1]
int n,cnt;
struct SPLAY{
	int num[4],tot,sz,fa,ch[2],f[4][4];
	SPLAY(int a=0,int b=0,int c=0,int d=0){
		num[0]=a,num[1]=b,num[2]=c,num[3]=a,tot=sz=d;
		fa=ch[0]=ch[1]=0;
		memset(f,0,sizeof(f));
		for(int i=0;i<4;i++)for(int j=i;j<4;j++)for(int k=i;k<=j;k++)f[i][j]=max(f[i][j],num[k]*tot);
	}
}t[200100];
void pushup(int x){
	if(!x)return;
	int g[4][4];
	memset(t[x].f,0,sizeof(t[x].f));
	t[x].sz=t[x].tot;
	for(int i=0;i<4;i++)for(int j=i;j<4;j++)for(int k=i;k<=j;k++)t[x].f[i][j]=max(t[x].f[i][j],t[x].num[k]*t[x].tot);
	if(lson){
		memset(g,0,sizeof(g));
		for(int i=0;i<4;i++)for(int j=i;j<4;j++)for(int k=i;k<=j;k++)g[i][j]=max(g[i][j],t[lson].f[i][k]+t[x].f[k][j]);
		for(int i=0;i<4;i++)for(int j=i;j<4;j++)t[x].f[i][j]=max(t[x].f[i][j],g[i][j]);
		t[x].sz+=t[lson].sz;
	}
	if(rson){
		memset(g,0,sizeof(g));
		for(int i=0;i<4;i++)for(int j=i;j<4;j++)for(int k=i;k<=j;k++)g[i][j]=max(g[i][j],t[x].f[i][k]+t[rson].f[k][j]);
		for(int i=0;i<4;i++)for(int j=i;j<4;j++)t[x].f[i][j]=max(t[x].f[i][j],g[i][j]);
		t[x].sz+=t[rson].sz;
	}
}
void connect(int x,int y,int dir){
	if(x)t[x].fa=y;
	t[y].ch[dir]=x;
}
int identify(int x){
	return t[t[x].fa].ch[1]==x;
}
void rotate(int x){
	int y=t[x].fa;
	int z=t[y].fa;
	int dirx=identify(x);
	int diry=identify(y);
	int b=t[x].ch[!dirx];
	connect(b,y,dirx);
	connect(y,x,!dirx);
	connect(x,z,diry);
	pushup(y),pushup(x);
}
void splay(int x,int y){
	y=t[y].fa;
	while(t[x].fa!=y){
		int fa=t[x].fa;
		if(t[fa].fa==y)rotate(x);
		else if(identify(fa)==identify(x))rotate(fa),rotate(x);
		else rotate(x),rotate(x);
	}
}
int findkth(int k){
	if(!k)return 0;
	int x=ROOT;
	while(true){
		if(t[lson].sz>=k)x=lson;
		else if(t[x].tot+t[lson].sz<k)k-=(t[x].tot+t[lson].sz),x=rson;
		else{splay(x,ROOT);return x;}
	}
}
void ins(SPLAY q,int pos){
	if(!ROOT){ROOT=++cnt,t[ROOT]=q;return;}
	if(!pos){
		int x=ROOT;
		while(lson)x=lson;
		splay(x,ROOT);
		++cnt;
		t[cnt]=q;
		connect(cnt,x,0);
		pushup(x);
	}else{
		int x=findkth(pos);
		int left=t[x].tot;
		t[x].tot=pos-t[lson].sz;
		left-=t[x].tot;
		++cnt;
		t[cnt]=q;
		connect(rson,cnt,1);
		connect(cnt,x,1);
		int y=cnt;
		if(left){
			++cnt;
			t[cnt]=SPLAY(t[x].num[0],t[x].num[1],t[x].num[2],left);
			connect(t[y].ch[1],cnt,1);
			connect(cnt,y,1);
			pushup(cnt);
		}
		pushup(y),pushup(x),splay(y,ROOT);
	}
}
void iterate(int x){
	if(lson)iterate(lson);
	for(int i=0;i<t[x].tot;i++)printf("(%lld,%lld,%lld)",t[x].num[0],t[x].num[1],t[x].num[2]);
	if(rson)iterate(rson);
}
signed main(){
	scanf("%lld",&n);
	for(int i=1,lans=0,a,b,c,d,e;i<=n;i++){
		scanf("%lld%lld%lld%lld%lld",&a,&b,&c,&d,&e);
		ins(SPLAY(b,c,d,e),a);
		printf("%lld\n",t[ROOT].f[0][3]-lans);
		lans=t[ROOT].f[0][3];
//		iterate(ROOT);puts("");
	}
	return 0;
}
```

# XXXVII.[[JXOI2012]奇怪的道路](https://www.luogu.com.cn/problem/P6239)

神题。

（为以示区别，题面中的$k$我们称作$p$）。

思路1.

观察到$k$很小，考虑状压。

设$f[i][j][k]$表示：

前$i$个位置的边已经全部连完了，位置$[i-p+1, i]$的状态压起来是$j$，并且连了$k$条边的方案数。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int f[50][1<<10][50],n,m,lim,p;
int ksm(int x,int y){
	int z=1;
	for(;y;x=(1ll*x*x)%mod,y>>=1)if(y&1)z=(1ll*z*x)%mod;
	return z;
}
int main(){
	scanf("%d%d%d",&n,&m,&p),lim=1<<p;
	f[0][0][0]=1;
	for(int i=0;i<n;i++)for(int j=0;j<min(1<<i,lim);j++)for(int k=0;k<=m;k++){
		if(!f[i][j][k])continue;
		for(int g=0;g<min(1<<(i+1),lim);g++){
			int diff=((g>>1)^j);
			if(__builtin_parity(diff)!=(g&1))continue;
			int cnt=__builtin_popcount(diff);
			for(int h=k+cnt;h<=m;h+=2)(f[i+1][g][h]+=1ll*f[i][j][k]*ksm(min(i,p),(h-k-cnt)>>1)%mod)%=mod;
		}
	}
//	for(int i=1;i<=n;i++)for(int j=0;j<min(1<<i,lim);j++)for(int k=0;k<=m;k++)printf("%d,%d,%d:%d\n",i,j,k,f[i][j][k]);
	printf("%d\n",f[n][0][m]);
	return 0;
}
```

一交，WA，$45\%$。

咋肥事？

因为这么连，会有重复计算的部分（因为边是无序的，同一组边集只不过因为**顺序**不同就会加不止一次）。

思路2.

为了凸显**顺序**，我们不得不考虑再增加一维。

设$f[i][j][k][l]$表示：

前$i$个位置的边已经全部连完了，连了$k$条边，位置$[i-p+1, i+1]$的状态压起来是$j$，并且位置$i+1$只与$[i-p+1, i-l]$里的点连了边的方案数。

显然，初始$f[1][0][0][0]=1$，答案是$f[n][m][0][0]$。

考虑如何转移（刷表法）。

1. 我们再连一条边$(i-l-1,i+1)$。

有$f[i][j+1][k\operatorname{xor}2^0\operatorname{xor}2^l][l]+=f[i][j][k][l]$。

2. 连接$(i-l-1,i+1)$之间的边已经全部连完，来到下一位。

有$f[i][j][k][l+1]+=f[i][j][k][l]$。

3. 当$l$枚举完成后，

如果有$k$的第$p$位为$0$，则可以转移到下一位，则有

$d[i+1][j][k<<1][\min(i, p)]+=f[i][j][k][0]$。

复杂度$O(nmp2^p)$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int n,m,p,f[40][40][1<<10][10],lim;
int main(){
	scanf("%d%d%d",&n,&m,&p),lim=(1<<(p+1));
	f[1][0][0][0]=1;
	for(int i=1;i<=n;i++)for(int j=0;j<=m;j++)for(int k=0;k<lim;k++){
		for(int l=min(i-1,p);l;l--){
			if(j<m)(f[i][j+1][k^(1<<l)^1][l]+=f[i][j][k][l])%=mod;
			(f[i][j][k][l-1]+=f[i][j][k][l])%=mod;	
		}
		if(!(k&(1<<p)))(f[i+1][j][k<<1][min(i,p)]+=f[i][j][k][0])%=mod;
	}
	printf("%d\n",f[n][m][0][0]);
	return 0;
}
```

# XXXVIII.[[CQOI2013]二进制A+B](https://www.luogu.com.cn/problem/P4574)

最后判无解试了很多次才判成功……主要是因为“$a, b, c\leq2^{30}$中有个$\leq$而不是$<$就很烦人。

思路很简单：设$f[i][j][k][l][0/1]$表示：

按位DP到第$i$位，

$a, b, c$中分别用了$j, k, l$个$1$，

并且进位的情况是$0/1$，

的最小方案。

转移之间枚举这一位$a, b$分别填$1$还是填$0$即可。

复杂度约是$O(\log^4)$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
const int lim=31;
int a,b,c,f[lim][lim][lim][lim][2],res=0x3f3f3f3f3f3f3f3f;
void read(int &x){
	int t;
	x=0;
	scanf("%lld",&t);
	for(int i=0;i<lim;i++)x+=((t>>i)&1);
}
void chmin(int &a,int b){
	a=min(a,b);
}
signed main(){
	read(a),read(b),read(c),memset(f,0x3f3f3f3f,sizeof(f));
//	printf("%d %d %d\n",a,b,c);
	f[0][0][1][1][0]=1;
	f[0][1][0][1][0]=1;
	f[0][1][1][0][1]=0;
	f[0][0][0][0][0]=0;
	for(int i=0;i<lim-1;i++)for(int j=0;j<=a;j++)for(int k=0;k<=b;k++)for(int l=0;l<=c;l++)for(int p=0;p<2&&j+p<=a;p++)for(int q=0;q<2&&k+q<=b;q++){
		chmin(f[i+1][j+p][k+q][l+((p+q)&1)][(p+q)>1],f[i][j][k][l][0]+(((p+q)&1)<<(i+1)));
		chmin(f[i+1][j+p][k+q][l+((p+q+1)&1)][(p+q)>0],f[i][j][k][l][1]+(((p+q+1)&1)<<(i+1)));
	}
//	for(int i=0;i<lim-1;i++)for(int j=0;j<=a;j++)for(int k=0;k<=b;k++)for(int l=0;l<=c;l++)for(int m=0;m<2;m++)printf("%d %d %d %d %d:%d\n",i,j,k,l,m,f[i][j][k][l][m]);
	for(int i=0;i<lim;i++)res=min(res,f[i][a][b][c][0]);
	printf("%lld\n",res>(0x7f7f7f7f)?-1:res);
	return 0;
}
```

# XL.[[IOI2005]Riv 河流](https://www.luogu.com.cn/problem/P3354)

新转移方式get~~~

我必须吐槽一下现在赞最多的那篇题解，虽然思路巧妙，但是明显没有“物尽其用”，对于各DP数组的真实含义也没有把握清楚。

一个naive的想法就是：设$f[i][j]$表示：在$i$的子树中，修了$j$个场子，的最小费用。

但是这样不是很好转移——子树传上来的信息不能直接合并，因为我们必须知道场子到底修哪了才能准确得出答案。

而我们又不可能在状态里面维护这么多场子——状压不了。

等等，我们为什么要从根记录子树，为什么不是从子树记录根？

我们设$f[x][j][k]$表示：

以$x$为根的子树中，修了$k$个堡。并且，强制在第$j$个点修个堡（$j$是$i$的祖先）。

这样，合并子树时就可以直接背包了——因为每个节点流到的堡确定了，代价自然就可以提前算出。

即：

$f[x][j][k]=\max\{f[x][j][l]+f[y][j][k-l]\}, \text{y is a son of x}$

每次将$x$的状态同$y$合并。

但这样就会出现一些问题——我们说要在$j$修个堡，但是这只是空头支票，没有算到$k$里面，当访问到$j$时，这个债是要还的！

因此对于$f[x][x][k]$，我们应该让$k$全体右移一位，即$f[x][x][k]=f[x][x][k-1]$，且$f[x][x][0]=\infty$（欠的一个堡还不回来，只能破产）。

还有，我们要计算$x$位置新产生的代价。这个代价要么$x$位置额外再修一个堡，要么就是到$j$的距离。因此我们有

$f[x][j][k]=\min\Big(f[x][j][k]+val_x*(dis_x-dis_k), f[x][x][k]\Big)$

则答案为$f[0][0][K+1]$（$0$号点有个免费的堡）。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,head[110],cnt,f[110][110][60],g[60],val[110],dis[110],anc[110],tp;
struct node{
	int to,next,val;
}edge[210];
void ae(int u,int v,int w){
	edge[cnt].next=head[u],edge[cnt].to=v,edge[cnt].val=w,head[u]=cnt++;
}
void dfs(int x){
	anc[++tp]=x;
	for(int i=head[x],y;i!=-1;i=edge[i].next){
		y=edge[i].to,dis[y]=dis[x]+edge[i].val,dfs(y);
		for(int j=1;j<=tp;j++){
			for(int k=0;k<=m;k++)g[k]=0x3f3f3f3f;
			for(int k=0;k<=m;k++)for(int l=0;l<=k;l++)g[k]=min(g[k],f[x][anc[j]][k-l]+f[y][anc[j]][l]);
			for(int k=0;k<=m;k++)f[x][anc[j]][k]=g[k];
		}
	}
	for(int j=m;j;j--)f[x][x][j]=f[x][x][j-1];
	f[x][x][0]=0x3f3f3f3f;
	for(int j=1;j<tp;j++)for(int k=0;k<=m;k++)f[x][anc[j]][k]+=val[x]*(dis[x]-dis[anc[j]]),f[x][anc[j]][k]=min(f[x][anc[j]][k],f[x][x][k]);
	tp--;
}
int main(){
	scanf("%d%d",&n,&m),m++,memset(head,-1,sizeof(head));
	for(int i=1,x,y;i<=n;i++)scanf("%d%d%d",&val[i],&x,&y),ae(x,i,y);
	dfs(0);
//	for(int i=1;i<=n;i++)printf("%d ",dis[i]*val[i]);puts("");
	printf("%d\n",f[0][0][m]);
	return 0;
}
```

# XLI.[CF1067A Array Without Local Maximums ](https://www.luogu.com.cn/problem/CF1067A)

这题DEBUG的我心态爆炸……后来发现是一个$i$打成$j$了……无语。

很容易想到，设$f[i][j][0/1]$表示：

到第$i$位时，位置$i$填入了$j$，且$j\geq\text{位置i-1上的数}$的状态是$0/1$的种数。

但这就会有问题：$\geq$反过来是$\leq$，而不是$<$。

因此我们还要记录一下是否相等。即设$f[i][j][0/1/2]$表示：

到第$i$位时，位置$i$填入了$j$，且$j$相较于上一位是小于/等于/大于。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
const int mod=998244353;
const int lim=200;
int n,num[100100],f[2][210][3],res;
signed main(){
	scanf("%lld",&n);
	for(int i=1;i<=n;i++)scanf("%lld",&num[i]);
	if(num[1]==-1)for(int i=1;i<=lim;i++)f[1][i][0]=1;
	else f[1][num[1]][0]=1;
	for(int i=2;i<=n;i++){
		for(int j=1;j<=lim;j++)f[i&1][j][0]=f[i&1][j][1]=f[i&1][j][2]=0;
		int s;
		s=0;
		for(int j=1;j<=lim;j++){
			if(num[i]==-1||j==num[i])f[i&1][j][0]=s;
			(s+=f[!(i&1)][j][0]+f[!(i&1)][j][1]+f[!(i&1)][j][2])%=mod;
		}
		for(int j=1;j<=lim;j++)if(num[i]==-1||j==num[i])f[i&1][j][1]=(f[!(i&1)][j][0]+f[!(i&1)][j][1]+f[!(i&1)][j][2])%mod;
		s=0;
		for(int j=lim;j>=1;j--){
			if(num[i]==-1||j==num[i])f[i&1][j][2]=s;
			(s+=f[!(i&1)][j][1]+f[!(i&1)][j][2])%=mod;
		}
//		printf("%d:",i);for(int j=1;j<=lim;j++)if(f[i&1][j][0]||f[i&1][j][1])printf("(%d:%d %d)",j,f[i&1][j][0],f[i&1][j][1]);puts("");
	}
	for(int i=1;i<=lim;i++)(res+=f[n&1][i][1]+f[n&1][i][2])%=mod;
	printf("%lld\n",res);
	return 0;
}
```

# XLII.[CF1073E Segment Sum](https://www.luogu.com.cn/problem/CF1073E)

数位DP裸题。

设$f(pos, sta, lim, lead)$表示：

到第$pos$个位置时，

$0\sim9$的出现状态状压出来是$sta$，

是否压上限/是否有前导零的状态是$lim$和$lead$。

$f$要维护这样的数的个数和他们的和。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
#define pii pair<int,int>
const int mod=998244353;
int l,r,k,num[23],pov[23],tp;
pii f[23][1<<10];
pii dfs(int pos,int sta,bool lim,bool lead){
	if(__builtin_popcount(sta)>k)return make_pair(0,0);
	if(!pos)return make_pair(0,1);
	if(!lim&&!lead&&f[pos][sta]!=make_pair(-1ll,-1ll))return f[pos][sta];
	pii res=make_pair(0,0);
	for(int i=0;i<=(lim?num[pos]:9);i++){
		pii tmp=dfs(pos-1,sta|(lead&&!i?0:(1<<i)),lim&&(i==num[pos]),lead&&(!i));
		(res.first+=tmp.first)%=mod;
		(res.second+=tmp.second)%=mod;
		(res.first+=tmp.second*i%mod*pov[pos]%mod)%=mod;
	}
	if(!lim&&!lead)f[pos][sta]=res;
	return res;
}
int calc(int ip){
	tp=0;
	while(ip)num[++tp]=ip%10,ip/=10;
	return dfs(tp,0,1,1).first;
}
signed main(){
	scanf("%lld%lld%lld",&l,&r,&k),l--,memset(f,-1,sizeof(f));
	pov[1]=1;
	for(int i=2;i<23;i++)pov[i]=(pov[i-1]*10)%mod;
	printf("%lld\n",(calc(r)-calc(l)+mod)%mod);
	return 0;
}
```

# XLIII.[CF888F Connecting Vertices](https://www.luogu.com.cn/problem/CF888F)

这个奇怪的限制（两条边不能有交点）让我们想到什么？

对于任何一种方案，不存在$x_0<x_1<y_0<y_1$，其中连边$(x_0, y_0), (x_1, y_1)$。

也就是说，对于任何一段区间$[i, j]$，如果里面所有点全都连通：

要么$i, j$两点之间自己连了条边，此时，存在且仅存在一个$k$，使得区间$[i, k]$和$[k+1, j]$间有且只有$(i, j)$一条边；

要么可以找到一个点$k$，使得区间$[i, k-1]$与$[k+1, j]$之间没有边，并且$k$与两个集合连通。

因此我们可以轻而易举写出：

$(a_{i, j}=1):f[i, j]=\sum\limits_{k=i}^{j} f[i, k]*f[k+1, j]$

$f[i, j]=\sum\limits_{k=i+1}^{j-1} f[i, k]*f[k, j]$

但是这样会出问题：

```要么可以找到一个点$k$，使得区间$[i, k-1]$与$[k+1, j]$之间没有边，并且$k$与两个集合连通。

```

并不表示这样的$k$唯一。例如，$(1,2)\rightarrow(2,3)\rightarrow(3,4)$中，$2$是一个$k$，$3$也是一个$k$，这同一种方案就被算了两边！

因此，我们可以只拿最左边那个$k$为准。即，$i$与$k$直接连边的$k$才是好$k$。

我们新增维数：

设$f[i,j][0/1]$表示：区间$i,j$全部连通，并且$i,j$强制连边/强制不连边。

则有

$(a_{i,j}=1):f[i,j][0]=\sum\limits_{k=i}^{j} (f[i,k][0]+f[i,k][1])*(f[k+1,j][0]+f[k+1,j][1])$

$f[i,j]=\sum\limits_{k=i+1}^{j-1} f[i,k][0]*(f[k,j][0]+f[k,j][1])$。

代码：

```cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=1e9+7;
int n,f[510][510][2];
bool g[510][510];
int main(){
	scanf("%d",&n);
	for(int i=1;i<=n;i++)for(int j=1;j<=n;j++)scanf("%d",&g[i][j]);
	for(int i=1;i<=n;i++)f[i][i][0]=1;
	for(int l=2;l<=n;l++)for(int i=1,j=i+l-1;j<=n;i++,j++){
		if(g[i][j])for(int k=i;k<j;k++)(f[i][j][0]+=1ll*(f[i][k][0]+f[i][k][1])*(f[k+1][j][0]+f[k+1][j][1])%mod)%=mod;
		for(int k=i+1;k<j;k++)if(g[i][k])(f[i][j][1]+=1ll*f[i][k][0]*(f[k][j][0]+f[k][j][1])%mod)%=mod;
	}
	printf("%d\n",(f[1][n][0]+f[1][n][1])%mod);
	return 0;
}
```

# XLIV.[CF599E Sandy and Nuts](https://www.luogu.com.cn/problem/CF599E)

神题。

本题给我一个忠告：无论什么题，都要先看数据范围（~~废话~~）。

没看到$n\leq 13$之前以为是道毒瘤题，看到之后……还是毒瘤题。

因为数据范围小，可以状压。

先不考虑LCA和边的限制。设$f[x][U]$表示：在以$x$为根的**子树**中，选择了$U$里面的点，的方案数。

转移就是枚举$u\subseteq \{U\setminus x\}$，其中$\setminus$符号表示从某个集合中删掉一个数/一个集合。这个$u$表示$x$的某个儿子所包含的子树集。然后就有

$f[x][U]=\sum\limits_{u\subseteq \{U\setminus x\}}\sum\limits_{y\in u}f[y][u]*f[x][{U\setminus u}]$

但是这个枚举会重复计算：假设$x$有两个儿子$y_1$和$y_2$，那么枚举$y_1$时，$y_2$的情况会被算上；同时，枚举$y_2$时，$y_1$也会被计算！

这样，我们必须只计算包含某个点$pos$的那种方案所贡献的答案。即，随便找出一个$pos\in\{U\setminus x\}$，则只有$u\ni pos$的$u$才是合法的$u$。

下面我们考虑加上边和$LCA$的限制，什么样的$u$才是合法的$u$。

### I. LCA的限制

#### I. I. 确保LCA是LCA而不是单纯的CA（common ancestor）。

即，对于$(a_i, b_i, c_i)$，如果有$c_i=x$，则$a_i\in u$与$b_i \in u$不能同时出现，否则它们的LCA就不是$x$了。

#### I. II. 确保LCA一定是A（ancestor）

即，对于$(a_i, b_i, c_i)$，如果有$c_i\in u$，必有$a_i\in u$且$b_i \in u$。

### II. 边的限制

#### II. I. 确保边的存在

即，对于$(a_i, b_i)$，如果有$a_i\neq x$且$b_i\neq x$但是$a_i\in u$与$b_i\in u$却有且只有一个条件成立，则这条边不可能存在。

#### II. II. 确保边的可能

即，对于所有的$y\ \operatorname{s.t.}\ \exists(x, y)$，一个$u$里最多只能有这么一个$y$，因为一棵子树中最多只能同父亲连一条边。

如果只存在一个$y\in u$，那么转移就只能从这个$y$而来，即

$f[x][U]=f[y][u]*f[x][{U\setminus u}]$

否则，即不存在$y\in u$，就是上面的式子

$f[x][U]=\sum\limits_{y\in u}f[y][u]*f[x][{U\setminus u}]$

边界为$f[x][\{x\}]=1$，最终答案为$f[0][\{0\sim n-1\}]$。

为了方便，采取记忆化搜索的形式实行。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int n,m,p,f[15][1<<15];
bool g[15][15];
pair<int,int>e[15];
pair<pair<int,int>,int>l[110];
bool in(int x,int y){return x&(1<<y);}
int dfs(int x,int U){
	int &res=f[x][U],pos=0;
//	printf("%d,%d:%d\n",x,U,res);
	if(~res)return f[x][U];
	U^=(1<<x),res=0;
	for(;pos<n;pos++)if(in(U,pos))break;
	for(int u=U;u;u=(u-1)&U){
		if(!in(u,pos))continue;
		bool ok=true;
		for(int i=0;i<p;i++)if(l[i].second==x&&in(u,l[i].first.first)&&in(u,l[i].first.second)){ok=false;break;}
		if(!ok)continue;
		for(int i=0;i<p;i++)if(in(u,l[i].second)&&(!in(u,l[i].first.first)||!in(u,l[i].first.second))){ok=false;break;}
		if(!ok)continue;
		for(int i=0;i<m;i++)if(e[i].first!=x&&e[i].second!=x&&(in(u,e[i].first)^in(u,e[i].second))){ok=false;break;}
		if(!ok)continue;
		int cnt=0,y;
		for(int i=0;i<n;i++)if(g[x][i]&&in(u,i))cnt++,y=i;
		if(cnt>1)continue;
		if(cnt==1)res+=dfs(y,u)*dfs(x,U^u^(1<<x));
		else for(y=0;y<n;y++)if(in(u,y))res+=dfs(y,u)*dfs(x,U^u^(1<<x));
	}
//	printf("%d,%d:%d\n",x,U,res);
	return res;
}
signed main(){
	scanf("%lld%lld%lld",&n,&m,&p),memset(f,-1,sizeof(f));
	for(int i=0,x,y;i<m;i++)scanf("%lld%lld",&x,&y),x--,y--,g[x][y]=g[y][x]=true,e[i]=make_pair(x,y);
	for(int i=0,a,b,c;i<p;i++)scanf("%lld%lld%lld",&a,&b,&c),a--,b--,c--,l[i]=make_pair(make_pair(a,b),c);
	for(int i=0;i<n;i++)f[i][1<<i]=1;
	printf("%lld\n",dfs(0,(1<<n)-1));
	return 0;
} 
```

# XLV.[CF1088E Ehab and a component choosing problem](https://www.luogu.com.cn/problem/CF1088E)

思路1.$n^2$DP。

考虑设$f[i][j][0/1]$表示：

节点$i$，子树分了$j$个集合，节点$i$是/否在某个集合内的最大值。

但是这样是没有前途的——你再怎么优化也优化不了，还是只能从题目本身的性质入手。

思路2. 分析性质，$O(n)$解决。

发现，答案最大也不会超过最大的那个集合的和。

我们考虑把每个集合看成一个数。那么，题目就让我们从一堆数中选一些数，使得它们的平均值最大。只选最大的那一个数，则答案就是最大的那一个数；但是最大的数可能不止一个，因此要找到所有值最大且互不相交的集合的数量。

找到最大的那个集合，可以直接$O(n)$DP出来。设$f_x$表示以$x$为根的子树中，包含$x$的所有集合中最大的那个，则有

$f_x=\sum\limits_{y\in son_x}\max(f_y, 0)$

这样最大的那个集合就是$f_x$的最大值。

至于互不重叠的限制吗……再DP一遍，当一个$f_x$达到最大时，计数器++，并将$f_x$清零。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int n,val[300100],f[300100],mx=0x8080808080808080,res,head[300100],cnt;
bool vis[300100];
struct node{
	int to,next;
}edge[600100];
void ae(int u,int v){
	edge[cnt].next=head[u],edge[cnt].to=v,head[u]=cnt++;
	edge[cnt].next=head[v],edge[cnt].to=u,head[v]=cnt++;
}
void dfs1(int x,int fa){
	f[x]=val[x];
	for(int i=head[x];i!=-1;i=edge[i].next)if(edge[i].to!=fa)dfs1(edge[i].to,x),f[x]+=max(0ll,f[edge[i].to]);
}
void dfs2(int x,int fa){
	f[x]=val[x];
	for(int i=head[x];i!=-1;i=edge[i].next)if(edge[i].to!=fa)dfs2(edge[i].to,x),f[x]+=max(0ll,f[edge[i].to]);
	if(f[x]==mx)res++,f[x]=0x8080808080808080;
}
signed main(){
	scanf("%lld",&n),memset(head,-1,sizeof(head));
	for(int i=1;i<=n;i++)scanf("%lld",&val[i]);
	for(int i=1,x,y;i<n;i++)scanf("%lld%lld",&x,&y),ae(x,y);
	dfs1(1,0);
	for(int i=1;i<=n;i++)mx=max(mx,f[i]);
	dfs2(1,0);
	printf("%lld %lld\n",1ll*res*mx,res);
	return 0;
}
```

# XLVI.[[NOI2002]贪吃的九头龙](https://www.luogu.com.cn/problem/P4362)

思路1.

设$f[i][j][k]$表示：在以$i$为根的子树上有$j$个点是归大头吃的，并且第$i$个点是归第$k$个头吃的。

但这样做不仅复杂度高（似乎是$O(n^5)$？），还有个问题：无法保证每个头都至少吃了一个果子。

思路2.

设$f[i][j][0/1]$表示：在以$i$为根的子树上有$j$个点是归大头吃的，并且第$i$个点 不是$(0)$/是$(1)$归大头吃的。

当$m=2$时，对于一条边来说，只有一边归大头吃而另一边归小头吃时才**不会有损失**。证明显然。

否则，即$m>2$，对于一条边来说，只有两边都归大头吃才**会有损失**。不归大头吃的地方，可以黑白染色直接造成没有任何地方有损失。

答案为$f[1][k][1]$。复杂度$O(n^3)$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,p,head[310],cnt,f[310][310][2],g[310][2];
struct node{
	int to,next,val;
}edge[610];
void ae(int u,int v,int w){
	edge[cnt].next=head[u],edge[cnt].to=v,edge[cnt].val=w,head[u]=cnt++;
	edge[cnt].next=head[v],edge[cnt].to=u,edge[cnt].val=w,head[v]=cnt++;
}
void dfs(int x,int fa){
	f[x][0][0]=f[x][1][1]=0;
	for(int i=head[x],y;i!=-1;i=edge[i].next){
		if((y=edge[i].to)==fa)continue;
		dfs(y,x);
		for(int j=0;j<=p;j++)for(int u=0;u<2;u++)g[j][u]=0x3f3f3f3f;
		for(int j=0;j<=p;j++)for(int k=0;k<=j;k++)for(int u=0;u<=min(j-k,1);u++)for(int v=0;v<=min(k,1);v++)g[j][u]=min(g[j][u],f[x][j-k][u]+f[y][k][v]+edge[i].val*(m==2?!(u^v):(u&v)));
		for(int j=0;j<=p;j++)for(int u=0;u<2;u++)f[x][j][u]=g[j][u];
	}
//	printf("%d:",x);for(int i=0;i<=p;i++)printf("(%d,%d)",f[x][i][0],f[x][i][1]);puts(""); 
}
int main(){
	scanf("%d%d%d",&n,&m,&p),memset(head,-1,sizeof(head)),memset(f,0x3f3f3f3f,sizeof(f));
	for(int i=1,x,y,z;i<n;i++)scanf("%d%d%d",&x,&y,&z),ae(x,y,z);
	if(m+p-1>n){puts("-1");return 0;}
	dfs(1,0);
	printf("%d\n",f[1][p][1]);
	return 0;
}
```

# XLV.[CF1178F1 Short Colorful Strip](https://www.luogu.com.cn/problem/CF1178F1)

考虑设$f[i, j]$表示：假设区间$[i, j]$里面一开始所有格子的颜色都是相同的，那么，染成目标状态共有多少种染法。

我们找到$[i, j]$中最小的那个颜色，设为$mp$。则显然，我们下一步要染上$mp$这种颜色。

设最终在位置$p_{mp}$上染上了颜色$mp$。则我们可以在所有这样的区间$[k, l]$上染上$mp$（$i\leq k\leq p_{mp}\leq l\leq j$）。

或许你会以为这意味着$f[i, j]=\sum\limits_{k=i}^{p_{mp}}\sum\limits_{l=p_{mp}}^jf[i, k-1]*f[k, l]*f[l+1, j]$。

但是，这样是错误的，因为当$[k, l]=[i, j]$时，$f[i, j]$便无法从子状态转移过来！

我们考虑拆开$f[k, l]$。因为再往后的染色中，位置$p_{mp}$一定没有再被染色过，因此有$f[k, l]=f[k, p_{mp}-1]*f[p_{mp}+1, l]$。

则$f[i, j]=\sum\limits_{k=i}^{p_{mp}}\sum\limits_{l=p_{mp}}^jf[i, k-1]*f[k, p_{mp}-1]*f[p_{mp}+1, l]*f[l+1, j]$。

特殊定义一下，对于$f[i, j]$，如果$i>j$，则$f[i, j]=1$。这也是为了转移的正确（在应用上述式子时可能会调用到这样的$f[i, j]$。

上面的转移是$O(n^4)$的；但当我们拆开两个$\sum$，就可以把它化成$O(n^3)$的。

$f[i, j]=(\sum\limits_{k=i}^{p_{mp}}f[i, k-1]*f[k, p_{mp}-1])*(\sum\limits_{l=p_{mp}}^jf[p_{mp}+1, l]*f[l+1, j])$

前后两个括号内的内容互不干涉，故可以分开计算。

复杂度$O(n^3)$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=998244353;
int n,num[510],f[510][510];
int main(){
	scanf("%d%d",&n,&n);
	for(int i=1;i<=n;i++)scanf("%d",&num[i]);
	for(int i=1;i<=n+1;i++)for(int j=0;j<i;j++)f[i][j]=1;
	for(int i=1;i<=n;i++)f[i][i]=1;
	for(int l=2;l<=n;l++)for(int i=1,j=i+l-1;j<=n;i++,j++){
		int mp=i;
		for(int k=i;k<=j;k++)if(num[k]<=num[mp])mp=k;
		int A=0,B=0;
		for(int k=mp;k>=i;k--)(A+=(1ll*f[i][k-1]*f[k][mp-1]%mod))%=mod;
		for(int l=mp;l<=j;l++)(B+=(1ll*f[mp+1][l]*f[l+1][j]%mod))%=mod;
		f[i][j]=1ll*A*B%mod;
	}
	printf("%d\n",f[1][n]);
	return 0;
} 
```

# XLVI.[CF1178F2 Long Colorful Strip](https://www.luogu.com.cn/problem/CF1178F2)

首先，每一次染色，最多把一整段连续的同色格子，分成了三段。

并且，明显我们可以把连续的同色格子，直接看作一个。

这就意味着，在这么压缩后，有$m<2n$。

这就意味着$O(m^3)$的复杂度是可以接受的。

还是考虑和前一道题一样的DP。

但是这题，并非所有的$f[i, j]$都是合法的；只有对于每一种颜色，它所有的格子要么全都在段内，要么全都在段外，这样的$f[i, j]$才是合法的。**因为，两个格子只要从什么时候开始颜色不一样了，那它们的颜色也会一直不一样下去**。

考虑如何转移。

因为每种颜色都可能出现了不止一次，所以对于一种颜色$c$，我们有必要记录它出现的最左端$mn_c$与最右端$mx_c$。

则转移时的左右两端仍然可以采取和上一问一模一样的转移方式，即

$f[i, j]=(\sum\limits_{k=i}^{mn_{mp}}f[i, k-1]*f[k, mn_{mp}-1])*(\sum\limits_{l=mx_{mp}}^jf[mx_{mp}+1, l]*f[l+1, j])$

同时，对于区间$[mn_{mp}, mx_{mp}]$内的非$mp$的所有连续格子段$[p_x, q_x]$，我们也都应该计算它们的贡献。

因此我们最终得到的是

$f[i, j]=(\sum\limits_{k=i}^{mn_{mp}}f[i, k-1]*f[k, mn_{mp}-1])*(\sum\limits_{l=mx_{mp}}^jf[mx_{mp}+1, l]*f[l+1, j])*\prod f[p_x, q_x]$

复杂度仍是$O(n^3)$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
const int mod=998244353;
int n,m,num[1000100],f[1010][1010],mn[1010],mx[1010];
int main(){
	scanf("%d%d",&n,&m);
	memset(mn,0x3f3f3f3f,sizeof(mn));
	for(int i=1;i<=m;i++){
		scanf("%d",&num[i]);
		if(num[i]==num[i-1])i--,m--;
	}
	if(m>2*n){puts("0");return 0;}
//	for(int i=1;i<=m;i++)printf("%d ",num[i]);puts("");
	for(int i=1;i<=m;i++)mx[num[i]]=max(mx[num[i]],i),mn[num[i]]=min(mn[num[i]],i);
//	for(int i=1;i<=n;i++)printf("%d %d\n",mx[i],mn[i]);
	for(int i=1;i<=m+1;i++)for(int j=0;j<i;j++)f[i][j]=1;
	for(int l=1;l<=m;l++)for(int i=1,j=i+l-1;j<=m;i++,j++){
		int mp=0x3f3f3f3f;
		for(int k=i;k<=j;k++)mp=min(mp,num[k]);
		if(mn[mp]<i||mx[mp]>j)continue;
		int A=0,B=0;
		for(int k=mn[mp];k>=i;k--)(A+=(1ll*f[i][k-1]*f[k][mn[mp]-1]%mod))%=mod;
		for(int l=mx[mp];l<=j;l++)(B+=(1ll*f[mx[mp]+1][l]*f[l+1][j]%mod))%=mod;
		f[i][j]=1ll*A*B%mod;
//		printf("(%d,%d):\n",i,j);
		for(int p=mn[mp]+1,q=mn[mp];p<mx[mp];){
			while(q<j&&num[q+1]!=mp)q++;
//			printf("(%d,%d)\n",p,q);
			f[i][j]=1ll*f[i][j]*f[p][q]%mod;
			q++,p=q+1;
		}
//		printf("%d\n",f[i][j]);
	}
	printf("%d\n",f[1][m]);
	return 0;
} 
```

# XLVII.[CF906C Party](https://www.luogu.com.cn/problem/CF906C)

DP是门艺术。

$n\leq 22$一眼状压。但是怎么状压就比较困难，因为同一个$f[x]$可以代表成千上万种含义。

这里我们采用，设$f[x]$表示当$x$集合中所有的点都处于同一个团内的最小代价。

则我们有$f[x \operatorname{or}sta_i]=\max\limits_{i\in x}\{f[x]+1\}$。其中$sta_i$表示与$i$有边的集合。

初始为$f[\{i\}]=0$，其它均为$+\infty$。

复杂度为$O(n2^n)$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
int f[1<<22],fr[1<<22],id[1<<22],n,m,sta[22],mxn;
stack<int>s;
int main(){
	scanf("%d%d",&n,&m),mxn=(1<<n),memset(f,0x3f3f3f,sizeof(f));
	for(int i=1,x,y;i<=m;i++)scanf("%d%d",&x,&y),x--,y--,sta[x]|=(1<<y),sta[y]|=(1<<x);
	if(m*2==n*(n-1)){puts("0");return 0;}
	for(int i=0;i<n;i++)f[1<<i]=0;
	for(int x=1;x<mxn;x++)for(int i=0;i<n;i++){
		if(!(x&(1<<i)))continue;
		int y=x|sta[i];
		if(y==x)continue;
		if(f[y]>f[x]+1)f[y]=f[x]+1,fr[y]=x,id[y]=i;
	}
	printf("%d\n",f[mxn-1]);
	int x=mxn-1;
	while(__builtin_popcount(x)!=1)s.push(id[x]),x=fr[x];
	while(!s.empty())printf("%d ",s.top()+1),s.pop();
	return 0;
}
```

# XLVIII.[CF11D A Simple Task](https://www.luogu.com.cn/problem/CF11D)

我感觉状压DP是所有DP中最能玩出花的那一种……因为状态保存下来了因此什么奇奇怪怪的限制都能满足。

比如说这题。

一个环可以看作一条首尾相接的路径。我们可以设$f[S][j]$表示：在集合$S$中的点构成了一条路径，且路径的起点为$j$的方案数。

为了避免重复计算，我们约定这条路径的起点必须是$S$中最小的那个数。换句话说，即`` `lowbit(S)` ``。

则我们只需要枚举$j$的下一条遍是去哪的就可以。复杂度为$O(n^22^n)$。

另外，一个环会顺时针逆时针算两次，并且路径也会被看作是二元环而算进去，记得统计进去。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int n,m,lim,f[1<<20][20],res;
bool g[20][20];
signed main(){
	scanf("%lld%lld",&n,&m),lim=(1<<n);
	for(int i=1,x,y;i<=m;i++)scanf("%lld%lld",&x,&y),x--,y--,g[x][y]=g[y][x]=true;
	for(int i=0;i<n;i++)f[1<<i][i]=1;
	for(int i=1;i<lim;i++)for(int j=0;j<n;j++){
		if(!(i&(1<<j)))continue;
		for(int k=__builtin_ctz(i);k<n;k++){
			if(!g[j][k])continue;
			if(i&(1<<k))res+=f[i][j]*(__builtin_ctz(i)==k);
			else f[i|(1<<k)][k]+=f[i][j];
		}
	}
	printf("%lld\n",(res-m)/2);
	return 0;
}
```

# IL.[CF24D Broken robot](https://www.luogu.com.cn/problem/CF24D)

DP必须要有方向性。没有明确顺序的DP都是在耍流氓。这就是为什么有“树上DP”和“DAG上DP”而没有“图上DP”，图上有环就不知道应该按什么顺序做了！（像是基环树DP和仙人掌DP都是缩点了，因此顺序还是确定的；环形DP也有“断环成链”的trick）。

那如果真有DP来给你耍流氓怎么办？

还能怎么办？耍回去啊！

例如这题，有两种思路。

1. 同一行中，转移顺序不定；但是不同行之间，转移顺序还是确定的。因此我们行与行之间以普通的DP转移；同一行中，暴力高斯消元消过去。

我们看一下怎么高斯消元。设有$m$行$n$列。

则有

$f_{i, j}=\begin{cases}[j=1]:\dfrac{f_{i, j}+f_{i-1, j}+f_{i, j+1}}{3}+1\\ [j=n]:\dfrac{f_{i, j}+f_{i-1, j}+f_{i, j-1}}{3}+1\\\text{otherwise}:\dfrac{f_{i, j}+f_{i-1, j}+f_{i, j-1}+f_{i, j+1}}{4}+1\end{cases}$

处理一下：

$\begin{cases}[j=1]:2f_{i, j}-f_{i, j+1}=f_{i-1, j}+3\\ [j=n]:2f_{i, j}-f_{i, j-1}=f_{i-1, j}+3\\\text{otherwise}:3f_{i, j}-f_{i, j-1}-f_{i, j+1}=f_{i-1, j}+4\end{cases}$

这其中，上一行的DP值可以看作是常量。

这样复杂度是$O(n^4)$，铁定过不去。

但如果我们把高斯消元的矩阵列出来$(5\times5)$：

$\begin{bmatrix}2&-1&0&0&0\\-1&3&-1&0&0\\0&-1&3&-1&0\\0&0&-1&3&-1\\0&0&0&-1&2\end{bmatrix}$

更大一点：

$\begin{bmatrix}2&-1&0&\cdots&0&0&0\\-1&3&-1&\cdots&0&0&0\\0&-1&3&\cdots&0&0&0\\\vdots&\vdots&\vdots&\ddots&\vdots&\vdots&\vdots\\0&0&0&\cdots&3&-1&0\\0&0&0&\cdots&-1&3&-1\\0&0&0&\cdots&0&-1&2\end{bmatrix}$

也就是说，它是一个非常稀疏的矩阵，并且非零元素只分布在主对角线两侧！

在这种特殊矩阵上高斯消元只需要消对角线两侧的位置即可，复杂度是$O(n)$的。

则总复杂度是$O(n^2)$的。

另外，从点$(X, Y)$出发走到第$n$行，可以看作是从第$X$行的任何点出发，走到点$(n, Y)$的方案数。

代码：

``` cpp
#include<bits/stdc++.h> 
using namespace std;
int n,m,X,Y;
double f[1010],g[1010][1010];
void Giaos(){
//	for(int i=1;i<=n;i++){for(int j=1;j<=n;j++)printf("%lf ",g[i][j]);puts("");}puts("");
	for(int i=1;i<n;i++){
		/*int mp=i;
		for(int j=i+1;j<=min(n,i+2);j++)if(fabs(g[j][i])>fabs(g[mp][i]))mp=j;
		if(mp!=i){
			for(int j=i;j<=min(n,i+2);j++)swap(g[mp][j],g[i][j]);
			swap(g[mp][n+1],g[i][n+1]);
		}
		assert(mp==i);*/
		double tmp=g[i+1][i]/g[i][i];
		g[i+1][i]=0,g[i+1][i+1]-=tmp*g[i][i+1],g[i+1][n+1]-=tmp*g[i][n+1];
	}
//	for(int i=1;i<=n;i++){for(int j=1;j<=n;j++)printf("%lf ",g[i][j]);puts("");}puts("");
	f[n]=g[n][n+1]/g[n][n];
	for(int i=n-1;i>=1;i--)f[i]=(g[i][n+1]-g[i][i+1]*f[i+1])/g[i][i];
}
int main(){
	scanf("%d%d%d%d",&m,&n,&X,&Y),m-=X-1,X=1;
	if(m==1){puts("0");return 0;}
	if(n==1){printf("%d\n",(m-1)*2);return 0;}
	for(int i=1;i<m;i++){
		g[1][1]=2,g[1][2]=-1,g[1][n+1]=f[1]+3;
		g[n][n]=2,g[n][n-1]=-1,g[n][n+1]=f[n]+3;
		for(int j=2;j<n;j++)g[j][j-1]=g[j][j+1]=-1,g[j][j]=3,g[j][n+1]=f[j]+4;
		Giaos();
	}
	printf("%lf\n",f[Y]);
	return 0;
}
```

2. 因为“保留4位小数”，所以……

跑$50$遍最普通的DP完事。

代码：

``` cpp
#include<bits/stdc++.h> 
using namespace std;
int n,m,X,Y;
double f[1010][1010];
int main(){
	scanf("%d%d%d%d",&m,&n,&X,&Y),m-=X-1,X=1;
	if(m==1){puts("0");return 0;}
	if(n==1){printf("%d\n",(m-1)*2);return 0;}
	for(int i=1;i<m;i++)for(int tmp=1;tmp<=50;tmp++)for(int j=1;j<=n;j++){
		if(j==1)f[i][j]=(f[i][j+1]+f[i][j]+f[i-1][j])/3+1;
		else if(j==n)f[i][j]=(f[i][j-1]+f[i][j]+f[i-1][j])/3+1;
		else f[i][j]=(f[i-1][j]+f[i][j]+f[i][j-1]+f[i][j+1])/4+1;
	}
	printf("%lf\n",f[m-1][Y]);
	return 0;
}
```

# L.[CF53E Dead Ends](https://www.luogu.com.cn/problem/CF53E)

$n\leq 10$，我还是第一次见到这么小的状压……

我们设$f[S][s]$表示：将集合$S$内的点连成一棵树，且集合$s$里的节点是叶子节点的方案数。

则有$f[S\cup\{j\}][\{s\setminus i\}\cup\{j\}]+=f[S][s], i\in S, j\notin S, \exists(i, j).$。

但是，一棵树可能会被不同的顺序构造出来。因此有$f[S][s]$应该除以$|s|$。

代码：

``` cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int n,m,p,f[1<<11][1<<11],lim,res;
bool g[11][11];
signed main(){
	scanf("%lld%lld%lld",&n,&m,&p),lim=(1<<n);
	for(int i=1,x,y;i<=m;i++)scanf("%lld%lld",&x,&y),x--,y--,g[x][y]=g[y][x]=true,f[(1<<x)|(1<<y)][(1<<x)|(1<<y)]=2;
	for(int S=1;S<lim;S++)for(int s=S;s;s=(s-1)&S){
		f[S][s]/=__builtin_popcount(s);
		for(int i=0;i<n;i++){
			if(!(S&(1<<i)))continue;
			int t=s&((lim-1)^(1<<i));
			for(int j=0;j<n;j++){
				if(S&(1<<j))continue;
				if(!g[i][j])continue;
				f[S|(1<<j)][t|(1<<j)]+=f[S][s];
			}
		}		
	}
	for(int i=0;i<lim;i++)if(__builtin_popcount(i)==p)res+=f[lim-1][i];
	printf("%lld\n",res);
	return 0;
}
```

到这里为止，DP已经有50题了。我现在都是打一个字卡两秒的情况了，txt也已经突破了4000行。接下来我将开一篇新的DP博客。[portal](https://www.luogu.com.cn/blog/Troverld/dp-shua-ti-bi-ji-ii)
