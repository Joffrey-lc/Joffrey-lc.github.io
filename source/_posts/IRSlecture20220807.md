---
title: 20220807IRS讲座-一种优化算法
excerpt: 离散相位、IRS+CSI-free scheme 
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220807105936888.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - IRS
categories:
  - Paper Reading
  - Intelligent Reflecting Surface
comment: valine
math: true
hide: false
date: 2022-08-07 13:25:45
---

# Quick Review

离散相位、{% label primary @CSI-Free %} Model

但是他的CSI-free model还是根据直接采样得到的值，的条件均值，选取最大的Phase Shift

![image-20220807105936888](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220807105936888.png)

## System Model

![image-20220807101657856](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220807101657856.png)

## 离散相位

![image-20220807101858754](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220807101858754.png)

解决 离散相位、Unknown Channel

K—$$\infty$$，即连续相位，可以线性调整



K—$$\infty$$

用SDP，只能达到全局最优的67%

![image-20220807102448872](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220807102448872.png)

罗智泉等人找到一种方法实现多项式时间内求解这个问题。





## Unknown Channel

![image-20220807104058014](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220807104058014.png)



### Method 1

![image-20220807104226771](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220807104226771.png)

random 选一个信号强度最大的。



### Method 2

sample一些样本，然后做统计均值？



### Analysis

![image-20220807104652312](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220807104652312.png)

Method2 需要更多的sample，但是可以实现更好的性能



![image-20220807105324829](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/image-20220807105324829.png)
