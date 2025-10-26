---
title: Midterm Review
subtitle:
date: 2025-10-26T20:56:35+08:00
draft: false
author:
  name:
  link:
  email:
  avatar:
description:
keywords:
license:
comment: true
weight: 0
tags:
  - draft
categories:
  - draft
hiddenFromHomePage: false
hiddenFromSearch: false
hiddenFromRelated: false
hiddenFromFeed: false
summary:
resources:
  - name: featured-image
    src: featured-image.jpg
  - name: featured-image-preview
    src: featured-image-preview.jpg
toc: true
math: true
lightgallery: false
password:
message:

# See details front matter: https://fixit.lruihao.cn/documentation/content-management/introduction/#front-matter
---

数字逻辑期中复习笔记 (Digital Logic Midterm Review Notes)
===============================================

<!--more-->

知识点总结 (Knowledge Points)
------------------------

### 进制转换与数据表示 (Number Systems and Data Representation)

**定义：** 数字系统中常用的进制包括十进制、二进制、八进制和十六进制等，它们之间可以通过一定的方法相互转换。二进制使用 0 和 1 表示数字，八进制和十六进制则是二进制的简写表示形式，每三位二进制可表示一位八进制，每四位二进制可表示一位十六进制。

_Definition:_ Common number systems in digital logic include decimal (base 10), binary (base 2), octal (base 8), and hexadecimal (base 16). These can be converted between each other using standard methods. The octal and hexadecimal systems serve as shorthand for binary – every 3 binary digits correspond to one octal digit, and every 4 binary digits correspond to one hexadecimal digit.

*   **进制转换方法：** 将其他进制数转换为十进制时，可使用位权展开公式：例如对于基数为 $r$ 的数 $ (d_{n}d_{n-1}...d_1d_0.d_{-1}d_{-2}...)_r$，其十进制值为 $\sum_{i=-m}^{n} d_i \times r^i$。反之，将十进制整数转换为 $r$ 进制可反复除以 $r$ 取余数，将十进制小数转换为 $r$ 进制可反复乘以 $r$ 取整数部分。 

_Conversion methods:_ To convert a number in base $r$ to decimal, use positional weights: for a number $(d_{n}...d_0.d_{-1}...)_r$, the decimal value is $\sum_{i=-m}^{n} d_i \times r^i$. Conversely, to convert a decimal integer to base $r$, repeatedly divide by $r$ and record remainders; to convert a decimal fraction, repeatedly multiply by $r$ and record integer parts.
    
*   **示例 (Example):** 将二进制数 $010010.01_2$ 转换为十进制、五进制和十六进制。其整数部分 $010010_2=18_{10}$，小数部分 $0.01_2=0.25_{10}$，所以 (a) 十进制结果为 $18.25$；(b)转换为五进制：$18_{10}=33_5$，$0.25_{10}\approx0.11_5$（保留两位小数）得到 $33.11_5$；(c)转换为十六进制：$18_{10}=12_{16}$ (即 $0x12$)，$0.25_{10}=0.4_{16}$，结果为 $12.4_{16}$。 

_Example:_ Convert binary number $010010.01_2$ to decimal, base-5, and hexadecimal. The integer part $010010_2 = 18_{10}$ and fractional part $0.01_2 = 0.25_{10}$. Thus (a) in decimal it is $18.25$; (b) in base-5: $18_{10}=33_5$ and $0.25_{10}\approx0.11_5$ (two digits after point), so $33.11_5$; (c) in hexadecimal: $18_{10}=12_{16}$ and $0.25_{10}=0.4_{16}$, giving $12.4_{16}$.
    
*   **补码与有符号数 (Complements & Signed Numbers):** 为了方便电路实现减法运算，引入了 “补码” 概念。对基数为 $r$ 的 $n$ 位数，其 $(r-1)$’s 补码（反码）定义为 $r^n-1- N$，而 $r$’s 补码（补码）为 $r^n- N$。在二进制系统中，1’s 补码就是按位取反；2’s 补码则是在 1’s 补码的基础上加 1。例如，二进制数 $10110000_2$ 的 1’s 补码为 $01001111_2$，其 2’s 补码为 $01010000_2$。

_Complements:_ Complements are used to simplify subtraction circuits. For a number $N$ with base $r$ and $n$ digits, the diminished radix complement ((r-1)’s complement) is defined as $r^n - 1 - N$, and the radix complement (r’s complement) is $r^n - N$. In binary, the 1’s complement is obtained by flipping all bits, and the 2’s complement is obtained by taking the 1’s complement and then adding 1. For example, the 1’s complement of $10110000_2$ is $01001111_2$, and its 2’s complement is $01010000_2$.
    
*   **有符号二进制表示 (Signed binary representation):** 在计算机中采用最高位作为符号位，0 表示正、1 表示负。常见的有符号表示法有三种：**原码** (sign-magnitude) 用符号位加绝对值大小表示；**1’s 补码表示**将负数表示为正数的 1’s 补码；**2’s 补码表示**将负数表示为正数的 2’s 补码。2’s 补码表示法最常用，因为它消除了 “+0” 和“-0”的二义性，并简化了加减运算。例如，$(-5)_{10}$ 在 8 位二进制的 2’s 补码表示为 $11111011_2$。 

_Signed numbers:_ In binary signed representation, the most significant bit (MSB) is the sign bit (0 for positive, 1 for negative). Common schemes include: **Sign-magnitude**, which uses a sign bit plus the magnitude; **1’s complement**, where negative numbers are represented as the 1’s complement of the positive magnitude; and **2’s complement**, where negatives are represented as the 2’s complement of the magnitude. 2’s complement is widely used because it avoids dual representations of zero and simplifies arithmetic. For example, $-5_{10}$ in 8-bit 2’s complement form is $11111011_2$.
    
