---
title: 知识储备-P/NP/NPC/NP-hard问题
excerpt: 介绍P问题/NP问题/NPC问题/NP-hard问题
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/v2-df33fc6b9fb9c526f7e21d4bbbdee578_1440w.jpg
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - NP-hard
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2022-04-25 10:55:34
---

参考[知乎博客](https://zhuanlan.zhihu.com/p/83990003)

## 规约

首先解释一下**规约**的概念，如果能找到这样一个变化法则，对任意一个程序A的输入，都能按这个法则变换成程序B的输入，使两程序的输出相同，那么我们说，问题A可约化为问题B，即可以用问题B的解法解决问题A，或者说，问题A可以“变成”问题B。

例如A是求一元一次方程的解，B是求一元二次方程的解，A的输入参数是k和m，B的输入参数是a，b和c。

显然，我们可以令$$a=k^2, b=2km, c=m^2$$，这样我们就可以通过解问题B来求解问题A了。当然，A和B问题都不是NP问题。

可以看出，B的时间复杂度高于或者等于A的时间复杂度。也就是说，**问题A不比问题B难**。

## P

P问题: **能在多项式时间内解决的问题**。考虑时间复杂度，P问题的时间复杂度总是可以用多项式表示，或小于某多项式表示的。

## NP

NP问题: 不能在多项式时间内解决或不确定能不能在多项式时间内解决，但能在多项式时间**验证**的问题。

## NPC

NPC问题：它是一个NP问题，且所有的NP问题都可以用多项式时间约化到它。更本质的理解，我们把**规约**看作一种偏序关系，那么NPC就是NP的上届。一句话，**所有NP问题都不比NPC难。**

## NP-hard

NP-Hard问题：NP-hard满足所有的NP问题都可以用多项式时间约化到它，但并不要求其是一个NP的问题。或者说，NP-hard是所有问题的上届。也就是说，**所有问题都不比NP-hard难。**

可以看出，NP-hard问题的范围比NPC的范围更大。

![P, NP, NPC 和 NPhard](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/v2-df33fc6b9fb9c526f7e21d4bbbdee578_1440w.jpg)





