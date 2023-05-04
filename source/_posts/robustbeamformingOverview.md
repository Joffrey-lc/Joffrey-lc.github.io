---
title: Robust Beamforming -- OverView
excerpt: 总结了一下最近做的Robust Beamforming
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20211203212547096.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Robust Beamforming
categories:
  - Paper Reading
  - Robust Beamforming
comment: valine
math: true
hide: false
date: 2022-12-30 11:00:41
---

## Bounded model

有界模型，一般是通过S-Procedure将问题转化为矩阵正定的问题：
$$
\begin{align}
&\text{Pr}\{|\mathbf{h}^\mathrm{H}\boldsymbol{\Theta}\mathbf{G}\mathbf{w}|^2\geq T\}\\
=
&\text{Pr}\{|\mathbf{v}^\mathrm{T}\left(\mathbf{H}+\Delta\mathbf{H}\right)\mathbf{w}|^2\geq T\}\\
=&\text{Pr}\{\mathbf{v}^\mathrm{T}(\mathbf{H}+\Delta\mathbf{H})\mathbf{w}\mathbf{w}^\mathrm{H}(\mathbf{H}+\Delta\mathbf{H})^\mathrm{H}\mathbf{v}^\mathrm{*}\geq T\}
\\
=&\text{Pr}\{\text{vec}^\mathrm{H}(\Delta\mathbf{H})\mathbf{Q}\text{vec}(\Delta\mathbf{H})+2\Re\{\mathbf{q}^\mathrm{H}\text{vec}(\Delta\mathbf{H})\}+c\geq T\}
\end{align}
$$
然后通过限定误差项$$\Delta\mathbf{H}$$的界，得到：
$$
\text{vec}^\mathrm{H}(\Delta\mathbf{H})\mathbf{Q}\text{vec}(\Delta\mathbf{H})+2\Re\{\mathbf{q}^\mathrm{H}\text{vec}(\Delta\mathbf{H})\}+c-T\geq 0\\
\text{vec}(\Delta\mathbf{H}^\mathrm{H})\text{vec}(\Delta\mathbf{H})\leq \frac{k_{\mathrm{h}}+k_\mathrm{G}+1}{(1+k_\mathrm{h})(1+k_\mathrm{G})}\frac{F_{\chi_{2 M N}^2}^{-1}\left(1-P_{\text {out }}\right)}{2}
$$
由General S-procedure，对于形如$$f_i(\mathbf{x})=\mathbf{x}^\mathrm{H}\mathbf{Q}_i\mathbf{x}+2\Re{\mathbf{q}_i\mathbf{x}}+c_i$$，其中$$\mathbf{Q}$$是Hermit的。对于任意使得$$f_0(\mathbf{x})\geq0$$的可行$$\mathbf{x}$$，有$$f_i(\mathbf{x})\to f_0(\mathbf{x})$$当且仅当存在一个$$t$$满足：
$$
\begin{align}

\left[
\begin{array}{cc}
\mathbf{Q}_0& \mathbf{q}_0\\
\mathbf{q}_0^\mathrm{H}&c_0
\end{array}
\right]
-t\left[
\begin{array}{cc}
\mathbf{Q}_1& \mathbf{q}_1\\
\mathbf{q}_1^\mathrm{H}&c_1
\end{array}
\right]
\succeq\mathbf{0}.

\end{align}
$$
当
$$
\mathbf{Q}_0=\mathbf{Q},\mathbf{q}_0=\mathbf{q},c_0=c-T;\\
\mathbf{Q}_1=-\mathbf{I}_{MN\times MN},\mathbf{q}_1=\mathbf{0}_{MN\times1},c_1=\frac{k_{\mathrm{h}}+k_\mathrm{G}+1}{(1+k_\mathrm{h})(1+k_\mathrm{G})}\frac{F_{\chi_{2 M N}^2}^{-1}\left(1-P_{\text {out }}\right)}{2};
$$
时，可以得到：
$$
\begin{aligned}
 \min _{\mathbf{W}, t} & \quad\operatorname{Tr}\left(\mathbf{W}\right) \\