*   **二进制编码 (Binary codes):** 数字电路中常用特殊编码，例如 **BCD 码**用 4 位二进制表示一位十进制数字（例如 $396_{10}$ 表示为 BCD 码是 $0011,1001,0110$）。**格雷码 (Gray Code)** 是相邻码字仅有 1 位不同的编码，可用于减少变换时的逻辑变化。**ASCII 码**用 7 或 8 位二进制表示文本字符。**奇偶校验位 (Parity bit)** 用于错误检测，在数据后附加一位，使得 1 的总个数为偶数（偶校验）或奇数（奇校验）。例如，在偶校验方案中，如果发送的 7 位信息 “1000001” 中 1 的个数为奇数，则校验位取 1 使总数成偶数。 _Binary codes:_ Several binary coding schemes are used in digital systems. For example, **BCD (Binary-Coded Decimal)** uses four bits to represent a single decimal digit (e.g., $396_{10}$ is coded as $0011,1001,0110$ in BCD). **Gray code** is a binary sequence where adjacent values differ in only one bit, useful for preventing spurious outputs during transitions. **ASCII code** represents text characters in 7 or 8 bits. A **parity bit** is an extra bit for error detection, making the total number of 1’s either even or odd. For instance, under even parity, if the 7-bit data "1000001" has an odd number of 1’s, the parity bit is set to 1 to make the total count even.
    

### 布尔代数定律 (Laws of Boolean Algebra)

**定义：** 布尔代数遵循一组基本定律，这些定律描述了逻辑变量及算符（如与、或、非）的数学性质，利用它们可以对逻辑表达式进行等价变换和化简。 _Definition:_ Boolean algebra follows a set of fundamental laws governing operations on logical variables (using AND, OR, NOT, etc.). These laws enable equivalent transformations and simplification of logic expressions. 以下是主要的布尔代数定律（中英文对照）：

*   **交换律 (Commutative Law)：** $x + y = y + x,;;x \cdot y = y \cdot x$.
    
*   **结合律 (Associative Law)：** $(x + y) + z = x + (y + z),;;(x \cdot y) \cdot z = x \cdot (y \cdot z)$.
    
*   **分配律 (Distributive Law)：** $x \cdot (y + z) = x y + x z,;;x + (y \cdot z) = (x + y),(x + z)$.
    
*   **恒等律 (Identity Law)：** $x + 0 = x,;;x \cdot 1 = x$.
    
*   **归零 / 归一律 (Null Law)：** $x + 1 = 1,;;x \cdot 0 = 0$.
    
*   **幂等律 (Idempotent Law)：** $x + x = x,;;x \cdot x = x$.
    
*   **双重否定律 (Involution Law)：** $(x')' = x$.
    
*   **补余律 (Complement Law)：** $x + x'= 1,;;x \cdot x' = 0$.
    
*   **吸收律 (Absorption Law)：** $x + x y = x,;;x \cdot (x + y) = x$.
    
*   **德摩根定律 (DeMorgan’s Laws)：** $(x + y)'= x' y',;;(x \cdot y)' = x'+ y'$.
    

上述定律可以指导我们进行逻辑化简。例如，利用吸收律可简化表达式 $x + x'y$ 为 $x + y$（因为 $x + x'y = (x + x')(x + y) = 1 \cdot (x+y) = x+y$）。 _These laws are used to simplify logic expressions._ For example, using absorption, $x + x'y$ simplifies to $x + y$, since $x + x'y = (x + x')(x + y) = 1 \cdot (x+y) = x+y$.

### 布尔函数的表示与化简 (Boolean Function Representation and Simplification)

**表示方法：** 一个布尔函数可以用多种形式表示，包括真值表、逻辑代数表达式以及规范形式。真值表列举了所有输入组合对应的输出值。逻辑代数表达式使用二元变量和算符描述输出如何由输入获得。**规范和标准形**包括**最小项之和 (SOP) **和**最大项之积 (POS) **形式：前者将函数表示为若干**最小项**（即使输出为 1 的输入组合对应的积项) 之和；后者将函数表示为若干**最大项**（输出为 0 时对应的和项) 之积。例如，函数 $F(A,B,C)$ 在 SOP 形式下可写为 $F=\sum m(1,4,6)$ 表示当输入组合对应的最小项索引为 1、4、6 时输出为 1；同一函数也可写为 POS 形式 $F=\prod M(0,2,3,5,7)$ 表示输出为 0 时的索引集合。 _Function representation:_ A Boolean function can be described by a truth table or by logical expressions, including canonical forms. A **truth table** lists the output for every input combination. An algebraic expression uses binary variables and operators to define the output. **Canonical forms** include **Sum of Products (SOP)** and **Product of Sums (POS)**. In SOP form, the function is expressed as a sum (OR) of **minterms** (AND terms corresponding to input combinations that produce output 1); in POS form, it is expressed as a product (AND) of **maxterms** (OR terms for input combinations that produce output 0). For example, a function $F(A,B,C)$ can be written in SOP as $F=\sum m(1,4,6)$, meaning $F=1$ for minterm indices 1,4,6, or equivalently as $F=\prod M(0,2,3,5,7)$ in POS, listing where $F=0$.

