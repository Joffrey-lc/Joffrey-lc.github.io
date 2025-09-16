---
title: Two type IDs for SWIPT and only zero or one Energy Beamforming is needed
excerpt: Multiuser MISO Beamforming for Simultaneous Wireless Information and Power Transfer
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202404102351506.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - WET
categories:
  - Paper Reading
  - Wireless Energy Transfer
comment: valine
math: true
hide: false
date: 2024-04-10 23:51:13
---

Date: 2024.04.10  11:29
Author: Joffrey LC

-------------------------------------

**Multiuser MISO Beamforming for Simultaneous Wireless Information and Power Transfer**.  *Jie Xu* et.al.  **IEEE Transactions on Signal Processing, September 2014**  ([pdf](https://ieeexplore.ieee.org/document/6860253))  (Citations **387**)

## Quick Overview

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202404102351506.png" alt="image-20240410234946862" style="zoom:33%;" />

==Note that all the analysis is under the assumption of independently distributed user channels.==

- Type I: without the capability of cancelling the interference from energy signals.
- Type II: with the capability of cancelling the interference from energy signals.
- No dedicated energy beam is used for the case of Type I; and employing no more than one energy beam is optimal.
- Establish a new form of the celebrated uplink-downlink duality for the downlink beamforming problems and thereby develop alternative algorithms to obtain the same optimal solutions as by SDR



## System model

the SINR of two types:

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202404102351509.png" alt="image-20240410192508020" style="zoom:33%;" />

The two types can be formulated as:

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202404102351497.png" alt="image-20240410192754113" style="zoom:33%;" />

Both problems can be shown to maximize a convex quadratic function with $$\mathbf{G}$$ being positive semidefinite, subject to various quadratic constrains; thus they are both non-convex QCQPs.

### Check on their feasibility

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202404102351571.png" alt="image-20240410193858013" style="zoom:33%;" />

code varify

```matlab
clc;clear;close all;
P = 1;
M = 10;
K = 4;
los = generate_channel_simple(M, K, -pi+2*pi*rand, -pi+2*pi*rand, -pi+2*pi*rand);
nlos = sqrt(1/2)*(randn(K, M)+1j*randn(K, M));
kappa = 0;
G_all = sqrt(kappa/(1+kappa))*los+sqrt(1/(1+kappa))*nlos;

G = 0;
for k=1:1:K
    G = G + G_all(k, :)'*G_all(k, :);
end

[U, S] = eig(G);
optimal_w = U(:, 1);
optimal_w = optimal_w/norm(optimal_w)*P;


trace(optimal_w*optimal_w'*G)

close_form = S(1,1)*P


cvx_begin quiet
    variable V(M,M) hermitian semidefinite
    rece_power = 0;
    rece_power = rece_power+ real(trace(V*G));
    maximise rece_power
    subject to
    total_power = 0;
    trace(V)<= P;
cvx_end


[U2, S2] = eig(V);
re_w = U2(:, end);
re_w = re_w/norm(re_w)*P;
re_power = trace(re_w*re_w'*G)
```



## 问题的等价

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202404102351501.png" alt="image-20240410231200966" style="zoom:33%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202404102351538.png" alt="image-20240410231413232" style="zoom: 33%;" />





<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202404102351000.png" alt="image-20240410231523192" style="zoom:33%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202404102351008.png" alt="image-20240410231613204" style="zoom:33%;" />



根据等价问题二，可以通过对偶来解决这个问题：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202404102351071.png" alt="image-20240410232427626" style="zoom:33%;" />



有意思的是，作者还对比了分离式设计：

- Type I: 先设计信息用户，再把剩下的功率全部用给能量。由于此时IDs不具备能量信号干扰消除，所以需要在发射端进行消除，所以使用了Null space方案。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202404102351119.png" alt="image-20240410234551396" style="zoom:33%;" />

- Type II: 和上面类似，先满足信息用户，然后把剩下的功率全部给能量。由于此时IDs可以消除能量干扰，所以可以直接用OeBF方案。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202404102351241.png" alt="image-20240410234718045" style="zoom:33%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202404102351352.png" alt="image-20240410234901762" style="zoom:33%;" />
