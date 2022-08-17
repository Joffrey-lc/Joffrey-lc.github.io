---
title: 知识储备-无线信道
excerpt: 简要总结无线信道
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20211203212547096.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - basic knowledge
  - communicaiton
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2022-02-28 19:48:31
---

# Wireless Channel

## 强度衰减

 $L_s=32.44+20\log d(km)+20\log f(MHz)$

即路径衰减与电磁波的**频率**及**距离**有关。

## 多普勒频移

由于发射或接收端的运动引起的频率偏移

## 多径效应

电磁波从发射端到接收端有许多时延不同、损耗各异的传输路径，例如直射、反射、绕射等。不同路径的相同信号在接收端叠加会增大或减小信号能量。

![image-20220228195339911](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220228195339911.png)

# 结论

**一旦发射机、接收机、以及周边的环境相对位置固定了，无线信道就是固定的，不会随时间变化。**



## 无线信道传播下的功率变化

### 大尺度衰落

是指在当前周围环境下，接收端离发射端一定距离时的电磁波信号功率的平均衰落水平。

主要影响：**环境**和**距离**
$$
L_s=32.44+20\log d(km)+20\log f(MHz)
$$
距离差不多要有千米量级才会有接收功率的差别。所以称之为**大尺度**，而且一般而言可以认为是整个信号频带内影响相同的，**即可以认为大尺度衰落相对于实际通信系统的信号而言，是与频率无关的（只与中心频点有关）。**



### 小尺度衰落

主要由信号的多径传播以及收发端的相对运动引起，对收发端相对距离变化比较敏感。**且一般和信号带宽内的各频率分量有关。**

## 多径

### 相干带宽-信道衰落近似相等的一段带宽

![image-20220518213858184](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220518213858184.png)

不同的时延（由多径产生）对应到频域就是相位旋转。相关带宽内，可以认为总的衰落系数仅有相位差别

> 相关带宽的量级为该信道时延扩展（$$\tau_1-\tau_2$$）的倒数的量级

![image-20220518214007417](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220518214007417.png)

==当两个发射信号的频率间隔⼩于信道的相⼲带宽，那么这两个经过信道后的，受到的信道传输函数是相似的，由于通常的发射信号不是单⼀频率的，即⼀路信号也是占有⼀定带宽的，如果，这路信号的带宽⼩于相⼲带宽，那么它整个信号受到信道的传输函数是相似的，即信道对信号⽽⾔是平坦特性的，⾮频率选择性衰落的。==

### 相干时间-信道衰落近似相等的一段时间

![image-20220518214315513](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220518214315513.png)

==在相⼲时间内，两路信号受到的传输函数也是相似的特性，通常发射的⼀路信号由于多径效应，有多路到达接收机，若这⼏路信号的时间间隔在相⼲时间之内，那么他们具有很强的相关性，接收机都可以认为是有⽤信号，若⼤于相⼲时间，则接收机⽆法识别，只能认为是⼲扰信号。==

从分集发射的角度而言：时间分集要求两次发射的时间要大于信道的相干时间，即如果发射时间小于信道的相干时间，则两次发射的信号会经历相同的衰落，分集抗衰落的作用就不存在了。

> 无线信道相干时间的量级为该信道多普勒扩展的倒数的量级

![image-20220518215116994](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220518215116994.png)

## 无线信道的基带特征-等效基带信号

![image-20220518215444804](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220518215444804.png)

## 经典信道（很大可能存在的两个变化模型）

- 瑞利信道
- 莱斯信道

![image-20220518220127510](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220518220127510.png)



