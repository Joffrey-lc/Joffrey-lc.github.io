---
title: 大规模无线能量传输综述（能量信道CSI-Free）
excerpt: 综述-Onel L. A. López et.al Massive Wireless Energy Transfer-Enabling Sustainable IoT Toward 6G Era 
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20220319160750316.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - WET
  - WPT
  - SWIPT
categories:
  - Paper Reading
  - Channel State Information
comment: valine
math: true
hide: false
date: 2022-03-19 17:01:01
---

**Massive Wireless Energy Transfer: Enabling Sustainable IoT Toward 6G Era**.  *Onel L. A. López* et.al.  **IEEE Internet of Things Journal, June1, 1 2021**  ([pdf](https://ieeexplore.ieee.org/document/9319211))  (Citations **18**)

## 缩写说明

- DASs: Distributed Antenna Systems

##  Quick Overview



<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20220319160826065.png" alt="WIT和WET结构" style="zoom:67%;" />

**WET系统结构：**WIT和WET/WPT自然而然的会在一起考虑。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20220319160926828.png" alt="BS和PB实现WIT和WET" style="zoom:67%;" />

并且由于WET的路径损耗大，对功率要求高，所以得需要BS+PB才能达到到WIT Zone范围左右的WET Zone



<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20220319161142285.png" alt="WET和WIT的两种实现结构" style="zoom:67%;" />

设计WIT和WET发射机的两种形式，In-band 和Out-of-band。一般选择In-Band。其实就是**时分复用**和**频分复用**。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20220319161254502.png" alt="(a)多天线单PB (b)多PBs单天线 (c)多天线多PBs" style="zoom:67%;" />

在只考虑WET的情况下，上图(a)表示一个PB带有M个天线；(b)表示分布式天线，即一个PB只有一根天线，共M个PBs；下方表示的DAS和EB结合的模式，即4个/8个PBs，每个M/4||||M/8根天线。

**实验结果如图：**

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20220319161530798.png" alt="不同结构性能对比" style="zoom: 67%;" />

- *Single PB (EB):* A PB located at the circle center equipped with *M* antennas.

- *Single-Antenna PBs (DAS): M* single-antenna PBs random and uniformly distributed in the area.

- *Single-Antenna PBs (Optimized DAS –oDAS):* Similar to the single-antenna PBs deployment but the PBs’ locations are set using the well-known *K-means* clustering algorithm [60].

- *Four PBs (EB*+*oDAS):* Four PBs, each equipped with M/4 antennas, are deployed and their locations are set using the *K-means* clustering algorithm.

- *Eight PBs (EB*+*oDAS):* Eight PBs, each equipped with M/8 antennas, are deployed and their locations are set using the *K-means* clustering algorithm.

结论：

1. 没有位置优化（k-means 聚类）的DAS最差，甚至不如单个在圆心的结构
2. 位置优化能够给DAS带来巨大的性能提升
3. DAS+EB的效果更好

## CSI related

分四个部分：

### Partial CSI-Based EB/Statistical CSI

统计CSI，不是瞬时的

- 在大时间内变化， 而不需要频繁更新。
- 有限CSI采集开销和能量消耗得到。
- 更不容易出错（统计的）

**QUESTION：**

- *什么叫做信道的一阶统计信息、二阶统计信息（例如协方差矩阵）？？*

### CSI-Free

不需要CSI，具体有三种算法

- [APS-EMW](https://lcjoffrey.top/2022/03/20/CSI-FREE-Transmit-diversity/)

- [AA-IS/SA](https://lcjoffrey.top/2022/03/27/OnCSIFree/)

- [AA-SS 两种](https://lcjoffrey.top/2022/03/27/OnCSIFree/)

由图可知，APS-EMW和AA-IS/SA策略的物联网节点接收能量都比较发散（均匀）。而AA-SS的两种优化形式都比较具有方向性。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220328152458628.png" alt="image-20220328152458628" style="zoom: 50%;" />

从下图可以看到，APS-EMW的低能量区域比较大，说明它只适用于一些低能量要求的场景。SA是这几种方案中，唯一一种只需要单射频发射链路的，其结构最简单。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220328152530913.png" alt="image-20220328152530913" style="zoom:50%;" />

![image-20220328145642755](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220328145642755.png)

### Positioning-Based

在CSI-Free的基础上，通过位置信息，旋转PB的天线以获得更好的性能

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220328152756402.png" alt="image-20220328152756402" style="zoom:50%;" />

节点空域角度聚类，再进行天线旋转传输能量。AA-SS两种方案都从旋转角度中受益。

### Hybrid

混合模式，结合Perfect CSI、Limit CSI、CSI-free、Positioning-Based EB等。例如在IoT设备电量较低时先通过CSI-Free传输能量，电量得到补充后，可以传输导频，再使用perfect CSI等。
