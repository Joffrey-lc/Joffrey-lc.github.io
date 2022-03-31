---
title: CSI-FREE 统计分析CSI-FREE能量传输结构
excerpt: Onel L. A. López-Statistical Analysis of Multiple Antenna Strategies for Wireless Energy Transfer
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220324170240238.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - WET
  - WPT
  - CSI Free
categories:
  - Paper Reading
  - Simultaneous Wireless 
comment: valine
math: true
hide: false
date: 2022-03-24 17:58:34
---

**Statistical Analysis of Multiple Antenna Strategies for Wireless Energy Transfer**.  *Onel L. A. López* et.al.  **IEEE Transactions on Communications, Oct.  2019**  ([pdf](https://ieeexplore.ieee.org/document/8760520))  (Citations **16**)

## 缩写说明

- PB: Power Beacon

## Quick Overview

- 三种CSI-free方案和两种CSI-Based方案在不同条件下的性能对比
- 各种意义上的建模和数学推导（**太难了，看不懂啊**）

## 具体内容

系统模型：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220324170240238.png" alt="PB多天线ER单天线系统结构" style="zoom: 120%;" />

### CSI-Free Strategies

一般接收端接收信号建模为：
$$
\begin{aligned}
\xi^{rf}_j=\varrho_j|\textbf{h}_j^T\sum\limits^l_{k=1}\textbf{w}_kx_k|^2=\varrho_j\sum\limits_{k=1}^l|\textbf{h}_j^T\textbf{w}_k|^2
\end{aligned}
$$
其中$$\varrho_j$$是发射机到接收机的路径损耗$$\times$$总功率，$$\textbf{w}_k$$是发射机波束形成（precoding vector， 预编码向量）。

由于考虑二极管电路的特点，最终收到的能量$$\xi_j$$与接收机输入的能量$$\xi_j^{rf}$$之间的关系如下：

![最终能量额接收机输入能量的非线性关系式](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220324173153144.png)

其中$$\bar{w}_1$$代表接收门限；$$\bar{w}_2$$代表二极管的击穿电压，在未击穿的时候是线性的；击穿后是恒定的；$$\eta$$是能量效率。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220324173429153.png" alt="非线性关系式图解" style="zoom: 33%;" />



#### Only Antenna, OA

只有$$M$$根天线中的一根天线全功率输出。
$$
\begin{aligned}
\xi_{jOA}=g(\varrho_j|h_i,j|^2)
\end{aligned}
$$
其中$$\textbf{w}$$只有一个元素是1，其余全为0。

#### All Antenna at Once, AA

 一次性所有$$M$$根天线共同输出，总功率不变（每根天线的功率变为OA的1/M）,$$\textbf{w}=(1/\sqrt{M})\textbf{1}_{M\times1}$$：
$$
\begin{aligned}
\xi_{jAA}=g(\frac{\varrho_j}{M}|\sum\limits_{i=1}^Mh_{i,j}|^2)
\end{aligned}
$$
在$$M$$根天线中选择$$K$$个天线是一种普遍情况，这种普遍情况的性能应该介于OA和AA之间。

#### Switching Antennas, SA

 一次一根天线，分$$M$$个时间块，每根天线持续1个时间块：
$$
\begin{aligned}
\xi_{jSA}=\frac{1}{M}\sum\limits_{i=1}^Mg(\varrho_j|h_{i,j}|^2)
\end{aligned}
$$
其中$$\textbf{w}$$在每个时间块与OA相同，但是不同时间块选择不同的天线。等于OA的时变版本。

### CSI-Based

#### OA-CSI

对应于OA，在已知CSI的条件下，从整个集合中选择提供最大**总收获能量**的天线：
$$
\sum\limits_{j=1}^{|\mathcal{S}|}\xi_{jOA-CSI}=\max\limits_{i=1,\cdots,M}\sum\limits_{j=1}^{|\mathcal{S}|}g(\varrho_j|h_{i,j}|^2)
$$
其$$w$$和OA的类似，只有一个为1，其余全0。



#### AA-CSI

对应于AA，在一直CSI的条件下，不是在每个天线上以相同的功率进行发送，而是在发送之前通过$$\textbf{w}_k$$对信道和EH硬件效应进行预补偿，使得在接收端处的总收获能量被最大化：
$$
\begin{aligned}
\sum\limits_{j=1}^{|\mathcal{S}|}\xi_{jAA-CSI}=\max\limits_{\textbf{w}_k}\sum\limits_{j=1}^{|\mathcal{S}|}g(\varrho_j\sum\limits_{k=1}^{M}|\textbf{h}_j^T\textbf{w}_k|^2)
\end{aligned}
$$
**与AA−CSI相比，OA−CSI方案对CSI缺陷的敏感度较低。这是因为OA-CSI仅依赖于通道的功率增益，而AA−CSI需要通道系数的完全表征、包络和相位。**

### 结论

- 在小能量要求的情况下，AA-CSI>OA-CSI>SA>AA>OA
- 在大能量要求的情况下，AA很好，甚至超过OA-CSI，同样AA-CSI最好
- 天线单元之间的空间相关性，在所有天线以相同功率同时发射时，有好处，否则性能会随着相关性增大而降低
- SA策略由最小能量方差，这是很好的。因为我们不仅要最大的均值，也要最小的方差。方差小意味着可预测性强（能够预估收到多少能量）
- 在NLOS情况下，SA效果很好，当LOS增大时，天线以相同功率同时发射（AA）效果更好
- 随着设备数量的增加，CSI-free性能接近CSI-based





