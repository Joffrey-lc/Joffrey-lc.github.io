---
title: IRS综述阅读(一)
excerpt: IRS综述文章整理
index_img: https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220307223950922.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - IRS
categories:
  - Paper Reading
  - Intelligent Reflecting Surface
comment: valine
math: true
hide: false
date: 2022-03-07 14:55:43
---

# 介绍

*Intelligent Reflecting Surface-Aided Wireless Communications: A Tutorial*文章的整理。

- [x] IRS基础部分及建模
- [ ] IRS优化
- [ ] IRS信道估计
- [ ] IRS部署
- [ ] 拓展

## IRS介绍

**IRS**: Intelligent reflecting surface

### 背景

- 6G存在的需求，例如超高数据速率和能源效率，极高的可靠性和低延迟等
- 解决来自用户的时变无线信道

### 什么是IRS

Generally speaking, IRS is a planar surface comprising a large number of **passive reflecting elements**, each of which is able to induce a controllable amplitude and/or phase change to the incident signal independently

- IRS elements 是**无源的**（虽然后面会讲到还是需要一定的能源（用来调整幅度反射和相位反射），但是相比其他设备，这些能源是微乎其微的，还是可以认为是无源的）

### IRS作用及优势

**从概念上：**

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220307143040521.png" alt="IRS在无线信道重配置中额主要功能" style="zoom: 33%;" />

- (a): 创建虚拟视距(LoS)链接以通过智能反射面绕过收发器之间的障碍物
- (b): 在期望的方向添加额外的信号路径以提升信道等级条件
- (c): 改善信道分布，例如将瑞利/快衰落转换为Rician/慢衰落以实现超高可靠性
- (d): 抑制一些干扰

**在实施上**

- 因为是无缘的（仅被动反射信号），所以不需要任何发射射频反射链，硬件要求低（与传统有源中继相比）。
- 全双工工作模式，没有任何天线噪声放大和自干扰。
- 安装拆除简单
- 极大的灵活性和与现有无线系统的兼容性

## IRS挑战

- 无源反射原件需要适当设计，实现IRS element之间的协同信号聚焦或干扰消除。考虑与基站、用户的传输联合设计。
- 由于IRS没有发射射频链，所以要考虑如何获得IRS与其用户之间的信道状态信息。
- IRS在无线网络中最大化网络容量的最佳部署策略需要重新设计。

## IRS建模

