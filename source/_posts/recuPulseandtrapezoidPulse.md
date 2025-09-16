---
title: 知识储备-三角波/矩形波和梯形波频谱
excerpt: 测试三种波形的频谱, sinc函数, 以及时域加窗
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202503271528818.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - signal processing
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2025-03-27 15:21:46
---

工程上，很难实现完美的矩形波，所以讨论一下矩形波和三角波/梯形波的脉冲的频谱。

## 矩形波和三角波

### 时域波形

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202503271523452.png" alt="image-20250327152305383" style="zoom:33%;" />

### 频域波形

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202503271523940.png" alt="image-20250327152320897" style="zoom:33%;" />

### 从时域加窗的角度看待这个问题

可以观察到，二者的频谱的零点是一样的。但是，{% label primary @三角波明显衰减更快 %}。这个点很有意思，在OFDM工程实现中，经常在时域加窗。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202503271526595.png" alt="image-20250327152656492" style="zoom:33%;" />

这个点不太好理解，因为一般从脉冲整形的角度出发，是在频域加窗，即时域卷积升余弦滤波器。但是这里是在时域上称升余弦，降低首尾的功率强度，等于在频域卷积sinc。

合理的解释是：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202503271528818.png" alt="image-20250327152823682" style="zoom:33%;" />

参考 [CSDN](https://blog.csdn.net/a2145565/article/details/139580022)

{% note success %}

同样的，三角脉冲可以认为是加了窗的矩形脉冲，所以，其旁瓣被有效抑制。

{% endnote %}

## 矩形波和梯形波

![image-20250327153200824](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202503271532897.png)

看起来，只要保证整个：

{% label primary @梯形：上升沿+下降沿+稳定状态 = 矩形：稳定状态-上升沿 %}

那么频谱的零点没有变化。



所以说，如果是占空比相同的形式，非完美的矩形波会导致零点偏移：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202503271535731.png" alt="image-20250327153550666" style="zoom:33%;" />

也许加成型滤波也是为了将这个零点压下去？

## Test Code

```matlab
clc;clear;close all;
% 参数设置
Fs = 10;            % 采样频率
T = 1/Fs;             % 采样间隔
t = -2:T:5;           % 时间向量（-2到5秒）
pulseWidth = 3;       % 脉冲总宽度（秒）
riseTime = 0.5;       % 梯形波上升/下降时间（秒）
amplitude = 1;        % 脉冲幅度

% 生成矩形波脉冲
rectPulse = amplitude * rectpuls(t, pulseWidth); % 生成以0为中心的矩形脉冲

% 生成梯形波脉冲
trapezoidPulse = zeros(1, length(t));
for i = 1:length(t)
    if t(i) >= -pulseWidth/2 && t(i) < -pulseWidth/2 + riseTime
        % 上升沿
        trapezoidPulse(i) = (t(i) + pulseWidth/2) / riseTime;
    elseif t(i) >= -pulseWidth/2 + riseTime && t(i) < pulseWidth/2 - riseTime
        % 平顶部分
        trapezoidPulse(i) = amplitude;
    elseif t(i) >= pulseWidth/2 - riseTime && t(i) < pulseWidth/2
        % 下降沿
        trapezoidPulse(i) = (-t(i) + pulseWidth/2) / riseTime;
    else
        trapezoidPulse(i) = 0;
    end
end

% 绘制对比图
figure('Color', 'white', 'Position', [100, 100, 800, 400])
hold on

% 绘制矩形波
plot(t, rectPulse, 'b', 'LineWidth', 2, 'DisplayName', '矩形波')

% 绘制梯形波
plot(t, trapezoidPulse, 'r--', 'LineWidth', 2, 'DisplayName', '梯形波')

% 图形美化
grid on
title('脉冲波形对比（矩形波 vs 梯形波）')
xlabel('时间 (s)')
ylabel('幅度')
xlim([-2 5])
ylim([-0.1 1.2])
legend('show', 'Location', 'northeast')

% 添加参数标注
text(2, 0.7, sprintf('脉冲宽度 = %.1fs', pulseWidth), 'FontSize', 10)
text(2, 0.6, sprintf('上升时间 = %.1fs', riseTime), 'FontSize', 10)
text(2, 0.5, sprintf('采样率 = %dHz', Fs), 'FontSize', 10)

set(gca, 'FontSize', 10)

nfft = 100000;
figure(100)
subplot(211)
plot(((1:1:nfft)-ceil(nfft/2))/nfft*Fs, fftshift(abs(fft(rectPulse, nfft))))
subplot(212)
plot(((1:nfft)-ceil(nfft/2))/nfft*Fs, fftshift(abs(fft(trapezoidPulse, nfft))))
```

