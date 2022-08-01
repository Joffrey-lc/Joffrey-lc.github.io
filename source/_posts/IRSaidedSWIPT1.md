---
title: IRS辅助SWIPT（一）
excerpt: 武庆庆-Weighted Sum Power Maximization for Intelligent Reflflecting Surface Aided SWIPT
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220311150044247.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - IRS
  - SWIPT
categories:
  - Paper Reading
  - Intelligent Reflecting Surface
comment: valine
math: true
hide: false
date: 2022-03-11 15:03:11
---

原文[Weighted Sum Power Maximization for Intelligent Reflflecting Surface Aided SWIPT](https://ieeexplore.ieee.org/document/8941080)

## 缩写说明

- IDRs: Information Decoding Receivers
- EHRs: Energy Harvesting Receivers
- CSCG: Circularly Symmetric Complex Gaussian denoted by $$\mathcal{C}\mathcal{N}(x, \sigma^2)$$(with mean $$x$$ and variance $$\sigma^2$$ )

## 主要内容

### 主要思路：

提出使用**IRS协助多天线AP服务于多IDRs和多EHRs**。主要最大化加权和能量，同时满足IDRs的最小SINR。因为能量一般路径损耗较大，难以满足需求（需要更大能量才能被接收，而信息信号只需要少量功率就可以成功解调）。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220311150044247.png" alt="IRS辅助SWIPT" style="zoom:50%;" />

### 文章主要贡献：

- **提出一种联合优化发射机的预编码向量（波束赋形）、IRS的相移（反射幅度为1），在IDRs的单个信干噪比的约束下，最大化EHRs接收的加权和功率。**{% label primary @（考虑的是最大输入功率，而不是最大接收功率，也就是没有考虑EH接收机的非线性特性）%}
- **仅在AP处发送信息信号就可以同时服务于IDRs和EHRs，不需要专用的能量信号。（能量信号对于IDRs而言是干扰）**{% label primary @（证明了优化Information precoder和Energy precoder的结果（SDR1）和只优化Information precoder（SDR2）的最终结果是相同的。即只需要Information precoder）%}

理论上而言，如果用户之间（IDRs和EHRs）之间的信道是统计独立的，那么不需要再使用专用的能量信号[^1]。文章中Ⅳ小节中详细证明：即使用户的信道在统计上不是独立的，仅发送信息信号就足以在EHRs处实现最大加权和功率。（专用能量信号不仅消耗发射机功率，还会对IDRs产生干扰）

{% label primary @As the IRS reflects signals only in its front half-sphere instead of isotropically,  each reflecting element is assumed to have a 3 dBi gain.%}

## Optimization

### IRS aided WET

对于IRS只服务于WET，使用SCA的优化方式。SCA的难点在于怎么找到一个不等式，满足SCA条件，即在该可行点上，连续，函数值相等，一阶导数相等，且是凸的。



- 固定IRS elements $$\theta$$，在没有其他约束条件的情况下，可以快速求解$$\textbf{w}$$就是$$S$$的最大特征值对对应的特征向量（记得用特征值归一化）
- 有了$$\textbf{w}$$，可以由泰勒一阶展开得到下界的闭式解

然后重复上述步骤，不断迭代逼近。

![image-20220716194058901](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220716194058901.png)

### IRS aided SWIPT

麻烦点，先由SDR1，求解最优的$$\textbf{W}_i$$（注意两个$$\textbf{W}$$的秩不同）

![image-20220716194338197](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220716194338197.png)

- 固定$$\theta$$，根据**Proposition 1**可以另$$\mathbf{W_e}=0$$，然后求解最优的rank-one的$$\mathbf{W}_i$$

- 由求解出来的$$\mathbf{W}_i$$，优化求解最佳的$$\theta$$。然后利用高斯随机化[^3][^4]提升性能。

重复上述步骤，直到最优。

## 实验

实验模型：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220311145105721.png" alt="模型" style="zoom:50%;" />

其中$r_1=2$。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220311144927006.png" alt="提出的算法性能" style="zoom: 50%;" />

可以看到使用IRS能够极大提升EHRs接收性能；LoS信道比瑞利衰落信道下EHRs效率更高（接收更多RF能量）。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220311145433868.png" alt="EHRs接收能量和IDRs信噪比需求关系" style="zoom: 67%;" />

红色虚线代表文献[^1]中提出的单独设计专用能量信号的方案。即：

1. 先最小化满足SINR条件的IDRs总功率
2. 剩下的能量通过波束赋形全部用于EHRs

可以看到联合设计>单独设计>无IRS。也证明了文章中的建议：不应使用专用能量信号。



作者说文献[^2]研究内容与本文相似。

[^1]: Xu, Jie, Liang Liu, and Rui Zhang. "Multiuser MISO beamforming for simultaneous wireless information and power transfer." *IEEE Transactions on Signal Processing* 62.18 (2014): 4798-4810.
[^2]: Pan, Cunhua, et al. "Intelligent reflecting surface aided MIMO broadcasting for simultaneous wireless information and power transfer." *IEEE Journal on Selected Areas in Communications* 38.8 (2020): 1719-1734.
[^3]:https://lcjoffrey.top/2022/04/20/TransmitBF4Phy-layer-Multicasting/
[^4]:
