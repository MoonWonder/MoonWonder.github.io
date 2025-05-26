---
author: "MoonWonder"
author_link: "moonwonder.top"
title: "数值分析笔记——ODE"
date: 2025-05-26T19:11:43+08:00
lastmod: 2025-05-26T19:11:43+08:00
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

# 数值分析课程笔记 (详细版): 常微分方程数值解法

**授课老师**: Gemini
**日期**: 2025年5月26日

## 1. 引论 (Introduction to ODEs)

### 1.1. 定义与示例
**常微分方程 (Ordinary Differential Equation, ODE)** 是一个包含未知函数及其导数的方程，其中该未知函数是**单个独立自变量**的函数。
-   **一阶ODE**: 通式为 $y'(t) = f(t, y(t))$ 或 $\frac{dy}{dt} = f(t,y)$。
    -   示例1 (指数衰减/增长): $y' = ky$。若 $y(0)=y_0$，则解为 $y(t)=y_0 e^{kt}$。
    -   示例2 (逻辑斯蒂方程): $y' = ry(1 - y/K)$，描述种群增长。
    -   示例3 (RL电路): $L \frac{di}{dt} + Ri = V(t)$。
-   **高阶ODE**: 包含二阶或更高阶导数。例如，$n$ 阶ODE通式为 $y^{(n)}(t) = f(t, y, y', \dots, y^{(n-1)})$。
    -   示例 (简谐振子): $y'' + \omega^2 y = 0$。

### 1.2. 初值问题 (Initial Value Problem, IVP)
一个常微分方程通常有无穷多个解（包含任意常数）。为了得到一个唯一的特解，我们需要指定初始条件。
-   对于一阶ODE $y' = f(t,y)$，一个初值问题 (IVP) 通常形如：
    $$\begin{cases} y'(t) = f(t, y(t)) \\ y(t_0) = y_0 \end{cases}$$
    其中 $(t_0, y_0)$ 是已知的初始点和初始值。我们求解的是在 $t \ge t_0$ (或包含 $t_0$ 的某个区间) 上的函数 $y(t)$。
-   对于 $n$ 阶ODE，需要 $n$ 个初始条件，通常是在 $t_0$ 点的函数值及其前 $n-1$ 阶导数值：
    $y(t_0)=c_0, y'(t_0)=c_1, \dots, y^{(n-1)}(t_0)=c_{n-1}$。

### 1.3. 解的存在性与唯一性
对于IVP $y'(t) = f(t,y), y(t_0)=y_0$：
-   **存在性**: 如果 $f(t,y)$ 在包含点 $(t_0, y_0)$ 的某个矩形区域 $D = \{(t,y) | |t-t_0| \le a, |y-y_0| \le b \}$ 内连续，则IVP至少在区间 $|t-t_0| \le \min(a, b/M)$ (其中 $M=\max_D |f(t,y)|$) 内存在一个解。
-   **唯一性**: 如果在上述区域 $D$ 内，$f(t,y)$ 关于 $y$ 还满足**利普希茨条件 (Lipschitz condition)**，即存在常数 $L>0$ 使得对区域 $D$ 内的任意 $(t,y_1)$ 和 $(t,y_2)$，都有：
    $$|f(t,y_1) - f(t,y_2)| \le L|y_1 - y_2|$$
    则IVP在该存在区间内有唯一的解。
    一个更强的（但更容易验证的）条件是：如果 $\frac{\partial f}{\partial y}$ 在 $D$ 内存在且有界，则 $f$ 满足利普希茨条件。

### 1.4. 为何需要数值方法？
1.  **无解析解**: 大多数实际问题中的ODE（尤其非线性ODE）无法找到用初等函数表示的解析解。
2.  **解析解复杂**: 即使存在解析解，形式也可能非常复杂，不便于实际计算或分析。
3.  **模型仿真**: 物理、化学、生物、工程、经济等领域的许多动态系统用ODE建模，数值解法是进行系统行为预测和仿真的关键。

### 1.5. 数值解法的基本思想
给定IVP $y'(t) = f(t,y), y(t_0)=y_0$。我们希望在离散时间点 $t_0, t_1, t_2, \dots, t_N$ 上找到解的近似值 $y_0, y_1, y_2, \dots, y_N$。通常取等距节点 $t_k = t_0 + kh$，其中 $h$ 是**步长 (step size)**。
数值方法提供一个递推关系，从已知的 $(t_k, y_k)$ 和微分方程本身，计算出下一个点的近似值 $y_{k+1} \approx y(t_{k+1})$。

## 2. 欧拉方法 (Euler's Method)

### 2.1. 推导
1.  **泰勒展开**: $y(t_{k+1}) = y(t_k+h) = y(t_k) + h y'(t_k) + \frac{h^2}{2} y''(\xi_k)$ for $\xi_k \in (t_k, t_{k+1})$。
    已知 $y'(t_k) = f(t_k, y(t_k))$。忽略 $O(h^2)$ 项，并用 $y_k$ 近似 $y(t_k)$：
    $$y_{k+1} = y_k + h f(t_k, y_k)$$
2.  **差分近似**: $y'(t_k) \approx \frac{y(t_{k+1}) - y(t_k)}{h}$ (向前差分)。
    $f(t_k, y_k) \approx \frac{y_{k+1} - y_k}{h} \implies y_{k+1} = y_k + h f(t_k, y_k)$。

### 2.2. 几何解释
在点 $(t_k, y_k)$ 处，解曲线的斜率为 $f(t_k, y_k)$。欧拉法沿着这条切线方向前进一个步长 $h$，到达的点 $(t_{k+1}, y_k + hf(t_k,y_k))$ 作为 $y(t_{k+1})$ 的近似值 $y_{k+1}$。本质上是用直线段逼近解曲线。

### 2.3. 误差分析
-   **局部截断误差 (LTE)**: 假设 $y_k = y(t_k)$ (当前步初值精确)，一步计算产生的误差。
    LTE $= y(t_{k+1}) - (y_k + h f(t_k, y_k)) = y(t_{k+1}) - (y(t_k) + h y'(t_k)) = \frac{h^2}{2} y''(\xi_k)$。
    所以欧拉法的 LTE 是 $O(h^2)$。
-   **全局截断误差 (GTE)**: 在某个固定时间 $T = t_0 + Nh$ 处的累积误差 $E_N = |y(T) - y_N|$。
    可以证明，对于欧拉方法，GTE 是 $O(h)$。因此，欧拉法是一个**一阶方法**。这意味着误差与步长 $h$ 成正比。

### 2.4. 示例: $y'=y, y(0)=1$
精确解 $y(t)=e^t$。取 $h=0.1$。
-   $t_0=0, y_0=1$.
-   $k=0$: $f(t_0, y_0) = y_0 = 1$.
    $y_1 = y_0 + h f(t_0, y_0) = 1 + 0.1 \cdot 1 = 1.1$.
    $y(t_1) = y(0.1) = e^{0.1} \approx 1.10517$. 误差 $E_1 \approx 0.00517$.
-   $k=1$: $f(t_1, y_1) = y_1 = 1.1$.
    $y_2 = y_1 + h f(t_1, y_1) = 1.1 + 0.1 \cdot 1.1 = 1.21$.
    $y(t_2) = y(0.2) = e^{0.2} \approx 1.22140$. 误差 $E_2 \approx 0.01140$.
可见误差随步数增加而累积。

### 2.5. 局限性
精度低，除非 $h$ 非常小。对于某些“刚性”问题，稳定性差。

## 3. 泰勒级数方法 (Taylor Series Methods)

### 3.1. 基本思想
利用更高阶的泰勒展开项来提高精度。
$y(t_{k+1}) = y(t_k) + hy'(t_k) + \frac{h^2}{2!}y''(t_k) + \dots + \frac{h^p}{p!}y^{(p)}(t_k) + \frac{h^{p+1}}{(p+1)!}y^{(p+1)}(\xi_k)$

### 3.2. $p$ 阶泰勒方法
数值格式: $y_{k+1} = y_k + \sum_{j=1}^p \frac{h^j}{j!} f^{(j-1)}(t_k, y_k)$
其中 $f^{(j-1)}(t,y)$ 是 $f(t,y(t))$ 对 $t$ 的 $(j-1)$ 阶全导数。
$f^{(0)}(t,y) = f(t,y)$
$f^{(1)}(t,y) = \frac{df}{dt} = \frac{\partial f}{\partial t} + \frac{\partial f}{\partial y} y' = \frac{\partial f}{\partial t} + \frac{\partial f}{\partial y} f$
$f^{(2)}(t,y) = \frac{d}{dt}f^{(1)}(t,y) = \frac{\partial f^{(1)}}{\partial t} + \frac{\partial f^{(1)}}{\partial y} f$
    $= \frac{\partial}{\partial t}\left(\frac{\partial f}{\partial t} + \frac{\partial f}{\partial y} f\right) + \frac{\partial}{\partial y}\left(\frac{\partial f}{\partial t} + \frac{\partial f}{\partial y} f\right) f$
    $= \frac{\partial^2 f}{\partial t^2} + \frac{\partial^2 f}{\partial t \partial y}f + \frac{\partial f}{\partial y}\frac{\partial f}{\partial t} + \left( \frac{\partial^2 f}{\partial y \partial t} + \frac{\partial^2 f}{\partial y^2}f + \left(\frac{\partial f}{\partial y}\right)^2 \right)f + \frac{\partial f}{\partial y}\left( \frac{\partial f}{\partial t} + \frac{\partial f}{\partial y} f \right)$
(假设偏导数连续，混合偏导次序可交换，上式可化简，但依然复杂)

### 3.3. 误差与优缺点
-   LTE: $O(h^{p+1})$。GTE: $O(h^p)$ ( $p$ 阶方法)。
-   **优点**: 理论上可达任意高阶。
-   **主要缺点**: 计算 $f$ 的高阶全导数非常复杂且繁琐，对每个新的ODE都需要重新推导。

## 4. 龙格-库塔方法 (Runge-Kutta Methods, RK)

**核心思想**: 通过在步长 $[t_k, t_{k+1}]$ 内对 $f(t,y)$ 进行多次估值（计算斜率），然后对这些斜率进行加权平均，以构造出与高阶泰勒展开相匹配的更新公式，从而避免直接计算 $f$ 的高阶导数。

### 4.1. 一般形式 ($s$-级显式RK)
$$y_{k+1} = y_k + h \sum_{i=1}^s b_i k_i$$
其中 $k_i$ 是中间计算的斜率：
$$\begin{align*} k_1 &= f(t_k, y_k) \\\\ k_2 &= f(t_k + c_2 h, y_k + h a_{21} k_1) \\\\ &\vdots \\\\ k_s &= f\left(t_k + c_s h, y_k + h \sum_{j=1}^{s-1} a_{sj} k_j\right)\end{align*}$$
系数 $b_i, c_i, a_{ij}$ 通过匹配泰勒展开确定。通常 $\sum c_i = \sum a_{ij}$ (按行求和)。

### 4.2. 二阶龙格-库塔方法 (RK2)
LTE $O(h^3)$ (二阶方法)。系数满足 $b_1+b_2=1, b_2c_2=1/2, b_2a_{21}=1/2$。
-   **改进欧拉法 (Heun's Method / 修正欧拉法)**:
    选取 $b_1=1/2, b_2=1/2, c_2=1, a_{21}=1$。
    $k_1 = f(t_k, y_k)$
    $k_2 = f(t_k + h, y_k + h k_1)$ (预测步)
    $y_{k+1} = y_k + \frac{h}{2}(k_1 + k_2)$ (校正步，平均斜率)
-   **中点法 (Midpoint Method / 改进多边形法)**:
    选取 $b_1=0, b_2=1, c_2=1/2, a_{21}=1/2$。
    $k_1 = f(t_k, y_k)$
    $k_2 = f(t_k + \frac{h}{2}, y_k + \frac{h}{2} k_1)$ (计算中点处的斜率)
    $y_{k+1} = y_k + h k_2$ (用中点斜率推进整步)

### 4.3. 四阶龙格-库塔方法 (RK4 - "经典RK4")
LTE $O(h^5)$ (四阶方法)。每个步长内计算4次 $f(t,y)$。
**公式**: $$y_{k+1} = y_k + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$
其中：
$$\begin{align*} k_1 &= f(t_k, y_k) \\\\ k_2 &= f\left(t_k + \frac{h}{2}, y_k + \frac{h}{2} k_1\right) \\\\ k_3 &= f\left(t_k + \frac{h}{2}, y_k + \frac{h}{2} k_2\right) \\\\ k_4 &= f(t_k + h, y_k + h k_3)\end{align*}$$
-   **优点**: 精度高 (4阶)，自启动，不需计算 $f$ 的导数，稳定性较好。
-   **缺点**: 每步计算4次 $f$，计算量相对较大；标准RK4无直接的简便误差估计方法。

## 5. 自适应步长龙格-库塔方法

**动机**: 根据解的局部行为自动调整步长 $h$，以固定的精度要求优化计算效率。
**核心**: 利用嵌入式龙格-库塔对 (Embedded RK Pairs) 来估计局部截断误差。
-   同时计算一个 $p$ 阶近似 $y_{k+1}^{(p)}$ 和一个 $p+1$ 阶近似 $y_{k+1}^{(p+1)}$，要求它们共享大部分中间斜率 $k_i$ 的计算。
-   误差估计: $\Delta = |y_{k+1}^{(p+1)} - y_{k+1}^{(p)}|$，这可作为 $y_{k+1}^{(p)}$ 的LTE的估计。

### 5.1. 龙格-库塔-费尔贝格方法 (RKF45)
-   是一个(4,5)对，即 $y_{k+1}^{(4)}$ 是4阶解，$y_{k+1}^{(5)}$ 是5阶解。
-   共用 **6 次** $f(t,y)$ 的求值得到 $k_1, \dots, k_6$。
    $y_{k+1}^{(4)} = y_k + h \sum b_i^{(4)} k_i$
    $y_{k+1}^{(5)} = y_k + h \sum b_i^{(5)} k_i$
-   误差估计: $\Delta = |y_{k+1}^{(5)} - y_{k+1}^{(4)}|$ (这是对 $y_{k+1}^{(4)}$ 误差的估计，约为 $O(h^5)$)。
-   **步长控制**:
    1.  计算 $\Delta$。目标是使 $\Delta$ 约等于用户指定的容限 $\text{TOL}$。
    2.  新的建议步长 $h_{new} = S \cdot h_{old} \left(\frac{\text{TOL}}{\Delta}\right)^{1/(p+1)}$ (对于RKF45的 $y^{(4)}$，其误差是 $O(h^5)$, 所以分母中的阶数是5)。$S$ 是安全因子 ($0.8 \sim 0.9$)。
    3.  如果 $\Delta \le \text{TOL}$: 接受当前步。用更高阶的 $y_{k+1}^{(5)}$ 作为 $y_{k+1}$ (局部外推)。$t_{k+1} = t_k + h_{old}$。用 $h_{new}$ 作为下一尝试步长。
    4.  如果 $\Delta > \text{TOL}$: 拒绝当前步。不更新 $t, y$。用 $h_{new}$ (此时会变小) 作为当前步的步长，重新计算。
-   **优点**: 高效、可靠，用户只需指定全局容限。常用的还有Dormand-Prince对 (MATLAB `ode45`)。

## 6. 线性多步法 (Linear Multi-step Methods, LMM)

**思想**: 计算 $y_{n+k}$ 时，利用 $k$ 个历史点 $y_n, \dots, y_{n+k-1}$ 以及对应的导数值 $f_n, \dots, f_{n+k-1}$ (甚至 $f_{n+k}$)。
**一般形式 ($k$-步法)**: $\sum_{i=0}^k \alpha_i y_{n+i} = h \sum_{i=0}^k \beta_i f_{n+i}$ (通常 $\alpha_k=1$)
-   **显式 (Explicit)**: 若 $\beta_k = 0$ ($f_{n+k}$ 不出现)。
-   **隐式 (Implicit)**: 若 $\beta_k \ne 0$ ($f_{n+k}$ 出现，需解方程)。

### 6.1. 亚当斯方法 (Adams Methods)
基于对 $f(t,y(t))$ 的多项式插值，然后积分 $y_{n+k} - y_{n+k-1} = \int_{t_{n+k-1}}^{t_{n+k}} f(t,y(t)) dt$ (或 $y_{n+1} - y_n = \int_{t_n}^{t_{n+1}} f(t,y(t)) dt$ 等形式，这里以课上常用形式为准)。
具体形式为: $\alpha_k=1, \alpha_{k-1}=-1$, 其他 $\alpha_i=0$。
$y_{n+k} = y_{n+k-1} + h \sum_{i=0}^k \beta_i f_{n+i}$ (这里 $k$ 指的是使用 $f$ 的个数)

#### a) 亚当斯-巴什福思 (Adams-Bashforth, AB - 显式)
用 $(t_n, f_n), \dots, (t_{n-m+1}, f_{n-m+1})$ (共 $m$ 个点)插值 $f$，积分区间 $[t_n, t_{n+1}]$。
$y_{n+1} = y_n + h \sum_{j=0}^{m-1} \gamma_j f_{n-j}$
-   **AB1 (欧拉)**: $y_{n+1} = y_n + hf_n$. (阶1, LTE $O(h^2)$)
-   **AB2**: $y_{n+1} = y_n + h\left(\frac{3}{2}f_n - \frac{1}{2}f_{n-1}\right)$. (阶2, LTE $O(h^3)$)
-   **ABm**: $m$ 阶方法, LTE $O(h^{m+1})$。

#### b) 亚当斯-莫尔顿 (Adams-Moulton, AM - 隐式)
用 $(t_{n+1}, f_{n+1}), (t_n, f_n), \dots, (t_{n-m+1}, f_{n-m+1})$ (共 $m+1$ 个点) 插值 $f$，积分区间 $[t_n, t_{n+1}]$。
$y_{n+1} = y_n + h \sum_{j=0}^{m} \delta_j f_{n+1-j}$
-   **AM0 (向后欧拉)**: (用1个点 $f_{n+1}$) $y_{n+1} = y_n + hf_{n+1}$. (阶1, LTE $O(h^2)$)
-   **AM1 (梯形法)**: (用2个点 $f_{n+1},f_n$) $y_{n+1} = y_n + \frac{h}{2}(f_{n+1} + f_n)$. (阶2, LTE $O(h^3)$)
-   **AMm**: ($m+1$ 点公式) $m+1$ 阶方法, LTE $O(h^{m+2})$。AM法通常比亚当斯-巴什福思法阶数高1，且更稳定。

### 6.2. 预测-校正方法 (Predictor-Corrector Methods)
避免求解隐式方程的非线性问题。
1.  **P (Predict)**: 用显式法 (如AB) 估计 $y_{n+1}^{(0)}$。
2.  **E (Evaluate)**: 计算 $f_{n+1}^{(0)} = f(t_{n+1}, y_{n+1}^{(0)})$。
3.  **C (Correct)**: 用隐式法 (如AM)，但使用 $f_{n+1}^{(0)}$，得到 $y_{n+1}$。
    $y_{n+1} = y_n + h \sum \delta_j f_{n+1-j}^{(0 \text{ or previous})}$
4.  **(可选) E**: 计算 $f_{n+1} = f(t_{n+1}, y_{n+1})$。
-   **ABM对**: 如AB4作预测，AM4作校正。每步通常只需两次（或一次，取决于模式）函数求值。
-   $|y_{n+1} - y_{n+1}^{(0)}|$ 可用于误差估计和步长控制。

### 6.3. BDF 方法 (Backward Differentiation Formulas)
另一类重要的隐式多步法。通过用 $(t_{n+k}, y_{n+k}), \dots, (t_n, y_n)$ 插值 $y(t)$ 得到多项式 $P(t)$，然后令 $P'(t_{n+k}) = f(t_{n+k}, y_{n+k})$。
-   **BDFk**: $k$ 阶方法。常用于求解刚性方程。
    -   BDF1 (向后欧拉): $y_{n+1} - y_n = h f_{n+1}$
    -   BDF2: $y_{n+1} - \frac{4}{3}y_n + \frac{1}{3}y_{n-1} = \frac{2h}{3}f_{n+1}$

### 6.4. 多步法的优缺点
-   **优点**: 计算效率可能较高 (对同阶精度，每步 $f$ 求值次数少)，预测-校正法易于误差估计。
-   **缺点**: 非自启动 (需要前 $k$ 个值，通常由单步法提供)；步长改变困难；可能存在稳定性问题 (寄生根)。

## 7. 线性多步法的理论基础

对于LMM $\sum_{i=0}^k \alpha_i y_{n+i} = h \sum_{i=0}^k \beta_i f_{n+i}$ (设 $\alpha_k=1$):
-   **局部截断误差 (LTE)**: $T_{n+k} = \frac{1}{h\sigma(1)} \left( \sum \alpha_i y(t_{n+i}) - h \sum \beta_i y'(t_{n+i}) \right)$ (一种定义)。
    若 $LTE = C_p h^p + O(h^{p+1})$ (注意这里的LTE定义为误差本身，而不是$O(h^{p+1})$)，则方法为 $p$ 阶。
    通常 LTE 表示为 $C_{p+1}h^{p+1}y^{(p+1)}(t_n) + O(h^{p+2})$，则方法阶数为 $p$。
-   **特征多项式**: $\rho(z) = \sum_{i=0}^k \alpha_i z^i$, $\sigma(z) = \sum_{i=0}^k \beta_i z^i$.
-   **相容性 (Consistency)**: 方法至少为1阶 ($p \ge 1$)。条件:
    1.  $\rho(1) = 0 \quad (\Leftrightarrow \sum \alpha_i = 0)$
    2.  $\rho'(1) = \sigma(1) \quad (\Leftrightarrow \sum i \alpha_i = \sum \beta_i)$
-   **零稳定性 (Zero-Stability / D-Stability)**: $\rho(z)=0$ 的所有根 $z_j$ 满足:
    1.  $|z_j| \le 1$
    2.  若 $|z_j|=1$，则 $z_j$ 必须是单根。
    (主根 $z=1$ 总是存在的)。
-   **收敛性 (Convergence)**: **Dahlquist等价定理**: LMM收敛 $\iff$ 相容 + 零稳定。
-   **Dahlquist第一障碍**: 零稳定的 $k$-步LMM，其阶 $p \le k+2$ (若 $k$ 偶)，$p \le k+1$ (若 $k$ 奇)。显式则 $p \le k$。
-   **绝对稳定性**: 研究方法对测试方程 $y'=\lambda y$ ($\text{Re}(\lambda)<0$) 的行为。
    -   **特征方程**: $P(z; h\lambda) = \rho(z) - h\lambda \sigma(z) = 0$.
    -   **绝对稳定区域**: 使 $P(z;h\lambda)=0$ 的所有根 $|z_j|\le1$ (单位圆上根为单根) 的复数 $h\lambda$ 的集合。

## 8. 刚性微分方程 (Stiff Equations)

### 8.1. 定义与特征
-   解中包含变化速率差异极大的分量 (时间尺度差异大)。
-   对应雅可比矩阵 $\partial\mathbf{f}/\partial\mathbf{y}$ 的特征值 $\lambda_i$ 满足:
    1.  $\text{Re}(\lambda_i) \le 0$ (解稳定)
    2.  $\max_i |\text{Re}(\lambda_i)| / \min_j |\text{Re}(\lambda_j)| \gg 1$ (刚度比大)
-   显式方法求解刚性问题时，为保持数值稳定，步长 $h$ 必须由变化最快（即使已衰减）的分量决定，导致效率极低。

### 8.2. 求解刚性方程的方法
需要具有良好绝对稳定性的方法。
-   **A-稳定性 (A-stability)**: 绝对稳定区域包含整个左半复平面 $\text{Re}(h\lambda) \le 0$。
    -   向后欧拉法、梯形法是A稳定的。
    -   **Dahlquist第二障碍**: A稳定的LMM最高阶为2 (梯形法)；显式LMM不可能是A稳定的。
-   **L-稳定性 (L-stability)**: A稳定，并且当 $\text{Re}(h\lambda) \to -\infty$ 时，方法的放大因子趋于0 (能有效抑制刚性分量)。
    -   向后欧拉法是L稳定的；梯形法不是。
-   **后向差分公式 (BDFs)**:
    -   BDF1 (向后欧拉) 和 BDF2 是A稳定的 (且L稳定)。
    -   BDF3-BDF6 不是严格A稳定，但具有非常好的刚性稳定性 (stiffly stable)，绝对稳定区域包含左半平面一个大的楔形区域且包含负实轴远端。是求解刚性问题的常用方法。
-   **隐式龙格-库塔方法 (IRK)**: 某些IRK方法 (如基于Gauss-Legendre配置点的方法) 是A稳定的，可以达到很高阶。

### 8.3. 求解隐式方程
隐式方法每步需求解关于 $y_{k+1}$ 的代数方程 (组) $y_{k+1} = \Psi(y_{k+1})$ 或 $G(y_{k+1})=0$。
-   **不动点迭代**: $y_{k+1}^{(s+1)} = \Psi(y_{k+1}^{(s)})$。收敛性依赖 $h L < 1$。对刚性问题可能要求 $h$ 过小。
-   **牛顿法 (及其变种)**: 求解 $G(y_{k+1})=0$。
    $y_{k+1}^{(s+1)} = y_{k+1}^{(s)} - [J_G]^{-1} G(y_{k+1}^{(s)})$。
    对于 $y_{k+1} = \text{已知项} + h \beta_0 f(t_{k+1}, y_{k+1})$, 则 $G(y_{k+1}) = y_{k+1} - h \beta_0 f(t_{k+1}, y_{k+1}) - \text{已知项}$。
    雅可比矩阵 $J_G = I - h \beta_0 \frac{\partial f}{\partial y}(t_{k+1}, y_{k+1}^{(s)})$。对刚性问题更鲁棒。

## 9. 高阶ODE与一阶ODE组

### 9.1. 转化方法
一个 $N$ 阶ODE $y^{(N)}(t) = g(t, y, y', \dots, y^{(N-1)})$ 可以通过引入新变量转换为一个 $N$ 维的一阶ODE组。
令 $Y_1 = y, Y_2 = y', \dots, Y_N = y^{(N-1)}$。
则系统为:
$$
\begin{align*} Y_1' &= Y_2 \\\\ Y_2' &= Y_3 \\\\ &\vdots \\\\ Y_{N-1}' &= Y_N \\\\ Y_N' &= g(t, Y_1, Y_2, \dots, Y_N) \end{align*}
$$
初始条件也相应转换: $Y_j(t_0) = y^{(j-1)}(t_0)$。

### 9.2. 向量形式与数值方法应用
一阶ODE组可写为 $\mathbf{y}'(t) = \mathbf{f}(t, \mathbf{y}(t))$，其中 $\mathbf{y}, \mathbf{f}$ 是向量。
所有学过的数值方法 (欧拉、RK、LMM) 均可直接应用于此向量形式，只需将标量运算替换为向量运算。
-   **欧拉法**: $\mathbf{y}_{k+1} = \mathbf{y}_k + h \mathbf{f}(t_k, \mathbf{y}_k)$
-   **RK4**: $\mathbf{y}_{k+1} = \mathbf{y}_k + \frac{h}{6}(\mathbf{k}_1 + 2\mathbf{k}_2 + 2\mathbf{k}_3 + \mathbf{k}_4)$，其中 $\mathbf{k}_i$ 为向量。
-   **隐式方法**: 如向后欧拉 $\mathbf{y}_{k+1} = \mathbf{y}_k + h \mathbf{f}(t_{k+1}, \mathbf{y}_{k+1})$，每步需求解一个 $m$ 元非线性代数方程组，通常使用多维牛顿法，涉及雅可比矩阵 $J = \partial \mathbf{f}/\partial \mathbf{y}$。
    牛顿迭代: $\mathbf{y}_{k+1}^{(s+1)} = \mathbf{y}_{k+1}^{(s)} - [I - h \beta_0 J(t_{k+1}, \mathbf{y}_{k+1}^{(s)})]^{-1} (\mathbf{y}_{k+1}^{(s)} - \text{已知项} - h \beta_0 \mathbf{f}(t_{k+1}, \mathbf{y}_{k+1}^{(s)}))$.


```tex
\documentclass[UTF8,a4paper]{ctexart}
\usepackage{amsmath, amssymb, amsfonts, bm}
\usepackage{geometry}
\geometry{a4paper, margin=1in, bottom=1.5in} % Increased bottom margin for potentially long pages
\usepackage{array}
\usepackage{booktabs}
\usepackage{enumitem}
\usepackage{multicol} % For examples if needed

\setlength{\parskip}{0.5em} % Add some space between paragraphs
\setlength{\parindent}{0em} % No indent for new paragraphs

\title{数值分析课程笔记 (详细版): 常微分方程数值解法}
\author{Gemini 老师}
\date{2025年5月26日}

\begin{document}
\maketitle
\tableofcontents
\newpage

\section{引论 (Introduction to ODEs)}

\subsection{定义与示例}
\textbf{常微分方程 (Ordinary Differential Equation, ODE)} 是一个包含未知函数及其导数的方程，其中该未知函数是\textbf{单个独立自变量}的函数。
\begin{itemize}
    \item \textbf{一阶ODE}: 通式为 $y'(t) = f(t, y(t))$ 或 $\frac{dy}{dt} = f(t,y)$。
    \item \textbf{高阶ODE}: 包含二阶或更高阶导数。例如，$n$ 阶ODE通式为 $y^{(n)}(t) = f(t, y, y', \dots, y^{(n-1)})$。
\end{itemize}

\subsection{初值问题 (Initial Value Problem, IVP)}
对于一阶ODE $y' = f(t,y)$，一个初值问题 (IVP) 通常形如：
$$ \begin{cases} y'(t) = f(t, y(t)) \\ y(t_0) = y_0 \end{cases} $$
其中 $(t_0, y_0)$ 是已知的初始点和初始值。

\subsection{解的存在性与唯一性}
对于IVP $y'(t) = f(t,y), y(t_0)=y_0$：
如果 $f(t,y)$ 在区域 $D$ 内连续，且关于 $y$ 满足\textbf{利普希茨条件 (Lipschitz condition)} (即 $\exists L>0$ s.t. $|f(t,y_1) - f(t,y_2)| \le L|y_1 - y_2|$ 对所有 $(t,y_1), (t,y_2) \in D$)，则IVP在 $t_0$ 附近存在唯一的解。

\subsection{为何需要数值方法？}
许多实际问题中的ODE无解析解或解析解复杂。数值解法是进行系统行为预测和仿真的关键。

\subsection{数值解法的基本思想}
给定IVP $y'(t) = f(t,y), y(t_0)=y_0$。在离散时间点 $t_k = t_0 + kh$ ($h$为步长) 上找到解的近似值 $y_k \approx y(t_k)$。数值方法提供从 $(t_k, y_k)$ 计算 $y_{k+1}$ 的递推关系。

\section{欧拉方法 (Euler's Method)}
\subsection{推导}
基于泰勒展开 $y(t_{k+1}) = y(t_k) + h y'(t_k) + O(h^2)$，忽略 $O(h^2)$ 项，并用 $f(t_k, y_k)$ 代替 $y'(t_k)$：
$$y_{k+1} = y_k + h f(t_k, y_k)$$
\subsection{几何解释}
沿点 $(t_k, y_k)$ 处的切线方向前进一个步长 $h$。
\subsection{误差分析}
\begin{itemize}
    \item \textbf{局部截断误差 (LTE)}: $y(t_{k+1}) - (y(t_k) + h y'(t_k)) = \frac{h^2}{2} y''(\xi_k) = O(h^2)$。
    \item \textbf{全局截断误差 (GTE)}: $O(h)$ (一阶方法)。
\end{itemize}

\section{泰勒级数方法 (Taylor Series Methods)}
\subsection{基本思想}
$y(t_{k+1}) = y(t_k) + hy'(t_k) + \frac{h^2}{2!}y''(t_k) + \dots + \frac{h^p}{p!}y^{(p)}(t_k) + O(h^{p+1})$
\subsection{$p$ 阶泰勒方法}
$y_{k+1} = y_k + \sum_{j=1}^p \frac{h^j}{j!} f^{(j-1)}(t_k, y_k)$, 其中 $f^{(j-1)}$ 是 $f(t,y(t))$ 对 $t$ 的 $(j-1)$ 阶全导数。
$f^{(0)} = f$; $f^{(1)} = f_t + f_y f$; $f^{(2)} = (f_t + f_y f)_t + (f_t + f_y f)_y f$。
\subsection{误差与优缺点}
LTE: $O(h^{p+1})$ (方法为 $p$ 阶)。缺点: 计算 $f$ 的高阶全导数复杂。

\section{龙格-库塔方法 (Runge-Kutta Methods, RK)}
\textbf{思想}: 通过在步长 $[t_k, t_{k+1}]$ 内对 $f(t,y)$ 多次估值并加权平均，达到高阶精度，避免计算 $f$ 的高阶导数。
\textbf{一般形式 ($s$-级显式RK)}: $y_{k+1} = y_k + h \sum_{i=1}^s b_i k_i$, $k_1 = f(t_k, y_k)$, $k_i = f(t_k + c_i h, y_k + h \sum_{j=1}^{i-1} a_{ij} k_j)$.

\subsection{二阶龙格-库塔方法 (RK2)}
LTE $O(h^3)$ (二阶方法)。系数满足 $b_1+b_2=1, b_2c_2=1/2, b_2a_{21}=1/2$。
\begin{itemize}
    \item \textbf{改进欧拉法 (Heun's Method)}: $b_1=b_2=1/2, c_2=1, a_{21}=1$.
    $k_1 = f(t_k, y_k)$, $k_2 = f(t_k + h, y_k + h k_1)$, $y_{k+1} = y_k + \frac{h}{2}(k_1 + k_2)$.
    \item \textbf{中点法 (Midpoint Method)}: $b_1=0, b_2=1, c_2=1/2, a_{21}=1/2$.
    $k_1 = f(t_k, y_k)$, $k_2 = f(t_k + \frac{h}{2}, y_k + \frac{h}{2} k_1)$, $y_{k+1} = y_k + h k_2$.
\end{itemize}

\subsection{四阶龙格-库塔方法 (RK4 - "经典RK4")}
LTE $O(h^5)$ (四阶方法)。
\textbf{公式}: $y_{k+1} = y_k + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + 2k_4)$ (笔误修正：应为 $k_1+2k_2+2k_3+k_4$)
$$y_{k+1} = y_k + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$
其中：
\begin{align*}
    k_1 &= f(t_k, y_k) \\
    k_2 &= f\left(t_k + \frac{h}{2}, y_k + \frac{h}{2} k_1\right) \\
    k_3 &= f\left(t_k + \frac{h}{2}, y_k + \frac{h}{2} k_2\right) \\
    k_4 &= f(t_k + h, y_k + h k_3)
\end{align*}

\section{自适应步长龙格-库塔方法}
\textbf{核心}: 利用嵌入式RK对 (如 $p$ 阶和 $p+1$ 阶) 估计局部截断误差 $\Delta = |y_{k+1}^{(p+1)} - y_{k+1}^{(p)}|$。
\textbf{龙格-库塔-费尔贝格方法 (RKF45)}: (4,5)对，6次 $f$ 求值。用 $y^{(5)}$ 传播。
步长调整: $h_{new} = S \cdot h_{old} (\text{TOL}/\Delta)^{1/5}$ ($S$为安全因子)。

\section{线性多步法 (Linear Multi-step Methods, LMM)}
\textbf{思想}: 计算 $y_{n+k}$ 时利用 $k$ 个历史点信息。
\textbf{一般形式 ($k$-步法)}: $\sum_{i=0}^k \alpha_i y_{n+i} = h \sum_{i=0}^k \beta_i f_{n+i}$ ($\alpha_k=1$).
显式: $\beta_k = 0$。隐式: $\beta_k \ne 0$。

\subsection{亚当斯方法 (Adams Methods)}
($\alpha_k=1, \alpha_{k-1}=-1$, 其他 $\alpha_i=0$)
\begin{itemize}
    \item \textbf{亚当斯-巴什福思 (AB, 显式)}: $m$-步AB法为 $m$ 阶。
    AB2: $y_{n+1} = y_n + h(\frac{3}{2}f_n - \frac{1}{2}f_{n-1})$.
    \item \textbf{亚当斯-莫尔顿 (AM, 隐式)}: $m$-步AM法 ($m+1$个插值点 $f_{n+1}, \dots, f_{n-m+1}$) 为 $m+1$ 阶。
    AM2 (梯形法解ODE): $y_{n+1} = y_n + \frac{h}{2}(f_{n+1} + f_n)$.
\end{itemize}

\subsection{预测-校正方法 (Predictor-Corrector Methods)}
结合AB (预测P) 和 AM (校正C)。如AB4-AM4对。

\subsection{BDF 方法 (Backward Differentiation Formulas)}
隐式多步法，常用于刚性问题。BDF$k$ 是 $k$ 阶方法。
BDF1 (向后欧拉): $y_{n+1} - y_n = h f_{n+1}$.
BDF2: $y_{n+1} - \frac{4}{3}y_n + \frac{1}{3}y_{n-1} = \frac{2h}{3}f_{n+1}$.

\section{线性多步法的理论基础}
\begin{itemize}
    \item \textbf{LTE}: $T_n = O(h^{p+1})$ 则方法为 $p$ 阶。
    \item \textbf{特征多项式}: $\rho(z) = \sum_{i=0}^k \alpha_i z^i$, $\sigma(z) = \sum_{i=0}^k \beta_i z^i$.
    \item \textbf{相容性 (Consistency)}: $p \ge 1$. $\Leftrightarrow \rho(1)=0$ 和 $\rho'(1)=\sigma(1)$。
    \item \textbf{零稳定性 (Zero-Stability)}: $\rho(z)=0$ 的所有根 $z_j$ 满足 $|z_j| \le 1$，且单位圆上的根为单根。
    \item \textbf{收敛性 (Convergence)}: \textbf{Dahlquist等价定理}: 收敛 $\iff$ 相容 + 零稳定。
    \item \textbf{绝对稳定性}: 研究方法对 $y'=\lambda y$ 的行为。绝对稳定区域是使特征方程 $\rho(z) - h\lambda \sigma(z) = 0$ 的所有根 $|z_j|\le1$ 的 $h\lambda$ 集合。
\end{itemize}

\section{刚性微分方程 (Stiff Equations)}
\subsection{定义与特征}
解中包含变化速率差异极大的分量。雅可比矩阵特征值 $\lambda_i$ 满足 $\text{Re}(\lambda_i) \le 0$ 且 $\max|\text{Re}(\lambda_i)| \gg \min|\text{Re}(\lambda_j)|$.
显式方法求解刚性问题时，为保持稳定，步长 $h$ 必须非常小。
\subsection{求解刚性方程的方法}
\begin{itemize}
    \item \textbf{A-稳定性}: 绝对稳定区域包含整个左半复平面 $\text{Re}(h\lambda) \le 0$。
    向后欧拉法、梯形法是A稳定的。
    \item \textbf{L-稳定性}: A稳定，且当 $\text{Re}(h\lambda) \to -\infty$ 时，放大因子 $\to 0$。
    向后欧拉法是L稳定的。
    \item \textbf{BDF方法}: BDF1-BDF2 A稳定，BDF3-BDF6 刚性稳定。
    \item \textbf{隐式RK法}。
\end{itemize}
\subsection{求解隐式方程}
通常用牛顿法求解每步产生的非线性代数方程(组) $G(\mathbf{y}_{k+1}) = \mathbf{y}_{k+1} - h \beta_0 \mathbf{f}(t_{k+1}, \mathbf{y}_{k+1}) - \text{已知项} = \mathbf{0}$。
牛顿迭代: $\mathbf{y}_{k+1}^{(s+1)} = \mathbf{y}_{k+1}^{(s)} - [\mathbf{I} - h \beta_0 \mathbf{J}(t_{k+1}, \mathbf{y}_{k+1}^{(s)})]^{-1} G(\mathbf{y}_{k+1}^{(s)})$，其中 $\mathbf{J} = \partial \mathbf{f}/\partial \mathbf{y}$。

\section{高阶ODE与一阶ODE组}
\subsection{转化方法}
一个 $N$ 阶ODE $y^{(N)}(t) = g(t, y, \dots, y^{(N-1)})$ 可通过令 $Y_1=y, Y_2=y', \dots, Y_N=y^{(N-1)}$ 转化为 $N$ 个一阶ODE组成的方程组: $\mathbf{Y}'(t) = \mathbf{F}(t, \mathbf{Y}(t))$。
\subsection{向量形式与数值方法应用}
一阶ODE组可写为 $\mathbf{y}'(t) = \mathbf{f}(t, \mathbf{y}(t))$。所有学过的数值方法均可直接应用于此向量形式。
\begin{itemize}
    \item 欧拉法: $\mathbf{y}_{k+1} = \mathbf{y}_k + h \mathbf{f}(t_k, \mathbf{y}_k)$。
    \item RK4: $\mathbf{y}_{k+1} = \mathbf{y}_k + \frac{h}{6}(\mathbf{k}_1 + 2\mathbf{k}_2 + 2\mathbf{k}_3 + \mathbf{k}_4)$，其中 $\mathbf{k}_i$ 为向量。
\end{itemize}

\end{document}
```