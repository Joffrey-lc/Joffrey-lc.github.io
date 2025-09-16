---
title: Efficient Beamforming and Radiation Pattern Control Using Stacked Intelligent Metasurfaces
excerpt: Efficient Beamforming and Radiation Pattern Control Using Stacked Intelligent Metasurfaces. Naveed Ul Hassan et.al. 
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202402292123918.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Stacked Intelligent Metasurfaces
  - RIS
categories:
  - Paper Reading 
  - Stacked Intelligent Metasurfaces
comment: valine
math: true
hide: false
date: 2024-02-29 21:23:11
---

Date: 2024.02.26  14:14
Author: Joffrey LC

-------------------------------------

**Efficient Beamforming and Radiation Pattern Control Using Stacked Intelligent Metasurfaces**.  *Naveed Ul Hassan* et.al.  **IEEE Open Journal of the Communications Society, 2024**  ([pdf](https://ieeexplore.ieee.org/document/10379500))  (Citations **0**)

## Quick Overview

- continuous phase shift: gradient ascent algorithm
- discrete phase shift: AO-based algorithm



The contribution of this paper:

- a general path-loss model for SIM-assisted wireless communication systems.
- continuous and discrete phase shift model

惠更斯原理：

> **在波的传播过程中，波阵面上的每一点都可看作是发射子波的波源，在其后的任意时刻，这些子波的包迹就成为新的波阵面.**

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202402292123844.png" alt="image-20240229211756911" style="zoom:33%;" />



一个奇怪的现象是，随着SIM层数的增多，连续相移下，性能反而变差？离散值情况下没有出现减小的问题。作者留作future work了。



![image-20240229211611623](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202402292123918.png)

## Channel model/Path-loss model

channel model: 

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202402292123235.png" alt="image-20240229211643668" style="zoom:33%;" />

pathloss model: 

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202402292123233.png" alt="image-20240229211701615" style="zoom:33%;" />



## Solution 

gradient-based algorithm: 梯度下降法



AO-based algorithm: 固定一个原子进行迭代（离散才行，连续计算量太大了）



## Simulation

### continuous

![image-20240229212059779](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202402292123746.png)

### discrete

![image-20240229212112327](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202402292123795.png)
