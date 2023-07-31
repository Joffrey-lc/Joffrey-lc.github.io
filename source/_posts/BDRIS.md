---
title: Beyond Diagonal Reconfigurable intelligent surface
excerpt: BD-RIS versus D-RIS
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051603067.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - RIS
  - IRS
categories:
  - Study field
comment: valine
math: true
hide: false
date: 2023-06-05 15:53:49
---

[胡老师让我调研的BD-RIS](https://sites.google.com/view/ieee-comsoc-rcc-sig-bdris/home)



是否可以利用酉矩阵的特点来进行计算？因为约束条件变成了$$\boldsymbol{\Theta}\boldsymbol{\Theta}^H = \mathbf{I}_n$$，就是个酉矩阵。

## Overview

- D-RIS: diagonal RIS (D-RIS)，调整的相移是对角阵。等价于每个单元之间的相位是独立的，解耦合的
- BD-RIS: Beyond diagonal RIS (BD-RIS)，调整的相移不再是对角阵，等价于每个单元之间的相位调整非独立。



BD-RIS会增加额外的电路复杂性，但是会提高RIS的灵活性和性能（相比于D-RIS）。

信道估计会更困难，目前而言需要分别知道两个信道

- BD-RIS控制幅度和相位：==幅度控制体现在，不损失信号的情况下进行能量分配==
- BD-RIS可以透射、混合式、扇区工作、==Non-diagonal==。产生高方向性波束并实现全空间覆盖
- ==考虑调整相位离散时，BD-RIS分辨率更高==
- 相同性能下，BD-RIS需要的单元数更少（相较于D-RIS）
- ==i.i.d fading情况下，fully- 优于 single-connected；在LoS下fully- 和 single- 性能相同==

![image-20230605135001776](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051553185.png)

## BD-RIS

### fully-connected

其实就是fully-connected RIS：

4 elements RIS ：

- single connected RIS
- fully connected RIS

==因为约束不再和single-connected一样：single-要求每个element反射幅度为1，但是fully-要求总的，所以存在了可控的幅度==

![image-20230605135853521](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051553244.png)

### Group-connected 

然后，因为这样做可能会使得大量阻抗被使用，所以可以考虑分组：

![](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051553218.png)

### 小结

形成了group diagonal matrix。

到目前为止，可以考虑RIS分为三个结构：

- 广泛研究的single connected
- Fully-connected
- group-connected

==最上面的是一般化的模型，比较少人再研究，因为考虑了硬件的耦合等因素，比较复杂。==

![image-20230605140713918](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051553222.png)

---

接收功率的好处：

==目前他们的设计方案都是简单的MRC等，没有过多的考虑优化问题==

![image-20230605141105995](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051553213.png)

> - 在i.i.d fading的情况下，fully-connected 功率增益更高（即在每个elements上有不同的缩放$$\alpha$$）
> - 在LoS的情况下，二者相同。（或者说满足右下角的那个等式，Receiver-IRS的channel和IRS到Transmitter的channel元素模值只差一个常系数）



group connected 是single to fully的中间带

![image-20230605141652962](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051553168.png)

![image-20230605141930231](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051553078.png)

## Grouping Strategy

group-connected 在复杂度和power gain之间取trade-off，所以关注这个方案，可以考虑分组的形式：

- CG：受到相同/相关的衰落的被分到一起
- UG：受到不同的被分在一起
- OG：==最大化接收功率？？？？==这个和分组有什么关系？？

![image-20230605142156811](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051553273.png)

![image-20230605142749128](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051427415.png)

所以说就是在研究那些elements，怎么连接性能最好。

## 离散

==在离散的时候，fully-connected可以实现与连续的相同的性能。（蓝色线是连续，即离散的upper bound）==



![image-20230605143235447](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051553739.png)

## 反射+透射

![image-20230605143733091](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051553410.png)

从原本4天线反射的结构，变成了2反射2投射。这种结构其实并不改变电路。仅仅是把左侧的group 1 顺时针旋转90°。

混合模式也有点意思，

![image-20230605144102555](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051553542.png)



其实就是：

- $$\mathbf{G}$$信道共用，$$\mathbf{H}_1$$和$$\mathbf{H}_2$$单独，并且各自享有一个反射相位$$\boldsymbol{\Phi}_1,\boldsymbol{\Phi}_2$$

![image-20230605144637149](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051553524.png)

![image-20230605144938722](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051449044.png)

然后考虑刚刚说的single-, fully-, group-connected model

![image-20230605145333903](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051554743.png)

通过置零其中一个相移矩阵，等价于设计透射、反射、混合

![image-20230605145505861](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051553983.png)

![image-20230605145636437](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051456715.png)



## Sector-full space coverage

![image-20230605150155588](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051554904.png)



## Non-diagonal 

https://ieeexplore.ieee.org/document/9737373

![image-20230605150604709](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051554983.png)

==可以用来很好地解决幅度和相位耦合的问题：灵活地调整反射的相位，以实现反射相位幅度的最大化==

- 先计算每个单元+理想相位后的反射相位
- 然后对于设计好的波束赋形码本，进行最小化的量化误差的优化

因为量化到实际的相位后，量化误差越大，幅度损失越高。

然后可以做：

- 考虑完美相移：保证反射相位（波束对准）的情况下的结果
- 考虑完美幅度：保证反射幅度（波束可能没对准，但是反射的相位很准）的情况下的结果

## Conclusion

![image-20230605152344928](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202306051523142.png)
