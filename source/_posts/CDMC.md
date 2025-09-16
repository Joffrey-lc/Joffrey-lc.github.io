---
title: 知识储备-Channel-Capacity DCMC and CCMC
excerpt: 计算连续/离散输入连续输出的无记忆信道下的信道容量
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202411131219607.jpg
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Information Theory
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2024-11-07 21:57:56
---

最近项目需求计算CCMC和DCMC，

- CCMC：Continuous-input Continuous-output Memoryless Channel
- DCMC：Discrete-input Continuous-output Memoryless Channel

## CCMC

首先CCMC的一般计算形式是：
$$
C=B\log_2(1+\text{SINR})
$$
其中，考虑的是复数信道。并且这个capacity需要

- 在没有任何约束下
- 输入服从连续高斯分布

才能达到。



但是不管是DCMC还是CCMC，核心的东西都在于：

> 信道容量=通过调整输入的分布，经过信道传输后消除的最大不确定性，即
>
> $$C=\max_{p(x_i)}\left(I(X;Y)\right)$$
>
> 而互信息$$I(X;Y)=H(X)-H(X;Y)$$，即$$X$$原有的不确定性-收到$$Y$$之后$$X$$仍有的不确定性=通过传输$$Y$$获得的不确定性的减少。

## DCMC

### 一般情况

在考虑调制之后，输入变为离散的，例如QPSK就是离散的四个符号，可以假设这些符号服从均匀分布。

![b5378988bb25fd83ca39d7a8662f7f9](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202411131208427.jpg)

### 复杂情况-Beamforming/多用户

值得注意的是更复杂的情况：

- 考虑多用户：星座图的叠加
- 考虑beamforming：星座图的平移、旋转、缩放等

假设有两个单天线用户，$$N_t$$发射天线，形成一个MISO系统，则用户1接收到的信号为：
$$
Y_1=h_1w^H_1x_1+h_1w^H_2x_2+n
$$
如果$$N_t=1$$，那么beamforming的唯一作用就是调相，因为可以写成$$w_1=e^{j\theta_1}$$的形式。此时，两个用户的星座图就会通过旋转进行叠加。



以此类推，当$$N_t>1$$时，两个用户的星座图不进会相移（旋转），还会缩放（幅度），最后构成叠加态：



![bb497d9be1aa0a71fbe4024dda16cfd](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202411131217973.jpg)

最后再考虑信道的影响，即完成。

参考这段代码进行星座图叠加：

```matlab
 % Calculate the stacked constellation
        result_with_N_t = zeros(possible,N_t);
        for j=1:possible
            for k = 1:K
                result_with_N_t(j, :) = result_with_N_t(j, :)+W(:, k).'*modulation(all(j,k));
            end
        end
```



## Matlab Simulation



一般的DCMC计算如下：

```matlab
clc;clear;close all;

% +---------------------------------------------+
% | Choose the SNR, modulation and channel here |
% +---------------------------------------------+

% Affects the accuracy and duration of the simulation
symbol_count = 1000;%00000;
% Modulation scheme
% -----------------

% 2PSK
% modulation = [+1, -1];

% 4PSK
%modulation = [+1, +i, -1, -i];

% 8PSK
%modulation = [+1, sqrt(1/2)*(+1+i), +i, sqrt(1/2)*(-1+i), -1, sqrt(1/2)*(-1-i), -i, sqrt(1/2)*(+1-i)];

% 16QAM
modulation = sqrt(1/10)*[-3+3*1i, -1+3*1i, +1+3*1i, +3+3*1i, -3+1*1i, -1+1*1i, +1+1*1i, +3+1*1i, -3-1*1i, -1-1*1i, +1-1*1i, +3-1*1i, -3-3*1i, -1-3*1i, +1-3*1i, +3-3*1i];

% Channel

% Uncorrelated Rayleigh fading channel
% channel = sqrt(1/2)*(randn(1,symbol_count)+1i*randn(1,symbol_count));

% AWGN channel
channel = ones(1,symbol_count);

% +------------------------+
% | Simulation starts here |
% +------------------------+
snrs = -10:1:30;

for i = 1:length(snrs)
    snr=snrs(i);

    % Generate some random symbols
    symbols = ceil(length(modulation)*rand(1,symbol_count));

    % Generate the transmitted signal
    tx = modulation(symbols);

    % Generate some noise
    N0 = 1/(10^(snr/10));
    noise = sqrt(N0/2)*(randn(1,symbol_count)+1i*randn(1,symbol_count));
                        
    % Generate the received signal
    rx = tx.*channel+noise;

    % Calculate the symbol probabilities
    probabilities = max(exp(-(abs(ones(length(modulation),1)*rx - modulation.'*channel).^2)/N0),realmin);

    % Normalise the symbol probabilities
    probabilities = probabilities ./ (ones(length(modulation),1)*sum(probabilities));

    % Calculate the capacity
    channel_capacity(i) = log2(length(modulation))+mean(sum(probabilities.*log2(probabilities)));

end
figure(1)
plot(snrs,channel_capacity)
```

