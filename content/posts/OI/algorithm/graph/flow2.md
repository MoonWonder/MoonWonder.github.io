---
author: "MoonWonder"
author_link: "moonwonder.top"
title: "flow2"
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



 里是网络流学习笔记II。[上一篇笔记](https:\/\/www.luogu.com.cn\/blog\/Troverld\/wang-lao-liu-xue-xi-bi-ji)写够一百题了，故开个新坑。

本文中各种约定同上一篇笔记中一致。

现在开始！

# CI.[[国家集训队]部落战争](https:\/\/www.luogu.com.cn\/problem\/P2172)

第一题，挑道比较板子的题罢。

首先很明显可以抽象出一张从一个位置走到另一个的有向无环图出来（因为只能从上往下打）

然后就是最小路径覆盖问题的板子。很遗憾的是，我忘记了最小路径覆盖问题的解法，于是使用了XLIII.[[SDOI2010]星际竞速](https:\/\/www.luogu.com.cn\/problem\/P2469)中的拆点+最小费用最大流的做法，一样能过，就是被卡掉一个点，不得不吸氧。

代码：

``` cpp
#include<bits\/stdc++.h>
using namespace std;
int n,m,a,b;
char s[60][60];
namespace MCMF{
        const int N=5010,M=200000;
        int head[N],cnt,dis[N],fr[N],id[N],S,T,cost;
        struct node{
                int to,next,val,cost;
        }edge[M];
        void ae(int u,int v,int w,int c){
        \/\/    printf("%d %d %d %d\n",u,v,w,c);
                edge[cnt].cost=c,edge[cnt].next=head[u],edge[cnt].to=v,edge[cnt].val=w,head[u]=cnt++;
                edge[cnt].cost=-c,edge[cnt].next=head[v],edge[cnt].to=u,edge[cnt].val=0,head[v]=cnt++;
        }
        queue<int>q;
        bool in[N];
        bool SPFA(){
                memset(dis,0x3f,sizeof(dis)),dis[S]=0,q.push(S),in[S]=true;
                while(!q.empty()){
                        int x=q.front();q.pop(),in[x]=false;
        \/\/            printf("%d\n",x);
                        for(int i=head[x];i!=-1;i=edge[i].next){
                                if(!edge[i].val)continue;
                                if(dis[edge[i].to]>dis[x]+edge[i].cost){
                                        dis[edge[i].to]=dis[x]+edge[i].cost,fr[edge[i].to]=x,id[edge[i].to]=i;
                                        if(!in[edge[i].to])in[edge[i].to]=true,q.push(edge[i].to);
                                }
                        }
                }
                if(dis[T]==dis[T+1])return false;
                int x=T,mn=0x3f3f3f3f;
                while(x!=S)mn=min(mn,edge[id[x]].val),x=fr[x];
                cost+=dis[T]*mn,x=T;
                while(x!=S)edge[id[x]].val-=mn,edge[id[x]^1].val+=mn,x=fr[x];
                return true;
        }
}
using namespace MCMF;
int main(){
        scanf("%d%d%d%d",&n,&m,&a,&b),S=2*n*m,T=S+1,memset(head,-1,sizeof(head));
        int dx[4]={a,b,b,a},dy[4]={-b,-a,a,b};
        for(int i=0;i<n;i++)scanf("%s",s[i]);
        for(int i=0;i<n;i++)for(int j=0;j<m;j++){
                if(s[i][j]=='x')continue;
                ae(S,i*m+j,1,0);
                ae(i*m+j,T,1,1);
                ae(n*m+i*m+j,T,1,0);
                for(int k=0;k<4;k++){
                        int ii=i+dx[k],jj=j+dy[k];
                        if(ii<0||ii>=n||jj<0||jj>=m||s[ii][jj]=='x')continue;
        \/\/            printf("(%d,%d):(%d,%d)\n",i,j,ii,jj);
                        ae(i*m+j,n*m+ii*m+jj,1,0);
                }
        }
        while(SPFA());
\/\/    for(int i=0;i<cnt;i++)if(edge[i^1].val&&edge[i^1].to<n*m)printf("%d->%d\n",edge[i^1].to,edge[i].to);
        printf("%d\n",cost);
        return 0;
} 
```

