---
title: Statistical-CSI 一般CSI-Based模型+Statistical模型+低复杂度实现Statistical
excerpt: Onel-A Low-Complexity Beamforming Design for Multiuser Wireless Energy Transfer.
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220419163135323.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Channel Estimation
  - CSI
categories:
  - Paper Reading
  - Channel State Information
comment: valine
math: true
hide: false
date: 2022-04-19 16:30:55
---

**A Low-Complexity Beamforming Design for Multiuser Wireless Energy Transfer**.  *Onel L. A. López* et.al.  **IEEE Wireless Communications Letters, Jan.  2021**  ([pdf](https://ieeexplore.ieee.org/document/9184149))  (Citations **4**)



- $$\sup(\cdot)$$: 最小上界
- $$\inf(\cdot)$$: 最大下界

## Quick Overview

- 只利用信道的一阶统计量CSI-limited
- 提出了一种低复杂度但有效的EB算法，可以获得接近最优结果（在低$$\kappa$$时甚至优于平均CSI的最优化结果（Optimum））
- 多用户性能随天线数目的增加而提高，同时可以利用旋转天线来获得更好的性能
- **可以直接适用于WPCN和SWIPT**



## 主要内容

### 一般CSI-Based模型

第$$i$$th element接收信号为：
$$
y_i=\sqrt{\beta_i}\textbf{h}_i^T\sum\limits_{k=1}^K\textbf{w}_kx_k,\quad i=1,\cdots,N
$$
所以有接收到的能量：
$$
\begin{aligned}
E_i&=E[y_i^Hy_i]=\beta_iE_x\left[\left(\sum\limits_{k=1}^K\textbf{h}_i^T\textbf{w}_kx_k\right)^H\left(\sum\limits_{k=1}^K\textbf{h}_i^T\textbf{w}_kx_k\right)\right]\\
&=\beta_i\sum\limits_{k=1}^K|\textbf{h}_i^T\textbf{w}_k|^2E{[x_k^Hx_k]}=\beta_i\sum\limits_{k=1}^K|\textbf{h}_i^T\textbf{w}_k|^2
\end{aligned}
$$
<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220419154355123.png" alt="Proof" style="zoom: 33%;" />

目标是以公平的方式最大化每个设备收集的能量：
$$
\textbf{P1}: \text{maximize} \inf\limits_{i=1,\cdots,N}\{E_i\}\\
\text{subject to} \sum\limits_{k=1}^K||\textbf{w}_k||^2\leq1
$$
可以看到，优化目标是非凸的，优化约束是凸的。按照参考文献[^1]转换为SDP问题（semi-definite programming）：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220406225456729.png" alt="first part" style="zoom: 50%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220406225513750.png" alt="second part" style="zoom:48.6%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220419160245638.png" alt="证明" style="zoom:33%;" />

### Statistical Beamforming Design

因为前面的一般CSI-Based模型都需要完全知道CSI，即$$\textbf{h}$$是完全已知的。这在实际中有获取CSI消耗能量过大这类的限制，所以为了解决这个问题，可以使用统计CSI（部分CSI）来进行优化。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220419160707585.png" alt="image-20220419160707585" style="zoom:50%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220419161440897.png" alt="Proof" style="zoom: 33%;" />

- $$\bar{\textbf{h}}$$不容易估计错误
- 它在更大的时间范围内变化，不需要频繁更新
- 当信道完全确定，即$$\kappa\to\infty$$时，Statistical model与Full-CSI model接近，因为$$\hat{\textbf{h}}\to\textbf{0}$$



在本文中，$$\bar{\textbf{h}}_i=\sqrt{\frac{\kappa_i}{1+\kappa_i}}e^{\text{i}\phi_i}$$，$$\hat{\textbf{h}}_i\sim\sqrt{\frac{1}{\kappa_i+1}}\mathcal{CN}(\textbf{0},\textbf{I})$$，这是OneL大部分工作中使用的信道模型。

### A low Complexity Solution（Based on Statistical Beamforming Design）

随着PB天线数量增加，SDP方案计算成本很高，所以作者提出了一种低复杂度的算法（复杂度低，性能接近（低$$\kappa$$时超过）平均CSI的最优结果）：

> 可以考虑用于simple low-power IoT devices

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220419162008954.png" alt="image-20220419162008954" style="zoom: 50%;" />

- 只利用信道的一阶统计量CSI-limited
- 提出了一种低复杂度但有效的EB算法，可以获得接近最优结果（在低$$\kappa$$时甚至优于平均CSI的最优化结果（Optimum））
- 多用户性能随天线数目的增加而提高，同时可以利用旋转天线来获得更好的性能
- **可以直接适用于WPCN和SWIPT**

> [^1]:A. Thudugalage, S. Atapattu and J. Evans, "Beamformer design for wireless energy transfer with fairness," 2016 IEEE International Conference on Communications (ICC), 2016, pp. 1-6, doi: 10.1109/ICC.2016.7511170.

