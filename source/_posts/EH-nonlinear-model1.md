---
title: 无线能量传输-能量接收机的非线性接收模型（一）
excerpt: Elena Boshkovska et.al.-Practical Non-Linear Energy Harvesting Model and Resource Allocation for SWIPT Systems
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220425154153217.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - WPT
  - Energy Harvested Model
categories:
  - Paper Reading
  - Wireless Energy Transfer
comment: valine
math: true
hide: false
date: 2022-04-25 15:41:18
---

Date: 2022.04.22  17:07
Author: Joffrey LC

-------------------------------------

**Practical Non-Linear Energy Harvesting Model and Resource Allocation for SWIPT Systems**.  *Elena Boshkovska* et.al.  **IEEE Communications Letters, Dec.  2015**  ([pdf](https://ieeexplore.ieee.org/document/7264986))  (Citations **551**)

## Quick Overview

- 提出Energy Harvesting Model 是 non-linear的，并给出模型（需要根据具体测量值，拟合得到具体参数）
- 给出一种双重循环的快速解决方案（这部分简单看了一下）

{% note success %}
如果噪声是矩阵形式，应该表示为$$\textbf{n}\sim\mathcal{CN}(\textbf{0},\sigma^2\textbf{I})$$，其中$$\sigma^2$$表示噪声的功率
{% endnote %}

## 主要内容

### Energy Harvesting Model

Proposed a Non- Linear EH model based on the logistic (sigmoid) function: 
$$
\begin{aligned}
\Phi_{\mathrm{ER}_{j}}^{\text {Practical }} &=\frac{\left[\Psi_{\mathrm{ER}_{j}}^{\text {Practical }}-M_{j} \Omega_{j}\right]}{1-\Omega_{j}}, \Omega_{j}=\frac{1}{1+\exp \left(a_{j} b_{j}\right)} \\
\Psi_{\mathrm{ER}_{j}}^{\text {Practical }} &=\frac{M_{j}}{1+\exp \left(-a_{j}\left(P_{\mathrm{ER}_{j}}-b_{j}\right)\right)}
\end{aligned}
$$
其中，$$\Phi_{\mathrm{ER}_{j}}^{\text {Practical }}$$代表$$j$$-th ER 接受到的总能量；$$\Psi_{\mathrm{ER}_{j}}^{\text {Practical }}$$代表logistic function with respect to the receive RF power $$P_{\mathrm{ER}_{j}}$$。{% label primary @其他参数例如$$a_j,b_j,M_j$$都是通过对实际电路模型的测量值进行拟合得到 %}

{% note success %}

**并且由于$$\Omega_j$$并不影响$$\textbf{w}$$的设计，所以一般采用$$\Psi_{\mathrm{ER}_{j}}^{\text {Practical }}$$表示接收到的能量。**有典型值[^1]：

$$M_j=20\text{mW},a_j=6400,b_j=0.003$$

{% endnote %}

### 双循环解法

#### 原始问题建模：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220425153130097.png" alt="原始问题建模" style="zoom: 80%;" />

C1：功率约束

C2：SINR约束

#### Proposal 流程

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220425153239885.png" alt="提出算法流程" style="zoom: 60%;" />

{% note success %}

另外有一个重要理论（没有证明）：

{% endnote %}

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220425153355034.png" alt="重要理论" style="zoom:60%;" />



## Result

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220425153919035.png" alt="exp1" style="zoom:60%;" />

- Harvested Energy 随着Minimum required SINR 增大而减小
- Harvested Energy 随着单个ER的天线数量$$N_T$$的增大而增大：因为更多的天线带来更高的自由度，会得到更高效的资源分配方案

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220425153946764.png" alt="exp2" style="zoom:60%;" />

- Harvested Energy 随着ERs数量增大而增大，而且性能增益（Performance Gap between Non-Linear Model with Linear Model）增大：因为ERs数量增大，Baseline（Performance with Linear Model）的失配（mismatch）更严重

---

[^1]: T. Le, K. Mayaram and T. Fiez, "Efficient Far-Field Radio Frequency Energy Harvesting for Passively Powered Sensor Networks," in *IEEE Journal of Solid-State Circuits*, vol. 43, no. 5, pp. 1287-1302, May 2008, doi: 10.1109/JSSC.2008.920318. ↩