以$x(t)$表示等效复值基带发射信号，对于一个有$N$个反射单元的IRS，以$n$代表单元，即$n\in\{1, \cdots, N\}$，用$\alpha_{1, n}e^{-j\xi_{1, n}}$表示基带信号从发射机到IRS的反射单元$n$的复信道系数，其中$\alpha_{1, n}$表示幅度衰减（amplitude attenuation），$e^{-j\xi_{1,n}}$表示窄带系统平坦信道的相移。所以其带通信号（经过上变频）可以表示为：
$$
\begin{align}
y_{in,n}(t)=Re\{\alpha_{1, n}e^{-j\xi_{1, n}}x(t)e^{j2\pi f_ct}\}$
\end{align}
$$
其中，$f_c$是载波频率；该单元（第$n$个单元）的幅度衰减和时间延迟分别用$\beta_n\in[0, 1]$（因为是无源的）和$t_n\in[0, 1/f_c]$表示。忽略电路非线性和相位噪声等硬件缺陷，IRS单元$n$的反射信号表示为：
$$
\begin{align}
y_{out,n}(t)&=\beta_ny_{in,n}(t-t_n)\\
&=Re\{\beta_n\alpha_{1,n}e^{-j\xi_{1,n}}x(t-t_n)e^{j2\pi f_c(t-t_n)}\}
\\&\approx Re\{[\beta_ne^{-j\theta^{'}_n}\alpha_{1,n}e^{-j\xi_{1,n}}x(t)]e^{j2\pi f_ct}\}
\end{align}
$$
其中，在$t_n\leq1/f_c\ll1/B$的前提下，假设$x(t-t_n)\approx x(t)$；并有$-\theta_n^{'}\triangleq-2\pi f_ct_n\in[-2\pi,0]$是单元$n$引起的相移。由$s_{in,n}(t)\triangleq \alpha_{1, n}e^{-j\xi_{1, n}}x(t)$并且有$s_{out,n}\triangleq\beta_ne^{-j\theta^{'}_n}\alpha_{1,n}e^{-j\xi_{1,n}}x(t)$

进一步，由于$\theta^{'}_n$是以$2\pi$为周期的，所以为方便后续部分，取$\theta_n\in [0,2\pi]$，有：
$$
\begin{align}
s_{out,n}(t)=\beta_ne^{-j\theta^{'}_n}s_{in,n}(t)=\beta_ne^{j\theta_n}s_{in,n}(t)
\end{align}
$$
**所以在基带信号模型中，IRS单元$n$的输出/反射信号是通过将相应的输入/入射信号乘以复反射系数$\beta_ne^{-j\theta_n}$得到的**。

再接上从IRS单元$n$到接收端的信号（与前面相似的等效窄带平坦频率信道），则有接收端的表达式：
$$
\begin{align}
y_{r,n}(t)=Re\{[\alpha_{1,n}e^{-j\xi_{1,n}}\beta_ne^{j\theta_n}\alpha_{2,n}e^{-j\xi_{2,n}}x(t)]e^{j2\pi f_ct}\}
\end{align}
$$
用$h^*_{r,n}\triangleq\alpha_{1,n}e^{-j\xi_{1,n}}$（发射端到IRS的信道），并用$g_n\triangleq\alpha_{2,n}e^{-j\xi_{2,n}}$（IRS到接收端的信道），上式变为：
$$
y_n(t)=\beta_ne^{j\theta_n}h^*_{r,n}g_nx(t)
$$
<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/3328208a299ddde470516df2ab995f6.jpg" alt="IRS模型示意图" style="zoom:33%;" />

假设没有信号耦合，即所有IRS单元独立地反射入射信号。并忽略多次反射（因为路径损失较大），则有考虑$N$个单元时，有接收端：
$$
\begin{align}
y(t)=(\sum_{n=1}^N\beta_ne^{j\theta_n}h^*_{r,n}g_n)x(t)=\textbf{h}_r^H\Theta\textbf{g}x(t)
\end{align}
$$
其中$\textbf{h}_r^H=[h^*_{r, 1},\cdots,h^*_{r,N}]$，$\textbf{g}=[g_1,\cdots,g_N]^T$，$\Theta=diag(\beta_1e^{j\theta_1},\cdots,\beta_Ne^{j\theta_N})$因为每个IRS单元独立地反射信号，且没有信号耦合，所以$\Theta$是对角阵。

## IRS硬件实现

### 硬件结构

由于发射机、接收机以及周围物体的移动性，信道通常是时变的，因此需要基于信道变化的IRS实时可调。所以需要联网以进行自适应反射。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220307220020933.png" alt="IRS结构" style="zoom:33%;" />

- 智能控制器，FPGA，总的控制端

- 第一层，调整层，控制层，也可以布置一些传感器（感知周围感兴趣的无线电信号，以方便智能控制器设计反射系数）
- 第二层，铜，减少信号能量损失
- 第三层，可调整的单元

为了实现重新配置IRS单元以实现高度可控反射，有三种主要方法被提出：

- 机械驱动（机械旋转、平移）
- 功能材料（液晶、石墨烯等）
- 电子设备（PIN二极管等）

第三种电子设备（PIN二极管等）是最常用的。

### 实际限制

#### 离散的反射幅度和相移

用固定的PIN二极管，需要大数量才能控制精细相移，例如$\log_28=3$，即8级相移需要3个PIN二极管；使用变容二极管则需要更大范围的偏置电压，成本更高。

顺便提出了两个特殊结构：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220307221743796.png" alt="两种特殊结构" style="zoom: 67%;" />

#### 耦合的反射幅度和相移

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220307221921769.png" alt="实际IRS中反射幅度和相移之间的关系" style="zoom:50%;" />

有人提出反射的幅度和相移之间存在非线性耦合，所以不能单独调节。

产生这种现象的原因是因为：**0相移时**，反射电流与单元电流同相（in-phase），电流强度增加，导致**发热增多**，**反射幅度下降**；当**电流反相**时（out-of-phase），电流强度**减弱**，**发热变少**，**反射幅度增加**。



此外，IRS理论上是无源的（passive），但是例如控制PIN二极管时，需要消耗一部分能量。只是说这部分能量相对较小。



### 其他相关内容及未来研究方向

- **IRS单元之间的耦合**目前是被忽略的。考虑在增大IRS单元密度以提高性能时，可能会使耦合更严重，以至于不能忽略。**考虑耦合反射系数**或者**开发有效的去耦、隔离技术**。
- 目前考虑的模型对信号的**入射角不敏感**。目前的部分实现证明IRS反射系数，特别是相移，对**入射角非常敏感**。同时这也意味着**信道互易假设可能不再有效**，即上行链路的信道估计不再适用于下行链路的信道估计，vice versa。
- 对于**宽带信号**的建模以及**频率/时间偏移**、**相位噪声**等。







