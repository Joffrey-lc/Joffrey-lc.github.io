---
title: CSI_FREE 衰落对能量信号有益-发射分集
excerpt: Bruno Clerckx et.al-On the Beneficial Roles of Fading and Transmit Diversity in Wireless Power Transfer With Nonlinear Energy Harvesting
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220324180546189.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - CSI Free
  - WET
  - WPT
categories:
  - Paper Reading
  - Simultaneous Wireless Information and Power Transfer
comment: valine
math: true
hide: false
date: 2022-03-20 21:59:14
---

**On the Beneficial Roles of Fading and Transmit Diversity in Wireless Power Transfer With Nonlinear Energy Harvesting**.  *Bruno Clerckx* et.al.  **IEEE Transactions on Wireless Communications, Nov.  2018**  ([pdf](https://ieeexplore.ieee.org/document/8470248))  (Citations **40**)

只整理了**基础部分**：

- [x] 基础部分
- [ ] **proposed + Energy Waveform**
- [ ] **proposed + Energy Modulation**
- [ ] 不同结构的能量采集器是否都从proposed方法中受益
- [ ] 物理样机的实现

## 缩写说明

- CSIT：Channel State Information at the Transmitter

## Quick Overview

与直觉相反，fading、multiple antennas、diversity都对能量收集有益。**而且不需要信道信息CSI-FREE**。

- 证明了在能量信号捕获中（Energy Harvesting），**衰落（fading）对能量捕获是有益的**（由于EF-DC采集器的非线性特点）
- 提出一种**发射端分集**的方法，可以有效增强接收端的能量捕获（这个分集的作用是**改变信道特性**，所以对于多用户而言，收益很大，因为大量的用户都可以**直接**从这个信道特性中受益，而不需要额外的优化），还可以直接结合两种考虑非线性的算法，即设计能量波形（Energy Waveform）和设计能量调制（Energy Modulation）

- 在两种能量采集器结构中验证了提出算法的可行性和有效性，证明不是因为潜在的能量采集器特性造成的结果。并且进行样机实现

## 背景

以前能量收集性能提升的研究在于设计一个高效的整流器。之后，近几年出现了三个种类的研究方向：

- 设计能量波束赋形（Energy Beamforming），需要知道CSIT。
- 设计能量波形（Energy Waveform），有CSIT和无CSIT都可以设计。利用**能量采集器的非线性**。
- 设计能量调制（Energy Modulation），也是利用**采集器的非线性**。

## 主要内容

### Fading正向作用的证明

未调制的单频信号可以建模为：
$$
x(t)=\sqrt{2P}\cos(w_0t)=\sqrt{2P}\mathscr{R}\{e^{jw_0t}\}
$$
其中$$\mathscr{R}\{\cdot\}$$是取实部，且$$\mathbb{E}[x(t)^2]=P$$即信号的功率为$$P$$。接收机收到的信号表示为：
$$
y(t)=\sqrt{2P}\mathscr{R}\{\Lambda^{-1/2}he^{jw_0t}\}
$$
其中$$\Lambda$$是路径损耗，$$h$$是复衰落稀疏（由于变化很慢，可以省略时间相关性）

对二极管采集器电路建模，进行泰勒展开，因为其非线性特点体现在**四阶以及更高阶**，所以取**四阶**。（如果取到二阶，那么是线性的）

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20220320210336493.png" alt="天线等效电路和二极管整流器（包括非线性器件-二极管和低通滤波器）" style="zoom:67%;" />

则有eq(5):
$$
i_{out}\approx k_0'+k_2'R_{ant}\mathbb{E}[y(t)^2]+k_4'R^2_{ant}\mathbb{E}[y(t)^4]
$$

- 假设$$|h|^2=1$$，可以得到整流天线模型

$$
z_{dc,cw}=k_2R_{ant}\bar{P}_{rf}+\frac{3}{2}k_4R_{ant}\bar{P_{rf}^2}
$$

- 假设$$h\sim\mathcal{NC}(0, \sigma^2)$$，且$$\mathbb{E}[|h^2|]=1$$，$$\mathbb{E}[|h^4|]=2$$，则有：

$$
\begin{aligned}
\bar{z}_{dc,cw}&=\mathbb{E}_h[z_{dc,cw}]\\
&=k_2R_{ant}\bar{P}_{rf}\mathbb{E}[|h|^2]+\frac{3}{2}k_4R_{ant}^2\bar{P}^2_{rf}\mathbb{E}[|h|^4]\\
&=k_2R_{ant}\bar{P}_{rf}+3k_4R^2_{ant}\bar{P}^2_{rf}
\end{aligned}
$$

观察可以看到，二阶项没有变化，四阶项double了。所以fading对能量采集器的输入功率是有帮助的。

**但是这种快衰信道的信道容量不如AWGN，是否意味着对WPT有益，但对WIT有害？**

### Transmit Diversity的正向作用

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20220320212227078.png" alt="分集发射的一般结构" style="zoom:67%;" />

- 分集：[分集是接收端对它收到的衰落特性相互独立地进行特定处理，以降低信号电平起伏的办法。分集是指分散传输和集中接收。所谓分散传输是使接收端能获得多个统计独立的、携带同一信息的衰落信号。集中接收是接收机把收到的多个统计独立的衰落信号进行合并(选择与组合)以降低衰落的影响。]([https://baike.baidu.com/item/%E5%88%86%E9%9B%86%E6%8A%80%E6%9C%AF/2550274?fr=aladdin](https://baike.baidu.com/item/分集技术/2550274?fr=aladdin))

在保持总功率为$$P$$的前提下，可以得到每个天线的功率为$$P/M$$，发射分集的理论是在每个发射天线上添加一个时变的相位$$\psi_m(t)$$，所以第$$m$$个天线的发射信号变为：
$$
\begin{aligned}
x_m(t)&=\sqrt{\frac{2P}{M}}\cos(w_0t+\psi_m(t))\\
&=\sqrt{\frac{2P}{M}}\mathscr{R}\{e^{j(w_0t+\psi_m(t))}\}
\end{aligned}
$$
接收机信号变为：
$$
y(t)=\sqrt{\frac{2P}{M}}\mathscr\{\Lambda^{-1/2}h(t)e^{jw_0t}\}
$$
其中：
$$
h(t)=\sum\limits_{m=1}^Mh_me^{j\psi_m(t)}
$$
其中，接收天线的路径损耗和衰落为$$\Lambda ^{-1/2}h_m$$。

**可以理解为分集在$h$上乘了一个系数，等于创造了一个快衰信道？？**

### Multiple Antennas的正向作用

继续上面的公式，假设$$h_m=1\forall m$$，且$$\{\psi_m(t)\}_{\forall m}\sim U(0,2\pi)$$，则有：
$$
\begin{aligned}
\bar{z}_{dc,td-cw}&=k_2R_{ant}\bar{P}_{rf}\frac{\mathbb{E}[|h|^2]}{M}+\frac{3}{2}k_4R_{ant}^2\bar{P}^2_{rf}\frac{\mathbb{E}[|h|^4]}{M^2}\\
&=k_2R_{ant}\bar{P}_{rf}+\frac{3}{2}k_4R^2_{ant}\bar{P}^2_{rf}(1+\frac{M-1}{M})
\end{aligned}
$$
等于天线数目$$M$$也对能量采集器输入功率有提升，令$$G_{td}=(1+\frac{M-1}{M})$$，则有如下曲线：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20220320214305022.png" alt="随天线数目增益" style="zoom:67%;" />



小结一下**基础部分**：

- 这种发射多天线分集的方式，其实改变的是信道，所以无论有多少用户，都可以直接从中受益。并且是完全不需要信道信息的，即**CSI-FREE**。
- 二阶建模，只能用EB增强，因为没有涉及能量采集器的非线性；而四阶建模可以使用之前提到的三种+文章proposed+文章proposed和三种中的后两种结合。
- 文章proposed的方法可以和设计能量波形和设计能量调制完美结合并且能量采集器能够从中收到更大的增益。详细见文章第**Ⅴ**节。



## Future Work

- WIT和WPT的分集是否可以结合？
- 其他传输的分集方法是否对WPT有益？
