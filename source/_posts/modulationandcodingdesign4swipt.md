---
title: 阅读笔记-Modulation and Coding Design for Simultaneous Wireless Information and Power Transfer
excerpt: SWIPT相关阅读
index_img: >-
 https://img-blog.csdnimg.cn/img_convert/149477c0dc394a332caeea51db437e80.png
banner_img: 'https://img-blog.csdnimg.cn/img_convert/149477c0dc394a332caeea51db437e80.png'
tags:
  - SWIPT
categories:
  - Paper Reading
  - Simultaneous Wireless Information and Power Transfer
comment: valine
math: true
hide: false
date: 2022-02-26 15:45:41
---

## 缩写说明

- WPT: wireless power transfer
- WIT: wireless information transfer
- SWIPT: simultaneous wireless information and power transfer, coordinating WIT and WPT in the same RF spectral band thus yields the research of SWIPT

## Contributions

- Introduce the popular transceiver architecture of SWIPT
- unary code and run-length-limited (RLL) code in SWIPT. These two codes can show the trade-off between WIT and WPT performance
- The impact of wireless channels and hardware constraints on the practical modulation design in the SWIPT system is studied for a single user scenario.
- The principle of the modulation design in multi-user SWIPT systems relying on the superposition symbols is introduced.
- Open problems concerning the modulation and coding design in the SWIPT system are envisioned.



## 收发机结构

![trancevier](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/149477c0dc394a332caeea51db437e80.png)

## SWIPT接收机

接收机由两个部分，分别用作WIT和WPT。RF信号被接收机接收后，根据一定规则用作WIT和WPT。现有成果都主要研究收发机结构，很少研究编码和调制的影响。

### 非线性整流

只有当信号功率大于一定**阈值**，才会激活接收机的整流器电路，才会接收能量。



## 编码与SWIPT

![coding with SWIPT](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/006b17b4138c9d95b731f764a4715a8e.png)

结合上图，同一种调制方式2ASK(OOK)，因为编码后的码元不同，导致波形不同，根据上面接收机的设计，携带的能量也不同。给设备充电的能力也不同。**但是要注意能量不宜过高，造成能源浪费，也不宜过低，造成设备能源短缺。**

所以传输能量和信息之间有一个trade-off：

1. 无论传什么信息，编码都是全1，能量达到最大值，但是互信息为0（意味着接收机并不能接受到有用的信息）

   从信息论的角度而言，因为有$H(x)=H(X|Y)+I(X;Y)$

   其中$H(x)$是原本信宿有的信息量，$I(X;Y)=0$，则信道损失熵$H(X|Y)=H(X)$，意味着信息全部丢失。

2. 如果完全考虑WIT，则可能不满足WPT的要求，或者说WPT不可控？

基于此，有一些可用的编码方式（这些编码本身也就存在WIT和WPT的trade-off）：

**Compensation Energy Coding:** Dummy binary  bits are directly concatenated behind information bits in order to guarantee that the resultant  codeword has a certain percentage of bit “1.”  This coding approach has the lowest complexity. However, the dummy bits do not carry any  information, which may thus degrade the WIT  performance.
**Inverse Source Coding:** A classic source  encoder takes non-equi-probable messages to  generate binary sequences having equi-probable  binary bits. By contrast, an inverse source encoder  takes equi-probable messages to generate binary  sequences having certain structures for satisfying  the WPT requirement. However, the asynchronization between the encoder and the decoder imposes difficulties in the efficient decoding design.
**Constraint Coding:** Some constraint coding  techniques have degrees of freedom to change  the codeword structure for satisfying the WPT  requirement. Since they do not include any  dummy bits, the WIT performance may not suffer  significant degradation. Furthermore, the efficient  symbol-level trellis can be adopted for decoding  the constraint code.

以及文章中介绍的两种约束编码：

**Unary Code:** The unary encoder maps the j-th input binary  sequence onto a j-bit codeword, which has a  single bit “0” at the end and all the other bits in  front are “1.” For instance, the four-level unary  encoder is capable of encoding four different binary sequences {00, 01, 10, 11}. The first  input sequence ‘00’ is encoded as a codeword  ‘0’, while the fourth input sequence “11” is thus  encoded as a codeword “1110”. Obviously, a  different input binary sequence may be encoded  as a codeword having a different percentage of  energy bit “1.” Therefore, the average percentage of energy bit “1” in unary codewords can be  adjusted by changing the occurrence probabilities  of the input binary sequences, which hence controls the SWIPT performance of the codewords.

**Run-Length-Limited Code**:  Another constraint coding technique is the RLL  code [12]. A type-0 (d, k)-RLL code has the following constraints on a codeword: • The runs of bit “0” have a length of d at least  between successive bit “1.” • The runs of bit “0” have a length of k at most  between successive bit “1.” The run-length of bit “0” may be an arbitrary  value between d and k. For instance, a type-0 (1,  3) RLL code is capable of generating a binary bit  sequence of “10100010010001001 …,” where  the minimum run-length of bit “0” is 1 and its  maximum run-length is 3. Obviously, the average  percentage of energy bit “1” in a type-0 RLL codeword is determined by the occurrence probabilities  of the runs of bit “0” having different lengths. For  instance, if a type-0 (1, 3) RLL encoder increases  the occurrence probability of the runs of bit “0”  having a length of 1, the average percentage of  energy bit “1” can be thus increased. Therefore,  by adjusting the occurrence probabilities of the  runs of bit “0” having different lengths, we may  control the SWIPT performance of the type-0 RLL  codewords. For a type-1 RLL encoder, we should  focus on adjusting the occurrence probabilities of  the runs of bit “1” having different lengths in order  to control its corresponding SWIPT performance.

都是通过约束0-1出现的百分比，来控制WIT和WPT的权衡。

## Battery-Aware Design

因为编码-调制后，所带有的能量不宜过高，也不宜过低。过高会导致能量溢出，过低会导致设备能源短缺。所以在满足最低的信息传输性能后，需要考虑最小化电池过满概率和下溢概率。

## 调制与SWIPT(Single-user)

![signal power and threshold](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/c8ce5d538e20380058d694e86ecafa47.png)

因为整流要设置一定阈值，16-PSK全部不能收集能量（如果阈小于平均功率，16-PSK最好），16-QAM有四个符号超过了阈值（红圈）

**高阶调制方案往往具有更好的WPT性能**

另外，一些干扰，例如多径，会降低WIT性能，但是提高WPT性能。

## 调制与SWIPT(Multiple-user)

![constellation rotation](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/ce492042e336b8ee78f5d86b0930f953.png)

通过旋转星座图（如上图（下））来实现多用户时符号的叠加。图（上）的传统叠加方式，与原始符号相比，得到的叠加符号能量损失较大，导致WPT性能下降。而如图（下）的旋转，WPT性能满足，但是会损失一定的WIT性能（因为符号之间的最小欧式距离减小）。

## Future Challenges

The following open problems still need our further investigation.
**Concatenated Code:** A concatenated encoder  consisting of a source encoder, channel encoder and an energy encoder should be carefully  designed, while a powerful iterative decoder is  also required for processing the sophisticated  concatenated codewords.
**Coded Modulation:** The bit-to-symbol mapping from the binary bits to the modulated symbols has to be designed by jointly considering the  codeword structure and the modulation characteristic in order to satisfy both the WIT and WPT  requirements.
**Adaptive Modulation:** In order to exploit the  distinctive WPT and WIT features of a specific  modulation scheme, we should design an adaptive modulation scheme by considering the wireless channel characteristics, the non-linear rectifier  and the diverse SWIPT requirements.
