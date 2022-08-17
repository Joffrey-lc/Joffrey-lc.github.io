---
title: 20220806IRS讲座-IRS材料
excerpt: IRS调幅、调相、调极化方向、Active、IRS调制、IRS感知定位
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220801203534699.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - IRS
categories:
  - Paper Reading
  - Intelligent Reflecting Surface
comment: valine
math: true
hide: false
date: 2022-08-06 11:09:01
---

# Quick View

智能反射面调幅、调相、{% label success @调频 %}、调极化方向、{% label success @Active IRS（多单元share主动放大） %}、{% label success @IRS调制/反射调制 %}、IRS感知定位

{% note warning%}
调频可以结合：FDA+CSI-free，自动波束扫描
{% endnote %}

## 调幅（On/Off）

![image-20220801201438480](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220801201438480.png)

调整幅度、相位、==频率==、极化方向



![image-20220801202614373](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220801202614373.png)

选择阵面来实现空间波束赋形



## 调频

==频率调控==   时间编码

![image-20220801202841135](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220801202841135.png)

**单元与单元之间的相位相同，但是不同时间中的相位不同。**

使得，单频信号照射，反射的频谱展宽，变为多频率反射波。

![image-20220801203140467](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220801203140467.png)



## 编码

![image-20220801203534699](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220801203534699.png)

时间=调频

空间=空间波束赋形

## 可编程无线环境

![image-20220801203651157](C:/Users/32677/AppData/Roaming/Typora/typora-user-images/image-20220801203651157.png)

漫发射的原因是因为波束窄，想要给散射开



![image-20220801203945545](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220801203945545.png)

主动信道：怎么贴，贴在哪，贴多大

## Active IRS



![image-20220801204747976](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220801204747976.png)



## IRS调制

![image-20220801205234164](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220801205234164.png)

IRS调制

## IRS感知

![image-20220801210236549](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220801210236549.png)

IRS 感知



## IRS幅度相位解耦

IRS幅度相位单独调控比较难，但是不是不可以实现

## 实际响应速率

IRS响应响应速率（在5G6G中的应用及限制） - 响应时间、充放电时间等等。。。。。调控速率现在在60-70MHz



## 咨询问题

![image-20220801212426257](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220801212426257.png)

![image-20220801212452715](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220801212452715.png)
