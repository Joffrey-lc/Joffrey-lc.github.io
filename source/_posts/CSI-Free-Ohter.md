---
title: CSI相关其他文献阅读
excerpt: 整理了一些没有精读或者读不太懂的文章主要贡献，方便以后查阅。
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/infinity-1647319.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Sketchy Reading
categories:
  - Paper Reading
  - Channel State Information
comment: valine
math: true
hide: false
date: 2022-04-08 10:52:12
---

---

**Ultra-Low Latency, Low Energy, and Massiveness in the 6G Era via Efficient CSIT-Limited Scheme**.  *Onel L. A. Lopez* et.al.  **IEEE Communications Magazine, November  2020**  ([pdf](https://ieeexplore.ieee.org/document/9269936))  (Citations **9**)



总结了一些主要的**CSI在发射端获取的限制**，展望如何设计CSIT-limited scheme，然后提出future work。

- 依靠统计CSIT
- 使用基于位置的策略来有效分配导频序列

-------------

**A Low-Complexity Beamforming Design for Multiuser Wireless Energy Transfer**.  *Onel L. A. López* et.al.  **IEEE Wireless Communications Letters, Jan.  2021**  ([pdf](https://ieeexplore.ieee.org/document/9184149))  (Citations **4**)



**数学推导太多，目前看不懂**，提出一种优化方法（Ultra-Low Latency, Low Energy, and Massiveness）

- 只利用信道的一阶统计量CSI-limited
- 提出了一种低复杂度但有效的EB算法，可以获得接近最优结果（在低$$\kappa$$时甚至优于最优（全CSI））
- 多用户性能随天线数目的增加而提高，同时可以利用旋转天线来获得更好的性能
- **可以直接适用于WPCN和SWIPT**

---

