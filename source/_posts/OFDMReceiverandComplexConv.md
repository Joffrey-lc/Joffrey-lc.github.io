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

# Deep-Waveform

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



# Another paper/ old version https://arxiv.org/abs/1810.07181v3

- The model contains both dense and convolutional layers which are mostly linear activated, and new structures of residual and skip connections. (different from other works which only contain Fully-Connected layer and Relu activation.)
- complex convolutional layer is implemented within Tensorflow to process complex IQ data, instead of treating it as two independent real numbers. 

Typical pilot patterns in OFDM system are: block, comb, and scattered

![image-20240305111123753](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403052000673.png)





{% label primary @It is recommended to keep the CP while recovering the bits from the time-domain waveform. %}

## Basic OFDM Receiver (AWGN)

Firtstly, the author trains the basic DCCN OFDM receiver (i.e., without channel equalizer) for bit recovery. 

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403052000676.png" alt="image-20240305175722646" style="zoom:33%;" />

- The first part includes first 3 layers, which is intended to transform time-domain OFDM symbol into frequency-domain. The major component of the first part is a Complex Conv (C-Conv) layer of size N × S(N) × 1.
  - DCCN can drop CP by configuration. Dropping the CP before Complex 1D-Conv.
- The second part contains layers 4 to 6, which is intended to extract all the data cells of an OFDM frame, this is implemented by an FC layer.
  - the real part and imaginary part are stored in the last dimension of the tensors.
- Part 3 is for demodulation, which is convert the complex IQ data into soft bits. The output of softmax activation are soft bits, which represents each bit with 2 real numbers (e.g. Log-Likelihoods of 0 and 1).

## OFDM receiver Equalizer

- The equalizer usually located in the frequency domain to avoid the convolutional operator. Thus, the DFT-like component is located before the LS-like Equalization.

![image-20240305181423944](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403052000666.png)

- The first (layer 0-5) and fourth parts (last 4 layers) are DFT/IDFT-like complex Conv layers intended to perform time/frequency domain transformation. The layer 3 and last 2 layer are used for CP removing and adding back.
- Part 2, from layers 6 to 19, is for channel estimation.
- Part 3, layer 20, is frequency domain channel equalization implemented by complex division: the output of part 1 (frequency domain receive signal) over the output of part 2 (channel estimates).
  - LS-like channel equalizer



### Training configurations

The Two-stage training configurations:

![image-20240305182353730](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403052000628.png)

- It's too complex to be trained together at one time. 
- Firstly, training the basic OFDM receiver in AWGN channel {% label primary @without fading %}
- Then, Load the pre-trained basic OFDM receiver and insert the DCCN Equalizer before the DCCN OFDM receiver.
- Lastly, generate the Rx data {% label primary @with fading %}, and only the DCCN Equalizer is trained.
- Some tracks:
  - mini batch
  - to tensor
  - small and decaying learning rate
  - early stopping

The {% label primary @same loss function %} is used in the two stages. And the loss function is:

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403052000617.png" alt="image-20240305182603431" style="zoom: 67%;" />

- The logarithmic BER could prevent diminishing gradient due to tiny changes of CE when BER is very small. 
- Training SNR:

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202403052000669.png" alt="image-20240305183646134" style="zoom: 67%;" />
