---
tags: 
  - 字符串
  - 前缀和
  - 差分
  - Notebooks/OI/OJ/Luogu
title: CF17E-Palisection
date: '2021-01-31 14:27:28.677126'
modified: '2021-01-31 14:27:28.677152'

---
# CF17E-Palisection
## 题目:
### 题目描述:
In an English class Nick had nothing to do at all, and remembered about wonderful strings called palindromes. We should remind you that a string is called a palindrome if it can be read the same way both from left to right and from right to left. Here are examples of such strings: «eye», «pop», «level», «aba», «deed», «racecar», «rotor», «madam».

Nick started to look carefully for all palindromes in the text that they were reading in the class. For each occurrence of each palindrome in the text he wrote a pair — the position of the beginning and the position of the ending of this occurrence in the text. Nick called each occurrence of each palindrome he found in the text subpalindrome. When he found all the subpalindromes, he decided to find out how many different pairs among these subpalindromes cross. Two subpalindromes cross if they cover common positions in the text. No palindrome can cross itself.

Let's look at the actions, performed by Nick, by the example of text «babb». At first he wrote out all subpalindromes:

• «b» — $ 1..1 $ • «bab» — $ 1..3 $ • «a» — $ 2..2 $ • «b» — $ 3..3 $ • «bb» — $ 3..4 $ • «b» — $ 4..4 $ Then Nick counted the amount of different pairs among these subpalindromes that cross. These pairs were six:

 1. $ 1..1 $ cross with $ 1..3 $  2. $ 1..3 $ cross with $ 2..2 $  3. $ 1..3 $ cross with $ 3..3 $  4. $ 1..3 $ cross with $ 3..4 $  5. $ 3..3 $ cross with $ 3..4 $  6. $ 3..4 $ cross with $ 4..4 $ Since it's very exhausting to perform all the described actions manually, Nick asked you to help him and write a program that can find out the amount of different subpalindrome pairs that cross. Two subpalindrome pairs are regarded as different if one of the pairs contains a subpalindrome that the other does not.
### 输入格式:
The first input line contains integer $ n $ ( $ 1<=n<=2·10^{6} $ ) — length of the text. The following line contains $ n $ lower-case Latin letters (from a to z).
### 输出格式:
In the only line output the amount of different pairs of two subpalindromes that cross each other. Output the answer modulo $ 51123987 $ .
### 样例:
#### 样例输入1:
```
4
babb

```
#### 样例输出1:
```
6

```
#### 样例输入2:
```
2
aa

```
#### 样例输出2:
```
2

```
## 思路:

## 实现:
```cpp
// Problem: CF17E Palisection
// Contest: Luogu
// URL: https://www.luogu.com.cn/problem/CF17E
// Memory Limit: 125 MB
// Time Limit: 2000 ms
// Author: Ybw051114
//
// Powered by CP Editor (https://cpeditor.org)

#include "ybwhead/ios.h"
using namespace std;
// typedef int ll;
typedef long long int li;
const ll maxn = 4e6 + 51, mod = 51123987, inv2 = 25561994;
ll n, mxr, mid, c, res, lx, rx;
ll rad[maxn], f[maxn], g[maxn];
char s[maxn], ch[maxn];
int main()
{
    yin >> n >> (s + 1);
    ch[0] = '~', ch[n * 2 + 1] = '|';
    for (register int i = 1; i <= n; i++)
    {
        ch[i * 2 - 1] = '|', ch[i * 2] = s[i];
    }
    for (register int i = 1; i <= 2 * n + 1; i++)
    {
        rad[i] = i < mxr ? min(rad[(mid << 1) - i], rad[mid] + mid - i) : 1;
        while (ch[i + rad[i]] == ch[i - rad[i]])
        {
            rad[i]++;
        }
        rad[i] + i > mxr ? mxr = rad[i] + i, mid = i : 1;
    }
    for (register int i = 1; i <= 2 * n + 1; i++)
    {
        lx = i - rad[i] + 1, rx = i + rad[i] - 1, lx += lx & 1, rx -= rx & 1;
        if (lx <= rx)
        {
            lx >>= 1, rx >>= 1, f[lx]++, f[(i >> 1) + 1]--, g[(i + 1) >> 1]++, g[rx + 1]--;
            c = (c + (i >> 1) - lx + 1) % mod;
        }
    }
    for (register int i = 1; i <= n; i++)
    {
        f[i] += f[i - 1], g[i] += g[i - 1];
    }
    for (register int i = 1; i <= n; i++)
    {
        g[i] = (g[i] + g[i - 1]) % mod, res = (res + (li)f[i] * g[i - 1] % mod) % mod;
    }
    yout << ((li)c * (c - 1) % mod * inv2 % mod - res + mod) % mod << endl;
}

```
