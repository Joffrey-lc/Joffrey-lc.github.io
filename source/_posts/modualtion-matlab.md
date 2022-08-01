---
title: 通信基础-matlab数字调制
excerpt: matlab实现BPSK调制
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/202205093.jpg
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - matlab
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2022-05-09 14:54:38
---

# 数字信号调制

## 参数及之间的关系

- $$f_b$$：码元速率$$=1/T_b$$
- $$f_c$$：载波频率
- $$f_s$$：采样频率
- $$\text{sps}$$：一个符号采样多少个点
- $$\text{span}$$：表示截断的符号范围，对滤波器取了几个符号的长度

其中，$$f_s=\text{sps}\cdot f_b$$，$$B_{2psk}=2f_b$$

![image-20220509144938392](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220509144938392.png)

## 基带信号产生

产生随机数,$$M$$阶数

```matlab
msg=randi([0 M-1],1,100);
```

## 星座图映射

```matlab
msgmod=pskmod(msg,M);
```

## 成型滤波

### 插值

```matlab
msgmod = [msgmod;zeros(sps-1, length(msgmod))];
msgmod = reshape(msgmod, 1, sps*length(msgmod));
```

### 设计滤波器

```matlab
h = rcosdesign(0.35, span, sps);
```

### 滤波

```matlab
msgmod = filter(h, 1, msgmod);% 使用filter函数滤波
```

## 上变频

```matlab
t=(0:1:length(msgmod)-1)/fs;   
carry_c=exp(1i*2*pi*fc*t);   %载波信号
y=real(msgmod.*carry_c);               %上变频
```

## Result

```matlab
clear;clc;close all;
%% BPSK 调制
M=2; %BPSK
fc=7000;                      %载波频率
sps = 4;
span = 6;
fb = 1000; % 符号速率1e4
fs = sps*fb;

snr_dB=2000;                              %信噪比
msg=randi([0 M-1],1,100);   
msgmod=pskmod(msg,M);                %基带2-PSK调制

% figure(1)
% plot(abs(fft(msgmod)));
msgmod = [msgmod;zeros(sps-1, length(msgmod))];
msgmod = reshape(msgmod, 1, sps*length(msgmod));

h = rcosdesign(0.35, span, sps);

msgmod = filter(h, 1, msgmod);% 使用filter函数滤波

t=(0:1:length(msgmod)-1)/fs;   
carry_c=exp(1i*2*pi*fc*t);   %载波信号
y=real(msgmod.*carry_c);               %上变频

figure(1)
plot((-length(y)/2:length(y)/2-1)/length(y)*fs, fftshift(abs(fft(y))))
```

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/202205093.jpg" alt="202205093" style="zoom: 50%;" />