如果考虑调制方式、星座图、多用户，如下：

```matlab
clc;clear;close all;
symbol_count = 1000;%
K = 1; % No. of Users
N_t = 1; % No. of Tx
% 2PSK
% modulation = [+1, -1];
% 4PSK
% modulation = [+1, +i, -1, -i];
% 8PSK
% modulation = [+1, sqrt(1/2)*(+1+i), +i, sqrt(1/2)*(-1+i), -1, sqrt(1/2)*(-1-i), -i, sqrt(1/2)*(+1-i)];
% 16QAM
modulation = sqrt(1/10)*[-3+3*1i, -1+3*1i, +1+3*1i, +3+3*1i, -3+1*1i, -1+1*1i, +1+1*1i, +3+1*1i, -3-1*1i, -1-1*1i, +1-1*1i, +3-1*1i, -3-3*1i, -1-3*1i, +1-3*1i, +3-3*1i];

MT_count = 100;

% Channel
% Uncorrelated Rayleigh fading channel
channel_K_all = sqrt(1/2)*(randn(K, N_t, MT_count)+1i*randn(K, N_t, MT_count));

% Calculate all possible constellation
all = possible_generator(length(modulation),K);

possible=length(all);
% channel_K_all = ones(K, N_t, MT_count); % AWGN
for mt = 1:MT_count
    snrs = -10:1:30;
    for i = 1:length(snrs)
        channel_K = repmat(channel_K_all(:, :, mt), [1, 1, symbol_count]);
        % Beamforming
        W_LS = zeros(N_t, K); % LS 波束赋形
        W_MRT = zeros(N_t, K); % MRT 波束赋形
        H = squeeze(channel_K(:, :, 1)).'; % 取任意一组都行, N_t \times K
        for k = 1:K
            W_LS(:, k) = H(:, k) / norm(H(:, k)); % LS 波束赋形向量
            W_MRT(:, k) = conj(H(:, k)) / norm(H(:, k))^2; % MRT 波束赋形向量
        end
        % ZF 波束赋形
        W_ZF = H / (H' * H);
        for k = 1:K
            W_ZF(:, k) = W_ZF(:, k) / norm(W_ZF(:, k)); % 归一化
        end
        W_LS = W_LS./norm(W_LS, 'fro');
        W_MRT = W_MRT./norm(W_MRT, 'fro');
        W_ZF = W_ZF./norm(W_ZF, 'fro');

        W = W_ZF;

        for k = 1:K
            % Generate some random symbols
            symbols_K(k, :) = ceil(length(modulation)*rand(1,symbol_count));
            % Generate the transmitted signal
            tx_K(k, :) = modulation(symbols_K(k, :));
        end
        for k = 1:K
            % Generate some noise
            N0 = 1/(10^(snrs(i)/10));
            noise = sqrt(N0/2)*(randn(1,symbol_count)+1i*randn(1,symbol_count));
            % Generate the received signal
            rx_k(k, :) = tx_K(k, :).*reshape(squeeze(channel_K(k, :, :)).'*W(:, k), size(tx_K(k, :)))+noise;
            for kk=1:K
                if kk ~= k
                    rx_k(k, :) = rx_k(k, :) + tx_K(kk, :).*reshape(squeeze(channel_K(k, :, :)).'*W(:, kk), size(tx_K(k, :)));
                end
            end
        end
        % Calculate the stacked constellation
        result_with_N_t = zeros(possible,N_t);
        for j=1:possible
            for k = 1:K
                result_with_N_t(j, :) = result_with_N_t(j, :)+W(:, k).'*modulation(all(j,k));
            end
        end
        % Calculate the symbol probabilities
        probabilities = zeros(possible, symbol_count);
        for k = 1:K
            probabilities = max(probabilities, max(exp(-(abs(ones(possible,1)*rx_k(k, :) - result_with_N_t*reshape(squeeze(channel_K(k, :, :)), [], symbol_count)).^2)/N0),realmin));
        end
        % Normalise the symbol probabilities
        probabilities = probabilities ./ sum(probabilities, 1);
        % Calculate the capacity
        mt_channel_capacity(i, mt) = (log2(possible)+mean(sum(probabilities.*log2(probabilities))))/K;
    end
end
channel_capacity = mean(mt_channel_capacity, 2);
figure(1)
plot(snrs,channel_capacity)
hold off;

function all=possible_generator(M,dc)
    number =(0:M^dc-1);
    p_unsort=zeros(M^dc,dc);
    for i=1:dc
        if i==1
            p_unsort(:,i)=floor(number./M^(dc-i))';
        else
            temp=zeros(M^dc,1);
            for j=1:i-1
                temp=p_unsort(:,j).*M^(dc-j)+temp;
            end
            p_unsort(:,i)=floor((number'-temp)./M^(dc-i));
        end
    end
    all=p_unsort+1;
end
```

重点在于计算多个用户星座图的叠加

- 单天线的时候等于是旋转星座图
- 多天线的时候考虑beamforming来实现多用户分集



