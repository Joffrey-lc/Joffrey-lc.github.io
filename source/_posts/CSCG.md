---
title: 通信基础-循环对称复高斯噪声
excerpt: Circularly Symmetric Complex zero-mean white Gaussian noise
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220411200222029.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - CSCG
  - Communication
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2022-04-11 20:01:06
---

**CSCG: Circularly Symmetric Complex zero-mean white Gaussian noise 循环对称复高斯噪声**

## 定义

数学定义：
$$
\textbf{Z}\sim\mathcal{CN}(0,1)\to \Re{\textbf{Z}} \perp \!\!\! \perp\Im{\textbf{Z}}
\\and\\
\Re{\textbf{Z}}\sim \mathcal{N}(0,1/2)\quad \Im{\textbf{Z}}\sim\mathcal{N}(0,1/2)
$$




## 含义

- Circularly: means the variance of the real and imaginary parts are equal.
- Gaussian: means the probability distribution of the amplitudes of the noise samples is Gaussian

## Matlab 

```matlab
(randn(m,n)+1i*randn(m,n))*sigma/sqrt(2)
```

其中sigmal是方差

## 正态分布的再生性

设随机比昂量$$X$$和$$Y$$相互独立且分别服从正态分布$$N\sim(\mu_1,\sigma_1^2)$$和$$N\sim(\mu_2,\sigma_2^2)$$，则$$Z=X+Y$$服从正态分布$$N\sim(\mu_1+\mu_2,\sigma_1^2+\sigma_2^2)$$



