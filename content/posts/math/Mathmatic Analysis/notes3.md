---
author: "ybw051114"
author_link: "hugo.ybw051114.cf"
title: "数值分析笔记3"
date: 2025-05-16T21:45:17+08:00
lastmod: 2025-05-16T21:45:17+08:00
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
# 数值分析课程笔记 (详细版：切比雪夫节点 至 数值微分结束)

**授课老师**: Gemini
**日期**: 2025年5月16日

## 7. 插值法 (续)

### 7.5. 切比雪夫节点 (Chebyshev Nodes)

#### 7.5.1. 动机与目的
多项式插值的误差公式为：
$$E_n(x) = f(x) - P_n(x) = \frac{f^{(n+1)}(\xi_x)}{(n+1)!} \prod_{i=0}^n (x-x_i)$$
为减小误差，除了依赖于被插函数 $f$ 的高阶导数 $f^{(n+1)}(\xi_x)$ 外，我们主要能控制的是节点 $x_i$ 的选取，以使 $\max_{x \in [a,b]} \left| \prod_{i=0}^n (x-x_i) \right|$ 尽可能小。等距节点在区间端点附近会导致这一项的值很大，从而引发龙格现象。切比雪夫节点的选取正是为了优化这一连乘项。

#### 7.5.2. 切比雪夫多项式 (第一类)
第一类 $k$ 次切比雪夫多项式 $T_k(x)$ 定义在 $[-1, 1]$ 上：
$$T_k(x) = \cos(k \arccos x), \quad x \in [-1, 1]$$
例如：
-   $T_0(x) = 1$
-   $T_1(x) = x$
-   $T_2(x) = 2x^2 - 1$
-   $T_k(x)$ 的首项系数为 $2^{k-1}$ (对于 $k \ge 1$)。

**重要性质**: 在 $[-1,1]$ 上，所有首项系数为1的 $n$ 次多项式中，$\frac{1}{2^{n-1}}T_n(x)$ 的最大绝对值是最小的，为 $\frac{1}{2^{n-1}}$。

#### 7.5.3. 切比雪夫插值节点
要使 $\omega_{n+1}(x) = \prod_{i=0}^n (x-x_i)$ (一个 $n+1$ 次首一多项式) 的最大绝对值最小，应使其等于 $\frac{1}{2^n}T_{n+1}(x)$。因此，插值节点 $x_i$ (对于 $n$ 次插值多项式，共 $n+1$ 个节点) 应取为 $T_{n+1}(x)$ 在 $[-1,1]$ 上的零点。
$T_{n+1}(x) = \cos((n+1)\arccos x) = 0 \implies (n+1)\arccos \tilde{x}_k = \frac{(2k+1)\pi}{2}$
标准区间 $[-1, 1]$ 上的 $n+1$ 个切比雪夫节点为：
$$\tilde{x}_k = \cos\left(\frac{(2k+1)\pi}{2(n+1)}\right), \quad k=0, 1, \dots, n$$

#### 7.5.4. 节点变换至一般区间 $[a,b]$
通过线性变换 $x = \frac{a+b}{2} + \frac{b-a}{2}\tilde{x}$，可得 $[a,b]$ 上的切比雪夫节点：
$$x_k = \frac{a+b}{2} + \frac{b-a}{2} \cos\left(\frac{(2k+1)\pi}{2(n+1)}\right), \quad k=0, 1, \dots, n$$
这些节点在区间两端较为密集，中间较为稀疏，能有效减轻龙格现象。使用这些节点进行多项式插值，通常能获得比等距节点更好的逼近效果。

### 7.6. 分段插值与样条插值

#### 7.6.1. 分段插值的动机
高次多项式插值可能导致龙格现象，且计算复杂，对数据扰动敏感。分段插值通过在每个子区间上使用低次多项式来避免这些问题。

#### 7.6.2. 分段线性插值
-   **定义**: 在每对相邻数据点 $(x_i, y_i)$ 和 $(x_{i+1}, y_{i+1})$ 之间用直线段连接。
    $$P_i(x) = y_i + \frac{y_{i+1}-y_i}{x_{i+1}-x_i}(x-x_i), \quad x \in [x_i, x_{i+1}]$$
-   **性质**: 整体函数 $P(x)$ 是连续的 ($C^0$ 连续)。但在节点处，导数通常不连续，形成尖角，不够光滑。

#### 7.6.3. 样条插值的引入
为了获得更光滑的插值曲线，我们不仅要求函数在节点处连续，还要求其导数也连续。样条插值就是满足这种要求的特定分段多项式。

### 7.7. 三次样条插值详解 (Cubic Spline Interpolation)

