---
title: IRS + tracking MAP/CS/User Association Strategy/Deep Learning
excerpt: Mobile User Trajectory Tracking for IRS Enabled Wireless Networks/Codebook-Based Training Beam Sequence Design for Millimeter-Wave Tracking Systems/Mobility-Aware User Association Strategy for IRS-Aided mm-Wave Multibeam Transmission Towards 6G
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202304032044710.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - IRS
categories:
  - Paper Reading
  - IRS and Tracking/Beam Tracking
comment: valine
math: true
hide: false
date: 2023-04-03 20:37:50
---

## Mobile User Trajectory Tracking for IRS Enabled Wireless Networks

**Mobile User Trajectory Tracking for IRS Enabled Wireless Networks**.  *Deyou Zhang* et.al.  **IEEE Transactions on Vehicular Technology, August 2021**  ([pdf](https://ieeexplore.ieee.org/document/9479771))  (Citations **3**)



- Mobile User移动使用的是Markov random walk
- Rician channel：说的是假设Rician，实际上是LoS，但是加了一组Rician的实验。
- 依然假设IRS和AP位置固定，所以这段信道认为长时间不变的

- 用pilot symbols 估计Mobile User位置

{% label primary @估计误差会随着观测次数的增多而累计？？？？即观测次数越多，误差越大？ %}



构建MAP（最大后验概率），然后找到上界，最小化上界。使用了两种方式：

- Codebook
- MO： manifold optimization

---

## Codebook-Based Training Beam Sequence Design for Millimeter-Wave Tracking Systems

**Codebook-Based Training Beam Sequence Design for Millimeter-Wave Tracking Systems.** Deyou Zhang et.al. 



<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202304032039799.png" alt="image-20230328200202630" style="zoom:33%;" />

两均匀线阵

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202304032039794.png" alt="image-20230328200228951" style="zoom:33%;" />

$$\mathbf{A}_{UE}$$的每一列，代表了在$$\theta_i,i\in N_{UE}$$下的向量，同理$$\mathbf{A}_{BS}$$中的每一列代表了在$$\theta_j,j\in N_{BS}$$下的向量。等于在做Codebook的时候，将角度分割为$$N_{UE}$$和$$N_{BS}$$份。



因为发射端假设有$$K$$个径，接收端只有1个径，所以：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202304032039876.png" alt="image-20230328200941394" style="zoom:33%;" />

写成压缩感知的形式：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202304032039809.png" alt="image-20230328201009696" style="zoom:33%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202304032039824.png" alt="image-20230328201032853" style="zoom:33%;" />



重点来了，作者说用OMP等方式求解，效率不高。

但是我认为可以丢掉$$\mathbf{A}$$很多全0的列，然后再进OMP。因为$$\delta$$是自己设置的，所以可以知道什么地方的为0。

剩下的一堆分析构造MAP，并最小化错误概率。都可省略。

---

## Mobility-Aware User Association Strategy for IRS-Aided mm-Wave Multibeam Transmission Towards 6G

**Mobility-Aware User Association Strategy for IRS-Aided mm-Wave Multibeam Transmission Towards 6G**.  *Hiroaki Hashida* et.al.  **IEEE Journal on Selected Areas in Communications, May 2022**  ([pdf](https://ieeexplore.ieee.org/document/9681871))  (Citations **8**)

- 搞了个User和IRS的配对。
- {% label primary @不涉及跟踪本身的算法 %}，假设跟踪是完美执行的。
- 主要贡献在于合理分配IRS和用户链接，使得链接的中断概率和平均信道容量取得tradeoff（这个tradeoff是因为，当分配较多的IRS时，信道容量肯定上升，但是由于占用了较多的IRS，使得一旦有中断的情况发生，就没有中断鲁棒性）

BS、IRS、Ues进行详尽的波束扫描以确定最佳波束和User-IRS配对



在二维平面中的位置PDF由下式给出：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202304032046138.png" alt="image-20230329134754663" style="zoom:33%;" />

---

## Deep Learning for Channel Tracking in IRS-Assisted UAV Communication Systems

**Deep Learning for Channel Tracking in IRS-Assisted UAV Communication Systems**.  *Jiadong Yu* et.al.  **IEEE Transactions on Wireless Communications, September 2022**  ([pdf](https://ieeexplore.ieee.org/document/9743298))  (Citations **7**)



- 使用Deep Learning的方法（LSTM）：先预估计信道，再跟踪信道（两个机器学习模型，分别完成上述任务）



有点扯，IRS的相位调整没考虑。

![image-20230403204919147](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202304032049207.png)
