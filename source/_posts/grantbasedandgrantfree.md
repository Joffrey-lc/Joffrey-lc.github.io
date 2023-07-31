---
title: 知识储备-Grant-based versus Grant-free
excerpt: Massive Internet of Things.
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202305292212107.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - communication
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2023-05-29 22:11:54
---

[copy  form CSDN](https://blog.csdn.net/weixin_43413559/article/details/121973314)

## Intro

在B5G通信系统中，每平方千米的通信用户数规模可能达到$$10^7$$数量级，因此大规模接入或者超大规模接入在未来通信系统中变得越来越重要。虽然用户规模极其巨大，但幸运地是同一时间节点下，随机的活跃用户群规模却远远小于总用户数。因此，为了协调用户与基站(Base Station, BS)间的通信，就需要定义一种大规模接入协议。经典的随机接入协议有两种：{% label primary @基于授权的(Grant-based)接入协议 %}和{% label primary @不需要授权的(Grant-free)接入协议 %}。除此之外，还有一种新的随机接入范式：{% label primary @无源大规模随机接入(unsourced massive random access) %}。

## 基于授权的随机接入协议(Grant-based Random Access)

现行的5G窄带Iot(Internet of things)所采用的就是基于授权的接入协议。对于该协议，每一个活跃用户都需要获得BS的许可或者授权来接入网络，具体过程如下图所示：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202305292212107.png" alt="img" style="zoom:33%;" />

具体过程描述如下：

1. 步骤1：每个活跃用户从一组正交序列里随机地选择一个序列(preamble or say signature)，将该序列发送给基站。
2. 步骤2：基站对每个活跃用户做出回应，授权它们发送连接请求。
3. 步骤3：活跃用户发送连接请求，请求基站分配资源来传输数据。
4. 步骤4：如果步骤1发送的序列(preamble)是唯一的，那么基站就会对相应的请求授权，并且发送一条contention-resolution消息来告知该活跃用户可用的资源。否则，如果不唯一，就不会被授权。



{% note success %}基于授权的随机接入协议的优缺点：

优点：

1. 接收机基站端处理方便，复杂度相对较低。

缺点：

1. 因为相干时间较短，正交的序列是有限的，不能满足大规模用户的随机接入，具体来讲，就是当用户数很多时，两个用户变得更有可能选择同一个序列，导致碰撞概率增加，这将导致接入的延时显著增高。
2. 基于授权的协议需要4步传输，这会导致很大的信令开销(high signaling overhead)。因为信道容量有限，该信令开销在大规模接入场景下会变得更加让人难以忍受。

{% endnote %}

## 不需要授权的随机接入协议(Grant-free Random Access)

该协议只需要两步，第一步是活跃用户发送代表用户ID（唯一的）的导频序列到基站，第二步是发送数据。不需要授权的随机接入协议中，有一个重要的点是，基站端根据用户发送的导频序列来识别哪些用户是活跃的。但因为用户规模很大，序列之间不再满足正交性，因此会额外地引入多址干扰(multi-access interference, or say co-channel interference)，接收机处理的复杂度也会因此而增加。一般地，接收机的相关处理普遍利用压缩感知来恢复稀疏信号，也有部分学者使用基于方差的方法。
