---
author: "MoonWonder"
author_link: "moonwonder.top"
title: "数值分析笔记四——数值积分"
date: 2025-05-19T14:44:23+08:00
lastmod: 2025-05-19T14:44:23+08:00
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


# 数值分析课程笔记: 数值积分

**授课老师**: Gemini
**日期**: 2025年5月19日

## 1. 数值积分引论 (Numerical Integration / Quadrature)

-   **目的**: 计算定积分 $I = \int_a^b f(x) dx$ 的近似值。
-   **需求场景**:
    1.  被积函数 $f(x)$ 的原函数 $F(x)$ 难以找到或不存在初等函数形式。
    2.  $f(x)$ 仅以离散数据点形式给出。
-   **基本思想**: 用一个能够容易积分的函数 $P(x)$ (通常是多项式) 来近似 $f(x)$，即 $\int_a^b f(x) dx \approx \int_a^b P(x) dx$。
-   **求积公式一般形式**: $\int_a^b f(x) dx \approx \sum_{i=0}^n w_i f(x_i)$
    -   $x_i$: 求积节点 (nodes / abscissas)
    -   $w_i$: 求积权重 (weights / coefficients)

## 2. 牛顿-柯特斯公式 (Newton-Cotes Formulas)

基于在等距节点上对 $f(x)$ 进行多项式插值，然后对插值多项式积分。
$w_i = \int_a^b L_i(x) dx$，其中 $L_i(x)$ 是拉格朗日基函数。

### 2.1. 闭型公式 (Closed Formulas - 节点包含端点)

#### a) 梯形法则 (Trapezoidal Rule, $n=1$)
-   用连接 $(a, f(a))$ 和 $(b, f(b))$ 的直线段近似 $f(x)$。
-   **公式**: $\int_a^b f(x) dx \approx \frac{b-a}{2} [f(a) + f(b)]$
-   令 $h=b-a$。
-   **截断误差**: $E_T = -\frac{h^3}{12} f''(\xi) = -\frac{(b-a)^3}{12} f''(\xi)$, $\xi \in (a,b)$。精度为1。

#### b) 辛普森法则 (Simpson's Rule, $n=2$)
-   用通过 $(a, f(a))$, $(\frac{a+b}{2}, f(\frac{a+b}{2}))$, $(b, f(b))$ 的抛物线近似 $f(x)$。
-   令 $h = (b-a)/2$ (注意这里的 $h$ 是半区间宽度)。节点为 $a, a+h, a+2h=b$。
-   **公式**: $\int_a^b f(x) dx \approx \frac{h}{3} [f(a) + 4f(a+h) + f(b)] = \frac{b-a}{6} \left[f(a) + 4f\left(\frac{a+b}{2}\right) + f(b)\right]$
-   **截断误差**: $E_T = -\frac{h^5}{90} f^{(4)}(\xi) = -\frac{(b-a)^5}{2880} f^{(4)}(\xi)$, $\xi \in (a,b)$。精度为3。

### 2.2. 更高阶牛顿-柯特斯公式及其局限性
-   **$n=3$ (辛普森3/8法则)**: $\int_{x_0}^{x_3} f(x)dx \approx \frac{3h}{8}[f(x_0)+3f(x_1)+3f(x_2)+f(x_3)]$, $E_T=O(h^5)$。精度3。
-   **$n=4$ (布尔法则)**: $\int_{x_0}^{x_4} f(x)dx \approx \frac{2h}{45}[7f_0+32f_1+12f_2+32f_3+7f_4]$, $E_T=O(h^7)$。精度5。
-   **误差规律**: $n+1$ 个节点的闭型公式，若 $n$ 为奇数，精度为 $n$；若 $n$ 为偶数，精度为 $n+1$。
-   **局限性**:
    1.  **负权系数**: 当 $n \ge 8$ 时，部分 $w_i < 0$，可能导致数值不稳定和舍入误差放大。
    2.  **不稳定性**: 高阶等距节点插值可能出现龙格现象，积分结果可能不收敛或发散。
    因此，通常不使用非常高阶的牛顿-柯特斯公式，而是采用复化低阶公式。