#### 7.7.1. 定义
一个在区间 $[x_0, x_n]$ 上的三次样条函数 $S(x)$ 是一个满足以下条件的函数：
1.  在每个子区间 $[x_i, x_{i+1}]$ 上 ($i=0, \dots, n-1$)，$S(x)$ 是一个三次多项式，记为 $S_i(x)$。
2.  $S(x)$ 在整个区间 $[x_0, x_n]$ 上具有二阶连续导数 (即 $S(x) \in C^2[x_0, x_n]$)。这意味着：
    -   $S(x_i) = y_i$ (插值条件)
    -   $S_i(x_{i+1}) = S_{i+1}(x_{i+1}) = y_{i+1}$ (函数值在内部节点连续)
    -   $S'_i(x_{i+1}) = S'_{i+1}(x_{i+1})$ (一阶导数在内部节点连续)
    -   $S''_i(x_{i+1}) = S''_{i+1}(x_{i+1})$ (二阶导数在内部节点连续)

#### 7.7.2. $S_i(x)$ 的表示与二阶导数 $M_i$
令 $M_i = S''(x_i)$ 为节点 $x_i$ 处的二阶导数值。由于 $S_i(x)$ 是三次多项式，其二阶导数 $S_i''(x)$ 是线性函数。在 $[x_i, x_{i+1}]$ 上， $S_i''(x_i)=M_i, S_i''(x_{i+1})=M_{i+1}$，因此：
$$S_i''(x) = M_i \frac{x_{i+1}-x}{h_i} + M_{i+1} \frac{x-x_i}{h_i}$$
其中 $h_i = x_{i+1}-x_i$。

对 $S_i''(x)$ 积分两次可得 $S_i(x)$：
$$S_i(x) = M_i \frac{(x_{i+1}-x)^3}{6h_i} + M_{i+1} \frac{(x-x_i)^3}{6h_i} + C_1(x-x_i) + C_2$$
利用插值条件 $S_i(x_i)=y_i$ 和 $S_i(x_{i+1})=y_{i+1}$ 确定积分常数 $C_1, C_2$:
$C_2 = y_i - \frac{M_i h_i^2}{6}$
$C_1 = \frac{y_{i+1}-y_i}{h_i} - \frac{h_i}{6}(M_{i+1}-M_i)$
代入得到 $S_i(x)$ 的完整表达式（以 $M_i, M_{i+1}, y_i, y_{i+1}$ 表示）。

#### 7.7.3. 建立关于 $M_i$ 的方程组
利用一阶导数连续条件 $S'_{i-1}(x_i) = S'_i(x_i)$ 于内部节点 $x_i$ ($i=1, \dots, n-1$)：
对 $S_i(x)$ 求导:
$S_i'(x) = -M_i \frac{(x_{i+1}-x)^2}{2h_i} + M_{i+1} \frac{(x-x_i)^2}{2h_i} + \frac{y_{i+1}-y_i}{h_i} - \frac{h_i}{6}(M_{i+1}-M_i)$
计算 $S'_i(x_i)$ 和 $S'_{i-1}(x_i)$ 并令它们相等，整理后得到：
$$h_{i-1}M_{i-1} + 2(h_{i-1}+h_i)M_i + h_iM_{i+1} = 6\left(\frac{y_{i+1}-y_i}{h_i} - \frac{y_i-y_{i-1}}{h_{i-1}}\right)$$
此方程对 $i=1, 2, \dots, n-1$ 成立，共 $n-1$ 个方程，包含 $n+1$ 个未知数 $M_0, \dots, M_n$。

#### 7.7.4. 端点条件
为确定所有 $M_i$，需要两个额外的边界条件：
1.  **自然样条 (Natural Spline)**: $S''(x_0)=M_0=0$ 和 $S''(x_n)=M_n=0$。这是最常用的，当无额外信息时。
2.  **固定样条 (Clamped Spline)**: $S'(x_0)=y'_0$ 和 $S'(x_n)=y'_n$ (给定端点一阶导数值)。这会改变方程组的第一行和最后一行。

对于自然样条，将 $M_0=0, M_n=0$ 代入上述方程组，得到关于 $M_1, \dots, M_{n-1}$ 的 $n-1$ 个方程的线性方程组。该方程组的系数矩阵是三对角且严格对角占优的（若所有 $h_i>0$），可用追赶法高效求解。

#### 7.7.5. 计算样条系数
一旦求得所有 $M_i$ ($i=0, \dots, n$)，各段三次多项式 $S_i(x) = a_i' + b_i'(x-x_i) + c_i'(x-x_i)^2 + d_i'(x-x_i)^3$ 的系数为 (注意这里的撇号是为区分之前的积分常数 $C_1, C_2$):
-   $d_i' = y_i$ (或者说 $a_i=y_i$ 如果 $S_i(x)=a_i+b_i(x-x_i)+\dots$)
-   $c_i' = S_i'(x_i) = \frac{y_{i+1}-y_i}{h_i} - \frac{h_i}{6}(2M_i + M_{i+1})$ (这是 $b_i$ 在标准 $a_i+b_i(x-x_i)+\dots$ 形式下)
-   $b_i' = S_i''(x_i)/2 = M_i/2$ (这是 $c_i$ 在标准形式下)
-   $a_i' = S_i'''(x_i)/6 = \frac{M_{i+1}-M_i}{6h_i}$ (这是 $d_i$ 在标准形式下)