*   **布尔函数化简：** 简化布尔函数旨在用尽可能少的文字（变量）和项来表示逻辑。[geeksforgeeks.org](https://www.geeksforgeeks.org/digital-logic/introduction-of-k-map-karnaugh-map/#:~:text=In%20many%20digital%20circuits%20and,Boolean%20expressions%20by%20identifying%20patterns) 常用方法包括代数法（利用前述定律手工推导）和卡诺图法。** 卡诺图 (Karnaugh Map, K 图)** 是一种将真值表映射到格子的图形工具，可以利用人类的模式识别能力快速找出相邻的 1 组，从而推导最简表达式 [geeksforgeeks.org](https://www.geeksforgeeks.org/digital-logic/introduction-of-k-map-karnaugh-map/#:~:text=In%20many%20digital%20circuits%20and,Boolean%20expressions%20by%20identifying%20patterns)[geeksforgeeks.org](https://www.geeksforgeeks.org/digital-logic/introduction-of-k-map-karnaugh-map/#:~:text=1.%20Select%20the%20K,and%20sum%20them%20up%20for)。卡诺图的单元格按格雷码顺序排列，每个单元对应一种输入组合，标记为 1 表示该组合下输出为 1（0 表示输出为 0，$d$ 表示 “无关项”）[en.wikipedia.org](https://en.wikipedia.org/wiki/Karnaugh_map#:~:text=The%20required%20Boolean%20results%20are,expression%20representing%20the%20required%20logic)。通过在 K 图上圈出 $1$（包括可利用的无关项 $d$）的相邻组合（相邻单元数必须是 2 的幂，如 1、2、4、8...），可以找出约简项：圈住 $2^k$ 个相邻 1 将消去 $k$ 个变量。例如，在 4 变量 K 图中圈 8 个相邻格将得到仅含 1 个字母的项（圈 16 个则函数为常量 1）。 _Function simplification:_ The goal of simplification is to express the function with as few terms and literals as possible[geeksforgeeks.org](https://www.geeksforgeeks.org/digital-logic/introduction-of-k-map-karnaugh-map/#:~:text=In%20many%20digital%20circuits%20and,Boolean%20expressions%20by%20identifying%20patterns). Common techniques are algebraic manipulation (using the laws above) and the **Karnaugh map (K-map)** method. A K-map is a diagrammatic tool that organizes truth table values into a grid, allowing patterns of adjacent 1s to be identified for simplification[geeksforgeeks.org](https://www.geeksforgeeks.org/digital-logic/introduction-of-k-map-karnaugh-map/#:~:text=In%20many%20digital%20circuits%20and,Boolean%20expressions%20by%20identifying%20patterns)[geeksforgeeks.org](https://www.geeksforgeeks.org/digital-logic/introduction-of-k-map-karnaugh-map/#:~:text=1.%20Select%20the%20K,and%20sum%20them%20up%20for). Cells in the K-map are arranged in Gray code order, each cell representing one input combination; cells are filled with 1 for outputs that are HIGH (0 for LOW, and $d$ for “don’t care” if the output is unspecified)[en.wikipedia.org](https://en.wikipedia.org/wiki/Karnaugh_map#:~:text=The%20required%20Boolean%20results%20are,expression%20representing%20the%20required%20logic). By grouping adjacent 1s (including _don't-care_ cells $d$ if helpful) in power-of-two sized blocks (1, 2, 4, 8, ... cells), one can derive a reduced term: grouping $2^k$ cells eliminates $k$ variables from the term. For instance, in a 4-variable K-map, a group of 8 adjacent 1s yields a term with only one literal (and grouping all 16 yields the constant 1).
    
*   **卡诺图化简示例:** 设 $F(A,B,C) = \sum(1,3,6,7)$，其 K 图标记出这四个输出为 1 的格子。将相邻的 1 分成两个最大的组：一组包含了 $1$ 和 $3$（组合 A=0,C=1），另一组包含了 $6$ 和 $7$（组合 A=1,B=1）。由此得到最简结果为 $F = A' C + A B$[geeksforgeeks.org](https://www.geeksforgeeks.org/digital-logic/introduction-of-k-map-karnaugh-map/#:~:text=From%20red%20group%20we%20get,product%20term)。在该表达式中，每项对应一个组，且项中仅包含未被抵消的变量（如 $A'C$ 表示 A=0、C=1 的条件，B 被消去）。如果存在无关项，在 K 图中可将其当作 1 来合并以得到更大组合，从而进一步简化逻辑。 _K-map example:_ Suppose $F(A,B,C) = \sum(1,3,6,7)$. Marking these minterms on a 3-variable K-map, we form two largest groups of adjacent 1s: one group covers minterms 1 and 3 (A=0, C=1), and another covers 6 and 7 (A=1, B=1). The simplified result is $F = A' C + A B$[geeksforgeeks.org](https://www.geeksforgeeks.org/digital-logic/introduction-of-k-map-karnaugh-map/#:~:text=From%20red%20group%20we%20get,product%20term). Each term corresponds to a grouping and includes only the variables not eliminated by the grouping (for example, $A'C$ indicates A=0 and C=1, with B eliminated). If “don’t care” conditions are present, they can be treated as 1s in the K-map to form larger groups and further simplify the logic.
    
