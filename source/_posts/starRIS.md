---
title: STAR-RISs--Simultaneous Transmitting and Reflecting Reconfigurable Intelligent Surfaces
excerpt: Jiaqi Xu et.al. IEEE Communications Letters
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181654450.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - STAR RIS
  - RIS
categories:
  - Paper Reading
  - Simultaneous Transmitting and Reflecting RIS
comment: valine
math: true
hide: false
date: 2024-03-18 14:37:23
---

Date: 2024.03.18  10:50
Author: Joffrey LC

-------------------------------------

**STAR-RISs: Simultaneous Transmitting and Reflecting Reconfigurable Intelligent Surfaces**.  *Jiaqi Xu* et.al.  **IEEE Communications Letters, September 2021**  ([pdf](https://ieeexplore.ieee.org/document/9437234))  (Citations **171**)

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181654450.png" alt="image-20240318165416386" style="zoom:33%;" />

## Quick Overview

- Full diversity order can be achieved on both sides. 
- Far field and near field model

- ==The boundary between the near-field and the far-field is $$2L_a^2/\lambda$$，where$$L_a$$ is the largest dimension of the RIS aperture.==

## Far field 

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181437233.png" alt="image-20240318111855531" style="zoom: 33%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181437254.png" alt="image-20240318112135611" style="zoom:33%;" />

- 反射和透射的RIS相移可 independently adjusted
- 反射和透射有个功率分配，因为是passive，所以应该满足能量守恒

## Near field

根据Fresnel-Kirchhoff diffraction formula，应该建模为$$M$$个单元的求和：
$$
g^\chi=\frac{1}{j \lambda} \iint_{(\Sigma)} U^\chi(Q) F\left(\theta^\chi\right) \frac{e^{2 j \pi d_m^\chi / \lambda}}{d^\chi} d \Sigma
$$
<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181437329.png" alt="image-20240318112839450" style="zoom:33%;" />
$$
g^\chi=\frac{A_e}{j \lambda} \sum_m \Phi_m^\chi h_m F\left(\theta_m^\chi\right) \frac{e^{2 j \pi d_m^\chi / \lambda}}{d_m^\chi}
$$
<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181437439.png" alt="image-20240318112929059" style="zoom:33%;" />
$$
\left|g^\chi\right|=\frac{A_e}{\lambda}\left|\sum_m \Phi_m^\chi h_m\left(1+\cos \theta_m^\chi\right) \frac{e^{2 j \pi d_m^\chi / \lambda}}{2 d_m^\chi}\right| .
$$
<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181437353.png" alt="image-20240318113444192" style="zoom:33%;" />

## Diversity Analysis

All elements of STAR-RIS share the same power ratio, i.e., $$\beta^T_m=\beta^T,\beta^R_m=\beta^R,\forall m\in M$$.

In fact, we can include the power ratios constrains of each element for further improving the performance.

定义diversity order：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181437461.png" alt="image-20240318143353876" style="zoom:33%;" />



红色是考虑leaning factor/rate，而蓝色是没有使用leaning rate$$F(\theta)=1$$的

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181437432.png" alt="image-20240318143525743" style="zoom:33%;" />
