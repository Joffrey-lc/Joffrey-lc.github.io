---
title: Dense network for joint Transmitter and Receiver noncoherent codebook design
excerpt: unsupervised learning (maybe not appropriate), noncoherent (CSI is unavailable at the Receiver.)
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401171632907.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Deep Learning
categories:
  - Paper Reading
  - Deep Learning-based Waveform Design
comment: valine
math: true
hide: false
date: 2024-01-17 16:32:39
---

**Unsupervised Deep Learning for MU-SIMO Joint Transmitter and Noncoherent Receiver Design**.  *Songyan Xue* et.al.  **IEEE Wireless Communications Letters, February 2019**  ([pdf](https://ieeexplore.ieee.org/document/8437142))  (Citations **24**)

## Quick Overview

- Joint transmitter and ==noncoherent== receiver optimization fo MU-SIMO through unsupervised learning. Find the optimal waveform set $$\mathbf{A}$$ for multiusers. 
- Communication chain can be represented by a DNN with three essential layers.
  - The first layer is a partially-connected linear layer responsible for multiuser waveform joint optimization.
  - The others (the second and the third layers) are nonlinear dense layers for noncoherent multiuser detection at the received side



<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401171632907.png" alt="image-20240117161334411" style="zoom:33%;" />

其是很简单，就是在收发机联合训练，找到最适合的波形，使得其能够在发射端分离出来。所谓的创新点还有：

- 减少hidden layers，从而减轻梯度爆炸或消失，并且性能不会收到损失。
- 采用部分链接的Dense层来模拟多发射机并行传输的行为。
- 非对称DNN结构。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401171632951.png" alt="image-20240117163031144" style="zoom:33%;" />

## Transmitter

Codebook for transmitter:

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401171632426.png" alt="image-20240117155647446" style="zoom:33%;" />

Choose a transmitter codebook $$\mathbf{A}$$ to minimize the Channel Ambiguity. 



Each codebook has $$K$$ codewords. So the available codebook for $$m$$-th user is $$\mathbf{W}_m\in\mathbb{R}^{L\times K}$$. The one-hot vector $$\mathbf{a}_m$$ (uniformly distributed) has the size of $$K\times 1$$, which denotes the chosen index of codebooks.

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401171632393.png" alt="image-20240117162754584" style="zoom:33%;" />
