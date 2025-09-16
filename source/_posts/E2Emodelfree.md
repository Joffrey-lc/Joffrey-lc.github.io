---
title: End-2-End model-free Transceiver design
excerpt: Model-Free Training of End-to-End Communication Systems.  Fayçal Ait Aoudia et.al.
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405141051840.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Deep Learning
categories:
  - Paper Reading
  - Deep Learning-based Waveform Design
comment: valine
math: true
hide: false
date: 2024-05-14 10:51:18
---

Date: 2024.05.09  22:23
Author: Joffrey LC

-------------------------------------

**Model-Free Training of End-to-End Communication Systems**.  *Fayçal Ait Aoudia* et.al.  **IEEE Journal on Selected Areas in Communications, November 2019**  ([pdf](https://ieeexplore.ieee.org/document/8792076))  (Citations **131**)



[open source code](https://github.com/JS2498/Model_Free_E2E_Communication)

## Quick Overview

- 核心问题：end-to-end model (e.g., Autoencoder)需要可微信道模型。
- Training the receiver using the ==**True gradient**==, while training the transmitter using an ==approximation of the gradient==. 

​	For example, some parts of the transceiver, such as  quantization, which is non-differentiable.

- 与常规反向梯度传播的算法作比较，AWGN信道和瑞利快衰落信道上，实现了相同的性能。

## Gradient estimation without channel model

### The gradient of Receiver 

The True gradient between difference of the output of model and the training sample.



### The gradient of Transmitter

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405141051813.png" alt="image-20240514103833099" style="zoom:33%;" />

对于原Loss函数：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405141051810.png" alt="image-20240514103943490" style="zoom:33%;" />

进行变换得到：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405141051801.png" alt="image-20240514103950521" style="zoom:33%;" />

然后求导得到：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405141051837.png" alt="image-20240514104613471" style="zoom:33%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405141051832.png" alt="image-20240514104627207" style="zoom:33%;" />

## Training end-to-end communication systems

Transmitter: All non-differentiable operations on the transmitter output, e.g., quantization, can be assumed to be part of the channel (non-differentiable channel)



Receiver: the last layer of the receiver model is a softmax layer.



<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405141051840.png" alt="image-20240513205334542" style="zoom:33%;" />





Alternating Training for Receiver and Transmitter, and one is training, the another are kept fixed.



### Training the Receiver

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405141051348.png" alt="image-20240513210813371" style="zoom:33%;" />



Note that there is no relaxation of the Transmitter output, since it is not required to approximate the receiver gradient.



### Training the Transmitter

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405141051346.png" alt="image-20240513211308858" style="zoom:33%;" />

Not that we need to transmit the per-example losses to the transmitter end over a reliable feedback link, and then update the Transmitter model.



## Evaluation

Relaxation is achieved by adding a zero-mean Gaussian vector.

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202405141051343.png" alt="image-20240513211726394" style="zoom:33%;" />

$$\sqrt{1-\sigma^2}$$是为了功率归一化（信号和噪声功率和为1）

看起来会选择较小的$$\sigma^2$$，从而使得approximation逼近真实的gradient，但是作者实验结果证明过小的$$\sigma$$会使得估计器方差变大并且导致收敛变慢。
