---
title: 知识储备-信道模型整理
excerpt: 整理一些信道模型以及它们的使用场景
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220411223248985.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Channel
  - Communication
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2022-04-11 22:30:39
---

整理不同的信道模型以及它们的使用场景

## Rician Fading

### 介绍

**MISO System: Transmitter with M antennas and the receiver has only one antenna.**

It is a very general assumption that allows modeling a wide variety of channels by tuning the Rician factor $$\kappa\geq0$$

- $$\kappa=0$$, the channel envelope is Rayleigh distributed
- $$\kappa\to\infty$$, the channel is a fully deterministic LOS channel

> **莱斯衰落信**道指除了经反射折射散射等来的信号外， 还有从发射机直接到达接收机 （如从卫星直接到达地面接收机）的信号，那么总信号的强度服从分布莱斯分布。有一条主路径，其余多径传输过来的信号仍如**瑞利衰落**所述。
>
> **瑞利衰落**只适用于从发射机到接收机不存在直射信号（LOS，Line of Sight）的情况，即信道模型能够描述由电离层和对流层反射的短波信道，以及建筑物密集的城市环境。否则应使用**莱斯衰落**信道作为信道模型。

### 建模

$$
\textbf{h}=\sqrt{\frac{\kappa}{1+\kappa}}e^{\text{i}\varphi_0}\textbf{h}_{\text{los}}+\sqrt{\frac{1}{1+\kappa}}\textbf{h}_{\text{nlos}}
$$

其中$$\varphi_0$$是初始相位。有LOS部分：
$$
\textbf{h}_{\text{los}}=[1,e^{\text{i}\Phi_1},\cdots,e^{\text{i}\Phi_{M-1}}]^\mathrm{T}
$$
且$$\Phi_t=-t\pi\sin\phi$$，$$\phi$$是**azimuth angle** relative to the boresight of the transmitting antenna array。

有Rayleigh部分：
$$
\textbf{h}_{\text{nlos}}\sim\mathcal{CN}(\textbf{0},\textbf{R})
$$

### 适用范围

CSI-Free中，对Wireless Energy Transfer的信道进行建模。

{% note success %}