*   **最小与最大逻辑实现:** 简化后的函数通常以最小 SOP 或 POS 形式呈现，可直接用于逻辑电路实现。其中 SOP 形式可用与门 - 或门两级电路实现，POS 形式可用或门 - 与门两级实现 [en.wikipedia.org](https://en.wikipedia.org/wiki/Karnaugh_map#:~:text=Karnaugh%20maps%20are%20used%20to,Once)。任何布尔函数也都可以仅用 NAND 或仅用 NOR 门来实现，因为 NAND 和 NOR 都是**通用门**（功能完备）。实现方法通常是将目标表达式转换为只含 NAND 或 NOR：例如，对于 SOP 表达式，可用两层 NAND 门网络实现——第一层 NAND 实现各乘积项（同时产生取反），第二层 NAND 汇总（相当于或后取反），如果需要得到原函数则再取反一次。 _Implementation note:_ The simplified function, in minimal SOP or POS form, can be directly implemented using two-level gate circuits (AND-OR for SOP, OR-AND for POS)[en.wikipedia.org](https://en.wikipedia.org/wiki/Karnaugh_map#:~:text=Karnaugh%20maps%20are%20used%20to,Once). Any Boolean function can also be implemented using **only NAND gates** or **only NOR gates**, since NAND and NOR are _universal gates_. The implementation involves transforming the expression for use with the chosen gate type. For example, a SOP expression can be realized with a two-level NAND network – using NAND gates for the product terms (which yields the negated outputs) and a NAND as the second level to combine them (performing an OR with inversion), with an additional inversion if necessary to obtain the original function.
    

### 组合逻辑电路构造方法 (Combinational Logic Design Methods)

**基本概念：** **组合逻辑电路**的输出只取决于当前输入，没有记忆功能。这类电路可以通过真值表或布尔表达式来定义，并由基本逻辑门或功能模块实现。设计组合逻辑电路时，通常先根据需求写出真值表或表达式，然后选择合适的实现方法：直接使用基本门电路，或利用 ** 中规模集成 (MSI)** 组件如译码器、复用器等来构造。 _Basic concept:_ In a **combinational logic circuit**, outputs depend only on the current inputs, with no memory element. Such circuits can be specified by a truth table or Boolean expression and implemented using logic gates or functional modules. The typical design process is to derive the truth table or expression from the requirements, then choose an implementation approach: either using basic gates directly, or leveraging medium-scale integrated (MSI) components like decoders and multiplexers.

*   **译码器 (Decoder):** 译码器将 $n$ 位二进制输入转换为 $2^n$ 条独热编码输出，其中每一条输出线仅对应一种输入组合为真。换言之，译码器生成所有可能输入的**最小项**。带使能输入的译码器可以通过使能信号控制译码器的输出是否有效。一项常见应用是将译码器与或门相结合，实现任意逻辑函数：译码器输出提供各输入组合的指示，仅需选择性地将对应输出通过或门相加即可合成所需函数。例如，2 对 4 译码器产生 4 条输出，对应输入 00、01、10、11；如果某逻辑函数在输入为`01`和`10`时输出为 1，我们可以将译码器针对 01 和 10 的输出端通过 OR 连接来实现该函数。_Decoder:_ A decoder converts an $n$-bit input into $2^n$ unique one-hot outputs, with exactly one output line HIGH for each input combination. In other words, a decoder generates the **minterms** for all input combinations. Decoders often include enable inputs to control whether the decoding is active. A common use is to implement arbitrary logic functions by combining decoder outputs with OR gates: the decoder output lines indicate all input minterms, and by OR-ing the appropriate lines (those corresponding to when the function should be 1), the desired function is obtained. For example, a 2-to-4 decoder produces four outputs for inputs 00, 01, 10, 11; to implement a function that is 1 for inputs `01` and `10`, one can OR together the decoder outputs for 01 and 10.
    
*   **多路复用器 (MUX, Multiplexer):** 多路复用器从 $2^n$ 条输入中选择一条输出，由 $n$ 条**选通信号**决定选择哪一路。一个 $m$- 输入的逻辑函数可以用 $2^{m-1}:1$ 的 MUX 实现：将其中 $m-1$ 个变量作为 MUX 的选线，MUX 的 $2^{m-1}$ 个数据输入端接常量 0、1 或剩余第 $m$ 个变量（或其反）以生成所需的输出。由于 MUX 可实现任意真值表（数据输入端可以配置为对应输出值），因此 MUX 具有逻辑实现的通用性。例如，4:1 复用器可以实现四种输入条件下输出的任意组合：选线 S1S0 选择输入 $D_0...D_3$ 中的一个作为输出。若设计三输入函数 $F(A,B,C)$，可令 $A,B$ 接 MUX 选线 $S1,S0$，MUX 的四个数据输入 $D_0...D_3$ 根据 $C$ 和所需功能设定为 0、1、$C$ 或 $C'$，即可输出正确的 $F$ 值。_Multiplexer:_ A multiplexer selects one of $2^n$ data inputs to pass to the output, using $n$ **select lines** to choose the input. Any logic function of $m$ variables can be implemented with a $2^{m-1}:1$ MUX: use $m-1$ variables as the select lines, and connect the MUX’s $2^{m-1}$ data inputs to either constant 0, constant 1, or the remaining $m$th variable (or its complement) such that the output mimics the function truth table. Since a MUX can reproduce any mapping of select inputs to output values (by appropriate assignment of the data inputs), it is a universal logic implementation device. For example, a 4:1 MUX can realize an arbitrary function for four input cases: select lines S1 S0 pick one of data inputs $D_0...D_3$ as output. To design a 3-variable function $F(A,B,C)$, one could use $A,B$ as select lines $S1,S0$, and set the four data inputs $D_0...D_3$ to 0, 1, $C$, or $C'$ according to the desired $F$ output for each combination of $A,B$.
    
*   **其它组合模块:** 常见的还有**编码器 (Encoder)**，功能与译码器相反，将独热输入转换为二进制代码；**优先编码器**则在多个输入同时为 1 时输出最高优先级的编码。**加法器**电路如半加器、全加器用于二进制数相加；**比较器**比较两个二进制数的大小关系并输出比较结果。设计此类功能电路时，可利用真值表直接推导表达式，或在更高层次上利用上述 MSI 模块拼接实现。例如，2 位大小比较器可按位比较高位和低位：先比较高位 A1 与 B1 决定结果或平局，再在高位相等时比较低位 A0 与 B0。这些模块在实际电路中往往作为基本单元，可以组合构成更复杂的算术逻辑单元。_Other combinational blocks:_ Other useful modules include **encoders**, which perform the inverse of decoding by generating a binary code from one-hot inputs, and **priority encoders** which select the highest-priority active input among many. **Adders** (half-adder, full-adder) are used to perform binary addition, and **comparators** output the relational result (equal/greater/less) of two binary numbers. To design such circuits, one can derive logic expressions from truth tables, or compose the design using the MSI components mentioned. For example, a 2-bit comparator can be built by comparing the higher bits and lower bits: compare A1 vs B1 to decide the result or detect a tie, and if A1 and B1 are equal, then compare A0 vs B0 to determine the outcome. These functional blocks serve as building units in practice, often combined to form more complex arithmetic logic units.
    

### 锁存器与触发器 (Latches vs. Flip-Flops: Principles and Comparison)

**时序逻辑概念：** 锁存器和触发器是**时序逻辑电路**的基本存储元件，用于存储 1 位二进制状态。与组合逻辑不同，时序电路的输出取决于当前输入和存储的先前状态，需要时钟或控制信号来协调状态更新。锁存器和触发器通过一个控制（如时钟）信号的作用发生状态变化，该触发事件称为 “触发”。_Sequential logic:_ Latches and flip-flops are basic one-bit storage elements in **sequential circuits**, which have outputs depending on current inputs _and_ stored past state. Unlike combinational logic, sequential circuits require a clock or control signal to synchronize state changes. Latches and flip-flops change state in response to a control input (such as a clock); this event is called a “trigger”.

*   **SR 锁存器 (SR Latch)：** 最基本的锁存器由两个交叉耦合的 NOR 门或 NAND 门构成，实现**置位 / 复位**功能。SR 锁存器有两个输入 $S$ 和 $R$：当 $S=1, R=0$ 时，输出 $Q$ 被**置 1**；当 $S=0, R=1$ 时，输出 $Q$ 被**复位 0**；当 $S=R=0$ 时，输出保持原状态。由于 NOR 型 SR 锁存器在 $S=R=1$ 时两个输出都为 0，产生不稳定的**禁止状态**，实际电路应避免这一输入组合。SR 锁存器是无时钟的 “异步” 顺序电路，输入一改变就直接影响状态。 _SR latch:_ The simplest latch is an SR (Set-Reset) latch built from two cross-coupled NOR gates (or NAND gates for an active-low variant). It has inputs $S$ and $R$: when $S=1, R=0$, the output $Q$ is **set to 1**; when $S=0, R=1$, $Q$ is **reset to 0$; with $S=R=0$, the output retains its previous state. (For a NOR-based SR latch, $S=R=1$ forces both outputs low, an unstable **invalid state**, so that input combination is forbidden.) The SR latch is an asynchronous memory element – its state changes as soon as inputs change, without requiring a clock.
    
*   **D 锁存器 (D Latch)：** 为避免 SR 锁存器的不定态，引入了 D 锁存器。D 锁存器在内部用 $D$ 输入直接驱动 $S$，而 $D$ 的反相驱动 $R$。这样确保不会出现 $S$ 和 $R$ 同时为 1 的情况。D 锁存器通常配合一个使能（或时钟）信号工作：当使能信号 $C=1$ 时，D 输入**透明**地传输到输出 $Q$（$Q$ 跟随 $D$ 变化）；当 $C=0$ 时，锁存器**保持**之前的输出状态不变。由于输出在使能为高电平期间随输入变化，D 锁存器也被称为 “通透锁存器”。_D latch:_ The D latch was developed to eliminate the indeterminate state of the SR latch. It has a single data input $D$, internally connected such that $S=D$ and $R=\overline{D}$, thereby preventing $S$ and $R$ from being 1 simultaneously. A D latch is typically controlled by an enable (or clock) signal $C$: when $C=1$, the latch is **transparent**, meaning output $Q$ follows the input $D$ in real-time; when $C=0$, the latch **holds** its last value and ignores changes on $D$. Because the output passes input through during $C=1$, a D latch is also called a _transparent latch_.
    
*   **触发器 / 边沿触发 D 触发器 (Edge-Triggered D Flip-Flop)：** 触发器（尤其 D 触发器）是由两级锁存器（主从结构）或其他方式构成的**边沿敏感**存储器元件。常用的正沿 D 触发器在时钟信号从 0 变 1 的瞬间**捕获**输入 $D$ 的值，并锁存到输出，直到下一个时钟上升沿才更新。在时钟的高电平或低电平期间，输出 $Q$ 不会改变（保持稳定）。这种性质避免了锁存器通透时可能出现的多个状态变化，使电路更易于设计同步时序。触发器可看作由一个**主锁存器**（在时钟的一相位采样输入）和**从锁存器**（在时钟另一相位更新输出）组成。_Flip-Flop (Edge-triggered D FF):_ A flip-flop is a storage element (commonly built from two latches in master-slave configuration) that is **edge-sensitive** rather than level-sensitive. A standard positive-edge-triggered D flip-flop, for example, **samples** the $D$ input at the moment the clock transitions from 0 to 1 (rising edge) and updates the output $Q$ with this value, holding it stable until the next rising edge. During the high or low level of the clock, $Q$ does not change (it remains latched). This behavior prevents the multiple updates that a transparent latch can allow, simplifying synchronous sequential circuit design. Internally, a flip-flop can be viewed as a **master latch** (captures input on one phase of clock) followed by a **slave latch** (outputs on the next phase).
    
*   **比较与应用 (Comparison & Application):** 锁存器和触发器都可用于存储数据，但它们触发方式不同：锁存器对电平敏感，在使能信号为高时随时更新状态，而触发器对信号边沿敏感，只在触发边沿瞬间更新，从而在时钟两边沿之间保持输出稳定。在同步时序电路中通常倾向使用触发器，因为边沿触发的机制让所有状态更新在时钟边沿同时发生，避免了 ** 贯通 (transparency)** 效应造成的竞争和冒险。锁存器硬件开销较小且延迟小，适用于需要高速、且能够精心控制时序的设计，但使用不当可能导致时序问题。总体而言：**锁存器**简单快速但电平敏感、可能引入设计复杂性，**触发器**在时序控制上更可靠，是大多数寄存器和同步存储单元的实现方式。 _Comparison:_ Both latches and flip-flops store data, but differ in triggering: a **latch** is level-sensitive (transparent when enable is high, updating continuously), whereas a **flip-flop** is edge-sensitive, updating only on a clock transition and holding the output stable between clock edges. Flip-flops are preferred in synchronous systems because edge-triggering ensures all state changes occur only at clock edges, avoiding the transparency issues (and potential timing hazards) of latches. Latches use fewer gates and can be faster, which can be advantageous in high-speed designs if timing is carefully managed, but improper use can lead to timing races. In summary: **Latches** are simple and fast but level-sensitive (requiring careful design), while **flip-flops** provide safer timing control and are the standard choice for registers and synchronous storage elements.
    

考试题型与重点 (Exam Question Types and Key Focus Areas)
-------------------------------------------------

### 填空题常见考点 (Fill-in-the-Blank Questions – Key Topics)

数字逻辑的填空题往往考查基本概念和简单计算，要求对核心知识点熟记并能迅速应用：

*   **进制转换与数值计算：** 常涉及不同进制间的转换或数值计算，如 “将某二进制 / 十进制数转换为指定进制”、“一个 $n$ 位二进制能表示的最大无符号整数是？”。学生应熟练掌握除基换算、基数的幂等概念，以及诸如将二进制小数转换为十进制的方法等。 _Radix conversion & numeric computation:_ These blanks often require converting numbers between bases or performing small calculations. Examples include converting a given binary/decimal number to another base, or asking "what is the largest unsigned number representable by an $n$-bit binary?". Be comfortable with division/remainder and multiplication methods for base conversion and with concepts like the value range of $n$-bit numbers.
    
*   **逻辑门特性：** 对基本逻辑元件的性质进行填空也是常见考点。例如：“对于一个三输入 OR 门，有_______种输入组合会使输出为 HIGH”。要快速解答此类题，需要了解每种门电路的输出条件（如 OR 门仅在所有输入为 0 时输出为 0，其余情况下输出为 1，因此对于 3 输入 OR 门，$2^3-1=7$ 种输入会得到高电平输出)。 _Logic gate properties:_ Questions may ask for specifics of basic gates. For example: “A three-input OR gate has ______ different input combinations that produce a HIGH output”. To answer, recall the output condition for each gate type (e.g., an OR gate outputs 0 only when _all_ inputs are 0, otherwise 1; so for 3 inputs there are $2^3-1=7$ combinations that give HIGH).
    
