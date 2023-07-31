---
title: CSI-FREE/Massive IoT Beam rotation scheme
excerpt: CSI-Free Rotary Antenna Beamforming for Massive RF Wireless Energy Transfer.--Onel L. A. L&#x00F3;pez et.al
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306042154618.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - CSI Free
categories:
  - Paper Reading
  - Channel State Information
comment: valine
math: true
hide: false
date: 2023-06-04 21:54:21
---

-------------------------------------

**CSI-Free Rotary Antenna Beamforming for Massive RF Wireless Energy Transfer**.  *Onel L. A. L&#x00F3;pez* et.al.  **IEEE Internet of Things Journal, May15, 15 2022**  ([pdf](https://ieeexplore.ieee.org/document/9520826))  (Citations **1**)

## Quick Overview

M antennas BS (ULA), single antenna IoT device.

> 在EH中，噪声可以忽略。根据引用文章中，噪声为0。

- 提出RAB (Rotary Antenna Beamforming) 的无CSI方案，全方面覆盖并提供$$0.85\sqrt{M}$$的增益。
- 说明至少使用$$M$$等间距步进转子，可以提供准全向的方向图。
- 在已知用户位置信息的情况下，进行功率分配。给出了LP（线性规划）的解决方案和另外一个封闭的闭式结果。
- 考虑其他约束例如SAR（specific absorption rate），避免人体受害。
- RAB对NLoS的鲁棒性以及不同天线拓扑结构的可行性。





## System Model

用户在角度域上均匀分析，距离随机。



AA-SS-1：在ULA的视线/法线方向

AA-SS-2：在ULA的水平方向



## Design of Precoder

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306042154986.png" alt="image-20230604155451194" style="zoom:33%;" />

考虑的beamforming是在整个角度空间中能量最大化的beamforming。其实就是AA-SS-2。==说是在Rician信道上能也能实现最大化==

>在实际上，因为天线都具有一定的方向性，所以在ULA水平方向上的波束其实是有很大衰减的。

以下说明了类似于CSCG的循环对称性，即precoder只改变LoS部分，并不会改变NLoS部分的统计特性。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306042154040.png" alt="image-20230604160445516" style="zoom:33%;" />



maxima只有一个且在90度位置，增益等于$$M$$；==minima有$$M-1$$个==

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306042154963.png" alt="image-20230604160754803" style="zoom:33%;" />

## Average EH gain

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306042154987.png" alt="image-20230604160745284" style="zoom:33%;" />

算出来的天线的平均增益，即上面的$$G(\theta_i)$$在$$2\pi$$范围内积分的平均
$$
\frac{1}{2 \pi} \int_0^{2 \pi} G\left(\theta_i\right) \mathrm{d} \theta_i,
$$
<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306042154971.png" alt="image-20230604162049469" style="zoom:33%;" />

然后再进一步近似为：
$$
\bar{G} \approx 0.85 \sqrt{M}
$$

> 这点要是我不是90度的波束，可以近似吗？积分能求吗？

下图的结论说明在波束对准正面方向的时候反而平均增益是最低的，==这个有点不符合常理。==

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306042154966.png" alt="image-20230604164547248" style="zoom:33%;" />

实际上，这个平均增益是无法被所有用户享受到的，因为存在非常不公平的WET:

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306042154963.png" alt="image-20230604160754803" style="zoom:33%;" />

所以OneL等人想要用步进电机进行旋转，使得这个平均的增益被所有用户享受到。

> 他们文章中也说明了，如果选择旋转电机，很有可能导致旋转电机消耗的能量大于发射机的能量。这又是很大的开销。也是我们相控波束旋转的优势。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306042154439.png" alt="image-20230604171051789" style="zoom:33%;" />

==这个式子代表在一个周期内的平均收益。$$\theta_i$$代表用户的角度，$$G(\theta_i)$$表示在还没有旋转的时候，该用户收到的收益。$$\frac{j\pi}{M}$$代表开始旋转的时候，第$$j$$次旋转带来的收益。==

## Optimization based on location information

因为他们的旋转，在角度上已经是均匀的了，所以只需要考虑在功率分配上->等价于时间分配上。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306042154474.png" alt="image-20230604205509911" style="zoom:33%;" />

就是按距离的分配，最大化最小接收能量：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306042154548.png" alt="image-20230604205738104" style="zoom:33%;" />

Close form不好求，但是可以通过近似来获取：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306042154587.png" alt="image-20230604210044972" style="zoom:33%;" />

这个思路很好理解，其实就是说最大化最小的接收能量。pathloss最大的，就是性能最差的，此时保证这个最差的收到的来自主波束的能量一定，就==保证了在不同旋转过程中，最低的能量收获下界一定。==

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306042154579.png" alt="image-20230604210701348" style="zoom:33%;" />

所以其实就是和所有用户中，在每个beam中最差的那个（path-loss最大），进行功率分配。

---

需要知道用户的location，也就是距离。如果不知道距离，就不好进行。只能多个站进行交叉定位。



## Robustness of NLoS

就画了个图

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306042154618.png" alt="image-20230604212723971" style="zoom:33%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306042154869.png" alt="image-20230604212315021" style="zoom:33%;" />

$$M$$增多，可以提供：

- 更大能量的波束
- 分辨率（更小的波束宽度）
- 更多的旋转角度

使得可控因素增多，性能应该更好，但是复杂度应该会上升。这说明了其Closed form的重要性。



> <img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306042154888.png" alt="image-20230604213853606" style="zoom:33%;" />
>
> 全CSI的旋转方案？一次性只给有限个用户进行传能？



超大规模用户的时候，location信息无用。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306042154103.png" alt="image-20230604214849429" style="zoom:33%;" />

