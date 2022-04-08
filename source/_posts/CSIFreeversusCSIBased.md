---
title: CSI-FREE versus CSI-Based
excerpt: Onel L. A. López et.al.-CSI-Free vs CSI-Based Multi-Antenna WET for Massive Low-Power Internet of Things
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220329221305200.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - CSI Free
  - WET
  - WPT
categories:
  - Paper Reading
  - Channel State Information
comment: valine
math: true
hide: false
date: 2022-03-29 22:11:07
---

推导比较复杂， 主要整理了结论，更多信息见[我的论文笔记](.\MyPaperNote.html)

**CSI-Free vs CSI-Based Multi-Antenna WET for Massive Low-Power Internet of Things**.  *Onel L. A. López* et.al.  **IEEE Transactions on Wireless Communications, May  2021**  ([pdf](https://ieeexplore.ieee.org/document/9316281))  (Citations **1**)

## 缩写说明

- HTT: Harvest then Transmit
- HAP: Hybrid Access Point: 可以接收数据or发射能量

## Quick Overview

### assumption

- 构建的是**WPCN模型**，因为在实际中**WPCN**比**SWIPT**更贴近实际：**大量时间都进行WPT/WET，少量时间进行WIT**
- CSI-Free采用**SA策略**，CSI-Based采用**MMSE**和**ZF**进行波束形成（precoding）
- 以最差的（最远的、最大path loss的）节点性能来作为**衡量标准**
- 考虑**Possion Traffic** 和 **Periodic Traffic**两种情况

### Result

- 最远节点比其他节点**多**经历至少3dB的功率衰减时，**MRT波束形成器接近最优**（CSI-Based）
- SA虽然不能提供更高的平均EH增益，**但是提供更大的WIT、WET分集增益**，因为它只用一根天线WET，其余WIT
- **CSI-Free**在**Periodic Traffic**下性能很好，但是在**Possion Traffic**下不太行
- Possion Traffic **存在一个最佳的碰撞概率**
- 在**WPCN**场景中使用**MMSE**比**ZF**好

## 具体内容

### WET Performance

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220329211029929.png" alt="fig. 3" style="zoom: 80%;" />

- CSI-Based（green）随天线数量增多而降低，这是因为波束形成增益随$$|S|$$的增大而减小
- **CSI-Based（Red）是使用MRT对最远（最大path loss）节点进行供电时的下界（最远的节点->最差的能源接收性能），一直都比CSI-Free（Blue）大$$10\log_{10}M_t$$**
- SA和AA-IS虽然看起来性能曲线相同，但是由于SA的成本低（WET单发射链路），且可以WIT分集（只有一根天线做WET，其他的作WIT），所以之后都选择SA
- 当$$|S|\to \infty$$时，CSI-Based（Green）$$\approx$$ CSI-Free（Blue）
- CSI-Free（AA-SS，Yellow and Orange）仅支持某些特定空间（有ERs）



<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220329213211839.png" alt="fig. 4" style="zoom:80%;" />



- （上）Possion Traffic能量中断概率，（下）Periodic Traffic能量中断概率。横坐标表示对每个天线的导频信号进行CSI估计一些列处理所需要的能量
- 因为CSI-Free不需要导频，所以是一根直线；对于CSI-Free大量能量用于CSI，则EH能量减少，以至于能量中断
- 虽然天线数量$$M$$的增加看起来导致**CSI的获取成本增加**，但是多**天线带来的增益**显然比成本**更有好处**
- （下）明显比（上）效率更高：因为下面的确保active的能量是50μw，上面是20μw，意味着同等情况下（下）更容易出现中断

### WIT Performance

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220329213539222.png" alt="fig. 5" style="zoom:80%;" />

- （上）Possion Traffic信息传输中断概率，$$\xi$$为碰撞概率。$$t_s$$为到达时间间隔；$$T_c/\lambda$$是平均到达间隔时间。
- 一般而言，高SINR时，MMSE和ZF性能差不多，但是这边做出来的结果MMSE远好于ZF，e.g. fig 5（上）（因为是低功率第低速率WIT）。

### General Performance

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220329214330457.png" alt="fig. 6" style="zoom:80%;" />

- **（上）Possion Traffic 能量中断概率随碰撞概率曲线，可以看到存在一个最优碰撞概率（（上）中绿色标点）**
- $$M_t\geq M_r$$会得到更好的结果：（上）中$$M_t=M-1$$是最好结果
- Possion Traffic 对非完美SIC比较敏感：（下）中在-70dB就开始上升了（但是意义不大，因为SIC已经比较成熟了）

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220329214856838.png" alt="fig. 7" style="zoom:80%;" />

- （上）（中）Possion Traffic；（下）Periodic Traffic
- **在Possion Traffic中，小$$M$$时SA最好，大$$M$$时，需要CSI-Based结合一个公平的天线分配（$$M_t=M/2$$）**
- **Periodic Traffic中，SA吊打一切。**

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220329215404520.png" alt="fig. 8" style="zoom:80%;" />

- （上）Possion Traffic 能量中断概率是一个和**信息解码所需能量$$\tilde{\xi}_0$$**和**对导频信号一些列处理所需能量$$\xi_0$$**有关的函数（完美CSI的前提下）；
- （下）非完美CSI性能对比$$\tilde{\xi}_0$$太小，影响信息中断（信息解码不太行），太大，影响能量中断（没什么能量给EH了）

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220329220615250.png" alt="fig. 9" style="zoom:80%;" />

- （上）信息中断性能随平均到达间隔时间（Possion Traffic）曲线；（下）信息中断性能随到达间隔时间（Periodic Traffic）曲线