## 3. 复化求积公式 (Composite Quadrature Rules)

将区间 $[a,b]$ 分成 $N$ 个等长的子区间，宽度 $h=(b-a)/N$。在每个子区间上应用低阶牛顿-柯特斯公式。

### 3.1. 复化梯形法则
$$\int_a^b f(x) dx \approx \frac{h}{2} [f(x_0) + 2f(x_1) + \dots + 2f(x_{N-1}) + f(x_N)]$$
-   **截断误差**: $E_T = -\frac{(b-a)h^2}{12} f''(\bar{\xi})$, $\bar{\xi} \in (a,b)$。全局误差 $O(h^2)$。

### 3.2. 复化辛普森法则 ($N$ 必须为偶数)
将 $[a,b]$ 分成 $N$ 个子区间，应用 $N/2$ 次基本辛普森法则。
$$\int_a^b f(x) dx \approx \frac{h}{3} [f(x_0) + 4f(x_1) + 2f(x_2) + 4f(x_3) + \dots + 2f(x_{N-2}) + 4f(x_{N-1}) + f(x_N)]$$
-   **截断误差**: $E_T = -\frac{(b-a)h^4}{180} f^{(4)}(\bar{\xi})$, $\bar{\xi} \in (a,b)$。全局误差 $O(h^4)$。

## 4. 龙贝格积分 (Romberg Integration)

-   **基础**: 复化梯形法则 $T(h)$。
-   **误差展开 (欧拉-麦克劳林公式)**: $\int_a^b f(x)dx = T(h) + C_1 h^2 + C_2 h^4 + C_3 h^6 + \dots$
-   **理查森外推**: 利用不同步长的 $T(h)$ 值消除误差项。
-   **龙贝格表 (Romberg Tableau)**:
    $R_{k,0} = T(h_k)$，其中 $h_k = (b-a)/2^k$。
    $R_{0,0} = \frac{b-a}{2}[f(a)+f(b)]$
    $R_{k,0} = \frac{1}{2} R_{k-1,0} + h_k \sum_{i=1}^{2^{k-1}} f(a + (2i-1)h_k)$ for $k \ge 1$.
    外推公式: $R_{k,j} = R_{k,j-1} + \frac{R_{k,j-1} - R_{k-1,j-1}}{4^j - 1}$ for $j \ge 1, k \ge j$.
    -   $R_{k,1}$ (第一列外推) 具有 $O(h_k^4)$ 精度 (等价于复化辛普森)。
    -   $R_{k,2}$ (第二列外推) 具有 $O(h_k^6)$ 精度 (等价于复化布尔)。
    -   对角线元素 $R_{j,j}$ 提供最佳估计。
-   **优点**: 精度高、系统化、可估计误差。对光滑函数有效。

## 5. 高斯求积 (Gaussian Quadrature)

-   **思想**: 同时优化节点 $x_i$ 和权重 $w_i$ (共 $2n+2$ 个自由度) 以达到最大精度。
-   **精度 (Degree of Precision, DOP)**: 一个求积公式能精确积分的最高次多项式的次数。
    -   $n+1$ 点高斯求积的目标是达到 $2n+1$ 次精度。
-   **节点与权重的选择**:
    -   **待定系数法**: 对少量节点 ($n=0,1$)，通过令公式对 $1, x, x^2, \dots, x^{2n+1}$ 精确成立来求解 $x_i, w_i$。
        -   1点高斯 ($n=0$): $\int_{-1}^1 f(x)dx \approx 2f(0)$。DOP=1。
        -   2点高斯 ($n=1$): $\int_{-1}^1 f(x)dx \approx f(-1/\sqrt{3}) + f(1/\sqrt{3})$。DOP=3。
    -   **正交多项式**: 对于积分 $\int_a^b W(x)f(x)dx \approx \sum_{i=0}^n w_i f(x_i)$，要达到 $2n+1$ 次精度，节点 $x_i$ 必须是与权函数 $W(x)$ 和区间 $[a,b]$ 对应的 $(n+1)$ 次正交多项式 $\phi_{n+1}(x)$ 的零点。权重 $w_i = \int_a^b W(x) L_i(x) dx$ (其中 $L_i(x)$ 是基于高斯节点的拉格朗日基函数)，且 $w_i > 0$。