- **On CSI-Free Multiantenna Schemes for Massive RF Wireless Energy Transfer**.  *Onel L. A. López* et.al.  **IEEE Internet of Things Journal, Jan.1, 1 2021**  ([pdf](https://ieeexplore.ieee.org/document/9119347))  (Citations **8**)

{% endnote %}

### 实现

```matlab
function h = RicianFadingChannel(kappa,M,x,y, choice) 
    phi = atan(y/x);
    Phi = -(0:1:M-1)*pi*sin(phi);
    h_los = PreventiveAdjustmentofMeanShift(exp(1i.*Phi.'), M, choice);
    hnlos = 1/sqrt(2)*(randn(M,1)+1i*randn(M,1));
    h = sqrt(kappa/(1+kappa))*h_los*exp(1i*pi/4)+sqrt(1/(1+kappa))*hnlos;
end
```





## ?? Wideband geometric channel model

### 介绍

Consider a transmitter-IRS channel, $$\textbf{h}_{T,k}$$, (and similarly for the IRS-receiver channel) consisting of *L* clusters. Each cluster contributes with one ray from the transmitter to the IRS. The ray parameters are: azimuth/elevation angles of arrival, $$\theta_l,\phi_l\in[0,2\pi)$$; complex coefficient ; $$\alpha_l\in\mathbb{C}$$; time delay $$\tau_l\in\mathbb{R}$$. The transmitter-IRS path loss is denoted by $$\rho_T$$. The pulse shaping function, with $$T_s$$-spaced signaling, is defined as $$p(\tau)$$ at $$\tau$$ seconds. The frequency-domain channel vector, $$\textbf{h}_{T,k}$$, can then be defined as

###　建模

$$
\mathbf{h}_{\mathrm{T}, k}=\sqrt{\frac{M}{\rho_{\mathrm{T}}}} \sum_{d=0}^{D-1} \sum_{\ell=1}^{L} \alpha_{\ell} \mathbf{a}\left(\theta_{\ell}, \phi_{\ell}\right) p\left(d T_{S}-\tau_{\ell}\right) e^{-j \frac{2 \pi k}{K} d}
$$

where $$\mathbf{a}\left(\theta_{\ell}, \phi_{\ell}\right)\in\mathbb{C}^{M\times 1}$$  is the IRS array response vector. Assume a block-fading channel model, where $$\textbf{h}_{T,k}$$ and $$\textbf{h}_{T,k}$$ are assumed to stay constant over the channel coherence time.

### 适用范围

Both transmitter and Receiver have only one antenna.

{% note success %}

- **Deep Learning Coordinated Beamforming for Highly-Mobile Millimeter Wave Systems**.  *Ahmed Alkhateeb* et.al.  **IEEE Access, 2018**  ([pdf](https://ieeexplore.ieee.org/document/8395149))  (Citations **186**)
- **Deep Reinforcement Learning for Intelligent Reflecting Surfaces: Towards Standalone Operation**.  *Abdelrahman Taha* et.al.  **2020 IEEE 21st International Workshop on Signal Processing Advances in Wireless Communications (SPAWC), 26-29 May 2020**  ([pdf](https://ieeexplore.ieee.org/document/9154301))  (Citations **24**)

{% endnote %}

## Saleh-Valenzuela (SV) model (Narrowband geometric channel model) 

### 介绍

> Saleh-Valenzuela (SV) model where a geometric channel model is adopted with limited scattering.
>
> eg: BS->IRS



### 建模

$$
\textbf{H}=\sqrt{\frac{NM}{\rho}}\sum\limits_{l=1}^L\varrho_l\textbf{a}_r(\vartheta_l,\gamma_l)\textbf{a}_l^\mathrm{H}(\phi_l)
$$

其中，$$\rho$$ average path-loss between BS and IRS; $$L$$ is the number of paths; $$\varrho$$ denotes the complex gain associated with the $$l$$-th path; $$\vartheta_l$$  and $$\gamma_l$$ denote the azimuth angle and elevation angle of arrival (AoA), respectively. $$\phi_l$$  is the angle of departure (AoD),  $$\textbf{a}_r$$ and $$\textbf{a}_t$$ represent the receive and transmit array response vectors, respectively. 

假设IRS为一个有$$M_x\times M_y$$个elements的UPA (Uniform Planner Array)，则有：
$$
\textbf{a}_r(\vartheta_l,\gamma_l)=\textbf{a}_x(u)\otimes\textbf{a}_y(v)
$$
其中，$$\otimes$$表示Kronecker product（克罗内克积）。$$\textbf{a}_x(u)$$和$$\textbf{a}_y(v)$$表示导向矢量 or 相应向量 (steering vector) or 阵列流形 (array manifold)。 且$$u\triangleq2\pi d\cos(\gamma_l)/\lambda$$（即空间相位）,$$v\triangleq2\pi d\sin(\gamma_l)\cos(\vartheta_l)/\lambda$$，$$d$$表示天线位置：

{% note warning%}
在更多的文章中，$$v\triangleq2\pi d\sin(\gamma_l)\sin(\vartheta_l)/\lambda$$，这和选取的参考系相关。我个人认为选$$\sin\sin$$比较好
{% endnote %}
$$
\begin{aligned}
&\boldsymbol{a}_{x}(u) \triangleq \frac{1}{\sqrt{M_{x}}}\left[\begin{array}{llll}
1 & e^{j u} & \ldots & e^{j\left(M_{x}-1\right) u}
\end{array}\right]^{T} \\
&\boldsymbol{a}_{y}(v) \triangleq \frac{1}{\sqrt{M_{y}}}\left[\begin{array}{llll}
1 & e^{j v} & \ldots & e^{j\left(M_{y}-1\right) v}
\end{array}\right]^{T}
\end{aligned}
$$
**由于毫米波信道的稀疏散射特性，路径L的数目相对于G的维度很小。**

### 理解

毫米波信道可以简化为单径信道模型（求和）。主要是LoS场景。毫米波绕射能力差，路径稀疏，信道模型具有丰富的几何特征。

上面的$$\mathbf{H}$$其实就是接收为面阵，发射为线阵的导向矢量乘积，也就是==直射信道==。

### 适用范围

考虑毫米波稀疏散射特性，有$$L$$个路径。

{% note success %}

- **Compressed Channel Estimation for Intelligent Reflecting Surface-Assisted Millimeter Wave Systems**.  *Peilan Wang* et.al.  **IEEE Signal Processing Letters, 2020**  ([pdf](https://ieeexplore.ieee.org/document/9103231))  (Citations **72**)
- **Deep Channel Learning for Large Intelligent Surfaces Aided mm-Wave Massive MIMO Systems**.  *Ahmet M. Elbir* et.al.  **IEEE Wireless Communications Letters, Sept.  2020**  ([pdf](https://ieeexplore.ieee.org/document/9090876))  (Citations **51**)

{% endnote %}

### 实现

```matlab
function H = generate_channel(Nt, Nr, L)
    AOD = pi*rand(L, 1) - pi/2;  %-2/pi~2/pi
    AOA = pi*rand(L, 2) - pi/2;  %-2/pi~2/pi

    alpha(1) = 1; % gain of the LoS
    if L >1
        alpha(2:L) = 10^(-0.7)*(randn(1,L-1)+1i*randn(1,L-1))/sqrt(2);
    end
%     alpha(2:L) = 0;
    H = zeros(Nr, Nt);
    Nx = sqrt(Nr);
    Ny = sqrt(Nr);
    for ll=1:1:L
        ax = sqrt(1/Nx)*exp((0:Nx-1)*1j*pi*cos(AOA(ll, 2))).';
        ay = sqrt(1/Ny)*exp((0:Ny-1)*1j*pi*sin(AOA(ll, 1))*sin(AOA(ll, 2))).';
        ar =kron(ax, ay);
        at =  sqrt(1/Nt)*exp((0:Nt-1)*1j*pi*sin(AOD(ll, 1))).';
        H = H + sqrt(Nr * Nt)*alpha(ll)*ar*at';
    end
end
```

还有简化版本，只有一个主径：

```matlab
function H = generate_channel_simple(Nt, Nr, AOA1, AOA2, AOD)
    alpha = 1; % gain of the LoS
    Nx = sqrt(Nr); % 因为我这里是有Nr个element的IRS
    Ny = sqrt(Nr); % 方阵排布
    ax = sqrt(1/Nx)*exp((0:Nx-1)*1j*pi*cos(AOA2)).';
    ay = sqrt(1/Ny)*exp((0:Ny-1)*1j*pi*sin(AOA1)*sin(AOA2)).';
    ar =kron(ax, ay);
    at =  sqrt(1/Nt)*exp((0:Nt-1)*1j*pi*sin(AOD)).';
    H = sqrt(Nr * Nt)*alpha*ar*at';
end
```



