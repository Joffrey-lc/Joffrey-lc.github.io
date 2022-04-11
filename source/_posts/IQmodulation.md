---
title: 知识储备-IQ调制
excerpt: IQ调制基础
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/v2-5a91f588fa13b91ffb3773ad9b7ac892_1440w.jpg
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - IQ  Modulation
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2022-04-11 16:39:46
---

# IQ调制

## IQ调制原理

首先，已调信号可以表示为：
$$
M(t)\cos(wt+\phi(t))\label{eqn:1}
$$
所谓调制，无非是调整幅度$$M(t)$$或者相位$$\phi(t)$$（由于频率是相位关于时间的微分，所以调频也可以包含在调相中）。

如式$$\ref{eqn:1}$$的形式，在极坐标中可以表示为：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200317215459221.png" alt="调制信号极坐标表示" style="zoom:50%;" />

所以可以得到$$i(t)=M(t)\cos(\phi(t)),q(t)=M(t)\sin(\phi(t))$$。

映射完坐标，就需要上变频，IQ调制上变频的方式如下：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/v2-c78e0ca1a780df0d2f94628aa22985cb_1440w.jpg" alt="上变频" style="zoom: 67%;" />

根据频域卷积定理可得：
$$
\begin{aligned}
&i(t) \cdot \cos \left(\omega_{c} t\right) \leftrightarrow \frac{1}{2 \pi} \cdot I(\omega) *\left\{\pi \cdot\left[\delta\left(\omega+\omega_{c}\right)+\delta\left(\omega-\omega_{c}\right)\right]\right\}=\frac{1}{2} \cdot\left[I\left(\omega+\omega_{c}\right)+I\left(\omega-\omega_{c}\right)\right] \\
&q(t) \cdot \sin \left(\omega_{c} t\right) \leftrightarrow \frac{1}{2 \pi} \cdot Q(\omega) *\left\{j \pi \cdot\left[\delta\left(\omega+\omega_{c}\right)-\delta\left(\omega-\omega_{c}\right)\right]\right\}=\frac{1}{2} j \cdot\left[Q\left(\omega+\omega_{c}\right)-Q\left(\omega-\omega_{c}\right)\right]
\end{aligned}
$$
可以知道对I路$$i(t)$$乘$$\cos(w_ct)$$等于在频域上对信号频谱进行搬移。由于正余弦的傅里叶变换有：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/v2-0f4b43ee7389c065abde1f122ab65141_1440w.jpg" alt="正余弦傅立叶变换" style="zoom:67%;" />

则进行频谱搬移的过程可以由下图展示：

![img](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/v2-fe0a0c2d3fd5001439db3ddb585e3445_1440w.jpg)

可以看到，搬上去的时候出现了负频率（图画得有问题）。合路后发射。
{% note warning %}
带宽问题怎么理解？是单边带还是双边带？
{% endnote %}



接收端接受到了之后，进行下变频：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/v2-5a91f588fa13b91ffb3773ad9b7ac892_1440w.jpg" alt="下变频" style="zoom:67%;" />



对于$$q(t)$$路，$$i(t)$$路相关的基带信号抵消了，所以用一个低通滤波器就可以恢复出$$q(t)$$路；对$$i(t)$$路同理。

## 为什么IQ调制

(1) IQ调制可以通过**提高符号速率**或者**采用高阶调制**实现更高的数据速率，非常方便灵活，这是传统的模拟调制所远远不及的。

(2) 实现高速通信时，**IQ** **调制更加易于实现**。IQ 调制可以非常方便地将符号映射至矢量坐标系中，从而完成数字调制；同理，在接收侧也可以非常方便地根据符号映射解调出原始数据比特流。

(3) **IQ** **调制具有更高地频谱利用率**。因为I和Q是在相位上面正交的（不相干）,可以作为两路信号看待。
