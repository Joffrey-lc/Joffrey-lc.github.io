---
title: RANK-ONE Constraint及Precoder
excerpt: 整理了一下precoder/发射端BF遇到的问题
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220506200020959.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Beamforming
categories:
  - Paper Reading
  - Transmit Beamforming
comment: valine
math: true
hide: false
date: 2022-05-06 20:00:02
---

# Rank-One

由于在看precoder（发射端波束形成）时，不同文章建模的时候形式不同，有的有rank-one约束，有的没有，有的是放缩。在此做个整理

## 背景

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220421212504138.png" alt="image-20220421212504138" style="zoom: 33%;" />

其实无论是在通信中还是Wireless Energy Transfer中，都是相同的形式，即precoder可能是一个列向量$$\textbf{w}\in\mathbb{C}^{M\times 1}$$，也可能是一个矩阵$$\textbf{w}\in\mathbb{C}^{M\times K}$$。其中$$M,K$$分别是天线数量和用户数。



在最早的文章

>**Transmit beamforming for physical-layer multicasting**.  *N.D. Sidiropoulos* et.al.  **IEEE Transactions on Signal Processing, June 2006**  ([pdf](https://ieeexplore.ieee.org/document/1634819))  (Citations **904**)

作者认为

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220506192945337.png" alt="image-20220506192945337" style="zoom: 50%;" />

这是后面所有文章的基本，大家都是这么建模的；唯一问题是这里有个rank-one约束。一般的解决方法是通过drop rank-one constraint，然后得到优化结果后，再通过randomization得到最优的结果，笔记[^1]中有randomization相关内容。



但是在

>**Beamformer design for wireless energy transfer with fairness**.  *Amanthi Thudugalage* et.al.  **2016 IEEE International Conference on Communications (ICC), 22-27 May 2016**  ([pdf](https://ieeexplore.ieee.org/document/7511170))  (Citations **19**)

>**A Low-Complexity Beamforming Design for Multiuser Wireless Energy Transfer**.  *Onel L. A. López* et.al.  **IEEE Wireless Communications Letters, Jan.  2021**  ([pdf](https://ieeexplore.ieee.org/document/9184149))  (Citations **4**)

其实都是没有rank-one约束的，而是通过计算$$\mathbf{X}=\textbf{w}\textbf{w}^H$$的特征值和特征向量，以特征值为标准归一化（因为由$$\text{Tr}(\mathbf{X})=1$$约束，可知特征值之和为1）特征向量，并以归一化后的特征向量作为precoder。这里又存在一个新的问题，这个归一化是在{% label primary @时间上归一化 %}还是在{% label primary @功率上归一化 %}？其表达式和结果都是一样的，但是物理意义不同。

我认为在Onel文章中是在功率上归一化，在ICC中是以时间归一化



在多用户的BF模型中

>**Dual-Function Radar Communication Systems: A Solution to the Spectrum Congestion Problem**.  *Aboulnasr Hassanien* et.al.  **IEEE Signal Processing Magazine, Sept.  2019**  ([pdf](https://ieeexplore.ieee.org/document/8828023))  (Citations **78**)

>**MU-MIMO Communications With MIMO Radar: From Co-Existence to Joint Transmission**.  *Fan Liu* et.al.  **IEEE Transactions on Wireless Communications, April  2018**  ([pdf](https://ieeexplore.ieee.org/document/8288677))  (Citations **148**)

> **CSI-Free vs CSI-Based Multi-Antenna WET for Massive Low-Power Internet of Things**.  *Onel L. A. López* et.al.  **IEEE Transactions on Wireless Communications, May  2021**  ([pdf](https://ieeexplore.ieee.org/document/9316281))  (Citations **1**)

有表达式：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220505204643659.png" alt="image-20220505204643659" style="zoom:50%;" />

但是值得注意的是，其求和符号上限时而是用户数$$K$$，时而是天线数$$M$$。



总而言之，三个问题：

{% note success %}

- rank-one约束什么时候存在？
- 特征值归一化什么时候在时间上什么时候在功率上分配？
- 求和上限到底是什么？

{% endnote %}

## Answer

### rank-one约束

这个rank-one约束的存在是因为，一根天线只能乘一个权值，所以其实在一个时刻，可以认为$$\mathbf{X}=\mathbf{w}\mathbf{w}^H$$是由一个列向量$$\times$$列向量的共轭转置得到的结果，所以一定是rank-one的。



但是由于后面存在的Multiple Beamforming或者松弛，把rank-one丢掉了。

### 时间分配or功率分配

时间分配如下图，在ICC文章中如下：

![Mutiple BF示意图](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220421212040776.png)

功率分配暂时没有看到文章指出，但是是很好理解。



根据具体模型来判断，其结果完全一样。

### 求和上限

首先我觉得很多学者混用了。一般而言都应该是$$K$$（用户数），但是可能存在$$M=K$$的情况

又或者说，当$$M<K$$时，$$\mathbf{X}=\mathbf{w}\mathbf{w}^H$$的秩为$$\min\{M,K\}=M$$，这也意味着最多存在的BF个数为$$\min\{M,K\}=M$$个。所以可以用$$M$$作为求和上界。

## New Question

==既然rank-one BF不仅计算量大，而且性能不好，为什么不直接用特征值归一化的BF？==

[^1]: https://lcjoffrey.top/2022/04/20/TransmitBF4Phy-layer-Multicasting/
