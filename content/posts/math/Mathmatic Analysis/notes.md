---
author: "ybw051114"
author_link: "hugo.ybw051114.cf"
title: "Notes"
date: 2025-05-14T17:22:15+08:00
lastmod: 2025-05-14T17:22:15+08:00
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
math: true
lightgallery: true
linkToMarkdown: true
share:
  enable: true
comment: true
---

# 课程引言：什么是数值分析？ {#课程引言什么是数值分析 .unnumbered}

数值分析是一门研究如何用计算机来寻找数学问题近似解的学科。其核心思想包括：

-   **近似 (Approximation)**：用计算机可执行的有限步骤逼近真实的数学解。

-   **算法 (Algorithm)**：设计清晰的、一步一步的计算流程。

-   **误差分析 (Error
    Analysis)**：评估近似解与真实解的差距，并控制误差。

我们学习数值分析是为了理解计算机如何处理数学问题，解决实际工程与科学中那些没有解析解或解析解过于复杂的问题，并能明智地选择和使用数值方法。

# 第一讲：数值计算中的"误差"

误差是数值分析中无法回避的伙伴，理解和控制误差至关重要。

## 1.1 误差的来源 (Sources of Error) {#误差的来源-sources-of-error .unnumbered}

-   **模型误差 (Modeling
    Error)**：将现实问题简化为数学模型时产生的误差。

-   **测量误差 (Measurement Error / Data
    Error)**：输入数据本身带有的误差。

-   **截断误差 (Truncation Error)**：用有限过程近似无限过程产生的误差。
    例如，泰勒级数展开
    $e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \dots$，若只取前几项，则被截断部分构成截断误差。

-   **舍入误差 (Round-off Error)**：计算机存储数字位数有限导致的误差。
    例如，$1/3 = 0.33333\dots$ 在计算机中可能被存储为有限位数的小数。

## 1.2 误差的度量 (Measuring Error) {#误差的度量-measuring-error .unnumbered}

设 $p^*$ 为真实值，$p$ 为近似值。

-   **绝对误差 (Absolute Error)**： $E_a = |p^* - p|$

-   **相对误差 (Relative Error)**： $E_r = \frac{|p^* - p|}{|p^*|}$
    (前提 $p^* \neq 0$)

相对误差通常更能反映近似的"质量"。在实际中，若 $p^*$
未知，可用相邻两次迭代结果的差异来近似误差。

## 1.3 数字表示、有效数字与灾难性抵消 {#数字表示有效数字与灾难性抵消 .unnumbered}

计算机通常使用浮点表示法存储实数，其精度有限。

-   **有效数字 (Significant Digits)**：一个数中被认为是可靠的数字。

-   **灾难性抵消 (Catastrophic
    Cancellation)**：两个相近的数相减，可能导致有效数字急剧损失。例如，计算
    $0.1234567 - 0.1234555$，如果精度有限，结果的有效数字位数会显著减少。

## 1.4 误差传播、算法稳定性与问题条件 {#误差传播算法稳定性与问题条件 .unnumbered}

-   **误差传播 (Error
    Propagation)**：初始误差或计算过程中的误差如何影响最终结果。

-   **算法稳定性
    (Stability)**：稳定的算法对初始数据的小扰动不敏感。不稳定的算法会放大误差。

-   **问题条件 (Condition of a Problem)**：

    -   **病态问题 (Ill-conditioned
        problem)**：输入数据的微小变化导致解的巨大变化。

    -   **良态问题 (Well-conditioned
        problem)**：解对输入数据的微小变化不敏感。

稳定性是算法的属性，条件是问题本身的属性。

# 第二讲：方程求根 ($f(x) = 0$)

寻找使得函数 $f(x)$ 值为零的 $x$。

## 2.1 求根方法的分类 {#求根方法的分类 .unnumbered}

-   **区间法 (Bracketing
    Methods)**：如二分法。需要包含根的初始区间，通常稳健。

-   **开区间法 (Open
    Methods)**：如牛顿法、割线法。需要初始猜测点，收敛时较快，但不保证收敛。

## 2.2 二分法 (Bisection Method) {#二分法-bisection-method .unnumbered}

-   **依据**：介值定理。若 $f(x)$ 在 $[a,b]$ 连续且 $f(a)f(b)<0$，则
    $(a,b)$ 内有根。

-   **步骤**：

    1.  给定初始区间 $[a_0, b_0]$ 使得 $f(a_0)f(b_0)<0$，设定容差
        $\epsilon$。

    2.  计算中点 $m = (a_k + b_k)/2$。

    3.  判断根的位置：

        -   若 $f(m) \approx 0$ 或 $|b_k-a_k|/2 < \epsilon$，则 $m$
            为近似根，停止。

        -   若 $f(a_k)f(m) < 0$，则新区间为
            $[a_{k+1}, b_{k+1}] = [a_k, m]$。

        -   否则，新区间为 $[a_{k+1}, b_{k+1}] = [m, b_k]$。

    4.  重复步骤 2-3。

