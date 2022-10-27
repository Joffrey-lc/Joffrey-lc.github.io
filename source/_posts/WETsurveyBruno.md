---
title: WET-Survey Bruno Clerckx
excerpt: Bruno Clerckx et.al--Foundations of Wireless Information and Power Transfer-Theory, Prototypes, and Experiments/--/Wireless Power Transfer for Future Networks-Signal Processing, Machine Learning, Computing, and Sensing
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202208250000189.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Wireless Energy Transfer
categories:
  - Paper Reading
  - Wireless Energy Transfer
comment: valine
math: true
hide: false
date: 2022-08-24 23:59:50
---

两篇文章一起总结了

---

**Foundations of Wireless Information and Power Transfer: Theory, Prototypes, and Experiments**.  *Bruno Clerckx* et.al.  **Proceedings of the IEEE, Jan.  2022**  ([pdf](https://ieeexplore.ieee.org/document/9675011))  (Citations **0**)

只整理了WET，WIET暂时未关注...

{% cb WET部分, true, false%} 

{% cb WIET部分, false, false%} 

# WET1

## 整体

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202208250000189.png" alt="image-20220824163157533" style="zoom:50%;" />



上述的整个流程，对应于end-to-end能量转换效率：
$$
e=\frac{P_{\mathrm{dc}}^{s}}{P_{\mathrm{dc}}^{t}}=\underbrace{\frac{P_{\mathrm{rf}}^{t}}{P_{\mathrm{dc}}^{t}}}_{e_{1}} \underbrace{\frac{P_{\mathrm{rf}}^{r}}{P_{\mathrm{rf}}^{t}}}_{e_{2}} \underbrace{\frac{P_{\mathrm{dc}}^{r}}{P_{\mathrm{rf}}^{r}}}_{e_{3}} \underbrace{\frac{P_{\mathrm{dc}}^{s}}{P_{\mathrm{dc}}^{r}}}_{e_{4}}
$$

- $$e_1$$：DC-to-RF
- $$e_2$$：RF-to-RF
- $$e_3$$：RF-to-DC
- $$e_4$$：DC-to-DC

总结：

1. {% label success @高效的高功率放大器（HPA, high Power Amplifiers）可以实现较大的$e_1$ %}
2. 增加发射机天线和Q（DC combining整流器个数（天线数）），可以增大$$e_2$$
3. {% label success @在低Input power时，Multisine和CW的$e_3$都很小，但是随着Input power的增大，$e_3$增大，而且Multisine的$e_3$大于CW。（主要体现在四阶矩上） %}
4. DC-to-DC converter控制$$e_4$$

## 能量传输

多正弦波，频率为$$f_n=f_0+n\Delta_f$$：
$$
\mathbf{x}_{\mathrm{rf}}(t)=\sqrt{2} \Re\left\{\sum_{n=0}^{N-1} \mathbf{x}_{n} e^{j 2 \pi f_{n} t}\right\}
$$
其中$$\mathbf{x}_{n} \triangleq\left[x_{1, n}, \ldots, x_{M, n}\right]^{T}$$表示$$f_n$$频率上，天线发射的信号，$$x_{m, n}=s_{m, n} e^{j \phi_{m, n}}$$，$$s_{m,n}$$是幅度，$$e^{j\phi_{m,n}}$$是相位。（其实主要针对频率选择信道，根据信道的频率响应进行设计）

>在Bruno他们的文章中，做CSI-free时，使用的是等功率分配，也有效果

{% label success @高效的高功率放大器（HPA, high Power Amplifiers）可以实现较大的$e_1$ %}

It is the general understanding that single-diode rectififiers

are more suited for **low** input power and multiple-diode rectififiers for a **higher** power.





<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202208250000200.png" alt="image-20220824200627951" style="zoom:50%;" />

单二极管模型情况下，$$e_3$$在low Input Power时，两种type（CW，Multisine）相似，都比较低。但是随着Input Power增大而增大，且Multisine 转换率大于CW，{% label success @因为传递能量的突发性，有助于开启二极管 %}，并在低功率状态下提高整流器的灵敏度；到达击穿区，又逐渐减小。To operate beyond such input power and eliminate the saturation problem, a multiple-diode rectififier is recommended.



有输出的电压$$v_{out}$$

$$
v_{\text {out }}=f_{\mathrm{EH}}\left(y_{\mathrm{rf}}(t)\right)=\beta_{2} \mathbb{E}\left[y_{\mathrm{rf}}(t)^{2}\right]+\beta_{4} \mathbb{E}\left[y_{\mathrm{rf}}(t)^{4}\right]
$$
而且由Jesen不等式，有$$\mathbb{E}\left[y_{\mathrm{rf}}(t)^{i}\right] \geq\left(\mathbb{E}\left[y_{\mathrm{rf}}(t)^{2}\right]\right)^{\frac{i}{2}}=\left(P_{\mathrm{rf}}^{r}\right)^{\frac{i}{2}}$$，即有：
$$
v_{\text {out }} \geq \beta_{2} P_{\mathrm{rf}}^{r}+\beta_{4}\left(P_{\mathrm{rf}}^{r}\right)^{2}
$$
则$$e_3$$随着$$P_{\text{rf}}^r$$增大而增大（击穿区前）。{% label danger @最大化$P_\text{rf}^r$ 仅最大化下界而不是其本身 %}



如果假设Multisine不同频率功率均匀分配，则$$\mathbb{E}\left[y_{\mathrm{rf}}(t)^{4}\right]$$正比于$$N(P_{\text{rf}}^r)$$，所以Multisine（$$N=8$$）优于CW（$$N=1$$）。{% label danger @二者(may have)相同的二阶矩(功率)，但是不同的四阶矩 %}

## DC combining and RF combining

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202208250000133.png" alt="image-20220824205017878" style="zoom:50%;" />

整体而言，RF combining 效果更好。（更大$$e_3$$）

局部而言，增加发射机天线和Q（DC combining整流器个数（天线数）），可以增大$$e_2$$



DC-to-DC converter控制$$e_4$$



值得注意的是$$e_1,e_2,e_3,e_4$$之间是耦合的，单独最大化某一个并不一定整体$$e$$最大化。

## 多正弦波优化

根据信道频率响应进行优化。频率响应大的分配多功率。这种非平均的功率分配是最大化$$\beta_{2} \mathbb{E}\left[y_{\mathrm{rf}}(t)^{2}\right]+\beta_{4} \mathbb{E}\left[y_{\mathrm{rf}}(t)^{4}\right]$$第一项和第二项的trade-off

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202208250000202.png" alt="image-20220824210122547" style="zoom:50%;" />

## 信道估计

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202208250000197.png" alt="image-20220824210236629" style="zoom:50%;" />

- 第一种需要节点进行信号处理（信道估计）
- 第二种依赖于导频传输（pilot transmission）
- 第三种可以在ER的低通信和信号处理要求下实现，并且简单地依赖于采集器输出处的dc功率电平的测量和一些有限信息的反馈（不需要信道估计或导频传输，几bit信道信息)。

具体而言，通过ET在每个time slot一个codebook中的不同的码字（就是不同的waveform和Beamforming组合），然后ER返回最大化接收能量的码字的index。

- （胡老师的想法，ET-to-ER-to-ET，需要对信号进行设计）{% label primary @The fourth one is also encouraging due to the low energy consumption at the device and relies on the idea that the ET can exploit the backscatter signals to estimate the backscatter channel (i.e., ET-to-ER-to-ET) state informa tion, from which the transmit signal needs to be designed. %}



---



**Wireless Power Transfer for Future Networks: Signal Processing, Machine Learning, Computing, and Sensing**.  *Bruno Clerckx* et.al.  **IEEE Journal of Selected Topics in Signal Processing, Aug.  2021**  ([pdf](https://ieeexplore.ieee.org/document/9502719))  (Citations **8**)

# WET2

与之前的那篇Invited paper差不多，目前WET的主要关注点

- **Range:** Deliver wireless power at distances of 5-100 s meters (m) for energizing low-power devices in in door/outdoor settings
- **Efficiency:** Boost the end-to-end power transfer  efficiency (up to a fraction of a percent/a few percent) or equivalently the DC power level at the energy harvester for a given transmit power; 
- **Non-line of sight (NLoS):** Support Line of sight (LoS) and NLoS to widen real-world applications of future WIPT networks; 
- **Mobility support:** Support mobile devices at least for those at pedestrian speed;
- **Ubiquitous accessibility:** Provide power ubiquitously within the network coverage area; 
- **Safety and health:** Make RF system safe and comply with the regulations; 
- **Energy consumption:** Limit the energy consumption of wireless powered devices; 
- **Seamless integration of wireless communication and wireless power:** Unify wireless communication and wireless power into WIPT;
- **Integrated WPT, sensing, computing, and communication:** Integrate WPT with sensing/computing and communication in 5G-and-beyond systems with virtualization and network slicing



**SWIPT**: Energy and information are simultaneously transmitted from one or multiple transmitter(s) to one or multiple receiver(s).



**Wirelessly Powered Communication Networks (WPCNs):**Energy is transmitted in the downlink from an access point to a receiver and information is transmitted in the uplink.



***Wirelessly Powered Backscatter Communication (WPBC):*** Energy is transmitted in the downlink and information is transmitted in the uplink using backscatter modulation at a tag to reflect and modulate the incoming RF signal for communication with a reader.

## Multisine

单纯从WET的角度考虑，Multisine可以只用sin，如果要更好地结合WIT，需要考虑sinc;

对于Multisine和CW，结论和上一篇Invited Paper相同，有相同的功率（二阶矩$$\mathbb{E}[y_\text{rf}(t)^2]=P_{\text{rf}}^r$$），但是四阶矩（$$\mathbb{E}[y_\text{rf}(t)^4]$$）完全不同；最大化$$P_{\text{rf}}^r$$只是最大化收获能量下界（由Jensen不等式得到的下界）。

## IRS

关于IRS，作者提到了三种不同的形式：

- Single connected：diagonal $$\Theta$$
- Group connected：block diagonal $$\Theta=\text{diag}\{\Theta_1,\Theta_2,\cdots,\Theta_G\}$$，分$$G$$组，每组$$L/G=L_G$$个
- Full connected：a full $$\Theta$$

三种形式都满足：$$\Theta=\Theta^T$$ and $$\Theta^H\Theta=\mathbf{I}_L$$

**结论是full > Group > Single**，同时运算复杂度也是**full > Group > Single**

> 意思是，考虑全耦合的element，效果是最好的？？？

## Other Methods

- **time-reversal:**[^1][^2] 多径当作虚拟天线，增强$$e_2$$。需要large bandwidth in order to distinguish as many paths in channel as possible. 



- (有点久远)**retrodirective arrays:** [^3][^4] Upon receiving a signal from any direction, retrodirective arrays exploit channel reciprocity to transmit a signal response, in the form of a phase-conjugated version of the received signal, back to the same direction without the need of knowing the source direction or performing explicit channel estimation/feedback

[^1]: M. -L. Ku, Y. Han, H. -Q. Lai, Y. Chen and K. J. R. Liu, "Power Waveforming: Wireless Power Transfer Beyond Time Reversal," in IEEE Transactions on Signal Processing, vol. 64, no. 22, pp. 5819-5834, 15 Nov.15, 2016, doi: 10.1109/TSP.2016.2601283.
[^2]: M. -L. Ku, Y. Han, B. Wang and K. J. R. Liu, "Joint Power Waveforming and Beamforming for Wireless Power Transfer," in IEEE Transactions on Signal Processing, vol. 65, no. 24, pp. 6409-6422, 15 Dec.15, 2017, doi: 10.1109/TSP.2017.2755582.
[^3]: R. Y. Miyamoto and T. Itoh, "Retrodirective arrays for wireless communications," in IEEE Microwave Magazine, vol. 3, no. 1, pp. 71-79, March 2002, doi: 10.1109/6668.990692.
[^4]: C. Pon, "Retrodirective array using the heterodyne technique," in IEEE Transactions on Antennas and Propagation, vol. 12, no. 2, pp. 176-180, March 1964, doi: 10.1109/TAP.1964.1138191.
