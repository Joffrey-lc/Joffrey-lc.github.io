---
title: GCN小结
excerpt: 没有添加摘要
index_img: https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211204153907427.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Deep Learning
categories:
  - Paper Reading
  - Graph Convolutional Network
comment: valine
math: true
hide: false
date: 2021-12-04 15:37:47
---

# 入门必看
推荐顺序由简到难：

1. [何时能懂你的心——图卷积神经网络（GCN）](https://zhuanlan.zhihu.com/p/71200936)

2. [知乎Johnny Richards和superbrother的回答](https://www.zhihu.com/question/54504471)

3. [CSDN文章](https://blog.csdn.net/yyl424525/article/details/100058264)

4. 清华大学综述文章：Graph Neural Networks：A Review of Methods and Applications

5. GCN开山之作：Semi-Supervised Classification With Graph Convolutional Networks

# 提出思想及发展
## 提出
对于图（pictures）的处理，CNN是一件大法宝；但是由于CNN处理的对象都是Euclidean Structure，无法对Non Euclidean Structure数据进行处理。图（graph）就是典型的Non Euclidean Structure数据。所以GCN（Graph Convolutional Network）应运而生。

研究GCN的原因，主要可以简答概括为三点（参考知乎[superbrother](https://www.zhihu.com/question/54504471) 的回答）：
1. CNN无法处理Non Euclidean Structure数据（传统的离散卷积在Non Euclidean Structure数据上无法保持平移不变性）
2. 希望在拓扑图结构上有效地提取空间特征来进行机器学习
3. 拓扑连接是一种广义的数据结构，可应用范围广

## 解决方案
因为在Non Euclidean Structure数据中，传统的图像卷积操作（图像上的数据点的加权求和）不能适用，所以要想完成GCN，就需要重新定义卷积操作。
现在的卷积思路有两种：

### 谱域图卷积	
* 根据图谱理论和卷积定理，将数据从空（间）域转换到谱域进行处理
* 有较强的理论基础

因为傅里叶变换的一个重要性质：
*函数$f_1(t)$和函数$f_2(t)$的傅里叶变换，等于二者傅里叶变换的乘积的逆变换*,即：
$$f_1(x)*f_2(x)=\mathcal{F^{-1}[\mathcal{F_1(w)}\mathcal{F_2(w)}]}$$

| 符号                                                         | 定义                 |
| ------------------------------------------------------------ | -------------------- |
| $f_1(x)$、$f_2(x)$                                           | 函数                 |
| $\mathcal{F_1(w)}$、$\mathcal{F_2(w)}$                       | 对应函数的傅里叶变换 |
| 也就是说只要定义了图（graph）的频域变换，就可以推导出图的卷积计算 |                      |
#### 空域图卷积
* 不依靠图谱卷积理论，直接在空间上定义卷积操作（有点CNN那味儿了）
* 定义直观，灵活性强

本周主要了解的是谱域卷积。

## 发展
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200806105645321.png)
<center><b><font size ='2'>Fig1.发展时间线</font></b></center></font>
上图时间轴中，红色的是谱域卷积，蓝色的是空域卷积。

# 重要的结论
ChebNet到GCN的转变是重点。
因为推导过程有点复杂，在此只介绍结论：
| 符号                   | 定义                                   |
| ---------------------- | -------------------------------------- |
| $L=D-A$                | 分别是拉普拉斯矩阵、度矩阵、邻接矩阵   |
| $U$                    | 拉普拉斯矩阵的特征向量（特征分解得到） |
| $\boldsymbol{\Lambda}$ | 拉普拉斯矩阵的特征值（特征分解得到）   |
| $\hat{X}$              | 傅里叶变换结果                         |
* 结论一：
经过一系列复杂证明，我们可以知道Laplacian Matrix 的特征向量$U=(\bar{u}_1,\bar{u}_2,\bar{u}_3,...,\bar{u}_n,)$是n维空间的n个线性无关的正交向量。$U$可以构成一组正交基，且任意信号都可以由此基表示。
* 结论二：
$U$（拉普拉斯矩阵的特征向量）担任了基函数的位置；拉普拉斯矩阵的特征值担任了频率的位置。

由此二结论，可以推导拓展到谱域的傅里叶变换：
Fourier transform ：$\hat{X}=U^TX$
Inverse Fourier transform : $X=U\hat{X}$

由此定义了图卷积：
$$X*_G g = \mathcal{F^{-1}( \mathcal{F}(x)\odot\mathcal{F}(g))}=U(U^Tx\odot U^Tg)$$
其中，$\odot$是hamand积。
# 从ChebNet 到GCN
因为按上式计算，每次都要进行特征值分解，计算量很大。所以使用Chebyshev（切比雪夫）多项式代替谱域的卷积核：
>详见:Convolutional neural networks on graphs with fast localized spectral filtering 一文 
>
>$g_{\theta}=diag(U^Tg)$ ----->$g_{\theta}(\boldsymbol{\Lambda})=\sum^R_{k=0}\beta_kT_k \hat{(\boldsymbol{\Lambda}})$

此方法有以下特点：
1）卷积核只有K+1个可学习的参数，一般 K远小于n，参数的复杂度被大大降低
2）采用Chebyshev多项式代替谱域的卷积核后，经过公示推导，ChebNet不需要对拉普拉斯矩阵做特征分解了。省略了最耗时的步骤。 
3）卷积核具有严格的空间局部性。同时，K就是卷积核的“感受野半径”。即将中心顶点K阶近邻节点作为邻域节点。

关键在于GCN丢ChebNet进行了进一步的简化，它仅考虑一阶的ChebNet,得到一个非常简洁的表达式：
$$x*_G g_\theta=\theta(I_N+D^{-1/2}AD^{-1/2})x$$
> 详见 Semi-Supervised Classification With Graph Convolutional Networks 一文

| 符号     | 定义             |
| -------- | ---------------- |
| $I_N$    | 单位矩阵         |
| $D$、$A$ | 度矩阵、邻接矩阵 |
| $\theta$ | 可学习参数       |

现在还有一个问题，$I_N+D^{-1/2}AD^{-1/2}$的特征值范围[0,2]，在训练过程中可能会出现梯度消失或梯度爆炸，所以要进行归一化：
$$Z = \tilde{D}^{-1/2} \tilde{A}\tilde{D}^{-1/2} X\Theta$$
这就是最终的表达式。其中符号$\tilde{D}=\sum_j \tilde{A}_{ij}$，$\tilde{A}=A+I_N$(可以理解为再归一化的邻接矩阵和度矩阵)
# 应用
在Semi-Supervised Classification With Graph Convolutional Networks一文中，提出一个具有两层的GCN模型：
$$Z=f(X,A)=softmax(\tilde{A} ReLU（\tilde{A}XW^0）W^1)$$
其中$X$是节点特征矩阵，A是邻接矩阵。此GCN模型可以在很少的节点具有标签的情况下，完成节点的分类。

# 缺点
1. 谱域图卷积不能做有向图（无法特征分解）
2. 模型训练期间，图结构不能变
3. 复杂度问题
4. 层数太高会出现Over-Smoothing现象


# TODO LIST
空域图卷积
* GNN
    + 构建邻域（Random Walk）
    + 对邻域节点进行内积
    
    >详见：A Generalization of Convolutional Neural Networks to Graph-Structured Data
*  GraphSAGE
    + 卷积=采样+信息聚合
    
    >详见:Inductive representation learning on large graphs
* GAT
	+ 卷积定义为利用注意力机制对邻域节点有区别的聚合
	
	>详见：GRAPH ATTENTION NETWORKS
*  PGC
	+ 卷积认为是特定的取样函数与特定的权重函数相乘后求和
	
	> 详见：Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action
