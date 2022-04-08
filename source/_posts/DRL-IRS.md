---
title: DRL和IRS的结合（主要关注IRS怎么获取CSI）
excerpt: Abdelrahman Taha et.al.-Deep Reinforcement Learning for Intelligent Reflecting Surfaces—Towards Standalone Operation
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220407205815166.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - IRS
  - Deep Learning
categories:
  - Paper Reading
  - Intelligent Reflecting Surface
comment: valine
math: true
hide: false
date: 2022-04-08 10:30:54
---

**Deep Reinforcement Learning for Intelligent Reflecting Surfaces: Towards Standalone Operation**.  *Abdelrahman Taha* et.al.  **2020 IEEE 21st International Workshop on Signal Processing Advances in Wireless Communications (SPAWC), 26-29 May 2020**  ([pdf](https://ieeexplore.ieee.org/document/9154301))  (Citations **24**)

## Quick Overview

提出一种DRL（Deep Reinforcement Learning）的方法，不用**额外的训练开销**就可以获得接近Supervised Learning 和Perfect CSI的性能。而且这个方法不受其他基站控制，是**standalone**的。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220407205815166.png" alt="示意图" style="zoom: 50%;" />

值得注意的是，对于整个IRS，并不是全部无源的，而是部分有源，**称为Active element**，等同于对全部IRS CSI进行sample。



实验结果说明：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220407210210939.png" alt="实验一" style="zoom: 40%;" />

实验结果说明，虽然DRL需要更多的样本训练，但是DRL方案仅对每个训练片段使用一个Beam，而DL方案需要400个。



然后利用类似半监督-伪标记的方法，用DRL预测最优希望的$$k_B$$波束，并把这些波束添加到训练集中

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220408102154327.png" alt="image-20220408102154327" style="zoom: 80%;" />

同时，还可以看到，Ideal Rewarding 性能更加，即仅当可达速率等于期望值时，才给正向反馈，否则都是负向反馈。

## 具体内容

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220408102710833.png" alt="算法流程" style="zoom: 80%;" />

