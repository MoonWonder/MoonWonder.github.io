---
author: "MoonWonder"
author_link: "moonwonder.top"
title: "数值分析笔记二"
date: 2025-05-15T09:29:29+08:00
lastmod: 2025-05-15T09:29:29+08:00
draft: false
description: ""
license: ""

tags: ["Math","Compute"]
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

# 数值分析学习笔记 (第六至十讲汇总)


## 第六讲：线性方程组的误差分析与条件数的影响

### 1. 回顾与背景
在求解线性方程组 $Ax=b$ 时，输入数据 $A, b$ 的不精确性或计算过程中的舍入误差都会影响解的精度。条件数 $\kappa(A) = \|A\| \cdot \|A^{-1}\|$ ($\kappa(A) \ge 1$) 是衡量这种敏感性的关键指标。
* $\kappa(A)$ 接近 1：矩阵 $A$ 是良态的 (well-conditioned)。
* $\kappa(A)$ 很大：矩阵 $A$ 是病态的 (ill-conditioned)。

### 2. 右端项 $b$ 的扰动对解的影响
设 $A$ 精确且非奇异， $b$ 有扰动 $\Delta b$。
原系统：$Ax=b$。扰动后系统：$A(x+\Delta x) = b + \Delta b$。
推导可得：
$$ \frac{\|\Delta x\|}{\|x\|} \le \kappa(A) \frac{\|\Delta b\|}{\|b\|} $$
**解读**：解 $x$ 的相对误差上界是右端项 $b$ 的相对扰动乘以条件数 $\kappa(A)$。

### 3. 系数矩阵 $A$ 的扰动对解的影响
设 $b$ 精确，$A$ 有扰动 $\Delta A$。
原系统：$Ax=b$。扰动后系统：$(A+\Delta A)(x+\Delta x) = b$。
推导可得 (若 $x+\Delta x \neq 0$):
$$ \frac{\|\Delta x\|}{\|x+\Delta x\|} \le \kappa(A) \frac{\|\Delta A\|}{\|A\|} $$
**解读**：解 $x$ 的相对变化上界是系数矩阵 $A$ 的相对扰动乘以条件数 $\kappa(A)$。

### 4. $A$ 和 $b$ 同时存在扰动
若 $(A+\Delta A)(x+\Delta x) = b+\Delta b$，且 $\kappa(A) \frac{\|\Delta A\|}{\|A\|} < 1$，则有：
$$ \frac{\|\Delta x\|}{\|x\|} \le \frac{\kappa(A)}{1 - \kappa(A) \frac{\|\Delta A\|}{\|A\|}} \left( \frac{\|\Delta A\|}{\|A\|} + \frac{\|\Delta b\|}{\|b\|} \right) $$

### 5. 残差 (Residual) 与误差 (Error)
对于近似解 $\tilde{x}$，误差 $e = x - \tilde{x}$，残差 $r = b - A\tilde{x}$。
可以推导出：
$$ \frac{\|e\|}{\|x\|} \le \kappa(A) \frac{\|r\|}{\|A\|\|x\|} \quad \text{或近似地} \quad \frac{\|e\|}{\|x\|} \le \kappa(A) \frac{\|r\|}{\|b\|} $$
**关键结论**：即使相对残差很小，如果条件数 $\kappa(A)$ 很大，解的相对误差仍然可能很大。

### 6. 条件数的实际意义与精度损失
若 $\kappa(A) \approx 10^k$，并且计算精度为 $p$ 位有效数字，则解 $x$ 中可靠的有效数字大约只有 $p-k$ 位。

### 7. 如何估计条件数
直接计算 $A^{-1}$ 代价高。实际中，数值库 (如 LAPACK) 提供了高效的条件数估计器。

---

## 第七讲：线性方程组的迭代法 (一) —— 基本概念、雅可比法与高斯-赛德尔法

