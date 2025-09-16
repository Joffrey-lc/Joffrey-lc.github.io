---
title: Stacked Intelligent Metasurfaces for MIMO system.
excerpt: Stacked Intelligent Metasurfaces for Multiuser Beamforming in the Wave Domain.  Jiancheng An et.al. 
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202402272135243.png
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
date: 2024-02-27 21:33:08
---

Date: 2024.02.26  14:13
Author: Joffrey LC

-------------------------------------

**Stacked Intelligent Metasurfaces for Multiuser Beamforming in the Wave Domain**.  *Jiancheng An* et.al.  **ICC 2023 - IEEE International Conference on Communications, 28 May 2023**  ([pdf](https://ieeexplore.ieee.org/document/10279173))  (Citations **4**)

## Quick Overview

- 通过Stacked Intelligent Metasurfaces在BS端进行MISO设计
- 同时服务多个Users



<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202402272135243.png" alt="image-20240227213529211" style="zoom:33%;" />

## Channel Model

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202402272133945.png" alt="image-20240227212903847" style="zoom:33%;" />

## Signal model

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202402272133291.png" alt="image-20240227212919255" style="zoom:33%;" />

and <img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202402272133292.png" alt="image-20240227212929990" style="zoom:33%;" />

其实和传统的RIS类似。



## 求解

为了最大化加权和通信速率，要对每个用户分配的功率以及Stacked Intelligent Metasurfaces相移进行设计。

- 通过注水算法对发射功率进行求解
- 通过梯度下降对每个Metasurface的相移进行求解
- 通过AO对二者进行交替优化



<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202402272133297.png" alt="image-20240227213223105" style="zoom:33%;" />

