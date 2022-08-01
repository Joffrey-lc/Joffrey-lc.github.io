---
title: Max-Min Fair Beamforming->Single & Multiple BF
excerpt: Amanthi Thudugalage et.al.- Beamformer design for wireless energy transfer with fairness
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220420224457025.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Transmit Beamforming
categories:
  - Paper Reading
  - Transmit Beamforming
comment: valine
math: true
hide: false
date: 2022-04-20 22:40:50
---

-------------------------------------

**Beamformer design for wireless energy transfer with fairness**.  *Amanthi Thudugalage* et.al.  **2016 IEEE International Conference on Communications (ICC), 22-27 May 2016**  ([pdf](https://ieeexplore.ieee.org/document/7511170))  (Citations **19**)

## Quick Overview

Max-Min Fair Beamforming 

- 松弛为SDP问题
- 考虑Single Beamforming问题和Multiple Beamforming问题
- 利用randC（$$\textbf{w}_l=\textbf{U}\Sigma^{1/2}\textbf{v}_l$$）得到Single的最优解
- Mutiple BF可以得到精确的解
- Mutiple 比 Single更公平，简单分析了原因

## 主要内容

### Single Beamforming建模和松弛

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220420221710118.png" alt="建模和松弛" style="zoom: 44%;" />

松弛的结果不满足rank-one，可以使用*randC*进行进一步优化->randomization。

> 注意，Single Beamforming 意味着是天线在全时间段使用一组$$\textbf{w}$$，所以$$\textbf{w}\in\mathbb{C}^{M\times 1}$$，所以有rank-one约束。

### Multiple Beamforming建模和松弛

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220420222410043.png" alt="示意图" style="zoom:44%;" />

如上图所示，在时间$$T_c$$内，有多个Beamforming，下文中建模都是对(a) equal durations 进行建模，没有对different durations 建模。但是实验好像又用的different durations，只能说结构上是类似的。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220420222008513.png" alt="part 1" style="zoom:44%;" />

值得注意的是，这里没有rank-one约束，因为不再是single Beamforming了。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220420222100023.png" alt="Part 2" style="zoom:44%;" />

> 我理解的different durations，通过对$$\textbf{X}_{\text{opt}}$$进行特征值分解，丢弃$$10^{-5}$$以下，保留较大项。以特征值作为持续时间，特征向量作为$$\textbf{w}$$。从物理意义上而言，仅用较大特征值对应的特征向（作为$$\textbf{w}$$）就可以表示其余特征向量；亦或者说较大特征值占用较多时间，那么意味着较小特征值几乎没有占用时间，就可以丢弃了。

简而言之，由于不再是single Beamforming，所以没有rank-one约束，也没有其他rank约束，因为解出来的特征值较大项是多少就用多少的。不需要强制限制。

### 实验结果

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220420223523451.png" alt="exp1" style="zoom: 33%;" />

与Total-Energy Maximization相比，Single Beamforming的Max-Min Fair Beamforming更公平。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220420223624885.png" alt="exp2" style="zoom: 33%;" />

与Single Beamforming相比，Mutiple Beamforming更为公平（这里等于取rank=3）

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220420223713263.png" alt="exp3" style="zoom: 33%;" />

这张图也可以看出来，Mutiple Beamforming中几乎13/20个用户都处于相同水平的Energy；而Single 显得不是那么公平。



> 作者认为是因为Single Beamforming使用了Randomization，使结果偏离了最优解（除非无线大的集合里面取最优解）；而Mutiple Beamforming解出来的就是比较精确的解（特征值和特征向量）。