-   **例子**：$f(x) = x^3 - x - 2 = 0$ 在 $[1,2]$ 内的根。
    $a_0=1, f(1)=-2$; $b_0=2, f(2)=4$. $m_0 = 1.5, f(1.5)=-0.125$.
    新区间 $[1.5, 2]$. $m_1 = 1.75, f(1.75) \approx 1.609$. 新区间
    $[1.5, 1.75]$. (以此类推)

-   **特点**：

    -   优点：简单，一定收敛。误差 $|x^* - m_n| \le (b_0-a_0)/2^{n+1}$。

    -   缺点：线性收敛 ($p=1$)，速度慢。不能处理偶数重根。

## 2.3 不动点迭代法 (Fixed-Point Iteration) {#不动点迭代法-fixed-point-iteration .unnumbered}

将 $f(x)=0$ 转化为 $x=g(x)$ 的形式。迭代公式：$x_{i+1} = g(x_i)$。

-   **收敛条件**：若在根 $x^*$ 附近 $|g'(x)| \le L < 1$，则迭代收敛。

-   **例子**：$f(x) = x^2 - 2x - 3 = 0$。 若
    $x = \sqrt{2x+3} = g_1(x)$，对于根
    $x^*=3$，$g_1'(3)=1/3 < 1$，收敛。 若
    $x = (x^2-3)/2 = g_2(x)$，对于根 $x^*=3$，$g_2'(3)=3 > 1$，发散。

## 2.4 牛顿-拉夫逊法 (Newton-Raphson Method) {#牛顿-拉夫逊法-newton-raphson-method .unnumbered}

利用函数在 $x_i$ 处的切线与x轴的交点 $x_{i+1}$ 作为新的近似根。