### 1. 迭代法的基本思想
对于大型稀疏线性方程组 $Ax=b$，迭代法提供了一种替代直接法的方案。
* **核心思想**：从初始猜测 $x^{(0)}$ 开始，通过迭代规则 $x^{(k+1)} = f(x^{(k)})$ 生成序列 $x^{(1)}, x^{(2)}, \dots$，若收敛则逼近真解 $x$。
* **一般形式**：将 $A$ 分裂为 $A=M-N$ ($M$ 易求逆)，则 $Mx=Nx+b$。迭代格式为 $Mx^{(k+1)} = Nx^{(k)} + b$，即 $x^{(k+1)} = M^{-1}Nx^{(k)} + M^{-1}b = Tx^{(k)} + c$。
* **优点**：能利用矩阵稀疏性，每步计算量小，内存需求低，可控精度。
* **收敛性**：不保证收敛，依赖于迭代矩阵 $T$ 的性质（如谱半径 $\rho(T)<1$）。
* **停止条件**：基于解的连续变化、残差大小或最大迭代次数。

### 2. 雅可比法 (Jacobi Method)
将 $A=D-L-U$（$D$ 为对角阵，$-L$ 为严格下三角，$-U$ 为严格上三角）。
迭代公式：$Dx^{(k+1)} = (L+U)x^{(k)} + b$，即（假设 $a_{ii} \neq 0$）：
$$ x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j=1, j \neq i}^{n} a_{ij}x_j^{(k)} \right), \quad i=1, \dots, n $$
* **实现**：$x^{(k+1)}$ 的各分量可独立计算（并行性好）。
* **示例**：$\begin{cases} 4x_1 - x_2 = 1 \\\\ -x_1 + 3x_2 = 2 \end{cases}$. 若 $x^{(0)}=(0,0)^T$, 则 $x^{(1)}=(0.25, 0.6667)^T$.
* **收敛条件 (充分)**：$A$ 严格对角占优 (SDD)。

### 3. 高斯-赛德尔法 (Gauss-Seidel Method)
计算 $x_i^{(k+1)}$ 时使用本轮已更新的 $x_j^{(k+1)}$ ($j<i$)。
迭代公式：$(D-L)x^{(k+1)} = Ux^{(k)} + b$，即：
$$ x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j=1}^{i-1} a_{ij}x_j^{(k+1)} - \sum_{j=i+1}^{n} a_{ij}x_j^{(k)} \right), \quad i=1, \dots, n $$
* **实现**：顺序计算，可原地更新。
* **示例** (同上方程组)：若 $x^{(0)}=(0,0)^T$, 则 $x_1^{(1)}=0.25, x_2^{(1)}=0.75$.
* **收敛条件 (充分)**：$A$ SDD, 或 $A$ 对称正定 (SPD)。

---

## 第八讲：迭代法的收敛性与逐次超松弛法 (SOR)

### 1. 迭代法的收敛性分析 (续)
迭代格式 $x^{(k+1)} = Tx^{(k)} + c$。误差 $e^{(k)} = x^{(k)} - x^\*$。
* **误差传播**：$e^{(k+1)} = Te^{(k)} \implies e^{(k)} = T^k e^{(0)}$。
* **收敛充要条件**：迭代矩阵 $T$ 的谱半径 $\rho(T) < 1$，其中 $\rho(T) = \max_i |\lambda_i(T)|$。
* **收敛充分条件**：若存在某种诱导矩阵范数使 $\|T\| < 1$。
* **收敛速率**：$R = -\log_{10}(\rho(T))$。

### 2. 逐次超松弛法 (Successive Over-Relaxation, SOR)
加速高斯-赛德尔法。设 $\tilde{x}_i^{(k+1)}$ 为高斯-赛德尔建议值。
$$ x_i^{(k+1)} = (1-\omega)x_i^{(k)} + \omega \tilde{x}_i^{(k+1)} $$
其中 $\omega$ 是松弛参数。
* $0 < \omega < 1$：欠松弛。 $\omega = 1$：高斯-赛德尔。 $1 < \omega < 2$：超松弛。
* **SOR迭代公式**：
$$ x_i^{(k+1)} = (1-\omega)x_i^{(k)} + \frac{\omega}{a_{ii}} \left( b_i - \sum_{j=1}^{i-1} a_{ij}x_j^{(k+1)} - \sum_{j=i+1}^{n} a_{ij}x_j^{(k)} \right) $$
* **最优 $\omega$ ($\omega_{\text{opt}}$)**：存在使 $\rho(T_{SOR})$ 最小的 $\omega_{\text{opt}}$，但通常难求。
* **收敛条件**：必要条件 $0 < \omega < 2$。若 $A$ SPD 且 $0 < \omega < 2$，则SOR收敛。
* **示例** (同上方程组，$\omega=1.1$)：若 $x^{(0)}=(0,0)^T$,则 $x^{(1)}=(0.275, 0.8342)^T$.

