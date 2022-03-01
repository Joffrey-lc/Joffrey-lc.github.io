---
title: 知识储备-空间调制
excerpt: 空间调制SM介绍
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220301101910095.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - spatial modulation
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2022-03-01 11:17:54
---

# 空间调制

## 基本原理

空间调制（Spatial Modulation,SM）将一部分的比特信息隐含在发射天线的索引当中，在一定程度上拟补了频谱效率的损失。**是一种单射频链的系统**。

每次仅仅激活比特信息所映射的特定天线传输数据，从而避免了多天线间的干扰。

![SM结构示意图](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220301101910095.png)

输入的原始比特信息被分为两部分：

- 一部分映射为天线序号，用来选择被激活传输数据的物理天线，称为**空间比特**
- 一部分映射为APM符号，采用QAM/PSK调制，称为**符号比特**

每个时隙，仅有一根特定天线被激活用于传输特定的符号，其余天线则处于闲置状态，或者说发射的信号为0。

## 数学模型

假设如上图所示的一个$N_r\times N_t,N_t=2^{b_1}$的SM系统，其中$N_r$和$N_t$分别为接收和发射的天线数量，$b_1$为空间比特数。采用$M$阶数字调制，$M=2^{b_2}$，$b_2$为符号比特数目。所以单个时隙里传输的比特数为$B$:
$$
B=b_1+b_2=\log_2(N_t)+\log_2(N_r)
$$
将原始比特信息分为数量为$\log_2(N_t)$和$\log_2(M)$两部分，分别映射激活天线序号和APM符号。假设此时隙里被激活的天线序号为$i$，APM符号为$x_k$，其中$i\in\mathcal{A}=\{1,2,\cdots,N_t\}$，$k\in\mathcal{B}=\{1,2,\cdots,M\}$，此时发射信号可以表示为：
$$
\textbf{x}=\left[
\begin{matrix}
0&\cdots&\mathop{x_k}\limits_{i-th}&\cdots0
\end{matrix}
\right]^T
$$
发射信号$\textbf{x}$是一个稀疏向量，其中只存在一个非0元数$x_{k}$，由符号比特映射，而该元素的位置为$i$，对应着第$i$根发射天线，由空间比特所决定。其余0元素表示剩余未激活的天线不发送任何信号。

定义MIMO瑞利衰落的信道矩阵$\textbf{H}\in\mathbb{C}^{N_r\times N_t}$如下：
$$
\begin{align}
    \textbf{H}=&\left[\begin{array}{cccc}\textbf{h}_1&\textbf{h}_2&\cdots&\textbf{h}_{N_t}\end{array}\right]
    \\=&
    \left[
    \begin{array}{cccc}
    h_{11}&h_{12}&\cdots&h_{1N_t}\\
    h_{21}&h_{22}&\cdots&h_{2N_t}\\
    \vdots&\vdots&\ddots&\vdots\\
    h_{N_r1}&h_{N_r2}&\cdots&h_{N_rN_t}
    \end{array}
    \right]
\end{align}
$$
其中$\textbf{h}_l,l\in\mathcal{A}$，表示第$k$根发射天线与接收天线之间所对应的信道向量，其中包含$N_r$个元素，每个元素为信道的衰落系数，且都服从均值为0，方差为1的复高斯分布$\mathcal{C}\mathcal{N}(0,1)$。在经过无线信道后，接收信号矢量可以表示如下：
$$
\begin{align}
\textbf{y}=\sqrt{\rho}\textbf{H}\textbf{x}+\textbf{n}
\end{align}
$$
其中$\rho$表示系统的发射功率，$\textbf{n}$表示加性高斯白噪声向量，其中每个元素均服从高斯分布$\mathcal{C}\mathcal{N}(0,1)$。



## 缺陷及应用限制

优势：

- 单射频链
- 无天线间的干扰
- 合理利用空域资源
- ......

缺点：

- RF链和发射天线之间需要频繁切换，在信息速率时可能无法实现
- 增加天线可以增加空间比特数，但是导致空间星座点变多，星座点之间的欧式距离减少，空间调制性能下降。
- 仅有接收分集，没有发射分集。