# CII.[[NOI2015]小园丁与老司机](https:\/\/www.luogu.com.cn\/problemnew\/show\/P2304)

首先，老司机部分考虑DP：明显 $y$ 值不同的状态间转移是有阶段性的，但是 $y$ 值相同时则不然；于是为了凸显阶段性，我们设 $f_x$ 表示从位置 $x$ 进入某个 $y$ 值的最大收益，$g_x$ 表示从位置 $x$ 离开某个 $y$ 值的最大收益。

$g\rightarrow f$ 的转移（即为不同 $y$ 间的转移）就直接从左上、上、右上三个方向转移即可，这部分是简单的；关键是 $f\rightarrow g$，即同一 $y$ 间的转移。因为保证每个 $y$ 值的树不会太多，所以可以直接 $n^2$ 地枚举所有转移对进行转移即可。

记录路径，我们就完成了老司机部分。

然后是小园丁部分。为了找到所有最优路径的并，我们需要建出图来，每个 $f_x, g_x$ 各独立作一个节点（因此，总节点数应为 $2n+2$ 个），在可能出现的位置连边，并且从每个最优的终局节点反向推出所有合法的边。这样，我们便可以建出一张所有需要经过的边所构成的DAG。

此DAG上，每条边被经过的下限是 $1$，上限是 $\infty$（实际应用中取 $3n$ 即可，因为最多只会有不超过 $3n$ 条边）。于是我们建图跑上下界最小流即可。

代码:

