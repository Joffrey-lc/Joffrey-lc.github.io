---
title: IRS综述阅读（一）
excerpt: 武庆庆-Intelligent Reflecting Surface-Aided Wireless Communications-A Tutorial
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

**Intelligent Reflecting Surface-Aided Wireless Communications: A Tutorial**.  *Qingqing Wu* et.al.  **IEEE Transactions on Communications, May  2021**  ([pdf](https://ieeexplore.ieee.org/document/9326394))  (Citations **210**)

## Quick Overview

*Intelligent Reflflecting Surface-Aided Wireless Communications: A Tutorial*文章的整理。

{% cb IRS基础部分及建模, true, false%} 

{% cb IRS优化, true, false%} 

{% cb IRS信道估计, true, false%} 

{% cb IRS部署, true, false %} 

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

### IRS挑战

- 无源反射原件需要适当设计，实现IRS element之间的协同信号聚焦或干扰消除。考虑与基站、用户的传输联合设计。
- 由于IRS没有发射射频链，所以要考虑如何获得IRS与其用户之间的信道状态信息。
- IRS在无线网络中最大化网络容量的最佳部署策略需要重新设计。

### IRS建模

以$$x(t)$$表示等效复值基带发射信号，对于一个有$$N$$个反射单元的IRS，以$n$代表单元，即$$n\in\{1, \cdots, N\}$$，用$$\alpha_{1, n}e^{-j\xi_{1, n}}$$表示基带信号从发射机到IRS的反射单元$n$的复信道系数，其中$$\alpha_{1, n}$$表示幅度衰减（amplitude attenuation），$$e^{-j\xi_{1,n}}$$表示窄带系统平坦信道的相移。所以其带通信号（经过上变频）可以表示为：
$$
\begin{align}
y_{in,n}(t)=Re\{\alpha_{1, n}e^{-j\xi_{1, n}}x(t)e^{j2\pi f_ct}\}$
\end{align}
$$
其中，$$f_c$$是载波频率；该单元（第$$n$$个单元）的幅度衰减和时间延迟分别用$$\beta_n\in[0, 1]$$（因为是无源的）和$$t_n\in[0, 1/f_c]$$表示。忽略电路非线性和相位噪声等硬件缺陷，IRS单元$$n$$的反射信号表示为：
$$
\begin{align}
y_{out,n}(t)&=\beta_ny_{in,n}(t-t_n)\\
&=Re\{\beta_n\alpha_{1,n}e^{-j\xi_{1,n}}x(t-t_n)e^{j2\pi f_c(t-t_n)}\}
\\&\approx Re\{[\beta_ne^{-j\theta^{'}_n}\alpha_{1,n}e^{-j\xi_{1,n}}x(t)]e^{j2\pi f_ct}\}
\end{align}
$$
其中，在$$t_n\leq1/f_c\ll1/B$$的前提下，假设$$x(t-t_n)\approx x(t)$$；并有$$-\theta_n^{'}\triangleq-2\pi f_ct_n\in[-2\pi,0]$$是单元$$n$$引起的相移。由$$s_{in,n}(t)\triangleq \alpha_{1, n}e^{-j\xi_{1, n}}x(t)$并且有$s_{out,n}\triangleq\beta_ne^{-j\theta^{'}_n}\alpha_{1,n}e^{-j\xi_{1,n}}x(t)$$

进一步，由于$$\theta^{'}_n$$是以$$2\pi$$为周期的，所以为方便后续部分，取$$\theta_n\in [0,2\pi]$$，有：
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
用$$h^*_{r,n}\triangleq\alpha_{1,n}e^{-j\xi_{1,n}}$$（发射端到IRS的信道），并用$$g_n\triangleq\alpha_{2,n}e^{-j\xi_{2,n}}$$（IRS到接收端的信道），上式变为：
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
其中$$\textbf{h}_r^H=[h^*_{r, 1},\cdots,h^*_{r,N}]$$，$$\textbf{g}=[g_1,\cdots,g_N]^T$$，$$\Theta=diag(\beta_1e^{j\theta_1},\cdots,\beta_Ne^{j\theta_N})$$因为每个IRS单元独立地反射信号，且没有信号耦合，所以$\Theta$是对角阵。

### IRS硬件实现

#### 硬件结构

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

#### 实际限制

##### 离散的反射幅度和相移

用固定的PIN二极管，需要大数量才能控制精细相移，例如$\log_28=3$，即8级相移需要3个PIN二极管；使用变容二极管则需要更大范围的偏置电压，成本更高。

顺便提出了两个特殊结构：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220307221743796.png" alt="两种特殊结构" style="zoom: 67%;" />

##### 耦合的反射幅度和相移

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220307221921769.png" alt="实际IRS中反射幅度和相移之间的关系" style="zoom:50%;" />

有人提出反射的幅度和相移之间存在非线性耦合，所以不能单独调节。

产生这种现象的原因是因为：**0相移时**，反射电流与单元电流同相（in-phase），电流强度增加，导致**发热增多**，**反射幅度下降**；当**电流反相**时（out-of-phase），电流强度**减弱**，**发热变少**，**反射幅度增加**。



此外，IRS理论上是无源的（passive），但是例如控制PIN二极管时，需要消耗一部分能量。只是说这部分能量相对较小。

### 其他相关内容及未来研究方向

- **IRS单元之间的耦合**目前是被忽略的。考虑在增大IRS单元密度以提高性能时，可能会使耦合更严重，以至于不能忽略。**考虑耦合反射系数**或者**开发有效的去耦、隔离技术**。
- 目前考虑的模型对信号的**入射角不敏感**。目前的部分实现证明IRS反射系数，特别是相移，对**入射角非常敏感**。同时这也意味着**信道互易假设可能不再有效**，即上行链路的信道估计不再适用于下行链路的信道估计，vice versa。
- 对于**宽带信号**的建模以及**频率/时间偏移**、**相位噪声**等。

## System Model

### 有IRS的系统的接收信号

$$
y(t)=\left(\sum_{n=1}^{N} \beta_{n} e^{\jmath \theta_{n}} h_{r, n}^{*} g_{n}\right) x(t)=\boldsymbol{h}_{r}^{H} \boldsymbol{\Theta} \boldsymbol{g} x(t)
$$

其中
$$
\mathbb{E}\left(\left|h_{r, n}\right|^{2}\right) \propto c_{1}\left(\frac{d_{1}}{d_{0}}\right)^{-a_{1}}
$$

$$
\mathbb{E}\left(\left|g_n\right|^{2}\right) \propto c_{2}\left(\frac{d_{2}}{d_{0}}\right)^{-a_{2}}
$$

where *c*1(*c*2) denotes the corresponding path loss at the reference distance *d*0, while *a*1(*a*2) denotes the corresponding path loss exponent with typical values from 2 (in free-space propagation) to 6



意味着如果是free-space，path loss exponent 取2。

所以Average Received Power：
$$
P_{r, n} \propto \frac{1}{d_{1}^{a_{1}} d_{2}^{a_{2}}}
$$
称之为*product distance path loss model*，另外还有*sum-distance path loss model*，但是作者认为不是很适用。

### 调整幅度和相位

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220617154210815.png" alt="image-20220617154210815" style="zoom:33%;" />

不能单独调整幅度或相位，二者之间存在一定的耦合

## IRS反射优化

single-user single-input-single-output
$$
y=\left(\boldsymbol{h}_{r}^{H} \boldsymbol{\Theta} \boldsymbol{g}+h_{d}^{*}\right) \sqrt{P_{t}} x+z
$$
$P_t$ is the transmit power at the AP

所以信噪比SNR表示为:
$$
\begin{aligned}
\gamma &=\frac{P_{t}\left|\boldsymbol{h}_{r}^{H} \boldsymbol{\Theta} \boldsymbol{g}+h_{d}^{*}\right|^{2}}{\sigma^{2}} \\
&=\frac{P_{t}\left|\sum_{n=1}^{N} h_{r, n}^{*} \beta_{n} e^{\jmath \theta_{n}} g_{n}+h_{d}^{*}\right|^{2}}{\sigma^{2}}
\end{aligned}
$$
其achievable rate由$$\log_2(1+\gamma)$$给出。最大化achievable rate等效于最大化SNR，并且丢掉常数$$P_t$$和$$\sigma^2$$。
$$
\begin{aligned}
\max _{\boldsymbol{\theta}, \boldsymbol{\beta}} &\left|\sum_{n=1}^{N} h_{r, n}^{*} g_{n} \beta_{n} e^{\jmath \theta_{n}}+h_{d}^{*}\right|^{2} \\
\text { s.t. } 0 & \leq \theta_{n}<2 \pi, \quad n=1, \cdots, N \\
0 & \leq \beta_{n} \leq 1, \quad n=1, \cdots, N
\end{aligned}\label{eqn:1}
$$
由于最终的目的，希望信号在接收端同相叠加，（而不是相消），所以
$$
\theta_{n}^{\star}=\mod \left[\zeta-\left(\phi_{n}+\psi_{n}\right), 2 \pi\right], \quad n=1, \cdots, N
$$
就只剩下了模值：
$$
\begin{aligned}
&\max _{\boldsymbol{\beta}}\left|\sum_{n=1}^{N}|h_{r, n}|| g_{n}\left|\beta_{n}+\right| h_{d}|\right|^{2} \\
&\text { s.t. } 0 \leq \beta_{n} \leq 1, \quad n=1, \cdots, N .
\end{aligned}
$$
由复高斯和瑞利的关系，如果$$\textbf{h}_r^H$$和$$\textbf{g}$$服从CSCG，且功率为$$\varrho_h^2$$和$$\varrho_g^2$$，则接收端总功率：
$$
P_{r} \approx N^{2} \frac{P_{t} \pi^{2} \varrho_{h}^{2} \varrho_{g}^{2}}{16}
$$
<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20220619_1.jpg" alt="20220619_1" style="zoom:33%;" />

可以在不增加AP发射功率的前提下，增大$$N$$，就可以实现覆盖范围的增加。

```matlab
clc;clear;close all;
c0_dB = -30;
c0 = 10^(c0_dB/10);
Pt = 50e-3;
sigma_2_dBm = -90;
sigma_2 =  10^((sigma_2_dBm-30)/10);
d0= 50;
d2 = 5;
pathloss_free_space_los = c0*d0^(-2);
pathloss_free_space_los_2 = c0*d2^(-2);

pathloss_Rician = c0*d0^(-2.4);
pathloss_Rician_2 = c0*d2^(-2.4);

varrho_h_2 = c0*d0^(-2.8);
varrho_g_2 = c0*d2^(-2.8);

phi = 0;
SNR_free_space = [];
for N=20:1:500
    Phi = -(0:1:N-1)*pi*sin(phi);
    h_los = exp(1i.*Phi.');

    h_free_space_1 = sqrt(pathloss_free_space_los)*h_los;
    h_free_space_2 = sqrt(pathloss_free_space_los_2)*h_los;
    S_free = Pt*abs(abs(h_free_space_1).'*abs(h_free_space_2))^2;
    
    SNR_free_space = [SNR_free_space S_free/sigma_2];
end

kappa = 3;
SNR_all = zeros(1,481);
mtkl_a = 1000;
for mtkl=1:mtkl_a
    
    SNR_Rician = [];
    for N=20:1:500
        Phi = -(0:1:N-1)*pi*sin(phi);
        h_los = exp(1i.*Phi.');
        h_Rician_1 = sqrt(pathloss_Rician)*(sqrt(kappa/(kappa+1))*h_los+sqrt(1/(kappa+1))*sqrt(1/2)*(randn(N, 1)+1i*randn(N,1)));
        h_Rician_2 = sqrt(pathloss_Rician_2)*(sqrt(kappa/(kappa+1))*h_los+sqrt(1/(kappa+1))*sqrt(1/2)*(randn(N, 1)+1i*randn(N,1)));

        S_R = Pt*abs(abs(h_Rician_1).'*abs(h_Rician_2))^2;
        SNR_Rician = [SNR_Rician S_R/sigma_2]; 
    end
    SNR_all = SNR_all + SNR_Rician;
end
SNR_Rician = SNR_all/mtkl_a;
% 瑞利信道，就可以用文章中的结论Pr=N^2*Pt*pi^2*varrho_h^2*varrho_g^2/16
SNR_Rayleigh = [];
for N=20:1:500
    h = sqrt(varrho_h_2)*sqrt(1/2)*(randn(N, 1)+1i*randn(N,1));
    g = sqrt(varrho_g_2)*sqrt(1/2)*(randn(N, 1)+1i*randn(N,1));
    S_Ray = N^2*varrho_h_2*varrho_g_2*pi^2*Pt/16;
    S_Ray2 = Pt*abs(abs(h).'*abs(g))^2;
%     eta = S_Ray/S_Ray2
    SNR_Rayleigh = [SNR_Rayleigh S_Ray/sigma_2];
end


plot(20:1:500, log2(1+SNR_free_space))
hold on;
plot(20:1:500, log2(1+SNR_Rician))
hold on;
plot(20:1:500, log2(1+SNR_Rayleigh))
hold off;
grid on;
```

## MISO System

发射机多天线，downlink是MISO Uplink是SIMO。

则需要联合优化的问题是：
$$
\begin{aligned}
&\max _{\boldsymbol{w}, \boldsymbol{\theta}}\left|\left(\boldsymbol{h}_{r}^{H} \boldsymbol{\Theta} \boldsymbol{G}+\boldsymbol{h}_{d}^{H}\right) \boldsymbol{w}\right|^{2} \\
&\text { s.t. }\|\boldsymbol{w}\|^{2} \leq P_{t}, \\
&\quad 0 \leq \theta_{n}<2 \pi, \quad n=1, \cdots, N,
\end{aligned}
$$

### AO 求解 

这个问题是非凸的。可以通过固定其中一个参数：

- 固定参数$$\textbf{w}$$，和式$$\ref{eqn:1}$$是相同的
- 固定参数$$\theta$$，则最佳precoder可以由Maximum-ratio transmission （MRT）给出：

$$
\boldsymbol{w}_{\mathrm{MRT}}=\sqrt{P_{t}} \frac{\left(\boldsymbol{h}_{r}^{H} \Theta \boldsymbol{G}+\boldsymbol{h}_{d}^{H}\right)^{H}}{\left\|\boldsymbol{h}_{r}^{H} \Theta \boldsymbol{G}+\boldsymbol{h}_{d}^{H}\right\|}
$$

重复交替求解（Alternating Optimization）

### 直接带入$$\textbf{w}_{MRT}$$

直接带入$$\textbf{w}_{MRT}$$就可以得到一个只有参数$$\mathbf{\theta}$$的表达式：
$$
\begin{aligned}
&\max _{\boldsymbol{\theta}}\left\|\boldsymbol{h}_{r}^{H} \boldsymbol{\Theta} \boldsymbol{G}+\boldsymbol{h}_{d}^{H}\right\|^{2} \\
&\text { s.t. } 0 \leq \theta_{n} \leq 2 \pi, \quad n=1, \cdots, N .
\end{aligned}
$$
是NP-hard的。可以用一些例如

- 半松弛（SDR）+高斯随机化
- AO

等来求解

### AP-User距离影响

![image-20220619152753102](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220619152753102.png)

- AO：如4.1所示的AO求解
- AP-User MRT： $$\boldsymbol{w}=\sqrt{P_{t}} \frac{\boldsymbol{h}_{d}}{\left\|\boldsymbol{h}_{d}\right\|}$$，等于说是部分Beamforming，只对直射信道进行Beamforming。可以看到，当d比较小，AP-User距离近，这个Beamformer效果很好，但是随着距离增加，AP-IRS-User的作用更大，所以效果随着d增大而于AO产生了差距。
- AP-IRS MRT：$$\boldsymbol{w}=\sqrt{P_{t}} \frac{g}{\|\boldsymbol{g}\|}$$，和上面类似。当AP-User距离远，则等于AP-IRS进，AP-IRS信道贡献大，这个时候性能随着d增大逼近AO
- MRT without IRS： 只有AP-User MRT，没有IRS，所以性能一开始和AP-User MRT相似，然后随着d增大，性能变差。





### TODO...

## IRS Channel Estimation

现在有两种可以能的信道估计方案：

- Semi-Passive IRS
- Passive IRS

### Semi-Passive iRS

![semi-passive IRS](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220619153914505.png)

用一些有源element做信道估计。问题在于这些element（sensing device）的信道和reflecting element的信道其实不一样，但是有一定关联性。由这些有关联性的信道估计其他的信道也是一个研究点{% label success@压缩感知、机器学习等 %}

### Passive IRS

![Passive IRS](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220619154545950.png)

 估计级联信道。

## IRS Deployment

IRS需要部署接近AP or User以减小path-loss

### 在链路层级讨论IRS部署

#### Single IRS

只考虑AP-IRS-User路径：

![Single IRS](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220619155443385.png)

接收端的SNR可以表示为：
$$
\rho_{\mathrm{S}}=\frac{P \beta_{0}^{2} N^{2}}{\left(d^{2}+H^{2}\right)\left((D-d)^{2}+H^{2}\right) \sigma^{2}}
$$
<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220619160730564.png" alt="Proof" style="zoom:33%;" />

![image-20220620103728273](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220620103728273.png)

从结果看，IRS应该near user / near AP

#### Multiple Cooperative IRSs

![image-20220620104345370](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220620104345370.png)

一个IRS可以分为多个小尺寸的IRSs。IRS多，path-loss大，但是可以收到多IRS的被动波束形成增益。以如上图所示的placement，路径服从自由空间LoS，则接收端的SNR为：
$$
\rho_{\mathrm{D}}=\frac{P \beta_{0}^{3} N^{4}}{16 H^{4} D^{2} \sigma^{2}}
$$
所以当满足：
$$
N>\frac{4 H}{\sqrt{\beta_{0}}}
$$
时，这种Multiple cooperative IRSs效果更好。

### 在网络层级讨论IRS部署

分为两种：

- 分布式
- 集中式

分布式就是多个IRS参与工作，但是每个用户只能收到距离其最近的部分elements的反射。

集中式就是单个IRS，使AP的SNR最大化。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220620105955701.png" alt="cen vs dis" style="zoom:33%;" />

结论是集中式效果好，但是有时候分布式的布置更为灵活。

