---
title: OFDM Receiver Design and Complex Convolutional Networks
excerpt: OFDM receiver, DFT/IDFT is replaced by complex dense network. Complex convolutional networks
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401181652608.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Deep Learning
categories:
  - Paper Reading
  - Deep Learning-based Waveform Design 
comment: valine
math: true
hide: false
date: 2024-01-18 16:51:50
---

**Deep-Waveform: A Learned OFDM Receiver Based on Deep Complex-Valued Convolutional Networks**.  *Zhongyuan Zhao* et.al.  **IEEE Journal on Selected Areas in Communications, August 2021**  ([pdf](https://ieeexplore.ieee.org/document/9448141))  (Citations **25**)

[Open-source software ](https://github.com/zhongyuanzhao/dl_ofdm)

提出了一种利用deep complex-valued convolutional network 实现直接从时域信号解调OFDM bits的方案

- 结合CP-exploitation, channel estimation, and intersymbol interference，一起取得了比较好的效果
- 指导了新的方法进行复数运算
  - 传统方案一：拼成两列
  - 传统方案二：two channel
- Two stages for training in fading channel.
- 代码开源

## Quick Overview

- Use a deep complex-valued convolutional network (DCCN) to recover bits from time-domain OFDM signals without relying on any explicit DFT/IDFT.
- has the advantage of combining CP-exploitation, channel estimation, and intersymbol interference.
- guidelines of exact and approximate implementations of a complex-valued convolutional layer are provided for the design and analysis of convolutional networks for wireless PHY. 
- a suite of novel training techniques are developed to improve the convergence and generalizability of the trained model in fading channels. 





The Authors claimed that process complex data  in the $\mathbb{R}^2$ is differs from $$\mathbb{C}$$ field in multiplicative operations.



And DCCN can:

- a learned linear transform to replace DFT/IDFT by exploiting its cyclic prefix (CP).
- a data-driven interpretable DCCN channel equalizer that outperformances the legacy receivers and lower complexity. Combine CP exploitation, intersymbol interference mitigation and channel estimation.
- a training methods to improve the convergence and generalizability of the DNN-based receiver in fading channel.

## OFDM system

Diagram of legacy OFDM PHY

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401181652494.png" alt="image-20240118153805786" style="zoom:33%;" />

Exemplary OFDM coherence slot and time-domain waveform

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401181652608.png" alt="image-20240118153824808" style="zoom:33%;" />

An OFDM symbol contains $$N=32$$ subcarriers, and $$G=10$$ DC guard band and edge guard band among the subcarriers. 

A subcarrier in an OFDM symbol (the yellow column) is refereed to as a resource element (RE). And a coherence slot contains $$F=8$$ OFDM symbols, with $$P=7\times 8=56$$ pilot REs and $$D=16\times8=128$$ data REs, respectively. 

The length of a time-domain full OFDM symbol is $$S=N+N_{CP}$$.



## Channel estimation

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401181652892.png" alt="image-20240118161650143" style="zoom:33%;" />



Pilot signals are of either constant signal or low auto-correlation sequence (e.g., Zadoff-Chu sequence) known at the receiver. The basic pilot-aided channel equalizer in OFDM system is based on the least square (LS) estimator.



## Whole Structure

![image-20240118163753636](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401181652002.png)

And two stage training. 

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401181652006.png" alt="image-20240118163923111" style="zoom:33%;" />



## Simplify

Using the legacy data REs extraction and demodulation (Equalizer?)

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202401181652912.png" alt="image-20240118163730156" style="zoom:33%;" />