*   **术语和概念列表：** 填空题有时要求列举或补全专业术语，例如常见的 Verilog 关键字、逻辑定律名称等。例如：“列出 8 个 Verilog 的保留字：______”，学生需记忆课程中提到的关键字（如`module, input, output, wire, reg, assign, always, begin`等）。又如填写布尔代数基本定律名称或序号。这类题目侧重考查对专业名词的认识和记忆。 _Terminology lists:_ Sometimes the task is to list or complete technical terms, such as Verilog keywords or logic law names. For example: “List 8 keywords in Verilog: ______.” You should recall reserved words introduced in class (e.g., `module, input, output, wire, reg, assign, always, begin`, etc.). Similarly, a blank may ask for naming basic Boolean laws or postulates. These questions test recognition and recall of terminology.
    
*   **简单概念或公式：** 其他可能的填空内容包括数字逻辑的基本公式或概念。例如：“两位二进制数相加可能出现的最高进位是______”（答案：1）；“在二进制补码表示中，符号位为 1 表示______”（答案：负数）。这些要求对课程基础知识有准确的理解。 _Basic concepts or formulas:_ Other fill-ins may target foundational formulas or facts. For instance: “The maximum carry-out when adding two $n$-bit binary numbers is ______” (answer: 1); “In two’s complement binary, a sign bit of 1 indicates ______” (answer: a negative number). Such blanks ensure you understand core principles accurately.
    

