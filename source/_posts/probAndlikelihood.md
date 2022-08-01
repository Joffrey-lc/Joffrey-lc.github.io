---
title: 知识储备-概率和似然
excerpt: 先验后验似然
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20211203212547096.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Math
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2022-05-09 15:44:36
---

# 概率

**以观测/参数 推导 结果**

## 先验

先验概率（prior probability）是指在考虑“观测数据”前，不确定性的概率分布。是**根据以往经验和分析得到的概率**

> 例如在信号检测与估计中，在没有任何观测结果的前提下，根据以往的经验，可以知道是$$H_1$$的概率为0.5，是$$H_2$$的概率是0.5

## 后验

在考虑和给出相关证据或数据后所得到的条件概率，指在得到“结果”的信息后重新修正的概率，是“执果寻因”问题中的"果"。

> 例如在信号检测与估计中$$P(H_1|y)$$，即得到观测信号$$y$$后，检测为$$H_1$$状态的概率

# 似然

**以结果 推导观测/状态**

## 最大似然

在得到观测结果后，推断（最大可能性的）参数

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220509154136842.png" alt="似然的梨子 1" style="zoom: 50%;" />

找到似然函数的最大值

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220509154208000.png" alt="似然的梨子 2" style="zoom: 50%;" />

# 概率和似然

- 抛一枚均匀的硬币，拋20次，问15次拋得正面的可能性有多大？这里的可能性就是“概率”；

- 拋一枚硬币，拋20次，结果15次正面向上，问其为均匀的可能性？这里的可能性就是“似然”。