使用标准形式 $S_i(x) = a_i + b_i(x-x_i) + c_i(x-x_i)^2 + d_i(x-x_i)^3$:
-   $a_i = y_i$
-   $b_i = \frac{y_{i+1}-y_i}{h_i} - \frac{h_i}{6}(2M_i + M_{i+1})$
-   $c_i = \frac{M_i}{2}$
-   $d_i = \frac{M_{i+1}-M_i}{6h_i}$
这些系数定义了第 $i$ 段 $([x_i, x_{i+1}])$ 的三次样条。

### 7.8. 切比雪夫节点插值 vs. 三次样条插值 (详细比较)

| 特性             | 切比雪夫节点的多项式插值                                 | 三次样条插值                                             |
| :--------------- | :------------------------------------------------------- | :--------------------------------------------------------- |
| **基本构成** | 单一的 $n$ 次多项式。                                    | 多段（$n$段）三次多项式拼接而成。                             |
| **全局/局部** | **全局**：一个数据点的改变或扰动会影响整个区间的插值函数。    | **更局部**：一个数据点 $y_k$ 的改变主要影响其邻近的样条段。尽管 $M_i$ 的求解是全局的，但影响衰减快。 |
| **光滑性** | $C^\infty$ (多项式无限次可微)。                             | $C^2$ (保证到二阶导数连续)。通常对视觉和物理建模足够。         |
| **龙格现象** | 通过优化节点分布**显著减轻**，但不能完全消除（尤其对极高次或病态函数）。误差分布更均匀。 | **有效避免**，因其本质是低阶（三次）多项式的拼接。            |
| **节点选取** | 节点位置由切比雪夫多项式的零点确定，**不能任意指定**以达到最优效果。 | 节点 $x_i$ 可以是**任意给定**的，对实验数据更友好。           |
| **计算复杂度** | 节点计算简单。构造多项式 (如Lagrange或Newton) 和求值 (Horner) 相对直接。 | 需要求解一个三对角线性方程组 (通常 $O(N)$ 复杂度) 来确定 $M_i$，然后计算各段系数。设置稍复杂。 |
| **端点行为** | 由整体多项式特性决定。切比雪夫节点在端点密集，控制较好。       | 自然样条假设 $S''(x_0)=S''(x_n)=0$，是一种人为假设，可能不符合真函数的端点行为。固定样条可指定端点导数，更灵活但需要额外信息。 |
| **数据要求** | 只需要 $(x_i, y_i)$。节点 $x_i$ 按公式生成。              | 基本只需要 $(x_i, y_i)$。固定样条需要端点导数值。           |
| **适用场景** | 当需要全局 $C^\infty$ 光滑逼近，函数本身光滑，且可按切比雪夫节点采样时 (如函数逼近理论，谱方法)。 | 对离散/实验数据进行平滑插值，计算机图形学曲线绘制，当 $C^2$ 光滑度足够且要避免震荡时。 |

## 8. 数值微分

### 8.1. 引论
-   **目的**: 当函数 $f(x)$ 的解析导数未知或难以计算，或 $f(x)$ 仅以离散数据点形式给出时，近似计算其导数值 $f'(x), f''(x)$ 等。
-   **基本挑战**: 数值微分是**病态的 (ill-conditioned)** 或 **不适定的 (ill-posed)** 问题。它对输入数据中的误差（噪声）非常敏感，容易放大误差。
    -   **截断误差 ($E_T$)**: 由数学公式本身的近似造成 (如用差商代替极限)。通常随步长 $h$ 的减小而减小 (如 $E_T \propto h^p, p>0$)。
    -   **舍入误差 ($E_R$)**: 由计算机浮点运算的有限精度造成。当 $h$ 很小时，计算 $f(x+h)-f(x)$ 会发生灾难性抵消，此误差再被小 $h$ 除会急剧放大 ($E_R \propto \epsilon/h^k, k>0$)。
    -   必须在减小截断误差和控制舍入误差放大之间进行权衡，选择合适的步长 $h$。

### 8.2. 基于泰勒展开的差分公式 ($h>0$ 为步长)

#### 8.2.1. 一阶导数 $f'(x_0)$
1.  **向前差分 (Forward Difference)**
    $f(x_0+h) = f(x_0) + hf'(x_0) + \frac{h^2}{2}f''(\xi_1)$, $\xi_1 \in (x_0, x_0+h)$
    $$f'(x_0) = \frac{f(x_0+h) - f(x_0)}{h} - \frac{h}{2}f''(\xi_1)$$
    近似公式: $f'(x_0) \approx \frac{f(x_0+h) - f(x_0)}{h}$
    截断误差: $E_T = -\frac{h}{2}f''(\xi_1) = O(h)$

2.  **向后差分 (Backward Difference)**
    $f(x_0-h) = f(x_0) - hf'(x_0) + \frac{h^2}{2}f''(\xi_2)$, $\xi_2 \in (x_0-h, x_0)$
    $$f'(x_0) = \frac{f(x_0) - f(x_0-h)}{h} + \frac{h}{2}f''(\xi_2)$$
    近似公式: $f'(x_0) \approx \frac{f(x_0) - f(x_0-h)}{h}$
    截断误差: $E_T = \frac{h}{2}f''(\xi_2) = O(h)$