### 选择题易混概念 (Multiple-Choice Questions – Easily Confused Concepts)

数字逻辑的选择题（包括单选和多选）通常涉及对概念的辨析和综合应用，选项设计具有迷惑性。下面是常见容易混淆的知识点：

*   **卡诺图分组与化简：** 需要理解 K 图分组的原则及对化简项的影响。例如：“在四变量 K-map 中，一个圈包含多少个格子可以得到仅含一个文字的项？” 此考题考查**分组大小与简化后文字数**的关系——圈 8 个相邻格代表消去 3 个变量只剩 1 个变量。学生应牢记：圈的格子数为 $2^n$ 将消去 $n$ 个变量；圈覆盖整张图 (16 格) 则表示函数恒为 1。 _K-map grouping:_ You must understand grouping rules and their effect on simplified terms. For example: “In a 4-variable K-map, grouping how many adjacent cells yields a term with a single literal?” This tests the relationship between group size and the number of literals in the simplified term – grouping 8 cells eliminates 3 variables, leaving 1 literal. Remember: a group of $2^n$ cells drops $n$ variables; a group of all 16 cells means the function simplifies to 1.
    
*   **最小项与最大项形式：** 选择题可能给出几种函数表达式，问哪一个是 maxterm 之积形式（或 minterm 之和形式)。如：“以下哪个是函数 $F(A,B,C)$ 的积式（积表示法）的形式？” 选项往往混合了数种表示，需要识别**积范式**（每个括号包含一次性出现所有变量的或项)。学生要分清：∑表示和 - 最小项（1 的列表），∏表示积 - 最大项（0 的列表）；并注意选项中是否所有括号项包含了每个变量（漏掉变量意味着不是完整的 maxterm)。 _Minterm vs. maxterm forms:_ A question may present different expressions and ask which is in product-of-maxterms (or sum-of-minterms) form. For example: “Which of the following Boolean equations is in product of maxterms form for $F(A,B,C)$?”. The options can be tricky combinations; you must identify the **POS form** (a product of OR-terms, each containing all variables exactly once). Recall that Σ denotes a sum of minterms (list of indices where function =1), and ∏ denotes a product of maxterms (list where function =0). Check whether each candidate OR-term has all variables (if any term misses a variable, it’s not a full maxterm).
    
*   **不同进制含义：** 一些选择题考查对非十进制数的理解，例如：“要使等式 $\sqrt{41} = 5$ 成立，这两个数应视为何种进制下的数？”此题实为寻找满足 $ \sqrt{(4r+1)} = 5$ 的基数 $r$，解得 $r=6$。易错点在于将 “41” 直接当作四十一来理解，而正确理解应是基 $r$ 下的数字“4,1”。答题时应将选项逐一代入检验，理解数位在不同基数下的权值意义。 _Interpreting bases:_ Some questions probe understanding of numbers in bases other than decimal. For example: “Determine the base in which the equation $\sqrt{41} = 5$ is correct”. This requires solving $ \sqrt{(4\times r + 1)} = 5$ for radix $r$, giving $r=6$. The pitfall is misreading “41” as forty-one in decimal; instead, interpret it as digits 4 and 1 in base-$r$. Approach such problems by substituting each base option to test, and remember that digit positions carry different weights in different bases.
    
