---
title: STAR-RISs-- A Correlated T&R Phase-Shift Model and Practical Phase-Shift Configuration Strategies
excerpt: lossless, correlated phase shift model
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181651594.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - STAR RIS
  - RIS
categories:
  - Paper Reading
  - Simultaneous Transmitting and Reflecting 
comment: valine
math: true
hide: false
date: 2024-03-18 16:49:53
---

Date: 2024.03.12  16:26
Author: Joffrey LC

-------------------------------------

**STAR-RISs: A Correlated T&R Phase-Shift Model and Practical Phase-Shift Configuration Strategies**.  *Jiaqi Xu* et.al.  **IEEE Journal of Selected Topics in Signal Processing, August 2022**  ([pdf](https://ieeexplore.ieee.org/document/9774942))  (Citations **37**)

## Quick Overview

- To realize a full-space smart radio environment, each STAR-RIS element has to dynamically impose two distinct tunable phase-shift values, one for the transmitted signal and one for the reflected signal.
- The phase shift can/cant be adjusted independently. 

## Phase shift model

### Correlated adjustment

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181650680.png" alt="image-20240318151857353" style="zoom:33%;" />



<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181650713.png" alt="image-20240318152006933" style="zoom:33%;" />



### Independent adjustment

According to the Maxwell's Equations, the phase shift of both transmitting and reflecting can be adjusted independently if the if the impedances $$Z_e$$and $$Z_m$$​ in (1) and (2) can take on arbitrary complex values, which means that the STAR-RIS required a active or lossy elements.

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181650856.png" alt="image-20240318152013662" style="zoom:33%;" />





## OMA v.s. NOMA

### OMA

选择FDMA，且两个用户占用正交的、相同带宽的频带。则其可达速率为：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181650903.png" alt="image-20240318153729112" style="zoom:33%;" />

有意思的是，带宽变为1/2，因为两个用户各占一半，然后噪声功率也下降，因为用户带宽各占一半



### NOMA

一个用户采用SIC（连续干扰消除）来消除干扰。为了成功实施SIC，给强信道弱功率，弱信道强功率

- 基于CSI的用户排序
- CSI强的用户先解码CSI弱的用户的信号
- 然后CSI强的通过SIC减去用户弱的，得到自己的信号
- 弱信道将强信道（弱功率）当做干扰

例如，R强，T弱，则有：

- 先R解T:

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181650045.png" alt="image-20240318155609683" style="zoom:33%;" />

- 再R解R：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181650026.png" alt="image-20240318155622216" style="zoom:33%;" />

- 再T解T：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181650961.png" alt="image-20240318155641457" style="zoom:33%;" />

## Three available optimization methods

### Primary-Secondary Phase-Shift Configuration (PS-PSC) Strategy

step1: 先只考虑主要用户，而忽略其中的约束

step2: 再考虑次要用户，次要用户相移为主要用户的v调整（次要用户的相移为主要用户相移的$$+\pi/2$$ or $$+3\pi/2$$）

### Diversity Preserving Phase-Shift Configuration (DP-PSC) Stratege

先计算二者的最优：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181650947.png" alt="image-20240318162245084" style="zoom:33%;" />

然后通过查表进行：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181650067.png" alt="image-20240318162311920" style="zoom:33%;" />

记误差：
$$
\delta_m^\chi=\left|\phi_m^{\chi^*}-\Delta \phi_m^\chi\right|
$$
有:
$$
\delta_m^\chi\leq \pi/4
$$

### T/R-Group Phase-Shift Configuration (TR-PSC) Strategy

分组，分为透射和反射，分别用于不同用户

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403181650176.png" alt="image-20240318162619273" style="zoom:33%;" />

