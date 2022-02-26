---
title: 雷达通信频谱共享及一体化：综述与展望
excerpt: 雷达通信感知一体化综述
index_img: https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211204140733338.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Radar
categories:
  - Paper Reading
  -	Radar and Communication
comment: valine
math: true
hide: false
---

[原文链接](https://radars.ac.cn/article/doi/10.12000/JR20113?viewType=HTML)

## 缩写说明

- RCSS：雷达与通信的频谱共享  Radar and Communication Spectrum Sharing
- RCC：雷达与通信系统的同频共存 Radar-Communication Coexistence
- DFRC：雷达通信一体化系统设计 Dual-Functional Radar-Communication
- V2X：车联网 Vehicle to everything
- GNSS：全球卫星导航系统 Global Navigation Satellite System
- WPS：WiFi室内 定位系统 WiFi-based Positioning System

## RCSS研究路径

1. 雷达与通信频谱共享（RCC）：考虑分立的雷达与通信系统共同用同一频谱
2. 雷达通信一体化（DFRC）：除了共享同一频谱外，还共用同一硬件平台，如何设计一体化信号处理方案来同时实现通信与雷达感知功能（**重要**：不仅在于对频谱资源利用率的提升，还扩展到包括车联网、室内定位和隐蔽通信在内的多种新兴的民用与军用场景）

## 研究内容

1. 5G车联网毫米波定位

   ​	可以预见，5G通信技术能够利用大规模MIMO天线阵列和毫米波频谱赖满足V2X的高分辨率和低时延要求。

   - 毫米波段具有充裕的可用带宽，不仅可以实现更高的数据传输效率，也可以显著提升距离分辨率。
   - 大规模MIMO可以形成“铅笔式”的窄波束。补偿毫米波信号的路径损失，同时提高方位角的估计精度。
   - 由于毫米波的稀疏性，包含的多径分量少，毫米波信道中雷达目标回波受到的杂波干扰小。

2. WiFi室内定位及动作识别

   1. 根据用户端发射的信号进行TOA或者AOA，利用信号强度和其他信息来获取定位信息。
   2. WiFi路由能从信道状态信息提取因人体动作所引起的微多普勒频移，从而识别人的行为。

3. 无人机感知与通信

4. 多功能射频系统

5. 雷达辅助的低截获率通信

6. 无源雷达

## 主要研究问题

### RCC

1. 干扰信道估计：非合作式的干扰信道估计方法
2. 发射机设计：同时考虑雷达探测与通信的性能指标
3. 接收抗干扰设计：接收机会同时收到雷达回波和通信信号

## DFRC

1. 雷达通信一体化信息论
2. 雷达通信一体化信号处理（**国内外研究重要**）
3. 雷达通信一体化协议及系统架构设计

## 研究现状

### RCC

1. 机会频谱共享：要求次级用户（通信系统）感知频谱，在未占用时进行传输
2. 干扰信道估计
3. 具有闭式解的预编码方案
4. 基于凸优化方法的预编码设计
5. 接收机设计：接收机在雷达干扰的情况下解调通信信号，或者是在通信干扰的情况下对雷达目标进行估计

### DFRC

1. 雷达通信一体化系统的信息论研究
2. 雷达通信一体化系统的时频域信号处理：设计一种新型复用波形，使之既能携带通信信号，又能用于雷达目标探测
3. 雷达通信一体化系统的空频域信号处理
4. 5G时代的雷达通信一体化
