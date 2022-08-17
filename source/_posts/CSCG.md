---
title: 通信基础-常用的一些分布
excerpt: Circularly Symmetric Complex zero-mean white Gaussian noise
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220411200222029.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Signal Distribution
  - Communication
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2022-04-11 20:01:06
---

**CSCG: Circularly Symmetric Complex zero-mean white Gaussian noise 循环对称复高斯噪声**

## CSCG：循环对称复高斯

数学定义：
$$
\textbf{Z}\sim\mathcal{CN}(0,1)\to \Re{\textbf{Z}} \perp \!\!\! \perp\Im{\textbf{Z}}
\\and\\
\Re{\textbf{Z}}\sim \mathcal{N}(0,1/2)\quad \Im{\textbf{Z}}\sim\mathcal{N}(0,1/2)
$$

### 含义

- Circularly: means the variance of the real and imaginary parts are equal.
- Gaussian: means the probability distribution of the amplitudes of the noise samples is Gaussian

### Matlab 

```matlab
(randn(m,n)+1i*randn(m,n))*sigma/sqrt(2)
```

其中sigmal是方差

### 正态分布的再生性

设随机比昂量$$X$$和$$Y$$相互独立且分别服从正态分布$$N\sim(\mu_1,\sigma_1^2)$$和$$N\sim(\mu_2,\sigma_2^2)$$，则$$Z=X+Y$$服从正态分布$$N\sim(\mu_1+\mu_2,\sigma_1^2+\sigma_2^2)$$

## Rayleigh分布

复高斯分布的模服从瑞利分布：
$$
f(x)=\frac{x}{\sigma^{2}} e^{-\frac{x^{2}}{2 \sigma^{2}}}, x>0
$$

### Rayleigh分布和复高斯分布的关系

如果$$\textbf{A}\sim\mathcal{CN}(0,\sigma^2)$$，即$$\Re{\textbf{A}}\sim\mathcal{N}(0, \sigma^2/2)$$，$$\Im{\textbf{A}}\sim\mathcal{N}(0, \sigma^2/2)$$，则$$|\textbf{A}|\sim$$参数为$$\sigma^2/2$$的瑞利分布：
$$
f_{|\textbf{A}|}(x)=\frac{x}{\sigma^{2}/2} e^{-\frac{x^{2}}{\sigma^{2}}}, x>0
$$

### simulation

因为没有找到Rayleigh分布和复高斯分布的关系。使用matlab进行仿真验证。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/untitled.jpg" alt="untitled" style="zoom:33%;" />



## 卡方分布

非中心卡方分布由若干{% label primary @独立同方差的均值不全为0的 %}高斯随机变量平方和得到。

![image-20220720161758149](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220720161758149.png)
