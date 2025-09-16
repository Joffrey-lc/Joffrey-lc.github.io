---
title: Relay Joint Nulling--beyond SVD-based
excerpt: A Spatial-Domain Joint-Nulling Method of Self-Interference in Full-Duplex Relays.  Byungjin Chun et.al.  IEEE Communications Letters, April 2012
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403281709621.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Relay
  - Null sapce
categories:
  - Paper Reading
  - Null space
comment: valine
math: true
hide: false
date: 2024-03-28 17:09:36
---

Date: 2024.03.26  21:20
Author: Joffrey LC

-------------------------------------

**A Spatial-Domain Joint-Nulling Method of Self-Interference in Full-Duplex Relays**.  *Byungjin Chun* et.al.  **IEEE Communications Letters, April 2012**  ([pdf](https://ieeexplore.ieee.org/document/6151763))  (Citations **64**)

## Quick Overview



![image-20240328154857037](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403281709621.png)

- 两种中继（Relay）转发结构：

  - amplify-and-forward (AF)
  - decode-and-forward (DF)

- 两种中继方案的解调信噪比：

  <img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403281709637.png" alt="image-20240328161139883" style="zoom:33%;" />

​	AF: 算信噪比，并且结合两段$$\mathbf{d}^H$$，$$\mathbf{b}$$的增益

​	DF: 取min，relay不行解码就不行



假设echo signals 延迟足够大，就变成了一个干扰信号，所以需要消除干扰：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403281709768.png" alt="image-20240328162140743" style="zoom:33%;" />

## SVD based

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403281709185.png" alt="image-20240328162201418" style="zoom:33%;" />

有意思的是，通过$$\mathbf{U}^{(1)}$$和$$\mathbf{U}^{(2)}$$的正交性（$$\mathbf{V}^{(1)}$$和$$\mathbf{V}^{(2)}$$同理），当$$\mathbf{d}=\mathbf{U}^{(1)} \mathbf{b}$$，==且$$\mathbf{b}$$可以任意取值，只要满足功率约束就可==，同理$$\mathbf{p}=\mathbf{V}^{(2)} \mathbf{c}$$

则有：
$$
\begin{align}
\mathbf{d}^H\mathbf{H}\mathbf{p}=&\mathbf{b}^H\mathbf{U}^{(1),H}\left(\mathbf{U}^{(1)} \boldsymbol{\Sigma}^{(1)} \mathbf{V}^{(1) H}+\mathbf{U}^{(2)} \boldsymbol{\Sigma}^{(2)} \mathbf{V}^{(2) H}\right)\mathbf{V}^{(2)} \mathbf{c},\\
=&\mathbf{0}
\end{align}
$$
==因为$$\mathbf{U}^{(1)}$$消掉了$$\mathbf{U}^{(2)}$$项，因为$$\mathbf{V}^{(2)}$$消掉了$$\mathbf{V}^{(1)}$$项==

然后再选择最大化的$$\mathbf{b}$$和$$\mathbf{c}$$。



## Continuous domain based

核心思想是，通过正交投影，使得其中一个一定是正交的，这样就只用优化一个，并使得整个最大化。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403281709260.png" alt="image-20240328165659696" style="zoom:33%;" />



1. 由$$\mathbf{p}=\mathbf{P}_{\mathbf{z}}^{\perp} \mathbf{k}$$，则一定使得$$\mathbf{d}^H\mathbf{H}\mathbf{p}=\mathbf{0}$$成立。
2. 取$$\mathbf{k}=\frac{\left(\mathbf{h}_{r d}^H \mathbf{P}_{\mathbf{z}}^{\perp}\right)^H}{\left\|\mathbf{h}_{r d}^H \mathbf{P}_{\mathbf{z}}^{\perp}\right\|}$$，从而使得$$\mathbf{p}$$完全固定由$$\mathbf{H}^H\mathbf{d}$$求出。
3. 将问题转换为只与$$\mathbf{d}$$相关的问题

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403281709766.png" alt="image-20240328170527488" style="zoom:33%;" />

用梯度下降法求解。





## Numerical Results

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403281710140.png" alt="image-20240328170759254" style="zoom:33%;" />

- DF比AF好
- Proposed 比 SVD-based 好