### 3. 迭代法小结 (雅可比, 高斯-赛德尔, SOR)

| 方法         | 迭代矩阵 $T$ (基于 $A=D-L-U$)       | 每步计算 (稀疏)     | 主要收敛条件 (充分)      |
| :----------- | :-------------------------------------- | :-------------------- | :----------------------- |
| 雅可比       | $D^{-1}(L+U)$                           | $O(N_{nz})$           | $A$ SDD                  |
| 高斯-赛德尔  | $(D-L)^{-1}U$                           | $O(N_{nz})$           | $A$ SDD, 或 $A$ SPD      |
| SOR          | $(D-\omega L)^{-1}((1-\omega)D + \omega U)$ | $O(N_{nz})$           | $A$ SPD 且 $0<\omega<2$  |

($N_{nz}$ 表示 $A$ 中非零元素数)

---

## 第九讲：插值法 (一) —— 基本概念与拉格朗日插值

### 1. 什么是插值 (Interpolation)？
给定 $n+1$ 个离散数据点 $(x_0, y_0), \dots, (x_n, y_n)$ ($x_i$ 互异)，插值旨在找到函数 $P(x)$，使得 $P(x_i) = y_i$。
* **目的**：估计未知点函数值、函数近似、数值方法基础。
* **与拟合的区别**：插值精确通过数据点；拟合寻找最佳趋势。

### 2. 多项式插值 (Polynomial Interpolation)
* **优点**：易计算、求导、积分；光滑；Weierstrass逼近定理。
* **存在性与唯一性**：对于 $n+1$ 个互异节点，存在唯一的次数 $\le n$ 的多项式 $P_n(x)$ 通过这些点。

### 3. 构造插值多项式的方法

#### 3.1 方法一：解线性方程组 (范德蒙矩阵)
设 $P_n(x) = \sum a_j x^j$。代入 $P_n(x_i)=y_i$ 得 $Va=y$，其中 $V$ 是范德蒙矩阵。
* **缺点**：计算量大；范德蒙矩阵常病态。

#### 3.2 方法二：拉格朗日插值多项式
$P_n(x) = \sum_{k=0}^n y_k L_{n,k}(x)$，其中拉格朗日基多项式：
$$ L_{n,k}(x) = \prod_{j=0, j \neq k}^{n} \frac{x - x_j}{x_k - x_j}, \quad \text{满足 } L_{n,k}(x_j) = \delta_{kj} $$
* **示例 (二次插值)**：给定点 $(0,1), (1,3), (2,2)$，则 $P_2(x) = -1.5x^2 + 3.5x + 1$.
* **优缺点**：优点是公式直观；缺点是计算量大，增加新点需重算。

---

## 第十讲：插值法 (二) —— 牛顿均差插值与插值误差

### 1. 牛顿插值多项式的形式
$$ P_n(x) = c_0 + c_1(x-x_0) + c_2(x-x_0)(x-x_1) + \dots + c_n(x-x_0)\dots(x-x_{n-1}) $$
系数 $c_k = f[x_0, x_1, \dots, x_k]$ 是均差。

### 2. 均差 (Divided Differences)
* 零阶：$f[x_i] = y_i$
* 一阶：$f[x_i, x_j] = \frac{f[x_j] - f[x_i]}{x_j - x_i}$
* $k$阶递归：$$f[x_j, \dots, x_{j+k}] = \frac{f[x_{j+1}, \dots, x_{j+k}] - f[x_j, \dots, x_{j+k-1}]}{x_{j+k} - x_j}$$
均差表可系统计算系数。