### 5.1. 高斯-勒让德求积 (Gauss-Legendre Quadrature)
-   **积分**: $\int_{-1}^1 f(x)dx$ (即 $W(x)=1$, 区间 $[-1,1]$)。
-   **正交多项式**: 勒让德多项式 $P_k(x)$。
    -   $P_0(x)=1, P_1(x)=x, P_2(x)=\frac{1}{2}(3x^2-1), P_3(x)=\frac{1}{2}(5x^3-3x), \dots$
-   **节点**: $P_{n+1}(x)$ 的零点。
-   **权重**: $w_i = \frac{2}{(1-x_i^2)[P'_{n+1}(x_i)]^2}$。
-   **示例 (3点, $n=2$, DOP=5)**: 节点为 $0, \pm\sqrt{3/5}$。权重为 $w_0=w_2=5/9, w_1=8/9$。
    $\int_{-1}^1 f(x)dx \approx \frac{5}{9}f(-\sqrt{3/5}) + \frac{8}{9}f(0) + \frac{5}{9}f(\sqrt{3/5})$。
-   **区间变换**: 计算 $\int_a^b g(t)dt$，令 $t = \frac{b-a}{2}x + \frac{a+b}{2}$ ($x \in [-1,1]$)。
    $\int_a^b g(t)dt = \frac{b-a}{2} \int_{-1}^1 g\left(\frac{b-a}{2}x + \frac{a+b}{2}\right) dx \approx \frac{b-a}{2} \sum_{i=0}^n w_i g(t_i)$
    其中 $t_i = \frac{b-a}{2}x_i + \frac{a+b}{2}$，$x_i, w_i$ 为标准高斯-勒让德节点和权重。
-   **误差**: $E_n(f) = C_n f^{(2n+2)}(\xi)$ (系数 $C_n$ 较复杂)。误差与非常高阶的导数相关。

### 5.2. 其他类型的高斯求积
-   **高斯-切比雪夫**: $\int_{-1}^1 \frac{f(x)}{\sqrt{1-x^2}}dx \approx \frac{\pi}{n+1} \sum_{i=0}^n f(x_i)$，$x_i$ 为 $T_{n+1}(x)$ 零点。
-   **高斯-拉盖尔**: $\int_0^\infty e^{-x}f(x)dx \approx \sum w_i f(x_i)$，$x_i$ 为 $L_{n+1}(x)$ 零点。
-   **高斯-埃尔米特**: $\int_{-\infty}^\infty e^{-x^2}f(x)dx \approx \sum w_i f(x_i)$，$x_i$ 为 $H_{n+1}(x)$ 零点。

## 6. 自适应求积 (Adaptive Quadrature)

-   **动机**: 对函数变化剧烈部分加密计算，平缓部分减少计算，以固定精度要求下优化效率。
-   **核心思想**: 递归地划分区间。对子区间 $[c,d]$:
    1.  用两种不同精度的方法 (如 $S_1=S(c,d)$ 和 $S_2=S(c,m)+S(m,d)$，其中 $m=(c+d)/2$) 计算积分。
    2.  估计 $S_2$ 的误差 $E_{S_2} \approx \frac{1}{15}|S_2 - S_1|$ (对于辛普森规则)。
    3.  若 $\|E_{S_2}\| < \text{TOL}_{sub}$ (该子区间的容限)，则接受 $S_2$ (或 $S_2 + E_{S_2}$ 作为更高阶近似)。
    4.  否则，将 $[c,d]$ 分为两半，容限减半，递归调用。
-   **优点**: 高效、鲁棒、用户指定全局精度。
-   **缺点**: 实现稍复杂、可能被高度振荡函数欺骗、有递归开销。



```tex
\documentclass[UTF8,a4paper]{ctexart}
\usepackage{amsmath, amssymb, amsfonts}
\usepackage{geometry}
\geometry{a4paper, margin=1in}
\usepackage{array}
\usepackage{booktabs}
\usepackage{enumitem}

\title{数值分析课程笔记: 数值积分}
\author{Gemini 老师}
\date{2025年5月19日}

\begin{document}
\maketitle
\tableofcontents
\newpage

\section{数值积分引论 (Numerical Integration / Quadrature)}
\begin{itemize}
    \item \textbf{目的}: 计算定积分 $I = \int_a^b f(x) dx$ 的近似值。
    \item \textbf{需求场景}:
    \begin{enumerate}
        \item 被积函数 $f(x)$ 的原函数 $F(x)$ 难以找到或不存在初等函数形式。
        \item $f(x)$ 仅以离散数据点形式给出。
    \end{enumerate}
    \item \textbf{基本思想}: 用一个能够容易积分的函数 $P(x)$ (通常是多项式) 来近似 $f(x)$，即 $\int_a^b f(x) dx \approx \int_a^b P(x) dx$。
    \item \textbf{求积公式一般形式}: $\int_a^b f(x) dx \approx \sum_{i=0}^n w_i f(x_i)$
    \begin{itemize}
        \item $x_i$: 求积节点 (nodes / abscissas)
        \item $w_i$: 求积权重 (weights / coefficients)
    \end{itemize}
\end{itemize}

\section{牛顿-柯特斯公式 (Newton-Cotes Formulas)}
基于在等距节点上对 $f(x)$ 进行多项式插值，然后对插值多项式积分。
$w_i = \int_a^b L_i(x) dx$，其中 $L_i(x)$ 是拉格朗日基函数。

\subsection{闭型公式 (Closed Formulas - 节点包含端点)}

\subsubsection{梯形法则 (Trapezoidal Rule, $n=1$)}
用连接 $(a, f(a))$ 和 $(b, f(b))$ 的直线段近似 $f(x)$。
令 $h=b-a$。
\textbf{公式}: $$\int_a^b f(x) dx \approx \frac{h}{2} [f(a) + f(b)]$$
\textbf{截断误差}: $E_T = -\frac{h^3}{12} f''(\xi) = -\frac{(b-a)^3}{12} f''(\xi)$, $\xi \in (a,b)$。精度为1。

\subsubsection{辛普森法则 (Simpson's Rule, $n=2$)}
用通过 $(a, f(a))$, $(\frac{a+b}{2}, f(\frac{a+b}{2}))$, $(b, f(b))$ 的抛物线近似 $f(x)$。
令 $h = (b-a)/2$。节点为 $a, a+h, a+2h=b$。
\textbf{公式}: $$\int_a^b f(x) dx \approx \frac{h}{3} [f(a) + 4f(a+h) + f(b)] = \frac{b-a}{6} \left[f(a) + 4f\left(\frac{a+b}{2}\right) + f(b)\right]$$
\textbf{截断误差}: $E_T = -\frac{h^5}{90} f^{(4)}(\xi) = -\frac{(b-a)^5}{2880} f^{(4)}(\xi)$, $\xi \in (a,b)$。精度为3。

\subsection{更高阶牛顿-柯特斯公式及其局限性}
\begin{itemize}
    \item \textbf{$n=3$ (辛普森3/8法则)}: $\int_{x_0}^{x_3} f(x)dx \approx \frac{3h}{8}[f(x_0)+3f(x_1)+3f(x_2)+f(x_3)]$, $E_T=O(h^5)$。精度3。
    \item \textbf{$n=4$ (布尔法则)}: $\int_{x_0}^{x_4} f(x)dx \approx \frac{2h}{45}[7f_0+32f_1+12f_2+32f_3+7f_4]$, $E_T=O(h^7)$。精度5。
    \item \textbf{误差规律}: $n+1$ 个节点的闭型公式，若 $n$ 为奇数，精度为 $n$；若 $n$ 为偶数，精度为 $n+1$。
    \item \textbf{局限性}:
    \begin{enumerate}
        \item \textbf{负权系数}: 当 $n \ge 8$ 时，部分 $w_i < 0$，可能导致数值不稳定。
        \item \textbf{不稳定性}: 高阶等距节点插值积分结果可能不收敛或发散。
    \end{enumerate}
\end{itemize}

\section{复化求积公式 (Composite Quadrature Rules)}
将区间 $[a,b]$ 分成 $N$ 个等长的子区间，宽度 $h=(b-a)/N$。

\subsection{复化梯形法则}
$$\int_a^b f(x) dx \approx \frac{h}{2} [f(x_0) + 2f(x_1) + \dots + 2f(x_{N-1}) + f(x_N)]$$
\textbf{截断误差}: $E_T = -\frac{(b-a)h^2}{12} f''(\bar{\xi})$, $\bar{\xi} \in (a,b)$。全局误差 $O(h^2)$。

\subsection{复化辛普森法则 ($N$ 必须为偶数)}
$$\int_a^b f(x) dx \approx \frac{h}{3} [f(x_0) + 4f(x_1) + 2f(x_2) + 4f(x_3) + \dots + 2f(x_{N-2}) + 4f(x_{N-1}) + f(x_N)]$$
\textbf{截断误差}: $E_T = -\frac{(b-a)h^4}{180} f^{(4)}(\bar{\xi})$, $\bar{\xi} \in (a,b)$。全局误差 $O(h^4)$。

\section{龙贝格积分 (Romberg Integration)}
\begin{itemize}
    \item \textbf{基础}: 复化梯形法则 $T(h)$。
    \item \textbf{误差展开 (欧拉-麦克劳林公式)}: $\int_a^b f(x)dx = T(h) + C_1 h^2 + C_2 h^4 + C_3 h^6 + \dots$
    \item \textbf{理查森外推}:
    $R_{k,0} = T(h_k)$，其中 $h_k = (b-a)/2^k$。
    $R_{0,0} = \frac{b-a}{2}[f(a)+f(b)]$
    $R_{k,0} = \frac{1}{2} R_{k-1,0} + h_k \sum_{i=1}^{2^{k-1}} f(a + (2i-1)h_k)$ for $k \ge 1$.
    外推公式: $$R_{k,j} = R_{k,j-1} + \frac{R_{k,j-1} - R_{k-1,j-1}}{4^j - 1} \quad \text{for } j \ge 1, k \ge j$$
    对角线元素 $R_{j,j}$ 提供最佳估计。
    \item \textbf{优点}: 精度高、系统化、可估计误差。对光滑函数有效。
\end{itemize}

\section{高斯求积 (Gaussian Quadrature)}
\subsection{引论}
\begin{itemize}
    \item \textbf{思想}: 同时优化节点 $x_i$ 和权重 $w_i$ 以达到最大精度。
    \item \textbf{精度 (Degree of Precision, DOP)}: 一个求积公式能精确积分的最高次多项式的次数。
    $n+1$ 点高斯求积的目标是达到 $2n+1$ 次精度。
\end{itemize}
\subsection{如何选点与权重}
\begin{itemize}
    \item \textbf{待定系数法}: 对少量节点，通过令公式对 $1, x, \dots, x^{2n+1}$ 精确成立来求解。
    \begin{itemize}
        \item 1点高斯 ($n=0$): $\int_{-1}^1 f(x)dx \approx 2f(0)$。DOP=1。
        \item 2点高斯 ($n=1$): $\int_{-1}^1 f(x)dx \approx f(-1/\sqrt{3}) + f(1/\sqrt{3})$。DOP=3。
    \end{itemize}
    \item \textbf{正交多项式}: 对于 $\int_a^b W(x)f(x)dx \approx \sum_{i=0}^n w_i f(x_i)$，要达到 $2n+1$ 次精度，节点 $x_i$ 必须是与 $W(x)$ 和 $[a,b]$ 对应的 $(n+1)$ 次正交多项式 $\phi_{n+1}(x)$ 的零点。
\end{itemize}

\subsection{高斯-勒让德求积 (Gauss-Legendre Quadrature)}
\begin{itemize}
    \item \textbf{积分}: $\int_{-1}^1 f(x)dx$ ($W(x)=1$, 区间 $[-1,1]$)。
    \item \textbf{正交多项式}: 勒让德多项式 $P_k(x)$。
    \item \textbf{节点}: $P_{n+1}(x)$ 的零点。 \textbf{权重}: $w_i = \frac{2}{(1-x_i^2)[P'_{n+1}(x_i)]^2}$。
    \item \textbf{示例 (3点, $n=2$, DOP=5)}: 节点 $0, \pm\sqrt{3/5}$。权重 $w_0=w_2=5/9, w_1=8/9$。
    $$\int_{-1}^1 f(x)dx \approx \frac{5}{9}f(-\sqrt{3/5}) + \frac{8}{9}f(0) + \frac{5}{9}f(\sqrt{3/5})$$
    \item \textbf{区间变换}: 计算 $\int_a^b g(t)dt$，令 $t = \frac{b-a}{2}x + \frac{a+b}{2}$ ($x \in [-1,1]$)。
    $$\int_a^b g(t)dt \approx \frac{b-a}{2} \sum_{i=0}^n w_i g\left(\frac{b-a}{2}x_i + \frac{a+b}{2}\right)$$
    \item \textbf{误差}: $E_n(f) = C_n f^{(2n+2)}(\xi)$。
\end{itemize}

\subsection{其他类型的高斯求积公式}
\begin{itemize}
    \item \textbf{高斯-切比雪夫}: $\int_{-1}^1 \frac{f(x)}{\sqrt{1-x^2}}dx \approx \frac{\pi}{n+1} \sum_{i=0}^n f(x_i)$，$x_i$ 为 $T_{n+1}(x)$ 零点。
    \item \textbf{高斯-拉盖尔}: $\int_0^\infty e^{-x}f(x)dx \approx \sum w_i f(x_i)$，$x_i$ 为 $L_{n+1}(x)$ 零点。
    \item \textbf{高斯-埃尔米特}: $\int_{-\infty}^\infty e^{-x^2}f(x)dx \approx \sum w_i f(x_i)$，$x_i$ 为 $H_{n+1}(x)$ 零点。
\end{itemize}

\section{自适应求积 (Adaptive Quadrature)}
\begin{itemize}
    \item \textbf{动机}: 对函数变化剧烈部分加密计算，平缓部分减少计算。
    \item \textbf{核心思想}: 递归地划分区间。对子区间 $[c,d]$:
    \begin{enumerate}
        \item 用两种不同精度的方法 (如 $S_1=S(c,d)$ 和 $S_2=S(c,m)+S(m,d)$，$m=(c+d)/2$) 计算积分。
        \item 估计 $S_2$ 的误差 $E_{S_2} \approx \frac{1}{15}|S_2 - S_1|$ (对于辛普森规则)。
        \item 若 $|E_{S_2}| < \text{TOL}_{sub}$ (该子区间的容限)，则接受 $S_2$ (或 $S_2 + E_{S_2}$)。
        \item 否则，将 $[c,d]$ 分为两半，容限减半，递归调用。
    \end{enumerate}
    \item \textbf{优点}: 高效、鲁棒、用户指定全局精度。
    \item \textbf{缺点}: 实现稍复杂、可能被高度振荡函数欺骗。
\end{itemize}

\end{document}
```