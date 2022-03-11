---
title: Weighted Sum Power Maximization for Intelligent Reflecting Surface Aided SWIPT-梳理
excerpt:（武庆庆）IRS辅助SWIPT
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220311150044247.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - SWIPT
  - IRS
categories:
  - Paper Reading
  - Intelligent Reflecting Surface
comment: valine
math: true
hide: false
date: 2022-03-11 15:03:11
---

## 缩写说明

- IDRs: Information Decoding Receivers
- EHRs: Energy Harvesting Receivers
- CSCG: Circularly Symmetric Complex Gaussian denoted by $\mathcal{C}\mathcal{N}(x, \sigma^2)$(with mean $x$ and variance $\sigma^2$ )

## 主要内容

### 主要思路：

提出使用**IRS协助多天线AP服务于多IDRs和多EHRs**。因为能量一般路径损耗较大，难以满足需求（需要更大能量才能被接收，而信息信号只需要少量功率就可以成功解调）。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220311150044247.png" alt="IRS辅助SWIPT" style="zoom:50%;" />

### 文章主要贡献：

- **提出一种联合优化发射机的预编码向量（波束赋形）、IRS的相移（反射幅度为1），在IDRs的单个信干噪比的约束下，最大化EHRs接收的加权和功率。**
- **仅在AP处发送信息信号就可以同时服务于IDRs和EHRs，不需要专用的能量信号。（能量信号对于IDRs而言是干扰）**

理论上而言，如果用户之间（IDRs和EHRs）之间的信道是统计独立的，那么不需要再使用专用的能量信号[^1]。文章中Ⅳ小节中详细证明：即使用户的信道在统计上不是独立的，仅发送信息信号就足以在EHRs处实现最大加权和功率。（专用能量信号不仅消耗发射机功率，还会对IDRs产生干扰）

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

[1]: Xu, Jie, Liang Liu, and Rui Zhang. "Multiuser MISO beamforming for simultaneous wireless information and power transfer." *IEEE Transactions on Signal Processing* 62.18 (2014): 4798-4810.

[2]: Pan, Cunhua, et al. "Intelligent reflecting surface aided MIMO broadcasting for simultaneous wireless information and power transfer." *IEEE Journal on Selected Areas in Communications* 38.8 (2020): 1719-1734.
