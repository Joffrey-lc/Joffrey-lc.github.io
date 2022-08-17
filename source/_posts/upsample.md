---
title: 通信基础-上采样与频谱搬移
excerpt: 验证上采样的频谱搬移
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20211203212547096.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - communication
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2022-05-15 17:30:34
---

# 验证上采样

## 理论

上采样：

​	给原始$$f_s$$采样点后面补零（补up_rate-1个零）

​	等同于给原始信号（假设是模拟信号）乘上一个采样向量：
$$
\delta = \left[1, \underbrace{0,0,\cdots}_{(\text{up-rate}-1)个\text{0}},1,\underbrace{0,0,\cdots}_{(\text{up-rate}-1)个\text{0}}\right]
$$
​	根据于采样定理，频谱会以$$f_s$$为周期进行搬移。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220515173656991.png" alt="上采样示意图" style="zoom:25%;" />

## 实验验证

### Result

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220515172820661.png" alt="原始信号" style="zoom:33%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220515172854670.png" alt="10倍插值（上采样）" style="zoom:33%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220515172904552.png" alt="i成型滤波后" style="zoom:33%;" />

### code

```matlab
% 验证上采样补零的结果
clc;clear;close all;
f = 1e2;
fs = 1e3;
N = 1000;
t = (0:N-1)/fs;

y = sin(2*pi*f*t+randn*2*pi);

figure(1)
subplot(211)
plot(t, y)
subplot(212)
plot((-N/2:(N-1)/2)/N*fs, fftshift(abs(fft(y))));
suptitle('原始信号')
% 上采样
up_rate = 10;
y_up_sample = reshape([y;zeros(up_rate-1, N)], 1, up_rate*N);

N = length(y_up_sample);
figure(2)
subplot(211)
plot( y_up_sample)
subplot(212)
plot((-N/2:(N-1)/2)/N*fs*up_rate, fftshift(abs(fft(y_up_sample))));
suptitle('10倍插值（插9个0）')
% 成型滤波
sps = up_rate;
span = 6;
h = rcosdesign(0.35, span, sps);
y_after_rcos = filter(h, 1, y_up_sample);% 使用filter函数滤波
figure(3)
subplot(211)
plot(y_after_rcos)
subplot(212)
plot((-N/2:(N-1)/2)/N*fs*up_rate, fftshift(abs(fft(y_after_rcos))));
suptitle('成型滤波后的结果')
```