-   **迭代公式**：$x_{i+1} = x_i - \frac{f(x_i)}{f'(x_i)}$

-   **例子**：$f(x) = x^3 - x - 2 = 0$, $f'(x) = 3x^2 - 1$. 若
    $x_0 = 1.5, f(1.5)=-0.125, f'(1.5)=5.75$.
    $x_1 = 1.5 - (-0.125)/5.75 \approx 1.521739$. (收敛非常快)

-   **特点**：

    -   优点：若收敛，则为二次收敛 ($p=2$)，速度快。

    -   缺点：需计算导数 $f'(x)$。若 $f'(x_i) \approx 0$
        或初值不好则可能不收敛。对重根收敛变慢。

### 2.4.1 牛顿法二次收敛性证明 {#牛顿法二次收敛性证明 .unnumbered}

设 $x^*$ 为根，$f(x^*)=0$。误差 $e_i = x_i - x^*$。
$x_{i+1} = x_i - \frac{f(x_i)}{f'(x_i)}$
$e_{i+1} = x_{i+1} - x^* = e_i - \frac{f(x_i)}{f'(x_i)}$ 对
$f(x_i) = f(x^*+e_i)$ 在 $x^*$ 处泰勒展开：
$f(x_i) = f(x^*) + e_i f'(x^*) + \frac{e_i^2}{2} f''(x^*) + O(e_i^3) = e_i f'(x^*) + \frac{e_i^2}{2} f''(x^*) + O(e_i^3)$
对 $f'(x_i) = f'(x^*+e_i)$ 在 $x^*$ 处泰勒展开：
$f'(x_i) = f'(x^*) + e_i f''(x^*) + O(e_i^2)$ 代入 $e_{i+1}$ 表达式：
$e_{i+1} = e_i - \frac{e_i f'(x^*) + \frac{e_i^2}{2} f''(x^*) + O(e_i^3)}{f'(x^*) + e_i f''(x^*) + O(e_i^2)}$
$e_{i+1} = e_i - \frac{1}{f'(x^*)} \left(e_i f'(x^*) + \frac{e_i^2}{2} f''(x^*)\right) \left(1 - e_i \frac{f''(x^*)}{f'(x^*)} + O(e_i^2)\right)$
整理后得到： $e_{i+1} = \frac{f''(x^*)}{2f'(x^*)} e_i^2 + O(e_i^3)$
这表明 $e_{i+1} \propto e_i^2$，即二次收敛（需 $f'(x^*) \neq 0$）。

## 2.5 割线法 (Secant Method) {#割线法-secant-method .unnumbered}

用过点 $(x_{i-1}, f(x_{i-1}))$ 和 $(x_i, f(x_i))$ 的割线斜率近似
$f'(x_i)$。 $f'(x_i) \approx \frac{f(x_i) - f(x_{i-1})}{x_i - x_{i-1}}$

-   **迭代公式**：$x_{i+1} = x_i - f(x_i) \frac{x_i - x_{i-1}}{f(x_i) - f(x_{i-1})}$

-   **例子**：$f(x) = x^3 - x - 2 = 0$. $x_0=1, f(1)=-2$;
    $x_1=2, f(2)=4$.
    $x_2 = 2 - 4 \frac{2-1}{4-(-2)} = 4/3 \approx 1.3333$.

-   **特点**：

    -   优点：无需计算导数。收敛速度超线性
        ($p \approx 1.618$)，快于线性但慢于二次。

    -   缺点：需两个初值，不保证收敛。

## 2.6 求根方法比较 {#求根方法比较 .unnumbered}

  特性       二分法              不动点迭代       牛顿法               割线法
  ---------- ------------------- ---------------- -------------------- ----------------------------
  收敛保证   是 (若初区间含根)   否 (依赖$g'$)    否 (依赖初值/$f'$)   否 (依赖初值)
  收敛速度   线性 ($p=1$)        通常线性         二次 ($p=2$)         超线性 ($p \approx 1.618$)
  所需信息   $f(x)$, 区间        $g(x)$           $f(x), f'(x), x_0$   $f(x), x_0, x_1$
  主要优点   稳健                理论基础         收敛快               无需导数，较快
  主要缺点   慢，需初区间        $g(x)$选取关键   需导数，可能不收敛   需两初值，可能不收敛

  : 求根方法比较

# 第三、四讲：求解线性方程组 (直接法)

求解形如 $Ax=b$ 的方程组。

## 3.1 高斯消元法 (Gaussian Elimination) {#高斯消元法-gaussian-elimination .unnumbered}

-   **核心思想**：

    1.  **前向消元 (Forward Elimination)**：用基本行变换将增广矩阵
        $[A|b]$ 化为上三角形式 $[U|b']$。

    2.  **回代 (Back Substitution)**：从 $Ux=b'$ 中解出 $x$。

-   **基本行变换**：1) 交换两行；2) 一行乘以非零常数；3)
    一行的倍数加到另一行。

-   **示例**：求解
    $\begin{cases} 2x_1 + x_2 - x_3 = 8 \\ -3x_1 - x_2 + 2x_3 = -11 \\ -2x_1 + x_2 + 2x_3 = -3 \end{cases}$
    增广矩阵：$\left( \begin{smallmatrix} 2 & 1 & -1 & | & 8 \\ -3 & -1 & 2 & | & -11 \\ -2 & 1 & 2 & | & -3 \end{smallmatrix} \right)$
    $R_2 \leftarrow R_2 + 1.5 R_1$, $R_3 \leftarrow R_3 + 1 R_1$ 变为
    $\left( \begin{smallmatrix} 2 & 1 & -1 & | & 8 \\ 0 & 0.5 & 0.5 & | & 1 \\ 0 & 2 & 1 & | & 5 \end{smallmatrix} \right)$
    $R_3 \leftarrow R_3 - 4 R_2$ 变为
    $\left( \begin{smallmatrix} 2 & 1 & -1 & | & 8 \\ 0 & 0.5 & 0.5 & | & 1 \\ 0 & 0 & -1 & | & 1 \end{smallmatrix} \right)$
    回代得到 $x_3=-1, x_2=3, x_1=2$。

## 3.2 主元选择 (Pivoting) {#主元选择-pivoting .unnumbered}

解决主元为零或过小导致数值不稳定的问题。

-   **部分选主元法 (Partial Pivoting)**：在第 $k$ 步消元前，从当前第 $k$
    列对角线及以下元素中选取绝对值最大的元素作为主元，并通过行交换将其移至主元位置。

-   **好处**：避免除零，减小舍入误差 (保证乘数
    $|m_{ik}| \le 1$)，提高数值稳定性。

-   **示例**：$\begin{cases} 0x_1 + x_2 + x_3 = 2 \\ 2x_1 + 2x_2 - x_3 = 3 \\ x_1 - x_2 + 3x_3 = 3 \end{cases}$
    初始 $a_{11}=0$. 搜索第1列，发现 $a_{21}=2$ 绝对值最大。交换
    $R_1 \leftrightarrow R_2$。
    $\left( \begin{smallmatrix} 2 & 2 & -1 & | & 3 \\ 0 & 1 & 1 & | & 2 \\ 1 & -1 & 3 & | & 3 \end{smallmatrix} \right)$,
    然后继续消元。

## 3.3 LU 分解 (LU Decomposition) {#lu-分解-lu-decomposition .unnumbered}

将矩阵 $A$ 分解为 $A=LU$，其中 $L$ 是下三角矩阵，$U$ 是上三角矩阵。

-   **Doolittle 形式**：$L$ 的对角线元素为1。$U$
    是高斯消元后的上三角阵，$L$ 的严格下三角元素是消元过程中的乘数。

-   **求解 $Ax=b$**：

    1.  若 $A=LU$, 则 $LUx=b$. 令 $y=Ux$.

    2.  解 $Ly=b$ (前向替换)。

    3.  解 $Ux=y$ (回代)。

-   **用途**：高效处理多个右端项 $b$；计算行列式 ($\det(A)=\det(U)$ for
    Doolittle)；计算逆矩阵。

-   **示例** (Doolittle):
    $A = \begin{pmatrix} 2 & 1 & -1 \\ -2 & 1 & 3 \\ 4 & -2 & 1 \end{pmatrix}$.
    高斯消元得 $m_{21}=-1, m_{31}=2, m_{32}=-2$.
    $L = \begin{pmatrix} 1 & 0 & 0 \\ -1 & 1 & 0 \\ 2 & -2 & 1 \end{pmatrix}$,
    $U = \begin{pmatrix} 2 & 1 & -1 \\ 0 & 2 & 2 \\ 0 & 0 & 7 \end{pmatrix}$.

-   **带主元选择的LU分解**：$PA=LU$，其中 $P$ 是置换矩阵，记录行交换。
    求解 $Ax=b \implies PAx=Pb$. 令 $y=Ux$. 1. 解 $Ly=Pb$. 2. 解 $Ux=y$.

-   **计算复杂度**：分解 $O(2n^3/3)$，替换 $O(n^2)$。

# 第五讲：线性方程组的敏感性分析 (初步)

衡量解对数据扰动的敏感程度。

## 4.1 向量范数 (Vector Norms) {#向量范数-vector-norms .unnumbered}

衡量向量"长度"或"幅度"。对于向量 $x=(x_1, \dots, x_n)^T$：

-   $L_1$-范数: $\|x\|_1 = \sum_{i=1}^n |x_i|$

-   $L_2$-范数 (欧几里得范数): $\|x\|_2 = \sqrt{\sum_{i=1}^n x_i^2}$

-   $L_\infty$-范数 (最大范数):
    $\|x\|_\infty = \max_{1 \le i \le n} |x_i|$

**示例**: $x=(1, -2, 3)^T$.
$\|x\|_1=6, \|x\|_2=\sqrt{14}, \|x\|_\infty=3$.

## 4.2 矩阵范数 (Matrix Norms) {#矩阵范数-matrix-norms .unnumbered}

衡量矩阵"大小"或"放大能力"。由向量范数诱导的算子范数：$\|A\| = \max_{\|x\|=1} \|Ax\|$.

-   $\|A\|_1$ (最大绝对列和): $\max_{j} \sum_{i} |a_{ij}|$

-   $\|A\|_\infty$ (最大绝对行和): $\max_{i} \sum_{j} |a_{ij}|$

-   $\|A\|_2$ (谱范数): $A$ 的最大奇异值 $\sigma_{\max}(A)$.

**示例**: $A = \begin{pmatrix} 1 & -2 \\ 3 & 0 \end{pmatrix}$.
$\|A\|_1 = \max(|1|+|3|, |-2|+|0|) = \max(4,2) = 4$.
$\|A\|_\infty = \max(|1|+|-2|, |3|+|0|) = \max(3,3) = 3$.

## 4.3 条件数 (Condition Number) - 初步介绍 {#条件数-condition-number---初步介绍 .unnumbered}

衡量矩阵 $A$ (或线性系统 $Ax=b$) 病态程度的指标。
$$\kappa(A) = \|A\| \cdot \|A^{-1}\|$$ (使用同一种诱导范数)。

-   $\kappa(A) \ge 1$.

-   若 $\kappa(A)$ 接近 1, $A$ 是良态的 (well-conditioned)。

-   若 $\kappa(A)$ 很大, $A$ 是病态的 (ill-conditioned)，解对扰动敏感。



```tex
\documentclass[UTF8]{ctexart}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\usepackage{geometry}
\usepackage{booktabs} % For better tables
\usepackage{array}    % For better column definitions in tables

\geometry{a4paper, margin=1in}

\title{数值分析学习笔记}
\author{课程讲解内容整理}
\date{\today}

\begin{document}

\maketitle
\tableofcontents
\newpage

\section*{课程引言：什么是数值分析？}
数值分析是一门研究如何用计算机来寻找数学问题近似解的学科。其核心思想包括：
\begin{itemize}
    \item \textbf{近似 (Approximation)}：用计算机可执行的有限步骤逼近真实的数学解。
    \item \textbf{算法 (Algorithm)}：设计清晰的、一步一步的计算流程。
    \item \textbf{误差分析 (Error Analysis)}：评估近似解与真实解的差距，并控制误差。
\end{itemize}
我们学习数值分析是为了理解计算机如何处理数学问题，解决实际工程与科学中那些没有解析解或解析解过于复杂的问题，并能明智地选择和使用数值方法。

\section{第一讲：数值计算中的“误差”}
误差是数值分析中无法回避的伙伴，理解和控制误差至关重要。

\subsection*{1.1 误差的来源 (Sources of Error)}
\begin{itemize}
    \item \textbf{模型误差 (Modeling Error)}：将现实问题简化为数学模型时产生的误差。
    \item \textbf{测量误差 (Measurement Error / Data Error)}：输入数据本身带有的误差。
    \item \textbf{截断误差 (Truncation Error)}：用有限过程近似无限过程产生的误差。
        例如，泰勒级数展开 $e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \dots$，若只取前几项，则被截断部分构成截断误差。
    \item \textbf{舍入误差 (Round-off Error)}：计算机存储数字位数有限导致的误差。
        例如，$1/3 = 0.33333\dots$ 在计算机中可能被存储为有限位数的小数。
\end{itemize}

\subsection*{1.2 误差的度量 (Measuring Error)}
设 $p^*$ 为真实值，$p$ 为近似值。
\begin{itemize}
    \item \textbf{绝对误差 (Absolute Error)}： $E_a = |p^* - p|$
    \item \textbf{相对误差 (Relative Error)}： $E_r = \frac{|p^* - p|}{|p^*|}$ (前提 $p^* \neq 0$)
\end{itemize}
相对误差通常更能反映近似的“质量”。在实际中，若 $p^*$ 未知，可用相邻两次迭代结果的差异来近似误差。

\subsection*{1.3 数字表示、有效数字与灾难性抵消}
计算机通常使用浮点表示法存储实数，其精度有限。
\begin{itemize}
    \item \textbf{有效数字 (Significant Digits)}：一个数中被认为是可靠的数字。
    \item \textbf{灾难性抵消 (Catastrophic Cancellation)}：两个相近的数相减，可能导致有效数字急剧损失。例如，计算 $0.1234567 - 0.1234555$，如果精度有限，结果的有效数字位数会显著减少。
\end{itemize}

\subsection*{1.4 误差传播、算法稳定性与问题条件}
\begin{itemize}
    \item \textbf{误差传播 (Error Propagation)}：初始误差或计算过程中的误差如何影响最终结果。
    \item \textbf{算法稳定性 (Stability)}：稳定的算法对初始数据的小扰动不敏感。不稳定的算法会放大误差。
    \item \textbf{问题条件 (Condition of a Problem)}：
        \begin{itemize}
            \item \textbf{病态问题 (Ill-conditioned problem)}：输入数据的微小变化导致解的巨大变化。
            \item \textbf{良态问题 (Well-conditioned problem)}：解对输入数据的微小变化不敏感。
        \end{itemize}
\end{itemize}
稳定性是算法的属性，条件是问题本身的属性。

\section{第二讲：方程求根 ($f(x) = 0$)}
寻找使得函数 $f(x)$ 值为零的 $x$。

\subsection*{2.1 求根方法的分类}
\begin{itemize}
    \item \textbf{区间法 (Bracketing Methods)}：如二分法。需要包含根的初始区间，通常稳健。
    \item \textbf{开区间法 (Open Methods)}：如牛顿法、割线法。需要初始猜测点，收敛时较快，但不保证收敛。
\end{itemize}

\subsection*{2.2 二分法 (Bisection Method)}
\begin{itemize}
    \item \textbf{依据}：介值定理。若 $f(x)$ 在 $[a,b]$ 连续且 $f(a)f(b)<0$，则 $(a,b)$ 内有根。
    \item \textbf{步骤}：
        \begin{enumerate}
            \item 给定初始区间 $[a_0, b_0]$ 使得 $f(a_0)f(b_0)<0$，设定容差 $\epsilon$。
            \item 计算中点 $m = (a_k + b_k)/2$。
            \item 判断根的位置：
                \begin{itemize}
                    \item 若 $f(m) \approx 0$ 或 $|b_k-a_k|/2 < \epsilon$，则 $m$ 为近似根，停止。
                    \item 若 $f(a_k)f(m) < 0$，则新区间为 $[a_{k+1}, b_{k+1}] = [a_k, m]$。
                    \item 否则，新区间为 $[a_{k+1}, b_{k+1}] = [m, b_k]$。
                \end{itemize}
            \item 重复步骤 2-3。
        \end{enumerate}
    \item \textbf{例子}：$f(x) = x^3 - x - 2 = 0$ 在 $[1,2]$ 内的根。
        $a_0=1, f(1)=-2$; $b_0=2, f(2)=4$.
        $m_0 = 1.5, f(1.5)=-0.125$. 新区间 $[1.5, 2]$.
        $m_1 = 1.75, f(1.75) \approx 1.609$. 新区间 $[1.5, 1.75]$. (以此类推)
    \item \textbf{特点}：
        \begin{itemize}
            \item 优点：简单，一定收敛。误差 $|x^* - m_n| \le (b_0-a_0)/2^{n+1}$。
            \item 缺点：线性收敛 ($p=1$)，速度慢。不能处理偶数重根。
        \end{itemize}
\end{itemize}

\subsection*{2.3 不动点迭代法 (Fixed-Point Iteration)}
将 $f(x)=0$ 转化为 $x=g(x)$ 的形式。迭代公式：$x_{i+1} = g(x_i)$。
\begin{itemize}
    \item \textbf{收敛条件}：若在根 $x^*$ 附近 $|g'(x)| \le L < 1$，则迭代收敛。
    \item \textbf{例子}：$f(x) = x^2 - 2x - 3 = 0$。
        若 $x = \sqrt{2x+3} = g_1(x)$，对于根 $x^*=3$，$g_1'(3)=1/3 < 1$，收敛。
        若 $x = (x^2-3)/2 = g_2(x)$，对于根 $x^*=3$，$g_2'(3)=3 > 1$，发散。
\end{itemize}

\subsection*{2.4 牛顿-拉夫逊法 (Newton-Raphson Method)}
利用函数在 $x_i$ 处的切线与x轴的交点 $x_{i+1}$ 作为新的近似根。
\begin{itemize}
    \item \textbf{迭代公式}：$x_{i+1} = x_i - \frac{f(x_i)}{f'(x_i)}$
    \item \textbf{例子}：$f(x) = x^3 - x - 2 = 0$, $f'(x) = 3x^2 - 1$.
        若 $x_0 = 1.5, f(1.5)=-0.125, f'(1.5)=5.75$.
        $x_1 = 1.5 - (-0.125)/5.75 \approx 1.521739$. (收敛非常快)
    \item \textbf{特点}：
        \begin{itemize}
            \item 优点：若收敛，则为二次收敛 ($p=2$)，速度快。
            \item 缺点：需计算导数 $f'(x)$。若 $f'(x_i) \approx 0$ 或初值不好则可能不收敛。对重根收敛变慢。
        \end{itemize}
\end{itemize}

\subsubsection*{2.4.1 牛顿法二次收敛性证明}
设 $x^*$ 为根，$f(x^*)=0$。误差 $e_i = x_i - x^*$。
$x_{i+1} = x_i - \frac{f(x_i)}{f'(x_i)}$
$e_{i+1} = x_{i+1} - x^* = e_i - \frac{f(x_i)}{f'(x_i)}$
对 $f(x_i) = f(x^*+e_i)$ 在 $x^*$ 处泰勒展开：
$f(x_i) = f(x^*) + e_i f'(x^*) + \frac{e_i^2}{2} f''(x^*) + O(e_i^3) = e_i f'(x^*) + \frac{e_i^2}{2} f''(x^*) + O(e_i^3)$
对 $f'(x_i) = f'(x^*+e_i)$ 在 $x^*$ 处泰勒展开：
$f'(x_i) = f'(x^*) + e_i f''(x^*) + O(e_i^2)$
代入 $e_{i+1}$ 表达式：
$e_{i+1} = e_i - \frac{e_i f'(x^*) + \frac{e_i^2}{2} f''(x^*) + O(e_i^3)}{f'(x^*) + e_i f''(x^*) + O(e_i^2)}$
$e_{i+1} = e_i - \frac{1}{f'(x^*)} \left(e_i f'(x^*) + \frac{e_i^2}{2} f''(x^*)\right) \left(1 - e_i \frac{f''(x^*)}{f'(x^*)} + O(e_i^2)\right)$
整理后得到：
$e_{i+1} = \frac{f''(x^*)}{2f'(x^*)} e_i^2 + O(e_i^3)$
这表明 $e_{i+1} \propto e_i^2$，即二次收敛（需 $f'(x^*) \neq 0$）。

\subsection*{2.5 割线法 (Secant Method)}
用过点 $(x_{i-1}, f(x_{i-1}))$ 和 $(x_i, f(x_i))$ 的割线斜率近似 $f'(x_i)$。
$f'(x_i) \approx \frac{f(x_i) - f(x_{i-1})}{x_i - x_{i-1}}$
\begin{itemize}
    \item \textbf{迭代公式}：$x_{i+1} = x_i - f(x_i) \frac{x_i - x_{i-1}}{f(x_i) - f(x_{i-1})}$
    \item \textbf{例子}：$f(x) = x^3 - x - 2 = 0$.
        $x_0=1, f(1)=-2$; $x_1=2, f(2)=4$.
        $x_2 = 2 - 4 \frac{2-1}{4-(-2)} = 4/3 \approx 1.3333$.
    \item \textbf{特点}：
        \begin{itemize}
            \item 优点：无需计算导数。收敛速度超线性 ($p \approx 1.618$)，快于线性但慢于二次。
            \item 缺点：需两个初值，不保证收敛。
        \end{itemize}
\end{itemize}

\subsection*{2.6 求根方法比较}
\begin{table}[h!]
\centering
\begin{tabular}{>{\centering\arraybackslash}p{2.5cm} >{\centering\arraybackslash}p{2.5cm} >{\centering\arraybackslash}p{2.5cm} >{\centering\arraybackslash}p{3.5cm} >{\centering\arraybackslash}p{3cm}}
\toprule
特性 & 二分法 & 不动点迭代 & 牛顿法 & 割线法 \\
\midrule
收敛保证 & 是 (若初区间含根) & 否 (依赖$g'$) & 否 (依赖初值/$f'$) & 否 (依赖初值) \\
收敛速度 & 线性 ($p=1$) & 通常线性 & 二次 ($p=2$) & 超线性 ($p \approx 1.618$) \\
所需信息 & $f(x)$, 区间 & $g(x)$ & $f(x), f'(x), x_0$ & $f(x), x_0, x_1$ \\
主要优点 & 稳健 & 理论基础 & 收敛快 & 无需导数，较快 \\
主要缺点 & 慢，需初区间 & $g(x)$选取关键 & 需导数，可能不收敛 & 需两初值，可能不收敛 \\
\bottomrule
\end{tabular}
\caption{求根方法比较}
\end{table}

\section{第三、四讲：求解线性方程组 (直接法)}
求解形如 $Ax=b$ 的方程组。

\subsection*{3.1 高斯消元法 (Gaussian Elimination)}
\begin{itemize}
    \item \textbf{核心思想}：
        \begin{enumerate}
            \item \textbf{前向消元 (Forward Elimination)}：用基本行变换将增广矩阵 $[A|b]$ 化为上三角形式 $[U|b']$。
            \item \textbf{回代 (Back Substitution)}：从 $Ux=b'$ 中解出 $x$。
        \end{enumerate}
    \item \textbf{基本行变换}：1) 交换两行；2) 一行乘以非零常数；3) 一行的倍数加到另一行。
    \item \textbf{示例}：求解 $\begin{cases} 2x_1 + x_2 - x_3 = 8 \\ -3x_1 - x_2 + 2x_3 = -11 \\ -2x_1 + x_2 + 2x_3 = -3 \end{cases}$
    增广矩阵：$\left( \begin{smallmatrix} 2 & 1 & -1 & | & 8 \\ -3 & -1 & 2 & | & -11 \\ -2 & 1 & 2 & | & -3 \end{smallmatrix} \right)$
    $R_2 \leftarrow R_2 + 1.5 R_1$, $R_3 \leftarrow R_3 + 1 R_1$  变为
    $\left( \begin{smallmatrix} 2 & 1 & -1 & | & 8 \\ 0 & 0.5 & 0.5 & | & 1 \\ 0 & 2 & 1 & | & 5 \end{smallmatrix} \right)$
    $R_3 \leftarrow R_3 - 4 R_2$ 变为
    $\left( \begin{smallmatrix} 2 & 1 & -1 & | & 8 \\ 0 & 0.5 & 0.5 & | & 1 \\ 0 & 0 & -1 & | & 1 \end{smallmatrix} \right)$
    回代得到 $x_3=-1, x_2=3, x_1=2$。
\end{itemize}

\subsection*{3.2 主元选择 (Pivoting)}
解决主元为零或过小导致数值不稳定的问题。
\begin{itemize}
    \item \textbf{部分选主元法 (Partial Pivoting)}：在第 $k$ 步消元前，从当前第 $k$ 列对角线及以下元素中选取绝对值最大的元素作为主元，并通过行交换将其移至主元位置。
    \item \textbf{好处}：避免除零，减小舍入误差 (保证乘数 $|m_{ik}| \le 1$)，提高数值稳定性。
    \item \textbf{示例}：$\begin{cases} 0x_1 + x_2 + x_3 = 2 \\ 2x_1 + 2x_2 - x_3 = 3 \\ x_1 - x_2 + 3x_3 = 3 \end{cases}$
    初始 $a_{11}=0$. 搜索第1列，发现 $a_{21}=2$ 绝对值最大。交换 $R_1 \leftrightarrow R_2$。
    $\left( \begin{smallmatrix} 2 & 2 & -1 & | & 3 \\ 0 & 1 & 1 & | & 2 \\ 1 & -1 & 3 & | & 3 \end{smallmatrix} \right)$, 然后继续消元。
\end{itemize}

\subsection*{3.3 LU 分解 (LU Decomposition)}
将矩阵 $A$ 分解为 $A=LU$，其中 $L$ 是下三角矩阵，$U$ 是上三角矩阵。
\begin{itemize}
    \item \textbf{Doolittle 形式}：$L$ 的对角线元素为1。$U$ 是高斯消元后的上三角阵，$L$ 的严格下三角元素是消元过程中的乘数。
    \item \textbf{求解 $Ax=b$}：
        \begin{enumerate}
            \item 若 $A=LU$, 则 $LUx=b$. 令 $y=Ux$.
            \item 解 $Ly=b$ (前向替换)。
            \item 解 $Ux=y$ (回代)。
        \end{enumerate}
    \item \textbf{用途}：高效处理多个右端项 $b$；计算行列式 ($\det(A)=\det(U)$ for Doolittle)；计算逆矩阵。
    \item \textbf{示例} (Doolittle): $A = \begin{pmatrix} 2 & 1 & -1 \\ -2 & 1 & 3 \\ 4 & -2 & 1 \end{pmatrix}$.
        高斯消元得 $m_{21}=-1, m_{31}=2, m_{32}=-2$.
        $L = \begin{pmatrix} 1 & 0 & 0 \\ -1 & 1 & 0 \\ 2 & -2 & 1 \end{pmatrix}$, $U = \begin{pmatrix} 2 & 1 & -1 \\ 0 & 2 & 2 \\ 0 & 0 & 7 \end{pmatrix}$.
    \item \textbf{带主元选择的LU分解}：$PA=LU$，其中 $P$ 是置换矩阵，记录行交换。
        求解 $Ax=b \implies PAx=Pb$. 令 $y=Ux$.
        1. 解 $Ly=Pb$. 2. 解 $Ux=y$.
    \item \textbf{计算复杂度}：分解 $O(2n^3/3)$，替换 $O(n^2)$。
\end{itemize}

\section{第五讲：线性方程组的敏感性分析 (初步)}
衡量解对数据扰动的敏感程度。

\subsection*{4.1 向量范数 (Vector Norms)}
衡量向量“长度”或“幅度”。对于向量 $x=(x_1, \dots, x_n)^T$：
\begin{itemize}
    \item $L_1$-范数: $\|x\|_1 = \sum_{i=1}^n |x_i|$
    \item $L_2$-范数 (欧几里得范数): $\|x\|_2 = \sqrt{\sum_{i=1}^n x_i^2}$
    \item $L_\infty$-范数 (最大范数): $\|x\|_\infty = \max_{1 \le i \le n} |x_i|$
\end{itemize}
\textbf{示例}: $x=(1, -2, 3)^T$. $\|x\|_1=6, \|x\|_2=\sqrt{14}, \|x\|_\infty=3$.

\subsection*{4.2 矩阵范数 (Matrix Norms)}
衡量矩阵“大小”或“放大能力”。由向量范数诱导的算子范数：$\|A\| = \max_{\|x\|=1} \|Ax\|$.
\begin{itemize}
    \item $\|A\|_1$ (最大绝对列和): $\max_{j} \sum_{i} |a_{ij}|$
    \item $\|A\|_\infty$ (最大绝对行和): $\max_{i} \sum_{j} |a_{ij}|$
    \item $\|A\|_2$ (谱范数): $A$ 的最大奇异值 $\sigma_{\max}(A)$.
\end{itemize}
\textbf{示例}: $A = \begin{pmatrix} 1 & -2 \\ 3 & 0 \end{pmatrix}$.
$\|A\|_1 = \max(|1|+|3|, |-2|+|0|) = \max(4,2) = 4$.
$\|A\|_\infty = \max(|1|+|-2|, |3|+|0|) = \max(3,3) = 3$.

\subsection*{4.3 条件数 (Condition Number) - 初步介绍}
衡量矩阵 $A$ (或线性系统 $Ax=b$) 病态程度的指标。
$$\kappa(A) = \|A\| \cdot \|A^{-1}\|$$
(使用同一种诱导范数)。
\begin{itemize}
    \item $\kappa(A) \ge 1$.
    \item 若 $\kappa(A)$ 接近 1, $A$ 是良态的 (well-conditioned)。
    \item 若 $\kappa(A)$ 很大, $A$ 是病态的 (ill-conditioned)，解对扰动敏感。
\end{itemize}

\end{document}
```