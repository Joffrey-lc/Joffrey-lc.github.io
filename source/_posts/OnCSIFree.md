---
title: CSI-FREE 分析AA-SS/AA-IS/SA三种结构
excerpt: Onel L. A. López et.al.-On CSI-Free Multiantenna Schemes for Massive RF Wireless Energy Transfer
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20220327224651.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - CSI Free
  - WET
  - WPT
categories:
  - Paper Reading
  - Simultaneous Wireless Information and Power Transfer
comment: valine
math: true
hide: false
date: 2022-03-27 22:43:18
---

**On CSI-Free Multiantenna Schemes for Massive RF Wireless Energy Transfer**.  *Onel L. A. López* et.al.  **IEEE Internet of Things Journal, Jan.1, 1 2021**  ([pdf](https://ieeexplore.ieee.org/document/9119347))  (Citations **8**)

因为论文中设计大量推导以及证明和实验，所以具体内容只整理了部分，其余见[我的论文笔记](.\MyPaperNote.html)：

{% cb 信道建模、非线性能量转换建模、Preventive Adjustment of Mean Phases , true%}

{% cb AA-SS、AA-IS、SA等等 , false%}

{% cb 实验等 , false%}

## 缩写说明

AA-SS: PB所有天线都发射相同的信号，且每根天线功率相同

AA-IS: PB所有天线发射i. i. d.信号

SA: M根天线中随机选一根，持续时间1/M

## 基础知识

- 准静态信道：时间缓慢变换的信道就是准静态信道了，不随时间变化的信道一般就是静态信道。比如在一段时间内，信道是不变化的，那么在这段时间内就可以看成静态信道。多普勒频移的倒数可以看成信道时变性（信道相干时间）的基准，如果符号持续时间远大于相干时间，那么就是个非静态信道如果符号持续时间远小于相干时间，就可以认为是准静态信道了。

## Quick Overview

对AA-SS、AA-IS、SA三种结构进行建模分析，得到其接收机入射端的能量的均值和能量方差是一个Trade off。

- 近PB（path loss 小），AA-IS好；远PB（path loss 大），SA好（二者性能统计上比较接近，后面分析也是一起分析的）。
- 在AA-SS结构中，阵元数（天线数）$$M$$也不是越多越好。越多$$M$$越多极小值，取到极小值的几率也增大（fig 1(a)）。
- 可以通过$$\pi$$相移取得AA-SS的较好结果（图fig 2 (b)）:极小值个数不变；最佳增益在$$|\phi|=\pi/2$$时；**曲线下面积增大了**。**能量均值严重依赖天线的平均相移**。
- 优化AA-SS有两种：$$AA-SS_{\max E}$$和$$AA-SS_{\min Var}$$，$$\max E$$的variance大，$$\min Var$$的mean小。
- 优化AA-IS发现：能量均值计算时，由于$$M$$在分母，而分子的值极小，所以AA-IS**入射能量均值**与**天线数目关系不大**；而$$M$$的增大可以**有效减小方差**。
- 优化SA没有讲，因为难以建模，但是和AA-IS性能相近。
- 非特定空间/方向，选AA-IS or SA；特定空间和方向选择AA-SS
- AA-SS提供最大的能量均值，但是其方差性能差，而且中断概率高。**似乎AA-SS更适合物联网设备积累能量的场景。**
- 信道相关性对AA-SS是有益的。
- 预防性相移可以用来控制最大化能量均值或者最小化能量方差。
- 对于AA-SS， LOS并不是总是有益的。甚至$$\kappa=0dB$$的中断概率低于$$\kappa=10dB$$。
- AA-IS和SA都受益于小的相关性（越小越好），和大的天线数量（越多越好）和LOS

## 具体内容

### Channel Model 

莱斯信道建模，由$$\kappa$$来控制信道是**瑞利衰落信道**（$$\kappa=0$$）还是**完全确定LOS信道**（$$\kappa\to\infin$$）

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220327000145442.png" alt="image-20220327000145442" style="zoom: 67%;" />

其中，$$\textbf{h}_{los}=\left[\begin{array}11 & e^{i\Phi_1} & \cdots e^{i\Phi_{M-1}}\end{array}\right]$$是确定LOS信道，并且$$\Phi_t,t\in\{1,\cdots,M-1\}$$是第$$(t+1)$$个阵元相对于第一个阵元的平均相移。$$\varphi_0$$是初相；

其中，$$\textbf{h}_{nlos}\sim\mathcal{CN}(\textbf{0,R})$$表示瑞利信道系数。

考虑ULA，可以得到：
$$
\Phi_t=-t\pi\sin\phi
$$
其中，$$t$$是阵元间隔，$$\phi$$是来波（能量信号）和阵元的方向夹角。

### Preventive Adjustment of Mean Phases

做$$\textbf{h}^*=\Psi\textbf{h}$$，且有：
$$
\Psi=diag(1,e^{i\psi_1},\cdots,e^{i\psi_{M-1}})
$$
得到：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220327101257249.png" alt="image-20220327101257249" style="zoom: 67%;" />

证明见**Noteability**。

### EH Transfer Function

非线性表达式：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220327101409153.png" alt="image-20220327101409153" style="zoom:67%;" />

**a,b代表什么物理含义？？**