``` cpp
#include<bits\/stdc++.h>
using namespace std;
const int N=50100;
namespace MaxFlow{
    const int M=2000000;
    int head[N],cur[N],dep[N],cnt,S,T,s,t,ans,deg[N];
    struct node{
        int to,next,val;
    }edge[M];
    void ae(int u,int v,int w){
        edge[cnt].next=head[u],edge[cnt].to=v,edge[cnt].val=w,head[u]=cnt++;
        edge[cnt].next=head[v],edge[cnt].to=u,edge[cnt].val=0,head[v]=cnt++;
        }
    void AE(int u,int v,int l,int r){
\/\/            printf("%d %d [%d,%d]\n",u,v,l,r);
        deg[v]+=l,deg[u]-=l;
        edge[cnt].next=head[u],edge[cnt].to=v,edge[cnt].val=r-l,head[u]=cnt++;
        edge[cnt].next=head[v],edge[cnt].to=u,edge[cnt].val=0,head[v]=cnt++;
    }
    queue<int>q;
    inline bool bfs(){
        memset(dep,0,sizeof(dep)),q.push(S),dep[S]=1;
        while(!q.empty()){
            register int x=q.front();q.pop();
            for(register int i=cur[x]=head[x];i!=-1;i=edge[i].next)if(edge[i].val&&!dep[edge[i].to])dep[edge[i].to]=dep[x]+1,q.push(edge[i].to);
        }
        return dep[T]>0;
    }
    bool reach;
    inline int dfs(int x,int flow){
        if(x==T){
            ans+=flow;
            reach=true;
            return flow;
        }
        int used=0;
        for(register int &i=cur[x];i!=-1;i=edge[i].next){
            if(!edge[i].val||dep[edge[i].to]!=dep[x]+1)continue;
            register int ff=dfs(edge[i].to,min(edge[i].val,flow-used));
            if(ff){
                edge[i].val-=ff;
                edge[i^1].val+=ff;
                used+=ff;
                if(used==flow)break;
            }
        }
        return used;
    }
    inline void Dinic(){
        while(bfs()){
            reach=true;
            while(reach)reach=false,dfs(S,0x3f3f3f3f);
        }
    }
}
using namespace MaxFlow;
int n,x[N],y[N],nw[N],ne[N],f[N],g[N],F[N],G[N],res;\/\/f:maximal when arriving at i  g:maximal when leaving from i
vector<int>v[N],u[N],a;
void discrete(int *arr){
        a.clear();
        for(int i=0;i<=n;i++)a.push_back(arr[i]);
        sort(a.begin(),a.end()),a.resize(unique(a.begin(),a.end())-a.begin());
        for(int i=0;i<=n;i++)u[arr[i]=lower_bound(a.begin(),a.end(),arr[i])-a.begin()].push_back(i);
}
void buildgraph(){
        for(int i=0;i<a.size();i++){
                sort(u[i].begin(),u[i].end(),[](int X,int Y){return y[X]<y[Y];});
                for(int j=1;j<u[i].size();j++)v[u[i][j-1]].push_back(u[i][j]);
                u[i].clear();
        }
}
bool cmp(int X,int Y){return x[X]<x[Y];}
stack<int>st;
bool lim[N<<1],vis[N<<1];\/\/if position i is able to reach maximum
vector<int>w[N<<1];
bool dfscheck(int x){
        if(vis[x])return lim[x];vis[x]=true;
        for(auto y:w[x])if(dfscheck(y)){
                lim[x]=true;
                if(x>n)AE(x-n-1,y,1,3*n);
        }
        return lim[x];
}
int main(){
        scanf("%d",&n),memset(f,-1,sizeof(f)),memset(g,-1,sizeof(g)),memset(head,-1,sizeof(head));
        for(int i=1;i<=n;i++)scanf("%d%d",&x[i],&y[i]),nw[i]=x[i]+y[i],ne[i]=x[i]-y[i];
        discrete(nw),buildgraph();
        discrete(ne),buildgraph();
        discrete(x),buildgraph();
\/\/    for(int i=0;i<=n;i++){for(auto j:v[i])printf("%d ",j);puts("");}
        discrete(y),f[0]=0;
        for(int i=0;i<a.size();i++){
                sort(u[i].begin(),u[i].end(),cmp); 
                for(int j=0;j<u[i].size();j++)if(f[u[i][j]]!=-1)for(int k=0;k<u[i].size();k++){
                        int now=f[u[i][j]];
                        if(j<k)now+=k;
                        if(j>k)now+=u[i].size()-k-1;
                        if(g[u[i][k]]<=now)g[u[i][k]]=now,G[u[i][k]]=u[i][j];
                }
                for(auto j:u[i])if(g[j]!=-1)for(auto k:v[j])if(f[k]<=g[j]+1)f[k]=g[j]+1,F[k]=j;
        }
        for(int i=0;i<=n;i++)res=max(res,g[i]);
        printf("%d\n",res);
        for(int i=0;i<=n;i++){
                if(g[i]!=res)continue;
                while(i){
                        st.push(i);
                        int P=y[i];
                        int I=lower_bound(u[P].begin(),u[P].end(),i,cmp)-u[P].begin(),J=lower_bound(u[P].begin(),u[P].end(),G[i],cmp)-u[P].begin();
                        if(J<I){
                                for(int k=I-1;k>J;k--)st.push(u[P][k]);
                                for(int k=0;k<=J;k++)st.push(u[P][k]);
                        }
                        if(J>I){
                                for(int k=I+1;k<J;k++)st.push(u[P][k]);
                                for(int k=u[P].size()-1;k>=J;k--)st.push(u[P][k]);
                        }
                        i=F[G[i]];
                }
                break;
        }
        while(!st.empty())printf("%d ",st.top()),st.pop();puts("");
        s=n+1,t=n+2,S=n+3,T=n+4;
        for(int i=0;i<a.size();i++){
                for(int j=0;j<u[i].size();j++)if(f[u[i][j]]!=-1)for(int k=0;k<u[i].size();k++){
                        int now=f[u[i][j]];
                        if(j<k)now+=k;
                        if(j>k)now+=u[i].size()-k-1;
                        if(g[u[i][k]]==now)w[u[i][j]].push_back(u[i][k]+n+1);
                }
                for(auto j:u[i])if(g[j]!=-1)for(auto k:v[j])if(f[k]==g[j]+1)w[j+n+1].push_back(k);
        }
        for(int i=0;i<=n;i++)if(g[i]==res)lim[i+n+1]=true;
        dfscheck(0);
        for(int i=0;i<=n;i++)ae(s,i,3*n),ae(i,t,3*n);
        for(int i=0;i<=n;i++)if(deg[i]>0)ae(S,i,deg[i]);else ae(i,T,-deg[i]);
        Dinic();
        ae(t,s,3*n);
        Dinic();
        printf("%d\n",edge[cnt-1].val);
        return 0;
}
```
