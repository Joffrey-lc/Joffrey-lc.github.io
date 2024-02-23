---
title: 优化基础-IRM Rank-one constrain recovery
excerpt: Guassian Randomization and Iterative Rank Minimization
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20211203212547096.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Math
  - Optimization
categories:
  - Optimization
comment: valine
math: true
hide: false
date: 2023-12-13 20:10:40
---

## 前言

在做一些QCQP（抽空整理一下）问题的时候，存在求解：
$$
\mathbf{C}=\mathbf{c}\mathbf{c}^H
$$
后还要再求解$$\mathbf{c}$$的情况，其中$$\mathbf{C}\in\mathbb{C}^{N\times N}$$，$$\mathbf{c}\in\mathbb{C}^{N\times 1}$$。一般都是丢掉Rank one constrain 得到结果后再恢复rank one。

恢复算法之前一直采用的是Gaussian randomization，总觉得很奇怪。最近学习到了一个算法叫做IRM，效果不错.

## Gaussian Randomization

Refer to [my blog](https://lcjoffrey.top/2022/07/16/gaussianrandomization/)

## Iterative Rank Minimization

[参考解析1](https://zhuanlan.zhihu.com/p/63763400)

[参考解析2](https://blog.csdn.net/qq_25777815/article/details/89525721) 和文献

[1] Sun C , Liu Y C , Dai R , et al. Two Approaches for Path Planning of Unmanned Aerial Vehicles with Avoidance Zones[J]. Journal of Guidance Control & Dynamics, 2017, 40(8).

[2] Sun C , Dai R . An iterative approach to Rank Minimization Problems[C]// Decision & Control. IEEE, 2016.

[3] C. Sun, N. Kingry and R. Dai, "A Unified Formulation and Nonconvex Optimization Method for Mixed-Type Decision-Making of Robotic Systems," in *IEEE Transactions on Robotics*, vol. 37, no. 3, pp. 831-846, June 2021, doi: 10.1109/TRO.2020.3036619. 

对应于我最近的工作，想要解决问题：
$$
\begin{align}
		\text{(P1):  }\max_{\mathbf{v},\boldsymbol{\Theta}} \,\,&\text{trace}(\boldsymbol{\mathcal{C}}\boldsymbol{\mathcal{A}}_d)\label{eqn:eqnP1}\\
		\text{s.t.}\,\,\,\,&\text{diag}(\boldsymbol{\mathcal{C}})=\left|\mathbf{v}^T\boldsymbol{\beta}(\varpi_{G})\right|^2\mathbf{1}_N,\tag{\ref{eqn:eqnP1}a}\label{eqn:eqnP1consA}\\
		&\text{trace}(\boldsymbol{\mathcal{C}})\leq MNP,\tag{\ref{eqn:eqnP1}b}\label{eqn:eqnP1consB}\\
		&\text{trace}(\boldsymbol{\mathcal{C}}\boldsymbol{\mathcal{A}}_k)=0,\forall k\in K, k\neq d,\tag{\ref{eqn:eqnP1}c}\label{eqn:eqnP1consC}\\
		&\boldsymbol{\mathcal{C}} = \mathbf{c}^\dagger\mathbf{c}^T,\tag{\ref{eqn:eqnP1}d}\label{eqn:eqnP1consD}\\
		&\mathbf{c}^T=\mathbf{v}^T\boldsymbol{\beta}(\varpi_{G})\boldsymbol{\alpha}^T(\vartheta_G,\varphi_G)\boldsymbol{\Theta}\tag{\ref{eqn:eqnP1}e}\label{eqn:eqnP1consE},\\
		&\text{Rank}(\boldsymbol{\mathcal{C}}) = 1,\tag{\ref{eqn:eqnP1}f}\label{eqn:eqnP1consF}
\end{align}
$$
现丢掉Rank one constrain，得到：
$$
\begin{align}
\text{(P1.1):  }\max_{\boldsymbol{\Theta}_h} \,\,\,&\text{trace}(\boldsymbol{\mathcal{C}}\boldsymbol{\mathcal{A}}_d)\label{eqn:eqnP1p1}\\
	\text{s.t.}\,\,\,\,\,&\text{diag}(\boldsymbol{\mathcal{C}})=MP\mathbf{1}_N,\tag{\ref{eqn:eqnP1p1}a}\label{eqn:eqnP1p1consA}\\
	&\mathbf{c}^T=\sqrt{MP}\mathbf{1}_N^T\boldsymbol{\Theta}_h,\tag{\ref{eqn:eqnP1p1}b}\label{eqn:eqnP1p1consB}\\
	&\text{trace}(\boldsymbol{\mathcal{C}}\boldsymbol{\mathcal{A}}_k)\leq \tau_k,\forall k\in K,k\neq d,\tag{\ref{eqn:eqnP1p1}c}\label{eqn:eqnP1p1consC}\\
	&\eqref{eqn:eqnP1consB}, \eqref{eqn:eqnP1consD}, \tag{\ref{eqn:eqnP1p1}d}\label{eqn:eqnP1p1consD}
\end{align}
$$
再进行IRM恢复：
$$
\begin{align}
	\text{(P1.2):  }\min_{\boldsymbol{\Theta}_{h,l}, r} \,\,\,&-\text{trace}(\boldsymbol{\mathcal{C}}_l\boldsymbol{\mathcal{A}}_d)+\epsilon_l r\label{eqn:eqnP1p2}\\
	\text{s.t.}\,\,\,\,\,&\text{diag}(\boldsymbol{\mathcal{C}}_l)=MP\mathbf{1}_N,\tag{\ref{eqn:eqnP1p2}a}\label{eqn:eqnP1p2consA}\\
	&\mathbf{c}^T_l=\sqrt{MP}\mathbf{1}_N^T\boldsymbol{\Theta}_{h,l},\tag{\ref{eqn:eqnP1p2}b}\label{eqn:eqnP1p2consB}\\
	&\text{trace}(\boldsymbol{\mathcal{C}}_l\boldsymbol{\mathcal{A}}_k)\leq \tau_k,\forall k\in K,k\neq d,\tag{\ref{eqn:eqnP1p2}c}\label{eqn:eqnP1p2consC}\\
    &r\mathbf{I}_{N-1}-\mathbf{V}_l^H\boldsymbol{\mathcal{C}}_l\mathbf{V}_l \succeq \mathbf{0},\tag{\ref{eqn:eqnP1p2}d}\label{eqn:eqnP1p2consD}\\
	&\eqref{eqn:eqnP1consB}, \eqref{eqn:eqnP1consD}, \tag{\ref{eqn:eqnP1p2}e}\label{eqn:eqnP1p2consE}
\end{align}
$$
总的流程如下：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202312132112800.png" alt="image-20231213211208483" style="zoom: 67%;" />

