---
title: MAX–MIN FAIR BEAMFORMING -> SDP Question
excerpt: N.D. Sidiropoulos et.al.-Transmit beamforming for physical-layer multicasting
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220420212811327.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Transmit Beamforming
  - Channel Estimation
categories:
  - Paper Reading
  - Transmit Beamforming
comment: valine
math: true
hide: false
date: 2022-04-20 21:26:02
---

-------------------------------------

**Transmit beamforming for physical-layer multicasting**.  *N.D. Sidiropoulos* et.al.  **IEEE Transactions on Signal Processing, June 2006**  ([pdf](https://ieeexplore.ieee.org/document/1634819))  (Citations **904**)

## Quick Overview

考虑MAX–MIN FAIR BEAMFORMING

- 将 Precoder原先的非凸优化问题松弛到SDP问题
- 考虑松弛后，对结果进行再优化
  - 如果解出来的矩阵是rank-one，那么就是这个原始问题的最优结果
  - 如果解出来的矩阵不是rank-one，那么这个解就是满足约束的下限
- 在非rank-one的前提下，给出三种 based on *randomization*的方法，选择出最优的结果

## 主要内容

### 建模

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220420210025213.png" alt="建模" style="zoom: 50%;" />

值得注意的一个等价形式：
$$
\tilde{\mathbf{h}}_{i}^{H} \mathbf{w} \mathbf{w}^{H} \tilde{\mathbf{h}}_{i}=\Tr(\tilde{\mathbf{h}}_{i}^{H} \mathbf{w} \mathbf{w}^{H} \tilde{\mathbf{h}}_{i})=\Tr(\mathbf{w} \mathbf{w}^{H}\tilde{\mathbf{h}}_{i}\tilde{\mathbf{h}}_{i}^{H})=\Tr(\textbf{XQ}_i)
$$
Drop rank-one constraint 会得到一个松弛结果。

由松弛结果可以得到$$\textbf{X}_{\text{opt}}$$，然后得到a set of candidate weight vectors，再根据某种判别条件（好像不同文章中的从set中选择最优的条件不同）选择最优结果。

### randA

对解得的$$\textbf{X}_{\text{opt}}$$有$$\textbf{X}_{\text{opt}}=\textbf{U}\Sigma\textbf{U}^H$$，可以得到a set of candidate weight vectors $$\textbf{w}_l=\textbf{U}\Sigma^{1/2}\textbf{e}_l$$，其中$$[\textbf{e}_l]_i=e^{j\theta_{l,j}}$$，且$$\theta_{l,j}\sim U[0,2\pi)$$。以保证有$$\textbf{w}_l^H\textbf{w}_l=\Tr(\textbf{X}_{\text{opt}})$$

### randB

对解得的$$\textbf{X}_{\text{opt}}$$做$$[\textbf{w}_l]_i=\sqrt{[\textbf{X}]_{ii}}[\textbf{e}_l]_i$$，以保证有$$|[\textbf{w}_l]_i|^2=[\textbf{X}_{\text{opt}}]_{ii}$$，其中$$\textbf{e}_{l}$$同*randA*。

### randC

类似于*randA*，有$$\textbf{w}_l=\textbf{U}\Sigma^{1/2}\textbf{v}_l$$，其中$$\textbf{v}_l\sim\mathcal{CN}(0,1)$$，以保证有$$\text{E}[\textbf{w}_l\textbf{w}^H]=\textbf{X}_{\text{opt}}$$