*   **逻辑电路等效分析：** 选择题常以电路图或逻辑表达式考查对电路功能的理解。例如给出一个组合逻辑电路，问输出函数等于哪一个选项。解答时需要逐层分析电路：搞清每个门的作用及整体逻辑。有时多个选项仅一字母之差，需特别警惕。例如，一道题给出某电路，让判断输出是 $A'+ B'$ 还是 $A + B$ 抑或是恒 1 等。应通过真值分析或化简电路来选出正确答案。 _Circuit logic equivalence:_ Many multiple-choice questions present a logic circuit or an expression and ask which output/function it corresponds to. Solve these by analyzing the circuit step by step, determining the logic at each stage. Options may be deceptively similar (differing by a single literal or inversion), so be careful. For instance, a problem might show a gate network and ask if the output is $A'+ B'$, $A + B$, $B'$, or 1. Use truth tables or algebraic simplification of the circuit to identify the correct expression.
    
*   **逻辑功能的充分性：** 对逻辑门的功能完备性也可能以选择形式出现。例如多选题：“任何布尔函数都可以仅用以下哪种门电路实现？” 选项包括 NAND 门、NOR 门、XOR 门等。正确答案应识别 NAND 和 NOR 都是功能完备的（可实现任意函数)；而 XOR 门单独不能实现任意逻辑功能。做此类题时，若题目允许多选，要把所有正确的都选出（如 NAND 和 NOR 都选）。 _Functional completeness:_ Questions may ask which gates are functionally complete. For example: “Any Boolean function can be implemented using only which of the following?” (with options like NAND, NOR, XOR, etc.). The correct understanding is that **NAND** and **NOR** are universal gates (each alone can implement any function), whereas XOR alone is not sufficient. For multi-select, be sure to choose all that apply (in this case, both NAND and NOR).
    
*   **奇偶校验概念：** 考查奇偶校验码的选择题可能给出若干比特序列，问其中哪些传输后 “校验失败”。例如：“以下各含奇校验位的序列中，在假定至多发生一位错误的情况下，哪些未通过校验？”。解这种题要计算每个序列中 1 的个数：对于奇校验，总 1 数应为奇数，如果某序列的 1 数量为偶数，则校验不通过（说明发生了错误)。例如序列 A 和 C 1 的个数为偶数，因此为校验失败的序列。 _Parity check:_ Some items give bit sequences with parity bits and ask which ones “fail the parity check.” For instance: “Each of the following received sequences contains an ODD parity bit. Which sequences fail the parity check (assuming at most one error)?”. To solve, count the number of 1s in each sequence: under odd parity, the total number of 1s should be odd if no error. Any sequence with an even count of 1s indicates the parity check fails (an error has occurred). In the example, sequences A and C have an even number of 1s, so they would be identified as failing parity check.
    
*   **综合分析型选择题：** 有些选择题综合性较强，例如给出一个逻辑函数的索引表示和若干可能的化简结果，要求选出正确的化简。这需要较快地进行化简运算或者逐一代入验证。应对策略：可以先粗略判断选项的项数是否合理（例如可借助 K 图判断最简表达应有几项)，然后用真值法检验可疑选项。必要时考虑不要在一道题上花费过多时间，可标记后返回检查。 _Comprehensive MCQs:_ Some MCQs are complex, e.g., providing a function via minterm indices and several proposed simplified forms, asking which is correct. You must quickly simplify the function or test each option. A strategy is to estimate the likely number of product terms (for instance, using a mental K-map to guess how many groups) and eliminate options that have too many or too few terms. Then, if needed, plug in specific input combinations to verify the remaining candidates. Be mindful of time; if an option is not immediately clear, mark the question and revisit after addressing easier ones.
    

### 综合题解题方法与技巧 (Comprehensive Problems – Solving Methods and Tips)

综合题通常为主观题，要求学生完整地分析和设计电路。针对常见综合题型，以下是备考策略和解题要点：

*   **真值表推导及逻辑功能描述：** 对于给定文字描述的逻辑功能，第一步通常是列出**真值表**。例如题目描述 “输入 A 是 3 位二进制数，如果 A 是偶数则输出 B 为 A 的反码，如果 A 是奇数则 B 为 A+1”。应列出 A 的所有 8 种取值及对应的 B 输出（逐位写出二进制结果)。绘制真值表有助于理清输入输出关系，也是后续设计的基础。列真值表时注意包含所有边界情况，并根据描述确定每一行输出。 _Derive truth tables:_ When a problem describes a logic function in words, often the first task is to construct the **truth table**. For example, if the prompt says "A (3-bit) is even, then output B equals bitwise NOT of A; if A is odd, B equals A+1", you should enumerate all 8 values of A and determine the corresponding 3-bit output B (computing either the one’s complement or increment as specified). Writing out the truth table clarifies input-output relationships and forms the basis for design. Ensure all cases (like smallest/largest values, even/odd distinction) are correctly handled in the table.
    