3.  **中心差分 (Central Difference)**
    $f(x_0+h) = f(x_0) + hf'(x_0) + \frac{h^2}{2}f''(x_0) + \frac{h^3}{6}f'''(\xi_3)$
    $f(x_0-h) = f(x_0) - hf'(x_0) + \frac{h^2}{2}f''(x_0) - \frac{h^3}{6}f'''(\xi_4)$
    两式相减: $f(x_0+h) - f(x_0-h) = 2hf'(x_0) + \frac{h^3}{6}(f'''(\xi_3)+f'''(\xi_4))$
    若 $f'''$ 连续，则 $\frac{1}{2}(f'''(\xi_3)+f'''(\xi_4)) = f'''(\xi)$ for some $\xi \in (x_0-h, x_0+h)$.
    $$f'(x_0) = \frac{f(x_0+h) - f(x_0-h)}{2h} - \frac{h^2}{6}f'''(\xi)$$
    近似公式: $f'(x_0) \approx \frac{f(x_0+h) - f(x_0-h)}{2h}$
    截断误差: $E_T = -\frac{h^2}{6}f'''(\xi) = O(h^2)$ (通常精度更高)

#### 8.2.2. 二阶导数 $f''(x_0)$
1.  **中心差分 (Central Difference)**
    $f(x_0+h) + f(x_0-h) = 2f(x_0) + h^2f''(x_0) + \frac{h^4}{24}(f^{(4)}(\eta_1)+f^{(4)}(\eta_2))$
    若 $f^{(4)}$ 连续，则 $\frac{1}{2}(f^{(4)}(\eta_1)+f^{(4)}(\eta_2)) = f^{(4)}(\eta)$ for some $\eta \in (x_0-h, x_0+h)$.
    $$f''(x_0) = \frac{f(x_0+h) - 2f(x_0) + f(x_0-h)}{h^2} - \frac{h^2}{12}f^{(4)}(\eta)$$
    近似公式: $f''(x_0) \approx \frac{f(x_0+h) - 2f(x_0) + f(x_0-h)}{h^2}$
    截断误差: $E_T = -\frac{h^2}{12}f^{(4)}(\eta) = O(h^2)$

### 8.3. 基于插值多项式的微分公式
-   **一般思想**: 给定 $n+1$ 个点 $(x_i, f(x_i))$，构造插值多项式 $P_n(x)$，则 $f^{(k)}(x) \approx P_n^{(k)}(x)$。
-   **示例1: 两点线性插值 $P_1(x)$**
    过 $(x_0, f_0)$ 和 $(x_0+h, f_1)$，$P_1(x) = f_0 + \frac{f_1-f_0}{h}(x-x_0)$。
    $P_1'(x) = \frac{f_1-f_0}{h}$。在 $x_0$ 处即为向前差分。
-   **示例2: 三点二次插值 $P_2(x)$**
    过 $(x_0-h, f_{-1}), (x_0, f_0), (x_0+h, f_1)$。
    $P_2(x) = f_{-1} \frac{(x-x_0)(x-(x_0+h))}{2h^2} + f_0 \frac{(x-(x_0-h))(x-(x_0+h))}{-h^2} + f_1 \frac{(x-(x_0-h))(x-x_0)}{2h^2}$ (Lagrange形式)
    求导 $P_2'(x)$，并在 $x=x_0$ 处取值:
    $P_2'(x_0) = \frac{f_1 - f_{-1}}{2h}$ (中心差分公式 $O(h^2)$)。
    求二阶导 $P_2''(x)$:
    $P_2''(x_0) = \frac{f_1 - 2f_0 + f_{-1}}{h^2}$ (中心差分公式 $O(h^2)$)。

### 8.4. 舍入误差与步长选择 (详细)
总误差 $E_{total}(h) = E_T(h) + E_R(h)$。
设函数计算的舍入误差界为 $\epsilon$ (即 $|fl(f(x_i)) - f(x_i)| \le \epsilon$)。

1.  **向前/向后差分 $f'(x_0)$**:
    $E_T(h) = C_1 h$ (其中 $C_1 \approx \frac{1}{2}|f''(\cdot)|$)
    $E_R(h) \approx \frac{fl(f(x_0+h))-fl(f(x_0))}{h} - \frac{f(x_0+h)-f(x_0)}{h} = \frac{e_1-e_0}{h}$.
    $|E_R(h)| \le \frac{2\epsilon}{h}$.
    $|E_{total}(h)| \lesssim \frac{1}{2}|f''|h + \frac{2\epsilon}{h}$.
    要最小化此上界，对 $h$ 求导并令其为0: $\frac{1}{2}|f''| - \frac{2\epsilon}{h^2} = 0 \implies h_{opt} \approx \sqrt{\frac{4\epsilon}{|f''|}}$.
    此时最小总误差 $\approx 2\sqrt{\epsilon |f''|}$.

2.  **中心差分 $f'(x_0)$**:
    $E_T(h) = C_2 h^2$ (其中 $C_2 \approx \frac{1}{6}|f'''(\cdot)|$)
    $|E_R(h)| \le \frac{2\epsilon}{2h} = \frac{\epsilon}{h}$.
    $|E_{total}(h)| \lesssim \frac{1}{6}|f'''|h^2 + \frac{\epsilon}{h}$.
    最小化: $\frac{1}{3}|f'''|h - \frac{\epsilon}{h^2} = 0 \implies h_{opt} \approx \left(\frac{3\epsilon}{|f'''|}\right)^{1/3}$.
    此时最小总误差 $\approx \frac{1}{2}|f'''|^{1/3}(3\epsilon)^{2/3} + \epsilon^{2/3}(|f'''|/3)^{1/3} = \text{const} \cdot \epsilon^{2/3}$.

3.  **中心差分 $f''(x_0)$**:
    $E_T(h) = C_3 h^2$ (其中 $C_3 \approx \frac{1}{12}|f^{(4)}(\cdot)|$)
    $|E_R(h)| \le \frac{|e_1-2e_0+e_{-1}|}{h^2} \le \frac{4\epsilon}{h^2}$. (假设 $e_i$ 独立且界为 $\epsilon$)
    $|E_{total}(h)| \lesssim \frac{1}{12}|f^{(4)}|h^2 + \frac{4\epsilon}{h^2}$.
    最小化: $\frac{1}{6}|f^{(4)}|h - \frac{8\epsilon}{h^3} = 0 \implies h_{opt} \approx \left(\frac{48\epsilon}{|f^{(4)}|}\right)^{1/4}$.
    此时最小总误差 $\approx \text{const} \cdot \epsilon^{1/2}$.

**结论**:
-   $h$ 的选择是截断误差和舍入误差之间的权衡。
-   数值微分对噪声（舍入误差）非常敏感。
-   能达到的最高精度有限，且通常远低于机器精度 $\epsilon$。例如，对于中心差分 $f'(x_0)$，最佳误差约为 $O(\epsilon^{2/3})$。

### 8.5. 理查森外推法 (Richardson Extrapolation)

#### 8.5.1. 动机与原理
通过组合使用不同步长计算得到的近似值，来消除或减小截断误差中的低阶项，从而提高近似精度。
假设待求真值为 $M$，使用步长 $h$ 的近似值为 $N(h)$，且截断误差有如下形式：
$$M = N(h) + K_1 h^{p_1} + K_2 h^{p_2} + K_3 h^{p_3} + \dots \quad (0 < p_1 < p_2 < p_3 < \dots)$$
其中 $K_j$ 是不依赖于 $h$ 的常数。

#### 8.5.2. 外推公式推导
取两个步长 $h$ 和 $h/r$ (通常 $r=2$)：
(1) $M = N(h) + K_1 h^{p_1} + O(h^{p_2})$
(2) $M = N(h/r) + K_1 (h/r)^{p_1} + O(h^{p_2}) = N(h/r) + K_1 \frac{h^{p_1}}{r^{p_1}} + O(h^{p_2})$
将 (2) 乘以 $r^{p_1}$，然后减去 (1)：
$r^{p_1}M - M = r^{p_1}N(h/r) - N(h) + O(h^{p_2})$
$(r^{p_1}-1)M = r^{p_1}N(h/r) - N(h) + O(h^{p_2})$
$$M = \frac{r^{p_1}N(h/r) - N(h)}{r^{p_1}-1} + O(h^{p_2})$$
令 $N_1(h) = \frac{r^{p_1}N(h/r) - N(h)}{r^{p_1}-1}$。这个新的近似值 $N_1(h)$ 的误差是 $O(h^{p_2})$，消除了 $O(h^{p_1})$ 的误差项。
另一种常用形式 (令 $N(h/r)$ 为主项):
$$N_1(h) = N(h/r) + \frac{N(h/r) - N(h)}{r^{p_1}-1}$$

#### 8.5.3. 应用于中心差分求 $f'(x)$
对于中心差分公式 $D(h) = \frac{f(x+h)-f(x-h)}{2h}$，我们有：
$f'(x) = D(h) + K_1 h^2 + K_2 h^4 + K_3 h^6 + \dots$
这里 $p_1=2$。取 $r=2$ (即步长减半)。
$D_1(h) = D(h/2) + \frac{D(h/2) - D(h)}{2^2-1} = D(h/2) + \frac{D(h/2) - D(h)}{3}$
$D_1(h)$ 的误差为 $O(h^4)$。

#### 8.5.4. 迭代理查森外推 (Romberg方法思想)
此过程可以迭代。设 $N_{k,0} = N(h/2^k)$ 是初始计算序列 ($k=0,1,2,\dots$)。
$N_{k,j+1} = N_{k+1,j} + \frac{N_{k+1,j} - N_{k,j}}{2^{p_j}-1}$
其中 $p_j$ 是第 $j$ 次外推时要消除的误差项的阶数。
对于中心差分，误差为 $K_1h^2 + K_2h^4 + K_3h^6 + \dots$，所以 $p_1=2, p_2=4, p_3=6, \dots$。
表格形式如下：
$D_{0,0} = D(h)$  ($O(h^2)$)
$D_{1,0} = D(h/2)$ ($O(h^2)$) $\quad \rightarrow \quad D_{0,1} = D_{1,0} + \frac{D_{1,0}-D_{0,0}}{2^2-1}$ ($O(h^4)$)
$D_{2,0} = D(h/4)$ ($O(h^2)$) $\quad \rightarrow \quad D_{1,1} = D_{2,0} + \frac{D_{2,0}-D_{1,0}}{2^2-1}$ ($O(h^4)$) $\quad \rightarrow \quad D_{0,2} = D_{1,1} + \frac{D_{1,1}-D_{0,1}}{2^4-1}$ ($O(h^6)$)
$D_{3,0} = D(h/8)$ ($O(h^2)$) $\quad \rightarrow \quad D_{2,1} = D_{3,0} + \frac{D_{3,0}-D_{2,0}}{2^2-1}$ ($O(h^4)$) $\quad \rightarrow \quad D_{1,2} = D_{2,1} + \frac{D_{2,1}-D_{1,1}}{2^4-1}$ ($O(h^6)$) $\quad \rightarrow \quad \dots$
对角线元素 $D_{0,0}, D_{0,1}, D_{0,2}, \dots$ 给出越来越精确的近似。

#### 8.5.5. 优缺点
-   **优点**: 能显著提高精度；过程系统化；可提供误差估计。
-   **缺点**: 依赖于误差展开式的已知形式；初始计算值仍受舍入误差影响，如果 $h$ 过小，外推也无法弥补已损坏的数据。



```tex
\documentclass[UTF8,a4paper]{ctexart}
\usepackage{amsmath, amssymb, amsfonts}
\usepackage{geometry}
\geometry{a4paper, margin=1in}
\usepackage{array}
\usepackage{booktabs}
\usepackage{enumitem} % For more control over lists

\title{数值分析课程笔记 (详细版：切比雪夫节点 至 数值微分结束)}
\author{Gemini 老师}
\date{2025年5月16日}

\begin{document}
\maketitle
\tableofcontents
\newpage

\section{插值法 (续)}

\subsection{切比雪夫节点 (Chebyshev Nodes)}
\subsubsection{动机与目的}
多项式插值的误差公式为：
$$E_n(x) = f(x) - P_n(x) = \frac{f^{(n+1)}(\xi_x)}{(n+1)!} \prod_{i=0}^n (x-x_i)$$
为减小误差，除了依赖于被插函数 $f$ 的高阶导数 $f^{(n+1)}(\xi_x)$ 外，我们主要能控制的是节点 $x_i$ 的选取，以使 $\max_{x \in [a,b]} \left| \prod_{i=0}^n (x-x_i) \right|$ 尽可能小。切比雪夫节点的选取正是为了优化这一连乘项。

\subsubsection{切比雪夫多项式 (第一类)}
第一类 $k$ 次切比雪夫多项式 $T_k(x)$ 定义在 $[-1, 1]$ 上：
$$T_k(x) = \cos(k \arccos x), \quad x \in [-1, 1]$$
\textbf{重要性质}: 在 $[-1,1]$ 上，所有首项系数为1的 $n$ 次多项式中，$\frac{1}{2^{n-1}}T_n(x)$ 的最大绝对值是最小的，为 $\frac{1}{2^{n-1}}$。

\subsubsection{切比雪夫插值节点}
插值节点 $x_i$ (对于 $n$ 次插值多项式，共 $n+1$ 个节点) 应取为 $T_{n+1}(x)$ 在 $[-1,1]$ 上的零点。
标准区间 $[-1, 1]$ 上的 $n+1$ 个切比雪夫节点为：
$$\tilde{x}_k = \cos\left(\frac{(2k+1)\pi}{2(n+1)}\right), \quad k=0, 1, \dots, n$$

\subsubsection{节点变换至一般区间 $[a,b]$}
通过线性变换 $x = \frac{a+b}{2} + \frac{b-a}{2}\tilde{x}$，可得 $[a,b]$ 上的切比雪夫节点：
$$x_k = \frac{a+b}{2} + \frac{b-a}{2} \cos\left(\frac{(2k+1)\pi}{2(n+1)}\right), \quad k=0, 1, \dots, n$$
这些节点在区间两端较为密集，中间较为稀疏，能有效减轻龙格现象。

\subsection{分段插值与样条插值}
\subsubsection{分段插值的动机}
高次多项式插值可能导致龙格现象。分段插值通过在每个子区间上使用低次多项式来避免这些问题。
\subsubsection{分段线性插值}
在每对相邻数据点 $(x_i, y_i)$ 和 $(x_{i+1}, y_{i+1})$ 之间用直线段连接。
$$P_i(x) = y_i + \frac{y_{i+1}-y_i}{x_{i+1}-x_i}(x-x_i), \quad x \in [x_i, x_{i+1}]$$
整体函数 $P(x)$ 是 $C^0$ 连续，但导数在节点处通常不连续。
\subsubsection{样条插值的引入}
为获得更光滑的插值曲线，要求函数在节点处及其导数也连续。

\subsection{三次样条插值详解 (Cubic Spline Interpolation)}
\subsubsection{定义}
一个在 $[x_0, x_n]$ 上的三次样条函数 $S(x)$ 满足：
\begin{enumerate}
    \item 在每个子区间 $[x_i, x_{i+1}]$ 上，$S(x)$ 是一个三次多项式 $S_i(x)$。
    \item $S(x) \in C^2[x_0, x_n]$ (二阶连续导数)。
\end{enumerate}
\subsubsection{$S_i(x)$ 的表示与二阶导数 $M_i$}
令 $M_i = S''(x_i)$。在 $[x_i, x_{i+1}]$ 上，$h_i = x_{i+1}-x_i$：
$$S_i''(x) = M_i \frac{x_{i+1}-x}{h_i} + M_{i+1} \frac{x-x_i}{h_i}$$
积分两次并用 $S_i(x_i)=y_i, S_i(x_{i+1})=y_{i+1}$ 定积分常数：
$$S_i(x) = M_i \frac{(x_{i+1}-x)^3}{6h_i} + M_{i+1} \frac{(x-x_i)^3}{6h_i} + \left(\frac{y_i}{h_i} - \frac{M_i h_i}{6}\right)(x_{i+1}-x) + \left(\frac{y_{i+1}}{h_i} - \frac{M_{i+1} h_i}{6}\right)(x-x_i)$$
(注：此为一种推导形式，之前笔记中 $S_i(x)$ 系数形式更常用)
\subsubsection{建立关于 $M_i$ 的方程组}
利用一阶导数连续条件 $S'_{i-1}(x_i) = S'_i(x_i)$ 于内部节点 $x_i$ ($i=1, \dots, n-1$)，得到：
$$h_{i-1}M_{i-1} + 2(h_{i-1}+h_i)M_i + h_iM_{i+1} = 6\left(\frac{y_{i+1}-y_i}{h_i} - \frac{y_i-y_{i-1}}{h_{i-1}}\right)$$
\subsubsection{端点条件}
\begin{enumerate}
    \item \textbf{自然样条}: $M_0=0, M_n=0$.
    \item \textbf{固定样条}: $S'(x_0)=y'_0, S'(x_n)=y'_n$.
\end{enumerate}
\subsubsection{计算样条系数}
一旦求得所有 $M_i$，各段三次多项式 $S_i(x) = a_i + b_i(x-x_i) + c_i(x-x_i)^2 + d_i(x-x_i)^3$ 的系数为:
\begin{itemize}
    \item $a_i = y_i$
    \item $b_i = \frac{y_{i+1}-y_i}{h_i} - \frac{h_i}{6}(2M_i + M_{i+1})$
    \item $c_i = \frac{M_i}{2}$
    \item $d_i = \frac{M_{i+1}-M_i}{6h_i}$
\end{itemize}

\subsection{切比雪夫节点插值 vs. 三次样条插值 (详细比较)}
\begin{center}
\begin{tabular}{lll}
\toprule
特性 & 切比雪夫节点的多项式插值 & 三次样条插值 \\
\midrule
基本构成 & 单一的 $n$ 次多项式 & 多段三次多项式 \\
全局/局部 & 全局 & 更局部 \\
光滑性 & $C^\infty$ & $C^2$ \\
龙格现象 & 显著减轻 & 有效避免 \\
节点选取 & 公式确定，不任意 & 任意给定 \\
计算复杂度 & 构造/求值相对直接 & 需解三对角系统 \\
端点行为 & 整体多项式决定 & 自然样条有假设 \\
数据要求 & $(x_i, y_i)$，节点按公式 & $(x_i, y_i)$，固定样条需导数 \\
适用场景 & 函数逼近，谱方法 & 实验数据平滑，图形绘制 \\
\bottomrule
\end{tabular}
\end{center}

\section{数值微分}
\subsection{引论}
目的: 近似计算导数值。核心挑战: 截断误差 ($E_T$) 与舍入误差 ($E_R$) 的平衡。数值微分是\textbf{病态的 (ill-conditioned)}问题。

\subsection{基于泰勒展开的差分公式 ($h>0$ 为步长)}
\subsubsection{一阶导数 $f'(x_0)$}
\begin{enumerate}[label*=\arabic*.]
    \item \textbf{向前差分}: $f'(x_0) \approx \frac{f(x_0+h) - f(x_0)}{h}$, $E_T = -\frac{h}{2}f''(\xi_1) = O(h)$
    \item \textbf{向后差分}: $f'(x_0) \approx \frac{f(x_0) - f(x_0-h)}{h}$, $E_T = \frac{h}{2}f''(\xi_2) = O(h)$
    \item \textbf{中心差分}: $f'(x_0) \approx \frac{f(x_0+h) - f(x_0-h)}{2h}$, $E_T = -\frac{h^2}{6}f'''(\xi) = O(h^2)$
\end{enumerate}
\subsubsection{二阶导数 $f''(x_0)$}
\begin{enumerate}[label*=\arabic*.]
    \item \textbf{中心差分}: $f''(x_0) \approx \frac{f(x_0+h) - 2f(x_0) + f(x_0-h)}{h^2}$, $E_T = -\frac{h^2}{12}f^{(4)}(\eta) = O(h^2)$
\end{enumerate}

\subsection{基于插值多项式的微分公式}
一般思想: $f^{(k)}(x) \approx P_n^{(k)}(x)$，其中 $P_n(x)$ 为插值多项式。
例如，过 $(x_0-h, f_{-1}), (x_0, f_0), (x_0+h, f_1)$ 的二次插值多项式 $P_2(x)$，求导可得:
$P_2'(x_0) = \frac{f_1 - f_{-1}}{2h}$ (中心差分 $O(h^2)$)。
$P_2''(x_0) = \frac{f_1 - 2f_0 + f_{-1}}{h^2}$ (中心差分 $O(h^2)$)。

\subsection{舍入误差与步长选择 (详细)}
总误差 $E_{total}(h) = E_T(h) + E_R(h)$。设函数计算舍入误差界为 $\epsilon$。
\begin{itemize}
    \item \textbf{向前/向后差分 $f'(x_0)$}: $E_T \sim C_1h$, $|E_R| \lesssim \frac{2\epsilon}{h}$.
    $h_{opt} \approx \sqrt{\frac{4\epsilon}{|f''|}}$. 最小总误差 $\approx 2\sqrt{\epsilon |f''|}$.
    \item \textbf{中心差分 $f'(x_0)$}: $E_T \sim C_2h^2$, $|E_R| \lesssim \frac{\epsilon}{h}$.
    $h_{opt} \approx \left(\frac{3\epsilon}{|f'''|}\right)^{1/3}$. 最小总误差 $\approx \text{const} \cdot \epsilon^{2/3}$.
    \item \textbf{中心差分 $f''(x_0)$}: $E_T \sim C_3h^2$, $|E_R| \lesssim \frac{4\epsilon}{h^2}$.
    $h_{opt} \approx \left(\frac{48\epsilon}{|f^{(4)}|}\right)^{1/4}$. 最小总误差 $\approx \text{const} \cdot \epsilon^{1/2}$.
\end{itemize}
结论: $h$ 的选择是权衡；数值微分对噪声敏感；能达到的最高精度有限。

\subsection{理查森外推法 (Richardson Extrapolation)}
\subsubsection{动机与原理}
通过组合不同步长的近似值，消除低阶误差项。设真值 $M = N(h) + K_1 h^{p_1} + K_2 h^{p_2} + \dots$.
\subsubsection{外推公式推导}
取步长 $h$ 和 $h/r$ (通常 $r=2$)：
$$N_1(h) = \frac{r^{p_1}N(h/r) - N(h)}{r^{p_1}-1} = N(h/r) + \frac{N(h/r) - N(h)}{r^{p_1}-1}$$
$N_1(h)$ 的误差为 $O(h^{p_2})$。
\subsubsection{应用于中心差分求 $f'(x)$}
$D(h) = \frac{f(x+h)-f(x-h)}{2h}$, $f'(x) = D(h) + K_1 h^2 + K_2 h^4 + \dots$.
$p_1=2$, $r=2$: $D_1(h) = D(h/2) + \frac{D(h/2) - D(h)}{2^2-1} = D(h/2) + \frac{D(h/2) - D(h)}{3}$. $D_1(h)$ 误差 $O(h^4)$.
\subsubsection{迭代理查森外推 (Romberg方法思想)}
设 $N_{k,0} = N(h/2^k)$.
$N_{k,j+1} = N_{k+1,j} + \frac{N_{k+1,j} - N_{k,j}}{2^{p_j}-1}$.
(对于中心差分导数， $p_j = 2(j+1)$，即 $p_0=2, p_1=4, \dots$)
\begin{center}
\begin{tabular}{c|cccc}
$h$ & $N_{k,0} (O(h^2))$ & $N_{k,1} (O(h^4))$ & $N_{k,2} (O(h^6))$ & $\dots$ \\
\hline
$h_0$ & $N_{0,0}$ & & & \\
$h_0/2$ & $N_{1,0}$ & $N_{0,1}$ & & \\
$h_0/4$ & $N_{2,0}$ & $N_{1,1}$ & $N_{0,2}$ & \\
$\vdots$ & $\vdots$ & $\vdots$ & $\vdots$ & $\ddots$
\end{tabular}
\end{center}
\subsubsection{优缺点}
优点: 显著提高精度；过程系统化。缺点: 依赖误差展开式的已知形式；初始计算值仍受舍入误差影响。

\end{document}
```