\text { s.t. }& \left[\begin{array}{cc}
\mathbf{Q}+t \mathbf{I}_{MN\times MN} & \mathbf{q} \\
\mathbf{q}^H & c-t d^2
\end{array}\right] \succeq 0 ,\\
& t\geq 0, \\
& \mathbf{W} \succeq 0 , \\
& d=\sqrt{\frac{k_{\mathrm{h}}+k_\mathrm{G}+1}{(1+k_\mathrm{h})(1+k_\mathrm{G})}\frac{F_{\chi_{2 M N}^2}^{-1}\left(1-P_{\text {out }}\right)}{2}}, \\
& \mathbf{Q}=(\mathbf{W}\otimes\mathbf{V})^*, \\
&
\mathbf{q}=\mathbf{Q}\text{vec}(\mathbf{H}),\\
&c=\text{vec}(\mathbf{H})^\mathrm{H}\mathbf{Q}\text{vec}(\mathbf{H}).
\end{aligned}
$$
通过CVX求解得到$$\mathbf{W}$$。然后固定$$\mathbf{W}$$，求解$$\mathbf{V}$$。因为对于求解$$\mathbf{V}$$，该问题变为一个可行性检查问题，引入一个功率残差$$u$$，将$$T$$变为$$T+u$$，则新问题表示为：
$$
\begin{aligned}
 \max _{\mathbf{V}, t,u} & \quad u \\
\text { s.t. }& \left[\begin{array}{cc}
\mathbf{Q}+t \mathbf{I}_{MN\times MN} & \mathbf{q} \\
\mathbf{q}^H & c-t d^2-u
\end{array}\right] \succeq 0 ,\\
& t\geq 0, \\
& u\geq 0, \\
& \mathbf{V} \succeq 0 , \\
& \text{diag}(\mathbf{V}) =1 , \\
& d=\sqrt{\frac{k_{\mathrm{h}}+k_\mathrm{G}+1}{(1+k_\mathrm{h})(1+k_\mathrm{G})}\frac{F_{\chi_{2 M N}^2}^{-1}\left(1-P_{\text {out }}\right)}{2}}, \\
& \mathbf{Q}=(\mathbf{W}\otimes\mathbf{V})^*, \\
&
\mathbf{q}=\mathbf{Q}\text{vec}(\mathbf{H}),\\
&c=\text{vec}(\mathbf{H})^\mathrm{H}\mathbf{Q}\text{vec}(\mathbf{H}).
\end{aligned}
$$
最后，进行高斯随机化由$$\mathbf{W}$$和$$\mathbf{V}$$得到$$\mathbf{w}$$和$$\mathbf{v}$$

### Wang Jun & Liang Ying Chang