*   **分步设计与模块化实现：** 综合题经常细分为多问，要求逐步完成设计。例如上例可能要求：(a) 写出真值表；(b) 用基本门实现某位输出；(c) 利用译码器实现另一位输出；(d) 用复用器实现最后一位输出。解答时应针对每小问使用恰当的方法：对于指定只能用 NOR 门的部分，需将逻辑表达式转换为仅含 NOR 实现；对于要求用译码器或复用器的部分，要回忆这些模块的功能（如译码器产生最小项，复用器实现任意函数），然后合理连接来实现所需逻辑。** 技巧：** 充分利用前面小问的结果，例如先简化得到表达式，再根据门元件限制进行实现。 _Stepwise design & modular implementation:_ Large design problems often have parts (a, b, c, ...) guiding you through the solution. For instance, continuing the above scenario: (a) provide the truth table; (b) implement output bit $B_2$ using only NOR gates; (c) implement $B_1$ using two 2-to-4 decoders and gates; (d) implement $B_0$ using a 4:1 multiplexer and logic gates. Tackle each part with the appropriate method: for a section restricted to NOR gates, convert the derived expression into an all-NOR implementation (using De Morgan transformations if needed); for parts requiring decoders or multiplexers, recall their functions (decoder outputs are minterms, multiplexer can implement arbitrary logic) and wire them to realize the target function. _Tip:_ Leverage results from earlier parts – e.g. simplify an expression in part (b), then use that simplified form in part (c) with the given component constraints.
    
*   **电路分析与化简：** 一类综合题会给出已有逻辑电路图，要求写出中间节点表达式、化简输出函数并填写真值表。解题时，建议给电路中每个显著节点标注符号（如 $T_1, T_2,...$），逐一写出其逻辑表达式。接着，将输出表达式用代数方法进行化简。最后，可依据化简后的结果完成真值表的输出列填写。**技巧：**注意电路中的**共享节点**（同一个信号可能接到多个门）和**取反符号**，这些在化简中可能相互抵消或构成基本恒等式。 _Circuit analysis & simplification:_ Another type of problem gives a schematic of a logic circuit and asks you to derive expressions for intermediate nodes, simplify the output, and perhaps complete a truth table. The strategy is to first label important internal signals in the circuit (e.g. $T_1, T_2, ...$) and write the Boolean expression for each. Then derive the output $F$ in terms of the inputs (substituting the $T_i$ expressions) and simplify it algebraically. Finally, use the simplified expression to fill in the output column of the truth table for all input combinations. _Tips:_ Pay attention to **shared nodes** (signals feeding into multiple gates) and **inversions** in the diagram; these can cancel out or form recognisable patterns (like $X$ and $X'$ terms) during simplification.
    
*   **比较器和算术电路设计：** 若综合题要求设计如 “比较器” 或“加法器”等，需运用分解问题的策略。以 “2 位大小比较器” 为例，目标是判断 $A \ge B$，可以分步实现：先比较高位 $A_1, B_1$，若 $A_1>B_1$ 则输出为 1，若 $A_1<B_1$ 则输出为 0；若高位相等，再比较低位 $A_0, B_0$。实现时可以使用**优先级逻辑**或**分级 MUX**：例如利用一个 4:1 多路复用器，根据 $(A_1,B_1)$ 选择输出 $(1, 0, A_0 \ge B_0?, A_0 \ge B_0?)$。设计加法器时，则需要划分半加器 / 全加器模块，正确连接进位。** 技巧：** 画出时间流程或逻辑层级图，将问题分解为子功能，再用标准模块实现每个子功能。 _Comparator/Arithmetic design:_ For designing a comparator or adder, apply problem decomposition. For instance, designing a "2-bit magnitude comparator" (outputs 1 when $A \ge B$) can be broken down: compare the most significant bits $A_1, B_1$ first – if $A_1 > B_1$ output 1, if $A_1 < B_1$ output 0; if they are equal, then compare the lower bits $A_0, B_0$. One way to implement this is using **priority logic** or a cascaded MUX scheme: e.g., use a 4:1 multiplexer with $(A_1,B_1)$ as select inputs to choose the output from among fixed 1, fixed 0, or the result of $(A_0 \ge B_0)$ for the tie case. For an adder design, identify sub-modules like half-adders/full-adders and connect the carry properly. _Tip:_ Draw a flow chart or hierarchical diagram of the decision process, break the problem into sub-functions, then implement each sub-function with known modules (comparators, adders, MUXes, etc.).
    
*   **利用 K 图和无关项进行设计：** 有些综合题结合了化简和实现，如给定函数的公式包含无关项 $d$，要求 (a) 用 K-map 化简得到 SOP 形式，(b) 用指定门实现。解这种题时，首先按照 Karnaugh 图步骤，将 1 和 d 填入，圈出最大组合以得到最简表达式 [geeksforgeeks.org](https://www.geeksforgeeks.org/digital-logic/introduction-of-k-map-karnaugh-map/#:~:text=elsewhere%29,them%20up%20for%20SOP%20form)。然后，根据实现要求选择门电路。例如，要求 “仅用 NAND 门实现”，就需要将化简后的表达式转换为纯 NAND 形式（可以将表达式取反两次来引入 NAND 结构)。** 技巧：** 在 K 图化简过程中充分利用无关项来尽可能扩大圈；在门级实现时，牢记 NAND/NOR 实现等效变换的方法，如 $F = (AB + C)'$ 可实现为三个 NAND 级联。 _K-map with don't-cares & implementation:_ Some comprehensive questions combine simplification and implementation. For example, you might be given a function with don't-care conditions and asked (a) to simplify it to SOP form using a K-map, and (b) to implement the simplified expression using only NAND gates. Tackle this by first filling in the K-map with 1s and ds (don’t-cares) and grouping the cells to find the minimal SOP expression[geeksforgeeks.org](https://www.geeksforgeeks.org/digital-logic/introduction-of-k-map-karnaugh-map/#:~:text=elsewhere%29,them%20up%20for%20SOP%20form). Next, implement that expression with the specified gates. If the requirement is "NAND gates only", convert the simplified SOP into an all-NAND network (use double negation to introduce NAND structures). _Tips:_ Leverage don't-care cells in the K-map to form the largest groups possible for maximum simplification. For the implementation, recall NAND/NOR equivalences – for instance, if $F = AB + C$, you can rewrite $F$ as $F = ((AB + C)')'$ and implement the inner $(AB + C)'$ with NAND gates. Being comfortable with such transformations speeds up designing the final gate-level solution.
    
