---
title: RIS channel-Correlated Rayleigh Channel and Channel Harden
excerpt: RIS更实际的NLoS信道
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202308271417281.jpeg
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - IRS
categories:
  - Paper Reading
  - Intelligent Reflecting Surface 
comment: valine
math: true
hide: false
date: 2023-08-27 14:17:51
---

-------------------------------------

**Rayleigh Fading Modeling and Channel Hardening for Reconfigurable Intelligent Surfaces**.  *Emil Björnson* et.al.  **IEEE Wireless Communications Letters, April 2021**  ([pdf](https://ieeexplore.ieee.org/document/9300189))  (Citations **184**)

## Quick Overview

作者认为i.i.d.的Rayleigh信道是不合理的，在RIS中应该建模为一个相关的Rayleigh。

- but the i.i.d. Rayleigh fading model can be observed in practice if a half-wavelength-spaced uniform

  linear array (ULA) is deployed in an isotropic scattering environment.

- *Reproducible Research:* The simulation code is available at: https://github.com/emilbjornson/RIS-fading
- SISO模型

## Main content

作者认为信道模应该是：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202308271417251.png" alt="image-20230824210416741" style="zoom:33%;" />

其中$$\mathbf{R}\neq\mathbf{I}$$，而是等于：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202308271417406.png" alt="image-20230824210451110" style="zoom:33%;" />

==如果要实现上述的$$\mathbf{R}\neq\mathbf{I}$$，则需要满足所有单元之间间隔都是$$\lambda/2$$的整数倍，即对于线阵可以满足，但对于面阵无法满足（因为）对角为$$\sqrt{2}$$==:

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202308271417281.jpeg" alt="414e853b6c38c21859a5441a5cdb079" style="zoom:33%;" />

==这样是否就可行了？？？==





衡量信道相关性的一个方法是看$$\text{rank}(\mathbf{R})=N$$，且特征值都相同，则不相关（i.i.d.）:

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202308271417372.png" alt="image-20230824211639076" style="zoom:33%;" />





<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202308271417327.png" alt="image-20230824213235958" style="zoom:33%;" />

这张图的意思是，如果是i.i.d.，则特征值应该全是1（1600）个1，但是实际上，很多都不是1，特别是间距小于$$\lambda/2$$的时候，耦合增加，导致更具有相关性。

而$$\lambda/2$$时，后面有一些特征值为0；前面有一些大于0。说明还是具有相关性。





<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202308271417365.png" alt="image-20230824213620711" style="zoom:33%;" />

==这一点非常有趣，可以结合Null-space SWIPT作为下一个研究方向。==



有一种计算矩阵和矩阵之间关系的方法称为correlated matrix distance可以用来计算矩阵相似度（？？）



还讨论了RIS的信道硬化（还没来的及看）
