---
title: 多个WET Stations情况下非线性EHmodel的凸性
excerpt: Yuan et.al.--Convexity Analysis of Nonlinear Wireless Power Transfer with Multiple RF Sources
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20211203212547096.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - convexity
categories:
  - Paper Reading
  - Wireless Energy Transfer
comment: valine
math: true
hide: false
date: 2022-07-11 17:55:50
---

**Convexity Analysis of Nonlinear Wireless Power Transfer with Multiple RF Sources**.  *Xiaopeng Yuan* et.al.  **IEEE Transactions on Vehicular Technology, 2022**  ([pdf](https://ieeexplore.ieee.org/document/9808171))  (Citations **0**)

## Quick Overview

- 用Bruno给的能量收割模型，进行分析多个WET Stations联合供能的情况下，结合非线性，分析最终接收能量和入射能量的关系（最终接收能量对于入射能量的倒数是凸的）
- 多个WET stations 联合优化，就意味着可以通过在多个独立信号之间进行功率分配，这就是一个新的优化方向。

## System model

单个能量接收：
$$
\begin{aligned}
e^{\frac{R_{\mathrm{L}} I_{\mathrm{out}}}{n v} t}\left(I_{\mathrm{out}}+I_{s}\right) & \approx I_{s}+\sum_{i=1}^{n_{0}} \bar{k}_{i} R_{\mathrm{ant}}^{\frac{i}{2}} \mathbb{E}\left\{y_{\mathrm{in}}^{i}\right\} \\
& \approx I_{s}+\sum_{i=1}^{n_{0}} \beta_{i} \mathbb{E}\left\{y_{\mathrm{in}}^{i}\right\}
\end{aligned}
$$
然后得到：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220711164729354.png" alt="image-20220711164729354" style="zoom:33%;" />

最终得到单个的表达式：
$$
P_{\mathrm{dc}}=I_{\mathrm{out}}^{2} R_{\mathrm{L}} \approx\left(\frac{1}{a} W_{0}\left(a e^{a I_{s}}\left(I_{s}+\sum_{i=1}^{n_{0}} \beta_{i} \mathbb{E}\left\{y_{\mathrm{in}}^{i}\right\}\right)\right)-I_{s}\right)^{2} R_{L}
$$

## Main Idea

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220711165511715.png" alt="image-20220711165511715" style="zoom:33%;" />



由于
$$
I_{\mathrm{out}} \approx \frac{1}{a} W_{0}\left(a e^{a I_{s}} \varphi(\mathbf{Q})\right)-I_{s}
$$
且其Hessian矩阵为：
$$
\nabla_{\mathbf{u}}^{2} I_{\text {out }}(\mathbf{Q})=\frac{1}{\left(a \varphi(\mathbf{Q})+e^{a I_{\text {out }}(\mathbf{Q})}\right) \varphi(\mathbf{Q})}\left(\nabla_{\mathbf{u}}^{2} \varphi(\mathbf{Q}) \cdot \varphi(\mathbf{Q})-\nabla_{\mathbf{u}} \varphi(\mathbf{Q}) \cdot \nabla_{\mathbf{u}}^{T} \varphi(\mathbf{Q})+\frac{e^{2 a I_{\text {out }}(\mathbf{Q})} \nabla_{\mathbf{u}} \varphi(\mathbf{Q}) \cdot \nabla_{\mathbf{u}}^{T} \varphi(\mathbf{Q})}{\left(a \varphi(\mathbf{Q})+e^{a I_{\text {out }}(\mathbf{Q})}\right)^{2}}\right)
$$
所以有$$\varphi(\mathbf{Q})>0$$，且当满足
$$
\nabla_{\mathbf{u}}^{2} \varphi(\mathbf{Q}) \cdot \varphi(\mathbf{Q})-\nabla_{\mathbf{u}} \varphi(\mathbf{Q}) \cdot \nabla_{\mathbf{u}}^{T} \varphi(\mathbf{Q})
$$
为半正定的时候，$$I_{out}(\mathbf{Q})$$对于$$\textbf{u}$$是凸的。其实等价于$$f(\mathbf{Q}(\mathbf{u}))$$的Hessian矩阵是半正定的。

换句话说，保证$$f(\mathbf{Q}(\mathbf{u}))=\ln \varphi(\mathbf{Q}(\mathbf{u}))$$对于$$\mathbf{u}$$是凸的，$$I_{out}$$就是对于$$\mathbf{u}$$是凸的，而$$P_{dc}=I^2_{out}R_L$$也就是对于$$\mathbf{u}$$是凸的。



<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220711172804587.png" alt="image-20220711172804587" style="zoom:33%;" />

取$$u_{m}=\ln Q_{m} \text {, i.e., } Q_{m}\left(u_{m}\right)=e^{u_{m}}, \forall m \in \mathcal{M}$$

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220711173039702.png" alt="image-20220711173039702" style="zoom:33%;" />

然后证明了$$g(\mathbf{z})$$对于$$\mathbf{z}$$而言是半正定的，利用了

{% label primary @具有非负对角元的Hermit对角占优（主对角大于该列所有元素）矩阵是半正定的 %}性质

由于
$$
\nabla_{\mathbf{z}}^{2} \hat{g}(\mathbf{z})=\frac{1}{\left(\sum_{n=1}^{N} e^{z_{n}}\right)^{2}}\left\{\begin{array}{cclc}
e^{z_{1}} \sum_{n \neq 1} e^{z_{n}} & -e^{z_{1}} e^{z_{2}} & \ldots & -e^{z_{1}} e^{z_{N}} \\
-e^{z_{1}} e^{z_{2}} & e^{z_{2}} \sum_{n \neq 2} e^{z_{n}} & \ldots & -e^{z_{2}} e^{z_{N}} \\
\ldots & \ldots & \ldots & \ldots \\
-e^{z_{1}} e^{z_{N}} & -e^{z_{2}} e^{z_{N}} & \ldots & e^{z_{N}} \sum_{n \neq N} e^{z_{n}}
\end{array}\right\}
$$
所以$$P_{dc}$$对于$$\text{ln}Q_m$$而言是凸的。



然后由保凸原则得到

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220711174745003.png" alt="image-20220711174745003" style="zoom:33%;" />

进一步得到：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220711174757400.png" alt="image-20220711174757400" style="zoom:33%;" />



{% note success %}

The convexity properties proved in Theorem 1-4 hold for any given truncation order *n*0, namely they also hold if the truncation order n approaches infifinity

{% endnote %}

