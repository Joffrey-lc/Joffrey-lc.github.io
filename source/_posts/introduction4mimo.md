---
title: 知识储备-MIMO介绍
excerpt: 简单学习MIMO
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20220228235302024.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - MIMO
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2022-02-28 23:51:28
---

# MIMO

## MIMO介绍

SISO：Single Input Single Output：独木桥

MISO：Multi Input Single Output：发射端丢一点没关系，只要保证Multi Input 中有成功传输即可（发射分集）

SIMO：Single Input Multi Output：接收端丢一些没关系，只要保证Multi Output中有成功接收即可（接收分集）

MIMO：Multi Input Multi Output：利用多天线，复用空间中不同的传输路径并行发送多份不同数据来提升容量（空分复用）

![SISO到MIMO](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220228200503468.png)

**MIMO的性能受限于短板，即MIMO的最大容量受制于Input和Output端中天线数量少的一端。**

**For example：**

$A \times B $的MIMO，代表基站端有$A$根天线，用户端/手机有$B$根天线。$4\times 4$MIMO的最大容量可以达到SISO的**4**倍；而$4\times 2$MIMO的最大容量是SISO的**2**倍。

## MIMO建模

![2 times 2 MIMO示意图](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220228203934811.png)

得到一个方程组：
$$
\begin{align}
Y_1=h_{11}X_1+h_{21}X_2\\
Y_2=h_{12}X_1+h_{22}X_2\\

即\left[\begin{matrix}
Y_1\\Y_2
\end{matrix}
\right]=\left[
\begin{matrix}
h_{11}&h_{21}\\
h_{12}&h_{22}
\end{matrix}
\right]\cdot
\left[\begin{matrix}
X_1\\X_2
\end{matrix}
\right]
\end{align}
$$
但由于**信道之间存在相关性**，导致了容量的变化。

进一步推导，假设简化模型为：
$$
\left[\begin{matrix}
Y^{'}_1\\Y^{'}_2
\end{matrix}
\right]=\left[
\begin{matrix}
\lambda_1&0\\
0&\lambda_2
\end{matrix}
\right]\cdot\left[
\begin{matrix}
X_1^{'}\\X_2^{'}
\end{matrix}
\right]
$$
只有一个对角线有数据的矩阵称为对角阵，其中对角线上**非零数据**的个数，称为矩阵的秩。

很好理解，如果秩为1的话，即表达式中的$\lambda_2=0$，就表示这个2x2 MIMO系统的传输空间相关性很大，从MIMO退化成了SISO或者SIMO，只能同时收发一路数据；如果秩为2的话，就表示该系统有两条相对独立空间信道，可以同时收发两路数据。

但是这样的情况下也不一定是SISO的两倍。定义**条件数**：
$$
条件数=\frac{\lambda_1}{\lambda_2}
$$

- 如果条件数=1，说明两个信道半斤八两，此时的MIMO系统的容量达到最大。
- 如果条件数>1，说明两个信道有一定差距，此时系统会将主要资源放在质量好的信道上，此时$2\times 2$的MIMO系统的最大容量就介于$1\sim2$之间。

![合作通信](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220228234827809.png)

基站和用户（手机）之间是合作通信，所以信道信息是可知的，这样就可以让基站进行选择。

# Reference

https://zhuanlan.zhihu.com/p/41520064
