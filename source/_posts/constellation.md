---
title: 知识储备-星座图
excerpt: 星座图知识整理
index_img: https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/41f4fa54c7dc87329d6f03b81473b78a.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - signal processing 
  - communication
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2021-12-04 14:19:12
---

# 星座图
已知信号以IQ路表示：

![IMG_1101](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/92c9c4adef9ca809931193d74d875a22.png)

注意：

①相邻符号之间码元变化１bit（格雷码）

②相邻符号点之间的欧式距离越大，抗噪声能力越强

③随着SPS(每个符号的采样点个数)增加，星座图显得越“乱”。因为一个符号的相位和幅度信息增加了，在星座图上的点数也增多了，符号与符号之间的跳变变得平滑。如下图可见：

QPSK星座图符号位置：

![image-20210815164210448](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/b50efc495629ea035ec664c76517790b.png)

SPS=1，SNR=18dB，QPSK星座图:

![image-20210815164329496](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/f92376c8c9c8bdab82cc5ef29ff05741.png)

SPS=8，SNR=18dB，QPSK星座图:

![image-20210815164424105](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/41f4fa54c7dc87329d6f03b81473b78a.png)

SPS=32，SNR=18dB，QPSK星座图:

![image-20210815164642830](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/9001b3bf7d18301c23add6778f21da9c.png)
肉眼观察SPS=1最明显，调制识别正确率和SPS有没有关系呢？
