---
title: 鲁棒beamforming
excerpt: Ming-Min Zhao et.al.--Outage-Constrained Robust Beamforming for Intelligent Reflecting Surface Aided Wireless Communication
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202211231118900.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Robust Beamforming
categories:
  - Paper Reading
  - Robust Beamforming
comment: valine
math: true
hide: false
date: 2022-11-23 11:18:02
---

Date: 2022.11.21  16:15
Author: Joffrey LC

-------------------------------------

**Outage-Constrained Robust Beamforming for Intelligent Reflecting Surface Aided Wireless Communication**.  *Ming-Min Zhao* et.al.  **IEEE Transactions on Signal Processing, 2021**  ([pdf](https://ieeexplore.ieee.org/document/9352530))  (Citations **16**)



记录一下，zhougui等人的robust beamforming  github code ：https://github.com/ken0225/Framework-of-Robust-Transmission-Design-for-IRS-Aided-MISO-Communications

## Quick Overview

在用户最大CSI错误中断概率约束的前提下，联合优化AP和IRS以最小化AP处的发射功率。

- 先考虑单用户情况，计算单用户的平均信号的功率和方差来计算中断概率（功率和方差是trade-off）
- 多用户情况，很难求出闭式解，通过优化算法解决



现有的robust beamforming的算法，可以分为方向：

1. 假设部分信道不确定性（有界的CSI误差模型），联合设计precoder和IRS reflection matrix
2. 假设统计信号误差模型（高斯分布等）
3. 设计中断概率下界高于某个阈值



算法上：

- 对单用户，讨论MSP（mean signal power）的均值和方差的trade-off，通过一维搜索搞定
- 对多用户，SCA，并且先将离散的相位变化放缩到连续，进行优化后，放回离散值并固定，再对precoder进行优化，以补偿IRS相位从连续到离散的损失



## 单用户（过程很有意思）

有意思的是，其约束是一个概率：
$$
\begin{aligned}
\min _{\left\{\mathbf{w}_k\right\}, \boldsymbol{\Theta}} & \sum_{k \in \mathcal{K}}\left\|\mathbf{w}_k\right\|^2 \\
\text { s.t. } & \operatorname{Pr}\left(\operatorname{SINR}_k<\eta_k\right) \leq \epsilon_k, \forall k \in \mathcal{K}, \\
& \phi_n \in \mathcal{F}_d, \forall n \in \mathcal{N} .
\end{aligned}
$$
即优化目标为最小化发射功率，约束（6b）指中断概率小于一个阈值,（6c）指IRS相位的可行域

单用户的时候，可以丢掉下标$$k$$，然后写成矩阵形式有：
$$
\begin{aligned}
\min _{\mathbf{w}, \boldsymbol{\Theta}} &\|\mathbf{w}\|^2 \\
\text { s.t. } & \operatorname{Pr}\left(\left|\left(\mathbf{h}_r^H \boldsymbol{\Theta} \mathbf{G}+\mathbf{h}_d^H\right) \mathbf{w}\right|^2<\sigma^2 \eta\right) \leq \epsilon, \\
& \phi_n \in \mathcal{F}_d, \forall n \in \mathcal{N} .
\end{aligned}
$$
并且由变量替换：
$$
\mathbf{H}_k \triangleq \operatorname{diag}\left(\mathbf{h}_{r, k}^H\right) \mathbf{G}
$$
上式等于：
$$
\begin{aligned}
\min _{\mathbf{w}, \mathbf{v}} &\|\mathbf{w}\|^2 \\
\text { s.t. } & \operatorname{Pr}\left(\left|\left(\mathbf{v}^H \mathbf{H}+\mathbf{h}_d^H\right) \mathbf{w}\right|^2<\sigma^2 \eta\right) \leq \epsilon, \\
& v_n \in \mathcal{F}_d, \forall n \in \mathcal{N} .
\end{aligned}
$$
由于发射功率越大中断概率肯定越小，所以可以交换一下：
$$
\begin{aligned}
&\min _{\mathbf{w}, \mathbf{v}} \operatorname{Pr}\left(\left|\left(\mathbf{v}^H \mathbf{H}+\mathbf{h}_d^H\right) \mathbf{w}\right|^2<\sigma^2 \eta\right) \\
&\text { s.t. }\|\mathbf{w}\|^2 \leq p, \\
&v_n \in \mathcal{F}_d, \forall n \in \mathcal{N},
\end{aligned}
$$


然后，加法形式可以再次写成矩阵乘法形式：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202211231118600.png" alt="image-20221123105539827" style="zoom: 50%;" />

进一步，上述优化目标等于求CDF：
$$
\begin{aligned}
\min _{\mathbf{w}, \mathbf{v}} & \iint_{\mathbf{D}} \mathcal{C N}\left(z ; \tilde{\mathbf{v}}^H \overline{\mathbf{H}} \mathbf{w}, p \tilde{\mathbf{v}}^H \overline{\mathbf{V}} \tilde{\mathbf{v}}\right) \\
\text { s.t. } &\|\mathbf{w}\|^2 \leq p, \\
& v_n \in \mathcal{F}_d, \forall n \in \mathcal{N},
\end{aligned}
$$
因为其CDF为：
$$
\begin{aligned}
&\iint_{\mathbf{D}} \mathcal{C N}\left(z ; \tilde{\mathbf{v}}^H \overline{\mathbf{H}} \mathbf{w}, p \tilde{\mathbf{v}}^H \overline{\mathbf{V}} \tilde{\mathbf{v}}\right) \\
&=\mathcal{P}\left(\left.\frac{\eta \sigma^2}{\frac{1}{2} p \tilde{\mathbf{v}}^H \overline{\mathbf{V}} \tilde{\mathbf{v}}}\right|_2, \frac{\left|\tilde{\mathbf{v}}^H \overline{\mathbf{H}} \mathbf{w}\right|^2}{\frac{1}{2} p \tilde{\mathbf{v}}^H \overline{\mathbf{V}} \tilde{\mathbf{v}}}\right)
\end{aligned}
$$
意思是，服从自由度为2，参数为$$\lambda$$的卡方：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202211231118668.png" alt="image-20221123105944569" style="zoom: 50%;" />

需要同时最大化$$\frac{\tilde{\mathbf{v}}^H \overline{\mathbf{H}} \overline{\mathbf{H}}^H \tilde{\mathbf{v}}}{\tilde{\mathbf{v}}^H \overline{\mathbf{V}} \tilde{\mathbf{v}}}$$和$$\tilde{\mathbf{v}}^H \overline{\mathbf{V}} \tilde{\mathbf{v}}$$，$$\mathcal{P}\left[\left.\chi^2\right|_2, \lambda\right]$$是$$\chi$$的递增函数，是$$\lambda$$的递减函数。

但是同时最大化感觉是不合理的。只能在最大化二者之间找一个平衡：
$$
\begin{gathered}
\max _{\mathbf{v}} \tilde{\mathbf{v}}^H \overline{\mathbf{H}} \overline{\mathbf{H}}^H \tilde{\mathbf{v}}+\omega \tilde{\mathbf{v}}^H \overline{\mathbf{V}} \tilde{\mathbf{v}} \\
\text { s.t. } v_n \in \mathcal{F}_d, \forall n \in \mathcal{N},
\end{gathered}
$$
怎么解得，看不懂。



## 多用户

