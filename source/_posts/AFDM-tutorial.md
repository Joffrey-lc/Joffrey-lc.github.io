---
title: AFDM_tutorial
excerpt: Affine Frequency Diversity Multiplexing-HUAWEI讲座
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282132775.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - AFDM
categories:
  - Paper Reading
  - Affine Frequency Diversity Multiplexing
comment: valine
math: true
hide: false
date: 2024-10-28 21:31:16
---

Date: 2024.10.25  17:16
Author: Joffrey LC

---

**AFDM: A Full Diversity Next Generation Waveform for High Mobility Communications**.  *Ali Bemani* et.al.  **2021 IEEE International Conference on Communications Workshops (ICC Workshops), June 2021**  ([pdf](https://ieeexplore.ieee.org/document/9473655))  (Citations **26**)



The corresponding video can be found in [Bilibili](https://www.bilibili.com/video/BV1CkySYYE37/?spm_id_from=333.337.search-card.all.click&vd_source=4e18d3634d18ee20188cdddc5aa92d81).

## Quick Overview

AFDM: Affline Frequency Division Multiplexing

- chirp-based multicarrier transceiver 
- based on discrete affline Fourier transform (DAFT)
- Adjust the ==two parameters== to better cope with the doubly dispersive channels. And avoid the time domain channel paths with distinct delays or Doppler frequency shifts overlap in DAFT domain.
- Achieved full diversity of linear time-varying (LTV) channel. 



OFDM/single-carrier FDMA (SC-FDMA) achieved even optimal performance in ==time-invariant== frequency selective channels. 

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282135029.png" alt="image-20241028213541914" style="zoom:33%;" />



----

## AFDM for communication

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138536.png" alt="image-20241025160417663" style="zoom:33%;" />



![image-20241025160451941](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138518.png)

OFDM is designed for LTI channel, and we can use the orthogonal to modulate/demodulate

![image-20241025160637042](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138624.png)

![image-20241028113502486](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138595.png)

general AFT: 调整abcd以适用于各种变换

![image-20241025160833345](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138569.png)

discrete form：2 parameters and chirp periodic prefix (CPP) to avoid ISI like CP in OFDM

![image-20241025160924357](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138567.png)

相比于传统的OFDM 仅 IFFT 多了左右两个matrix, 主要特性来自于C1 matrix（frequency变化斜率）

CP-CPP

- OFDM子载波是固定频率
- AFDM子载波是chrip信号 线性调频

![image-20241025161134256](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138173.png)

信道模型：双色散信道， multiple paths, each of which has its own delay and Doppler shift

大频率间隔或者大持续时间下， 这两个现象可以被忽略（观察分母）

==时延和多普勒被分为整数部分和分数部分？？==

-  分数部分的delay处理起来比较困难，而且如上图所示有个取模的现象（增大到边界后下降到0再增加），这点很多文章都没注意。

![image-20241025161340753](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138288.png)



![image-20241025161450792](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138357.png)

只有整数时，如左侧图所示

而分数情况如右侧所示

![image-20241025161641074](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138338.png)

有了分数的Doppler shift之后，他们可能会重叠，如左侧图所示；或者如右图所示不重叠

==峰值的位置取决于C1==

![image-20241025161801275](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138344.png)

想要让整个delay-Doppler 表示能够有区分，需要满足以下公式：

- k_max denotes the maximal Doppler frequency shift, k_v is driven from the fractional Doppler shift.

![image-20241025161845785](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138701.png)



![image-20241025162056216](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138843.png)

AFDM with Zak transform

![image-20241025162143676](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138952.png)

AFDM with Zak transform

![image-20241025162226167](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138097.png)



![image-20241025162301680](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138574.png)

diversity

![image-20241025162444829](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138667.png)

diversity, rank=P (number of channel paths)

如果不满足2\*k_max+l_max+2\*k_max\*l_max的条件，会由于前面聊到的取模操作而产生重叠。

![image-20241025162453577](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138754.png)



![image-20241025162741157](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138096.png)

Only one pilot for AFDM channel estimation 

- P_GI depends on the max Doppler frequency shift and delay
- 可以把zeros位的功率全部给pilot，这样使得一个frame的功率不会发生变化
- for the channel estimation, we should only focus on the blue parts.

![image-20241025162828696](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138070.png)

整个公式都是聚焦于blue part， only one pilot symbol.

![image-20241025163022775](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138337.png)

同时，SNR也被称为overhead，因为如果我们想增大SNR，就意味着要给pilot增加更大的功率，就需要更多的guard（zeros）

![image-20241025163117675](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138409.png)

![image-20241028152311550](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138797.png)

Number of guard: AFDM需要更==少==的Guards，几乎是OTFS的一半

- 粉色和紫色是OTFS和AFDM的==共同的/重叠的==guard位
- 所有颜色的和是OTFS的guards
- 红色的等于是OTFS的额外开销（减小了channel capacity）

![image-20241025163211372](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138827.png)



![image-20241025163344000](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138278.png)

如果有稀疏性，C1的值就不需要取太大

- Situation a: We have a distribution of delay, and the Doppler shift is random. 多普勒random但是在不同delay中几乎都一样？？，
- Situation b: Everything is random.
- Situation c: Delay is random and we have the distribution of Doppler shift.每个谱图delay的多普勒几乎都一样？？？？

![image-20241025163432960](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138310.png)

How many pilot we need for the small C1

![image-20241025163730416](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138506.png)

得到最小的导频数量N_p

![image-20241025163943546](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138697.png)

----

## AFD M for ISAC



![image-20241025164128403](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138721.png)

P-target  and some self-interference

![image-20241028164653306](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138001.png)

用pilot处理，性能与处理整个信号相同

- chirp 的特性使得消除self-interference非常简单，before the ADC

![image-20241025164327745](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138053.png)

self-interference比回波大一个数量级，通过两个chirp分别dechirp扫描，去掉零频，就可以消除self-interference  like FMCW雷达

- 大C1增大处理复杂度



![image-20241025164440439](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138355.png)

DC-blocking for self-interference of full-duplex 

![image-20241025164738810](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138318.png)



![image-20241025164822896](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138435.png)

OTFS: full duplex SIC

AFDM: 1 RF chain

![image-20241025164956647](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138425.png)

Down-sampling for ADFM: generate another chirp signal, with length N/O, and ==C1== becomes to ==OC1==

![image-20241025165017363](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138479.png)

没有丢失分辨率

![image-20241028205843165](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138441.png)

![image-20241028210220090](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138586.png)

![image-20241025165649748](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138633.png)



![image-20241025165804482](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138697.png)

![image-20241028210424087](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202410282138609.png)