### 3. 用均差表构造牛顿插值多项式
**示例**：点 $(0,1), (1,3), (2,2)$。

$c_0 = f[0] = 1$; $c_1 = f[0, 1] = 2$; $c_2 = f[0, 1, 2] = -1.5$.

$P_2(x) = 1 + 2(x-0) - 1.5(x-0)(x-1) = -1.5x^2 + 3.5x + 1$.

### 4. 牛顿形式的优点
* **高效求值**：Horner法则，$O(n)$。
* **方便添加新数据点**：$P_{n+1}(x) = P_n(x) + c_{n+1}\prod_{i=0}^n (x-x_i)$。

### 5. 多项式插值的误差
误差 $E_n(x) = f(x) - P_n(x)$。
**插值误差定理**：若 $f$ 有 $n+1$ 阶连续导数，则 $\exists \xi$ 使得：
$$ E_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!} \prod_{i=0}^n (x-x_i) $$
* **解读**：误差与 $f^{(n+1)}(\xi)$ 和节点乘积项 $\prod (x-x_i)$ 有关。
* **龙格现象 (Runge's Phenomenon)**：高次多项式插值在等距节点上可能在区间端点处剧烈振荡。

---


```tex
\documentclass[UTF8]{ctexart}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\usepackage{geometry}
\usepackage{booktabs} % For better tables
\usepackage{array}    % For better column definitions in tables

\geometry{a4paper, margin=1in}

\title{数值分析学习笔记 (第六至十讲汇总)}
\author{课程内容整理}
\date{2025年5月15日}

\begin{document}

\maketitle
\tableofcontents
\newpage

% --- Lecture 6 Content ---
\section{第六讲：线性方程组的误差分析与条件数的影响}

\subsection*{1. 回顾与背景}
在求解线性方程组 $Ax=b$ 时，输入数据 $A, b$ 的不精确性或计算过程中的舍入误差都会影响解的精度。条件数 $\kappa(A) = \|A\| \cdot \|A^{-1}\|$ ($\kappa(A) \ge 1$) 是衡量这种敏感性的关键指标。
\begin{itemize}
    \item $\kappa(A)$ 接近 1：矩阵 $A$ 是良态的 (well-conditioned)。
    \item $\kappa(A)$ 很大：矩阵 $A$ 是病态的 (ill-conditioned)。
\end{itemize}

\subsection*{2. 右端项 $b$ 的扰动对解的影响}
设 $A$ 精确且非奇异， $b$ 有扰动 $\Delta b$。
原系统：$Ax=b$。
扰动后系统：$A(x+\Delta x) = b + \Delta b$。
推导可得：
$$ \boxed{\frac{\|\Delta x\|}{\|x\|} \le \kappa(A) \frac{\|\Delta b\|}{\|b\|}} $$
\textbf{解读}：解 $x$ 的相对误差上界是右端项 $b$ 的相对扰动乘以条件数 $\kappa(A)$。

\subsection*{3. 系数矩阵 $A$ 的扰动对解的影响}
设 $b$ 精确，$A$ 有扰动 $\Delta A$。
原系统：$Ax=b$。
扰动后系统：$(A+\Delta A)(x+\Delta x) = b$。
推导可得 (若 $x+\Delta x \neq 0$):
$$ \boxed{\frac{\|\Delta x\|}{\|x+\Delta x\|} \le \kappa(A) \frac{\|\Delta A\|}{\|A\|}} $$
\textbf{解读}：解 $x$ 的相对变化上界是系数矩阵 $A$ 的相对扰动乘以条件数 $\kappa(A)$。

\subsection*{4. $A$ 和 $b$ 同时存在扰动}
若 $(A+\Delta A)(x+\Delta x) = b+\Delta b$，且 $\kappa(A) \frac{\|\Delta A\|}{\|A\|} < 1$，则有：
$$ \frac{\|\Delta x\|}{\|x\|} \le \frac{\kappa(A)}{1 - \kappa(A) \frac{\|\Delta A\|}{\|A\|}} \left( \frac{\|\Delta A\|}{\|A\|} + \frac{\|\Delta b\|}{\|b\|} \right) $$

\subsection*{5. 残差 (Residual) 与误差 (Error)}
对于近似解 $\tilde{x}$，误差 $e = x - \tilde{x}$，残差 $r = b - A\tilde{x}$。
可以推导出：
$$ \frac{\|e\|}{\|x\|} \le \kappa(A) \frac{\|r\|}{\|A\|\|x\|} \quad \text{或近似地} \quad \frac{\|e\|}{\|x\|} \le \kappa(A) \frac{\|r\|}{\|b\|} $$
\textbf{关键结论}：即使相对残差很小，如果条件数 $\kappa(A)$ 很大，解的相对误差仍然可能很大。

\subsection*{6. 条件数的实际意义与精度损失}
若 $\kappa(A) \approx 10^k$，并且计算精度为 $p$ 位有效数字，则解 $x$ 中可靠的有效数字大约只有 $p-k$ 位。

\subsection*{7. 如何估计条件数}
直接计算 $A^{-1}$ 代价高。实际中，数值库 (如 LAPACK) 提供了高效的条件数估计器，通常在 $LU$ 分解后，用 $O(n^2)$ 的额外计算量来估计。

\newpage
% --- Lecture 7 Content ---
\section{第七讲：线性方程组的迭代法 (一) —— 基本概念、雅可比法与高斯-赛德尔法}

\subsection*{1. 迭代法的基本思想}
对于大型稀疏线性方程组 $Ax=b$，迭代法提供了一种替代直接法的方案。
\begin{itemize}
    \item \textbf{核心思想}：从初始猜测 $x^{(0)}$ 开始，通过迭代规则 $x^{(k+1)} = f(x^{(k)})$ 生成序列 $x^{(1)}, x^{(2)}, \dots$，若收敛则逼近真解 $x$。
    \item \textbf{一般形式}：将 $A$ 分裂为 $A=M-N$ ($M$ 易求逆)，则 $Mx=Nx+b$。迭代格式为 $Mx^{(k+1)} = Nx^{(k)} + b$，即 $x^{(k+1)} = M^{-1}Nx^{(k)} + M^{-1}b = Tx^{(k)} + c$。
    \item \textbf{优点}：能利用矩阵稀疏性，每步计算量小，内存需求低，可控精度。
    \item \textbf{收敛性}：不保证收敛，依赖于迭代矩阵 $T$ 的性质（如谱半径 $\rho(T)<1$）。
    \item \textbf{停止条件}：基于解的连续变化、残差大小或最大迭代次数。
\end{itemize}

\subsection*{2. 雅可比法 (Jacobi Method)}
将 $A=D-L-U$（$D$ 为对角阵，$-L$ 为严格下三角，$-U$ 为严格上三角）。
迭代公式：$Dx^{(k+1)} = (L+U)x^{(k)} + b$，即（假设 $a_{ii} \neq 0$）：
$$x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j=1, j \neq i}^{n} a_{ij}x_j^{(k)} \right), \quad i=1, \dots, n$$
\begin{itemize}
    \item \textbf{实现}：$x^{(k+1)}$ 的各分量可独立计算（并行性好）。
    \item \textbf{示例}：$\begin{cases} 4x_1 - x_2 = 1 \\ -x_1 + 3x_2 = 2 \end{cases}$. 若 $x^{(0)}=(0,0)^T$, 则 $x^{(1)}=(0.25, 0.6667)^T$.
    \item \textbf{收敛条件 (充分)}：$A$ 严格对角占优 (SDD)。
\end{itemize}

\subsection*{3. 高斯-赛德尔法 (Gauss-Seidel Method)}
计算 $x_i^{(k+1)}$ 时使用本轮已更新的 $x_j^{(k+1)}$ ($j<i$)。
迭代公式：$(D-L)x^{(k+1)} = Ux^{(k)} + b$，即：
$$x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j=1}^{i-1} a_{ij}x_j^{(k+1)} - \sum_{j=i+1}^{n} a_{ij}x_j^{(k)} \right), \quad i=1, \dots, n$$
\begin{itemize}
    \item \textbf{实现}：顺序计算，可原地更新。
    \item \textbf{示例} (同上方程组)：若 $x^{(0)}=(0,0)^T$, 则 $x_1^{(1)}=0.25, x_2^{(1)}=0.75$.
    \item \textbf{收敛条件 (充分)}：$A$ SDD, 或 $A$ 对称正定 (SPD)。
\end{itemize}

\newpage
% --- Lecture 8 Content ---
\section{第八讲：迭代法的收敛性与逐次超松弛法 (SOR)}

\subsection*{1. 迭代法的收敛性分析 (续)}
迭代格式 $x^{(k+1)} = Tx^{(k)} + c$。误差 $e^{(k)} = x^{(k)} - x^*$。
\begin{itemize}
    \item \textbf{误差传播}：$e^{(k+1)} = Te^{(k)} \implies e^{(k)} = T^k e^{(0)}$。
    \item \textbf{收敛充要条件}：迭代矩阵 $T$ 的谱半径 $\rho(T) < 1$，其中 $\rho(T) = \max_i |\lambda_i(T)|$。
    \item \textbf{收敛充分条件}：若存在某种诱导矩阵范数使 $\|T\| < 1$。
    \item \textbf{收敛速率}：$R = -\log_{10}(\rho(T))$。
\end{itemize}

\subsection*{2. 逐次超松弛法 (Successive Over-Relaxation, SOR)}
加速高斯-赛德尔法。设 $\tilde{x}_i^{(k+1)}$ 为高斯-赛德尔建议值。
$$x_i^{(k+1)} = (1-\omega)x_i^{(k)} + \omega \tilde{x}_i^{(k+1)}$$
其中 $\omega$ 是松弛参数。
\begin{itemize}
    \item $0 < \omega < 1$：欠松弛。 $\omega = 1$：高斯-赛德尔。 $1 < \omega < 2$：超松弛。
    \item \textbf{SOR迭代公式}：
    $$x_i^{(k+1)} = (1-\omega)x_i^{(k)} + \frac{\omega}{a_{ii}} \left( b_i - \sum_{j=1}^{i-1} a_{ij}x_j^{(k+1)} - \sum_{j=i+1}^{n} a_{ij}x_j^{(k)} \right)$$
    \item \textbf{最优 $\omega$ ($\omega_{\text{opt}}$)}：存在使 $\rho(T_{SOR})$ 最小的 $\omega_{\text{opt}}$，但通常难求。
    \item \textbf{收敛条件}：必要条件 $0 < \omega < 2$。若 $A$ SPD 且 $0 < \omega < 2$，则SOR收敛。
    \item \textbf{示例} (同上方程组，$\omega=1.1$)：若 $x^{(0)}=(0,0)^T$,则 $x^{(1)}=(0.275, 0.8342)^T$.
\end{itemize}

\subsection*{3. 迭代法小结 (雅可比, 高斯-赛德尔, SOR)}
\begin{table}[h!]
\centering
\begin{tabular}{llll}
\toprule
方法 & 迭代矩阵 $T$  & 每步计算 (稀疏) & 主要收敛条件 (充分) \\
     & (基于 $A=D-L-U$) & & \\
\midrule
雅可比 & $D^{-1}(L+U)$ & $O(N_{nz})$ & $A$ SDD \\
高斯-赛德尔 & $(D-L)^{-1}U$ & $O(N_{nz})$ & $A$ SDD, 或 $A$ SPD \\
SOR & $(D-\omega L)^{-1}((1-\omega)D + \omega U)$ & $O(N_{nz})$ & $A$ SPD 且 $0<\omega<2$ \\
\bottomrule
\end{tabular}
\caption{基础迭代法比较 ($N_{nz}$ 为 $A$ 中非零元素数)}
\end{table}

\newpage
% --- Lecture 9 Content ---
\section{第九讲：插值法 (一) —— 基本概念与拉格朗日插值}

\subsection*{1. 什么是插值 (Interpolation)？}
给定 $n+1$ 个离散数据点 $(x_0, y_0), \dots, (x_n, y_n)$ ($x_i$ 互异)，插值旨在找到函数 $P(x)$，使得 $P(x_i) = y_i$。
\begin{itemize}
    \item \textbf{目的}：估计未知点函数值、函数近似、数值方法基础。
    \item \textbf{与拟合的区别}：插值精确通过数据点；拟合寻找最佳趋势。
\end{itemize}

\subsection*{2. 多项式插值 (Polynomial Interpolation)}
\begin{itemize}
    \item \textbf{优点}：易计算、求导、积分；光滑；Weierstrass逼近定理。
    \item \textbf{存在性与唯一性}：对于 $n+1$ 个互异节点，存在唯一的次数 $\le n$ 的多项式 $P_n(x)$ 通过这些点。
\end{itemize}

\subsection*{3. 构造插值多项式的方法}
\subsubsection*{3.1 方法一：解线性方程组 (范德蒙矩阵)}
设 $P_n(x) = \sum a_j x^j$。代入 $P_n(x_i)=y_i$ 得 $Va=y$，其中 $V$ 是范德蒙矩阵。
\begin{itemize}
    \item \textbf{缺点}：计算量大；范德蒙矩阵常病态。
\end{itemize}

\subsubsection*{3.2 方法二：拉格朗日插值多项式}
$P_n(x) = \sum_{k=0}^n y_k L_{n,k}(x)$，其中拉格朗日基多项式：
$$L_{n,k}(x) = \prod_{j=0, j \neq k}^{n} \frac{x - x_j}{x_k - x_j}, \quad \text{满足 } L_{n,k}(x_j) = \delta_{kj}$$
\begin{itemize}
    \item \textbf{示例 (二次插值)}：给定点 $(0,1), (1,3), (2,2)$，则 $P_2(x) = -1.5x^2 + 3.5x + 1$.
    \item \textbf{优缺点}：优点是公式直观；缺点是计算量大，增加新点需重算。
\end{itemize}

\newpage
% --- Lecture 10 Content ---
\section{第十讲：插值法 (二) —— 牛顿均差插值与插值误差}

\subsection*{1. 牛顿插值多项式的形式}
$P_n(x) = c_0 + c_1(x-x_0) + c_2(x-x_0)(x-x_1) + \dots + c_n(x-x_0)\dots(x-x_{n-1})$
系数 $c_k = f[x_0, x_1, \dots, x_k]$ 是均差。

\subsection*{2. 均差 (Divided Differences)}
\begin{itemize}
    \item 零阶：$f[x_i] = y_i$
    \item 一阶：$f[x_i, x_j] = \frac{f[x_j] - f[x_i]}{x_j - x_i}$
    \item $k$阶递归：$f[x_j, \dots, x_{j+k}] = \frac{f[x_{j+1}, \dots, x_{j+k}] - f[x_j, \dots, x_{j+k-1}]}{x_{j+k} - x_j}$
\end{itemize}
均差表可系统计算系数。

\subsection*{3. 用均差表构造牛顿插值多项式}
\textbf{示例}：点 $(0,1), (1,3), (2,2)$。
$c_0 = f[0] = 1$; $c_1 = f[0, 1] = 2$; $c_2 = f[0, 1, 2] = -1.5$.
$P_2(x) = 1 + 2(x-0) - 1.5(x-0)(x-1) = -1.5x^2 + 3.5x + 1$.

\subsection*{4. 牛顿形式的优点}
\begin{itemize}
    \item \textbf{高效求值}：Horner法则，$O(n)$。
    \item \textbf{方便添加新数据点}：$P_{n+1}(x) = P_n(x) + c_{n+1}\prod_{i=0}^n (x-x_i)$。
\end{itemize}

\subsection*{5. 多项式插值的误差}
误差 $E_n(x) = f(x) - P_n(x)$。
\textbf{插值误差定理}：若 $f$ 有 $n+1$ 阶连续导数，则 $\exists \xi$ 使得：
$$E_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!} \prod_{i=0}^n (x-x_i)$$
\begin{itemize}
    \item \textbf{解读}：误差与 $f^{(n+1)}(\xi)$ 和节点乘积项 $\prod (x-x_i)$ 有关。
    \item \textbf{龙格现象 (Runge's Phenomenon)}：高次多项式插值在等距节点上可能在区间端点处剧烈振荡。
\end{itemize}

\end{document}
```