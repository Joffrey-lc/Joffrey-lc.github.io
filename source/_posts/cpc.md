---
title: Representation Learning with Contrastive Predictive Coding梳理
excerpt: 阅读解析CPC
index_img: https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/be8d1c3abdacb2f159997d74695c8d11.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Deep Learning
categories:
  - Paper Reading
  - Self-Supervised Learning
comment: valine
math: true
hide: false
date: 2021-12-04 14:27:41
---

一种通用的无监督学习方法——对比预测编码。通过自回归模型预测潜在空间（高维空间）的未来，以学习高级表征。在训练阶段不涉及具体下游任务。

[原文](https://arxiv.org/pdf/1807.03748.pdf)
参考：https://zhuanlan.zhihu.com/p/129076690

## 主要贡献

1. 将高维数据压缩到更加紧密的潜在嵌入空间，这个空间中条件预测更容易建模。
2. 在这个潜在空间中使用强大的**自回归**模型来做多步未来预测。
3. 损失函数依靠噪声对比估计，这是与自然语言模型中用于学习词嵌入类似的方式，需要整个模型以端到端的形式进行训练。将最终的模型（对比预测编码，CPC）用在了很多不同的数据模态中，包括图像、语音、自然语言和强化学习，结果表明同样的机制在每一个领域中都学到了有趣的高级表征，而且优于其他方法。

![image-20210908124633513](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/be8d1c3abdacb2f159997d74695c8d11.png)

对于输入样本$x_t$，有一个非线性编码器$g_{enc}$将其映射为潜在表示序列$z_t=g_{enc}(x_t)$；对于$t$时刻之前的所有$z_{t'},t'<t$有一个自回归模型(e.g. GRU)$g_{ar}$推断得到当前时刻的$c_t$，利用对当前时刻的推测$c_t$，推断(用一个矩阵$W_k$进行映射)得到后面几个时刻的潜在表示序列的映射**（预测值）**$z'_{t+1}$、$z'_{t+2}$、$z'_{t+3}...$；将真实的$x_{t+1}$、$x_{t+2}$、$x_{t+3}...$通过$g_{enc}$得到的潜在表示序列**（真实值）**做损失函数，达到收敛。最后利用$c_t$完成下游任务。

## 衡量$x$和$c$的相关性

互信息可以很好的衡量相关性：

$$I(x;c)=\sum\limits_{x,c}p(x,c)log\frac{p(x|c)}{p(x)}$$

但是由于不方便计算（可见MINE.md），作者采用一个正比于$\frac{p(x|c)}{p(x)}$的函数$f_k(x,c)$来代替，即：

$$f_k(x_{t+k}, c_t)\propto \frac{p(x_{t+k}|c_t)}{p(x_{t+k})}$$

然后这个$f_k(x_{t+k}, c_t)$函数的具体计算表达式为:

$$f_k(x_{t+k}, c_t)=exp(z^T_{t+k}W_kc_t)$$

我觉得应该才开看，第一步是$W_k^Tz_{t+k}$，用一个Linear层将$z_{t+k}$映射到与$c_t$同Size；第二步做$W_k^Tz_{t+k}$和$c_t$的内积，即$(W_k^Tz_{t+k})^T$$c_t$，展开为$z^T_{t+k}W_kc_t$；第三步做指数运算。

## 衡量互信息

经过一系列证明，可以得到：

$$I(x_{t+k};c_t)\geq log(N)-\mathcal{L}_N$$

其中$\mathcal{L}_N$为：

$$\mathcal{L}_N=-\mathop{\mathbb{E}}\limits_{X}[log\frac{f_k(x_{t+k}, c_t)}{\sum_{x_j\in X}f_k(x_j,c_t)}]$$

可见最小化$\mathcal{L}_N$即可完成最大化互信息量的下界。

其中，$p(x_{t+k},c_t)$ 指的是正在选用信号的片段$x_t$（正样本），而$p(x_j)$指的是我们可以随便从其他的声音信号里选择一个片段（负样本）。这就是**对比**的体现。

对$\mathcal{L}_N$反向梯度传播即可完成整个算法。

文章中还涉及了对图像、自然语言、语音的不同形式的信号的建模，有需要可以查看原文。
