---
title: Multiple Tasks Receiver Design
excerpt: Blind demodulation-Modulation recognition and bits recovery.
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401172127825.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Deep Learning
  - Receiver Design
categories:
  - Paper Reading
  - Deep Learning-based Waveform Design
comment: valine
math: true
hide: false
date: 2024-01-17 21:27:31
---

**Waveform Level Intelligent Multi-Task Receiver With BiLSTM**.  *Zhaorui Zhu* et.al.  **IEEE Communications Letters, March 2022**  ([pdf](https://ieeexplore.ieee.org/document/9656168))  (Citations **1**)

简而言之，可以拆分为两个network，一个估计modulation，一个根据modulation结果进行bits recovery。



## Quick Overview

- straightforwardly recover bit messages from waveform sequences of unknown modulation schemes without additional time synchronization module. The whole structure is an effective joint synchronization and detection method.
- The first attempt to establish purely one NN to directly process the oversampled waveform sequence with timing offset and blindly recover bits from multiple modulation schemes.
- Numerical results show that one NN can recover bits from four different modulation schemes with BER performance approaching the theoretical value in the ideal channel.

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401172127825.png" alt="image-20240117204216905" style="zoom:33%;" />

## signal model

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401172127880.png" alt="image-20240117204721152" style="zoom:33%;" />

## Network

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401172127834.png" alt="image-20240117204858739" style="zoom:33%;" />

Bits recovery (left) and Modulation recognition (right)

Three parts

- The uppermost two BiLSTM layers extract representation vectors with an overwhelming majority of learnable weights.

- They use LSTM layer for the variable-length sequence. And complementary bidirectional structure is applied due to trailing interference of filter between

  adjacent symbols.

  Reshape received data into 

  <img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401172127858.png" alt="image-20240117205349066" style="zoom:33%;" />

​	where $$N_s$$ denotes the number of symbols, and $$\gamma$$ denotes the oversample rate. 



## Train details

The output unit for "Dense-0" is $$k_\text{max}$$ (it mean the output dimension), while some lower order modulations need to padding zero as $$[b_1,b_2,0,0]$$

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401172127855.png" alt="image-20240117212402627" style="zoom:33%;" />



The loss function

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401172127849.png" alt="image-20240117212527495" style="zoom:33%;" />