**Robust Beamforming and Phase Shift Design for IRS-Enhanced Multi-User MISO Downlink Communication**.  *Jun Wang* et.al.  **ICC 2020 - 2020 IEEE International Conference on Communications (ICC), June 2020**  ([pdf](https://ieeexplore.ieee.org/document/9148947))  (Citations **17**) 

他们的文章结构就如同上述Bounded model。

### Zhou Gui & Pan Cun Hua

**A Framework of Robust Transmission Design for IRS-Aided MISO Communications With Imperfect Cascaded Channels**.  *Gui Zhou* et.al.  **IEEE Transactions on Signal Processing, 2020**  ([pdf](https://ieeexplore.ieee.org/document/9180053))  (Citations **135**) 

---

**Robust Beamforming Design for Intelligent Reflecting Surface Aided MISO Communication Systems**.  *Gui Zhou* et.al.  **IEEE Wireless Communications Letters, October 2020**  ([pdf](https://ieeexplore.ieee.org/document/9110587))  (Citations **108**)

**不同之处有：**

- 他们的WCL文章中，只是对$$\mathbf{h}$$信道建模误差，没有对$$\text{diag}(\mathbf{h})\mathbf{G}$$级联信道进行建模。

该模型的收敛速度很快。

- 他们的建模方式不太一样，Pan Cun Hua 他们经常使用Tayler Expression
- 他们的模型中SINR分母还会进行一个约束处理，这部分我一般可以省略，因为我做单用户，分母只有Noise

## Statistical model

这个模型与上述的Bounded Model完全不同，是通过如下的Bernstein-Type Inequality转换概率为不等式：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202212301124980.png" alt="image-20221230112411923" style="zoom:50%;" />

然后再进行求解。可以写为：
$$
\begin{aligned}
& \operatorname{Pr}\left\{\left(\mathbf{h}_k^{\mathrm{H}}+\mathbf{e}^{\mathrm{H}}\left(\widehat{\mathbf{G}}_k+\Delta \mathbf{G}_k\right)\right) \boldsymbol{\Phi}_k\left(\mathbf{h}_k+\left(\widehat{\mathbf{G}}_k+\Delta \mathbf{G}_k\right)^{\mathrm{H}} \mathbf{e}\right)-\sigma_k^2 \geq 0\right\} \\
& =\operatorname{Pr}\left\{\operatorname{vec}^{\mathrm{H}}\left(\triangle \mathbf{G}_k\right)\left(\boldsymbol{\Phi}_k^{\mathrm{T}} \otimes \mathbf{E}\right) \operatorname{vec}\left(\triangle \mathbf{G}_k\right)+2 \operatorname{Re}\left\{\operatorname{vec}^{\mathrm{H}}\left(\left(\mathbf{e h}_k^{\mathrm{H}}+\mathbf{E} \widehat{\mathbf{G}}_k\right) \boldsymbol{\Phi}_k\right) \operatorname{vec}\left(\triangle \mathbf{G}_k\right)\right\}\right. \\
& \left.+\left(\mathbf{h}_k^{\mathrm{H}}+\mathbf{e}^{\mathrm{H}} \widehat{\mathbf{G}}_k\right) \boldsymbol{\Phi}_k\left(\mathbf{h}_k+\widehat{\mathbf{G}}_k^{\mathrm{H}} \mathbf{e}\right)-\sigma_k^2 \geq 0\right\} \\
& =\operatorname{Pr}\left\{\varepsilon_{\mathbf{g}, k}^2 \mathbf{i}_{\mathbf{g}, k}^{\mathrm{H}}\left(\boldsymbol{\Phi}_k^{\mathrm{T}} \otimes \mathbf{E}\right) \mathbf{i}_{\mathbf{g}, k}+2 \operatorname{Re}\left\{\varepsilon_{\mathbf{g}, k} \operatorname{vec}^{\mathrm{H}}\left(\left(\mathbf{e h}_k^{\mathrm{H}}+\mathbf{E} \widehat{\mathbf{G}}_k\right) \boldsymbol{\Phi}_k\right) \mathbf{i}_{\mathbf{g}, k}\right\}+\left(\mathbf{h}_k^{\mathrm{H}}+\mathbf{e}^{\mathrm{H}} \widehat{\mathbf{G}}_k\right) \boldsymbol{\Phi}_k\left(\mathbf{h}_k+\widehat{\mathbf{G}}_k^{\mathrm{H}} \mathbf{e}\right)-\sigma_k^2 \geq 0\right\} . \\
&
\end{aligned}
$$
其中$$\mathbf{i}\sim\mathcal{CN}(0, \mathbf{I})$$。然后再进行求解$$\mathbf{W}$$:
$$
\begin{aligned}
\min _{\boldsymbol{\Gamma}, \mathbf{x}, \mathbf{y}} & \sum_{k=1}^K \operatorname{Tr}\left\{\boldsymbol{\Gamma}_k\right\} \\
\text { s.t. } & \varepsilon_{\mathbf{g}, k}^2 M \operatorname{Tr}\left\{\mathbf{\Phi}_k\right\}-\sqrt{2 \ln \left(1 / \rho_k\right)} x_k-\ln \left(1 / \rho_k\right) y_k \\
& +u_k \geq 0, \forall k \in \mathcal{K} \\
& \| \quad \varepsilon_{\mathbf{g}, k}^2 M \operatorname{vec}\left(\mathbf{\Phi}_k\right) \\
& \sqrt{2 M} \varepsilon_{\mathrm{g}, k} \mathbf{\Phi}_k\left(\mathbf{h}_k+\widehat{\mathbf{G}}_k^{\mathrm{H}} \mathbf{e}\right) \| \leq x_k, \forall k \in \mathcal{K} \\
& y_k \mathbf{I}+\varepsilon_{\mathbf{g}, k}^2 M \mathbf{\Phi}_k \succeq \mathbf{0}, y_k \geq 0, \forall k \in \mathcal{K} \\
& \boldsymbol{\Gamma}_k \succeq \mathbf{0}, \forall k \in \mathcal{K} \\
& \operatorname{rank}\left(\boldsymbol{\Gamma}_k\right)=1, \forall k \in \mathcal{K}
\end{aligned}
$$
并且类似的，可行性检查求解$$\mathbf{V}$$:
$$
\begin{aligned}
\max _{\mathbf{e}, \boldsymbol{\alpha}, \mathbf{x}, \mathbf{y}} & \sum_{k=1}^K \alpha_k \\
\text { s.t. } & \varepsilon_{\mathrm{g}, k}^2 M \operatorname{Tr}\left\{\mathbf{\Phi}_k\right\}-\sqrt{2 \ln \left(1 / \rho_k\right)} x_k \\
& -\ln \left(1 / \rho_k\right) y_k+u_k^{\mathbf{e}} \geq 0, \forall k \in \mathcal{K} \\
& \left\|\varepsilon_{\mathbf{g}, k}^2 M\right\| \mathbf{\Phi}_k \|_F \\
& \sqrt{2 M} \varepsilon_{\mathrm{g}, k} \mathbf{\Phi}_k\left(\mathbf{h}_k+\widehat{\mathbf{G}}_k^{\mathrm{H}} \mathbf{e}\right) \| \leq x_k, \forall k \in \mathcal{K} \\
& \boldsymbol{\alpha} \geq 0 \\
& \left|e_m\right|^2=1, \forall m \in \mathcal{M} .
\end{aligned}
$$

### Zhou Gui & Pan Cun Hua

**A Framework of Robust Transmission Design for IRS-Aided MISO Communications With Imperfect Cascaded Channels**.  *Gui Zhou* et.al.  **IEEE Transactions on Signal Processing, 2020**  ([pdf](https://ieeexplore.ieee.org/document/9180053))  (Citations **135**) 

发的TSP，包含了直射信道和级联信道都不准确的情况和仅级联信道不全的情况。

###  Kun-Yu Wang

**Outage Constrained Robust Transmit Optimization for Multiuser MISO Downlinks: Tractable Approximations by Conic Optimization**.  *Kun-Yu Wang* et.al.  **IEEE Transactions on Signal Processing, November 2014**  ([pdf](https://ieeexplore.ieee.org/document/6891348))  (Citations **392**)

最早做Robust Beamforming，但是没有IRS

## Hu Xiao Ling

垃圾文章，耽误我时间。巨多错误，巨多问题，甚至复现不出来，我怀疑其真实性和学术态度。

**Robust Design for IRS-Aided Communication Systems With User Location Uncertainty**.  *Xiaoling Hu* et.al.  **IEEE Wireless Communications Letters, January 2021**  ([pdf](https://ieeexplore.ieee.org/document/9184012))  (Citations **7**)
