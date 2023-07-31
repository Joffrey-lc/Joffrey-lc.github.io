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

推导比较复杂， 主要整理了结论，更多信息见[我的论文笔记](https://pan.baidu.com/s/1a0zqoWzu4MSEqukP2D-AYA?pwd=0623)

**CSI-Free vs CSI-Based Multi-Antenna WET for Massive Low-Power Internet of Things**.  *Onel L. A. López* et.al.  **IEEE Transactions on Wireless Communications, May  2021**  ([pdf](https://ieeexplore.ieee.org/document/9316281))  (Citations **1**)

## 缩写说明

- HTT: Harvest then Transmit
- HAP: Hybrid Access Point: 可以接收数据or发射能量

## 参数说明

参数说明：

- $$T_c$$相干时间
-  $$t/t_c$$??,$$t_s$$：periodicity of periodic traffic应该是指整个系统的周期，$$t$$应该是一个slot占据的时间。
- channel gain $$\beta_i$$, path loss $$1/\beta_i$$
- 上行channel $$\mathbf{h}_i^{(u)}$$, 下行$$\mathbf{h}_i^{(d)}$$，都是Rician，Rician factor $$\kappa$$
- $$p_c$$ units power to keep active， $$p_i$$ denotes the fixed transmit power of $$s_i$$，$$\xi_{csi}^{(u)}$$，$$\xi_{csi}^{(d)}$$ represent the energy resources (power$$\times$$ time) used by EH node (EH在两个阶段uplink 和 downlink阶段让HAP知道信道的能量开销)，所以$$\xi_{csi}^{(u)}<\xi_{csi}^{(d)}$$，因为uplink EH transmit pilot signals ，而在downlink EH 需要decoding\processing 再transmit。

- sup：supremum，中文叫上确界。sup(S)是指集合S的上确界，即大于或等于S的所有元素的最小值， 这个数不一定在集合S中。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202307062202307.png" alt="image-20230706113003210" style="zoom:33%;" />

## Quick Overview

HAP: Hybrid Access Point: 可以接收数据or发射能量



WET in downlink and **periodic** or **Poisson-traffic** WIT in the uplink



CSI-available：MRT is close to optimum whenever the  



WET长时间的，WIT零星的。所以WPCN可能更实际。



例如SA的上行解码，一根天线下行传输能量，其余的都进行信息解码（收信号），使用ZF或者MMSE。MMSE比ZF好。

==Periodic traffic 和 Poisson traffic都不适用于表征突发任务==(我理解中的Poisson是表述突发任务的)



MRT的最佳体现在，知道信道信息的情况下，当最差的性能比其他差3dB时，MRT是最优的（最公平的）。



周期性或者Poisson流，Poisson流下的性能会下降。提出了优化问题来找到最佳的导频重复使用因子。



对比CSI-based和CSI-free：CSI-free在Poisson下不行，在周期下不错。



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

## Wireless Energy Transfer

gain from EB decrease quickly as the number of ERs increases, and this hold even without accounting for the considerable energy resources demanded by CSI acquisition.

所以进行广播式的无线能量传输是可行的。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202307062202918.png" alt="image-20230704111603425" style="zoom:33%;" />

这个模型可以参考，一部分天线用作传能，一部分天线用作通信解码。==不考虑天线之间的干扰？==原文中假设可以干扰消除。

### Evaluation of outage probability

定义outage probability: 

1. 能量没有收集够$$\mathcal{O}^{(d)}_i$$
2. 能量收够了但信息解码失败$$\mathcal{O}^{(u)}_i$$

所以outage probability为$$\mathcal{O}_i=1-(1-\mathcal{O}_i^{(u)})(1-\mathcal{O}_i^{(d)})$$

整个network的性能指标为最差的性能：<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202307062202802.png" alt="image-20230705141110353" style="zoom:33%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202307062202946.png" alt="image-20230705141252059" style="zoom:33%;" />

由于都比较小，所以可以忽略掉乘积项，单独检查$$\mathcal{O}^{(d)}_i$$和$$\mathcal{O}^{(u)}_i$$即可

---

### CSI-based

#### outage probability

MRT下，Periodic traffic

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202307062202912.png" alt="image-20230706202201989" style="zoom: 33%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202307062202875.png" alt="image-20230706202213234" style="zoom: 33%;" />

MRT下，Poisson traffic

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202307062202915.png" alt="image-20230706202243172" style="zoom: 33%;" />

#### MRT的最优性

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202307062202252.png" alt="image-20230706155110231" style="zoom:33%;" />

==We resorted to simulation and standard fitting procedures, and found out that==

根据(9)，只有$$\mathbf{w}_1\neq \mathbf{0}$$,

通过分析对最差的node使用MRT，对其他node的影响发现（求不出来用拟合），得到$$\Omega=\inf _{s_i \in \mathcal{S} \backslash s_{i^{\prime}}}\left\{\mathbb{E}\left[E_i^{\mathrm{rf}}\right]\right\} / \mathbb{E}\left[E_{i^{\prime}}^{\mathrm{rf}}\right]$$，这个表达式的意义在于，除去$$s_{i'}$$后，最差的下界与$$\mathbb{E}[E_{i^{\prime}}^{\mathrm{rf}}]$$的比值大于1，则说明没有比$$\mathbb{E}[E_{i^{\prime}}^{\mathrm{rf}}]$$差的了，那么MRT并没有使得其他的变得更差，并且还使得对于$$s_{i'}$$更好，那么MRT就是最佳的。

但是值得说明的是，由于这里是均值，所以对于实际的真实值而言，不一定是最佳的，而是至少有一半的时间是最佳的。换句话说，即使$$\inf _{s_i \in \mathcal{S} \backslash s_{i^{\prime}}}\left\{\mathbb{E}\left[E_i^{\mathrm{rf}}\right]\right\} / \mathbb{E}\left[E_{i^{\prime}}^{\mathrm{rf}}\right]>1$$，但是$$\inf _{s_i \in \mathcal{S} \backslash s_{i^{\prime}}}\left\{E_i^{\mathrm{rf}}\right\} / E_{i^{\prime}}^{\mathrm{rf}}>1$$不一定都满足，但可以肯定的是，至少有一半的时间是满足的（PDF的角度而言）。

---

==我可以求一个精确解，求概率分布==

---

对于LoS channel，

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202307062202446.png" alt="image-20230705144733339" style="zoom:33%;" />

当worst node path-loss至少比其他的多3dB，则MRT在一半以上的时间是最优的。

==在LoS信道下的结果可以作为我后面文章的主体==

### CSI-free

#### outage probability

CSI-free的outage probability可以由CSI-based的推导得到，分别取

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202307062202386.png" alt="image-20230706201039910" style="zoom:33%;" />

而且这是一个准确解，而不是下界。

#### performance versus CSI-based

从mean来看，CSI-based比CSI-free大$$M$$倍

但是对于大规模用户，CSI-based的结果会接近与CSI-free。==解释的角度和我们之前的不一样==

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202307062202635.png" alt="image-20230706201428493" style="zoom:33%;" />



## Wireless Information Transfer

Successive Interference Cancellation (SIC)消除天线之间的干扰。导频正交（orthogonal pilot）

ZF:

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202307062202547.png" alt="image-20230706203334694" style="zoom:33%;" />

MMSE:

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202307062202619.png" alt="image-20230706203418662" style="zoom:33%;" />



---



## Numerical Results

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
