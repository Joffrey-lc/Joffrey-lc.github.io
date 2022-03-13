---
title: IRS辅助SWIPT（二）
excerpt: Cunhua Pan-Intelligent Reflecting Surface Aided MIMO Broadcasting for Simultaneous Wireless Information and Power Transfer
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20220313155156040.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - SWIPT
  - IRS
categories:
  - Paper Reading
  - Intelligent Reflecting Surface
comment: valine
math: true
hide: false
date: 2022-03-13 15:46:23
---

原文[Intelligent Reflecting Surface Aided MIMO Broadcasting for Simultaneous Wireless Information and Power Transfer](https://ieeexplore.ieee.org/document/9110849)

![IRS辅助SWIPT](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20220313155156040.png)

## 缩写说明

- WSR: Weighted sum rate
- TPC: Transmit precoding matrices
- WMMSE: weighted minimum mean-square error



## 主要挑战

通过IRS辅助SWIPT。联合优化BS、的发射预编码（波束赋形）矩阵TPC和IRS被动波束赋形的TPC，来描述WSR最大化问题，并满足EHS的能量需求。挑战在于引入能量捕获阈值后，是一个非凸约束。



## 算法内容

1. 通过WMMSE转化问题，方便应用BCD
2. 通过BCD算法将原优化问题分解为多个子问题
3. 基于每个子问题提出一种低复杂度的迭代算法，交替优化TPC矩阵和相移矩阵，并证明BCD算法收敛于原问题的KKT点
4. 设计可行性检查方法来探究其可行性



## Future work

- 本文考虑的是perfect CSI，imperfect CSI是一个极大地挑战
- 为了优化方便选取的是continued phase shift，实际中应该是discrete phase shift

