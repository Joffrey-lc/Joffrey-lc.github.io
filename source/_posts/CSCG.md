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



## 非中心卡方分布

非中心卡方分布由若干{% label primary @独立同方差的均值不全为0的 %}高斯随机变量平方和得到。

![image-20220720161758149](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220720161758149.png)

值得注意的是，例如OneL文章中以及其他参考文献中所述，常常写为$$\mathcal{X}^2(a,b)$$，其中，$$a$$为自由度，$$b$$为参数$$\lambda/\sigma^2$$。

所以，此时有期望$$E=a+b$$（事先归一化了方差，所以这里比上式少了一个$$\sigma^2$$）

方差$$V=2(a+2b)$$（事先归一化了方差，所以这里比上式少了一个$$\sigma^4$$）

---

参考书目：《数字通信》P46

非中心卡方分布的PDF为：
$$
p(x)= \begin{cases}\frac{1}{2 \sigma^2}\left(\frac{x}{s^2}\right)^{\frac{n-2}{4}} e^{-\frac{s^2+x}{2 \sigma^2}} I_{\frac{n}{2}-1}\left(\frac{s}{\sigma^2} \sqrt{x}\right) & x>0 \\ 0 & \text { otherwise }\end{cases}
$$
其中：
$$
\begin{align}
&s = \sqrt{\sum\limits_{i=1}^nm_i^2}\\

&I_\alpha(x)=\sum_{k=0}^{\infty} \frac{(x / 2)^{\alpha+2 k}}{k ! \Gamma(\alpha+k+1)}, \quad x \geq 0
\end{align}
$$
$$I_\alpha(x)$$是**modify Bessel function of the first kind and order $$\alpha$$**，$$\Gamma(x)$$是gamma function。

对于$$x>1$$，有常用近似$$I_0(x)\approx\frac{e^x}{\sqrt{2\pi x}}$$

其CDF为：
$$
F(x)= \begin{cases}1-Q_m\left(\frac{s}{\sigma}, \frac{\sqrt{x}}{\sigma}\right) & x>0 \\ 0 & \text { otherwise }\end{cases}
$$
其中$$2m=n$$，$$Q_m(a,b)$$为**generalized Marcum Q function**.

### matlab实现

generalized Marcum Q function 和modify bessel function of the first kind and order $$\alpha$$可以直接用matlab函数：

```matlab
marcumq(a,b,m) % calculate the generilized Marcum Q function
besseli(alpha,x) % calculate the modify bessel function of the first kind and order alpha
```



## CDF和PDF推导

例如之前遇到的典型问题，三个随机变量分别服从参数为$$\lambda_1$$,$$\lambda_2$$,$$\lambda_1$$的指数分布，记为$$\Gamma_1$$，$$\Gamma_2$$，$$\Gamma_3$$，即：
$$
\Gamma_1\sim\mathbf{E}(\lambda_1)\\
\Gamma_2\sim\mathbf{E}(\lambda_2)\\
\Gamma_3\sim\mathbf{E}(\lambda_3)\\
$$
则其和$$\Gamma=\Gamma_1+\Gamma_2+\Gamma_3$$的CDF为：
$$
\mathrm{F}_\Gamma(\gamma)=\text{Pr}(\Gamma\leq \gamma)=\text{Pr}(\Gamma_1+\Gamma_2+\Gamma_3\leq \gamma)
$$
令$$\Gamma^\S=\Gamma_1+\Gamma_2$$，则上式变为：
$$
\begin{align}
&\text{Pr}(\Gamma_1+\Gamma_2+\Gamma_3\leq \gamma)=\text{Pr}(\Gamma^\S+\Gamma_3\leq \gamma)\\
=&\text{Pr}(\Gamma^\S\leq \gamma-\Gamma_3)\\
=&\mathrm{F}_{\Gamma^\S}(\gamma-\Gamma_3)\\
=&\int^\gamma_0\mathrm{F}_{\Gamma^\S}(\gamma-\gamma_3)\mathrm{f}_{\Gamma_3}(\gamma_3)d\gamma_3
\end{align}
$$
因为：
$$
\begin{align}
&\mathrm{F}_{\Gamma^\S}(\gamma^\S)=\text{Pr}(\Gamma^\S\leq\gamma^\S)\\
=&\text{Pr}(\Gamma_1+\Gamma_2\leq\gamma^\S)\\
=&\text{Pr}(\Gamma_1\leq\gamma^\S-\Gamma_2)\\
=&\int^{\gamma^\S}_0\mathrm{F}_{\gamma_1}(\gamma^\S-\gamma_2)\mathrm{f}_{\Gamma_2}(\gamma_2)d\gamma_2\\
=&\int^{\gamma^\S}_0(1-e^{-\lambda_1(\gamma^\S-\gamma_2)})\lambda_2e^{-\lambda_2\gamma_2}d\gamma_2\\
=&-\frac{\lambda_1}{\lambda_1-\lambda_2}e^{-\lambda_2\gamma^\S}+1+\frac{\lambda_2}{\lambda_1-\lambda_2}e^{-\lambda_1\gamma^\S}
\end{align}
$$
所以：
$$
\begin{align}
&\text{Pr}(\Gamma_1+\Gamma_2+\Gamma_3\leq \gamma)\\
=&\int^{\gamma}_0\left(\frac{-\lambda_1}{\lambda_1-\lambda_2}e^{-\lambda_2(\gamma-\gamma_3)} +1+\frac{\lambda_2}{\lambda_1-\lambda_2}e^{-\lambda_1(\gamma-\gamma_3)}\right)\lambda_3e^{-\lambda_3\gamma_3}d\gamma_3\\
=&e^{-\lambda_3\gamma}c_3+e^{-\lambda_2\gamma}c_2+e^{-\lambda_1\gamma}c_1+1
\end{align}
$$
其中，有：
$$
\begin{align}
&c_3=\frac{\lambda_2\lambda_3}{(\lambda_1-\lambda_2)(\lambda_1-\lambda_3)}-\frac{\lambda_1\lambda_3}{(\lambda_1-\lambda_2)(\lambda_2-\lambda_3)}-1\\
&c_2=\frac{\lambda_1\lambda_3}{(\lambda_1-\lambda_2)(\lambda_2-\lambda_3)}\\
&c_1=-\frac{\lambda_2\lambda_3}{(\lambda_1-\lambda_2)(\lambda_1-\lambda_3)}
\end{align}
$$


其PDF为：
$$
-\lambda_3e^{-\lambda_3\gamma}c_3-\lambda_2e^{-\lambda_2\gamma}c_2-\lambda_1e^{-\lambda_1\gamma}c_1
$$

