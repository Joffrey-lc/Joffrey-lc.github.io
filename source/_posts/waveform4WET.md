---
title: Three waveforms for WET-deterministic sine, M-QAM, Gaussian
excerpt: Intelligent Reflecting Surface Aided Wireless Power Transfer With a DC-Combining Based Energy Receiver and Practical Waveforms-Qingdong Yue et.al
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062131618.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - wave form design
categories:
  - Paper Reading
  - Wave form design
comment: valine
math: true
hide: false
date: 2024-05-06 21:30:38
---

Date: 2024.04.25  15:39
Author: Joffrey LC

-------------------------------------

**Intelligent Reflecting Surface Aided Wireless Power Transfer With a DC-Combining Based Energy Receiver and Practical Waveforms**.  *Qingdong Yue* et.al.  **IEEE Transactions on Vehicular Technology, September 2022**  ([pdf](https://ieeexplore.ieee.org/document/9795236))  (Citations **6**)

## Quick Overview

- Multiple antennas energy receiver
- Three classic waveforms: deterministic waveform, M-QAM waveform and Gaussian waveform are considered for WPT.

- Each antenna with a EH.

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130812.png" alt="image-20240425160712519" style="zoom:33%;" />

一般文章都是认为总的RF能量为每根天线上的和，然后再进行整理为直流功率。但是由于每根天线上的信号的相位不同，没法很好地直接合并。所以每根天线一个EH，再进行合并。

- Active beamforming and Passive phase shift 都是closed-from

- The numerical results demonstrate that the Gaussian waveform has the best energy performance with a low input RF power to the energy harvesters. By contrast, the deterministic waveform becomes superior with a high input RF power to the energy harvesters.



## System model

- single $$N_t>1$$ antennas transmitter
- single $$N_r>1$$ antennas receiver
- single $$K>1$$​ elements IRS



- Tx and ER are both ULA, while IRS is UPA



- Tx-ER is Rayleigh fading



考虑三种波形：

- deterministic sinusoidal wave form
- M-QAM waveform
- Gaussian waveform

## Three kinds of waveforms

### the non-linear energy harvesting function

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130877.png" alt="image-20240506205841898" style="zoom:33%;" />

### deterministic sinusoidal wave form

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130816.png" alt="image-20240506162208427" style="zoom:33%;" />

the objective is formulated as 

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130760.png" alt="image-20240506162929658" style="zoom:33%;" />

进行一阶泰勒展式：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130756.png" alt="image-20240506163807634" style="zoom:33%;" />

得到结果，即最大化入射能量即可，因为后面$$N_rp_0$$是常数。



通过AO的方案进行：

- 固定$$\mathbf{\Phi}$$，优化$$\mathbf{f}$$，最优的$$\mathbf{f}$$是对齐级联信道的最大特征向量，

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130772.png" alt="image-20240506164914271" style="zoom:33%;" />

- 固定$$\mathbf{f}$$，优化$$\mathbf{\Phi}$$，通过 minorize-maximization (MM) technique进行，MM算法的核心是找到一个==替代函数==，对替代函数进行求解

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130201.png" alt="image-20240506203947834" style="zoom:33%;" />

这个替代函数的由来应该是直接打开
$$
\left\|\left(\mathbf{H}_d+\mathbf{G} \boldsymbol{\Phi}_c \mathbf{H}_r\right) \mathbf{f}\right\|_2^2
$$
并且丢掉和$$\operatorname{vec}\left(\boldsymbol{\Phi}_c\right)$$无关的项。

然后通过拉格朗日乘子法，求解对偶问题

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130305.png" alt="image-20240506204417595" style="zoom:33%;" />

然后写出对偶问题：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130303.png" alt="image-20240506204503576" style="zoom:33%;" />

以及KKT条件：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130383.png" alt="image-20240506204520454" style="zoom:33%;" />

最后得到闭式解。

### M-QAM waveform

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130438.png" alt="image-20240506162233766" style="zoom:33%;" />

乘了==功率==和==概率==

求解过程和deterministic sinusoidal wave form 类似，因为

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130751.png" alt="image-20240506205607935" style="zoom:33%;" />

### Gaussian waveform

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130838.png" alt="image-20240506162310295" style="zoom:33%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130909.png" alt="image-20240506162321040" style="zoom:33%;" />

用PDF（概率）积分算

一系列操作之后也和上面的类似





## WITH THE SAME MAXIMUM TRANSMIT POWER CONSTRAINT

### deterministic sinusoidal wave form

因为确定正弦波的功率是常数，所以可以直接乘系数搞定



### M-QAM waveform

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130038.png" alt="image-20240506211128308" style="zoom:33%;" />

也是乘常数搞定





### Gaussian waveform

也差不多





## Numerical results

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130001.png" alt="image-20240506211625184" style="zoom:33%;" />

- 4QAM和sine波相同，因为都有相同的包络
- 16QAM和Gaussian在低功率区间性能好，因为偶尔的高功率使得非线性EH被激活，并以高RF-DC效率运行
- 而高功率时，确定性波形一直都在高效率运行，而非确定性波形还可能在低效率区域运行



<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130046.png" alt="image-20240506212043729" style="zoom:33%;" />

- 考虑最大发射功率限制的时候，由于高阶调制会有很多低功率符号，所以WET性能差。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405062130116.png" alt="image-20240506212324470" style="zoom:33%;" />

类似于DC combiner and RF combiner

- 如果只有一个EH，在低功率区，多个RF的和输入EH，可能会使得EH工作在高效率区间。然而可能会使得在高功率情况下工作在饱和区

