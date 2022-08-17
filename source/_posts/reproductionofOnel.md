---
title: CSI-Free相关文献代码复现
excerpt: 复现AA-IS/AA_SA/AA-SS_minVar/AA-SS_maxE/APS-EMW/CSI-Based
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20211203212547096.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Reproduction
categories:
  - Paper Reading
  - Channel State Information
comment: valine
math: true
hide: false
date: 2022-04-24 17:55:37
---

# OneL's CSI-Free and CSI-Based Wireless Energy Transfer Method Reproduction

参考OneL's Github[^1]源码复现。

## Log

### Done

{% cb fix the bug of EH_Transfer_Funtion.m, true, false %}

{% cb build code by formula derivation, true, false %}

{% cb improve the CSI-based algorithm according to Reference 6, true, false %} 

### ToDo

{% cb Change the EH-Transfer-Function, false, false %}

{% cb Change the Channel Path loss, false, false %}

## Channel Path Loss

直接搬用OneL的log-distance model：

```matlab
function beta = channel_path_loss(x1, x2, y1, y2)
%Channel path-loss between device at position (x1,y1) and another device at position (x2,y2)

%% Input parameters:
% (x1,y1) -> coordinates of the first node
% (x2,y2) -> coordinates of the second node

%% Output parameters:
% beta    -> path-loss between the two nodes at (x1,y1) and (x2,y2)

%% The path loss is comupted using the log-distance model
% Setting path-loss exponent and attenuation at reference distance of 1m
exponent = 2.7;         %path loss exponent
attenuation1m = 1e-3;   %average power attenuation at 1m
% Path loss computation
beta = min(attenuation1m*sqrt((x1 - x2).^2 + (y1 - y2).^2).^-exponent, 1);
end
```

返回一个系数beta作为路径衰落。随相对距离Distance的指数衰减（但是我没有找到论文或者表述来描述这个所谓的log-distance model）

防止在Distance=0时beta>1，所以有一个$$\min(\cdot)$$。

## Channel Model

### Channel 

准静态信道，也是几乎所有OneL文章使用的模型[^2]，分为直射信道（LoS）和非直射信道（NLoS）:
$$
\begin{aligned}
\textbf{h}=\sqrt{\frac{\kappa}{1+\kappa}}e^{\text{i}\varphi_0}\textbf{h}_{\text{los}}+\sqrt{\frac{1}{\kappa+1}}\textbf{h}_{\text{nlos}}
\end{aligned}
$$

```matlab
function h = RicianFadingChannel(kappa,M,x,y, choice) 
    phi = atan(y/x); % 发射角度
    Phi = -(0:1:M-1)*pi*sin(phi);
    h_los = PreventiveAdjustmentofMeanShift(exp(1i.*Phi.'), M, choice);
    hnlos = 1/sqrt(2)*(randn(M,1)+1i*randn(M,1));
    h = sqrt(kappa/(1+kappa))*h_los*exp(1i*pi/4)+sqrt(1/(1+kappa))*hnlos;
end
```

### Preventive Adjustment of Mean Shift 

同时考虑到Preventive Adjustment of Mean Shift，有：

```matlab
function h = PreventiveAdjustmentofMeanShift(h, M, choice)
% M: Antennas
    switch choice
        case 'mean'
            varphi = mod((0:1:M-1),2)*pi;
            h = h.*(exp(1i*varphi)).';
        case 'variance'
            h = h;
        case 'none'
            h = h;
        otherwise
            error('not implement, only mean or variance') 
    end
end
```

choice可以选择：

- mean: 即文章[^2]中介绍的max-E的优化策略，相邻天线之间相移$$\pi$$
- variance: 即文章[^2]中介绍的min-variance的优化策略，相邻天线之间没有相移

## EH Transfer Function

```matlab
function harvested_energy = EH_transfer_function(RF_energy,sensitivity,saturation,efficiency)
%EH transfer function given RF energy input and EH hardware parameters [REF]

%% Input parameters:
% RF_energy    -> RF energy available at the input of the EH circuit 
% sensitivity  -> RF sensitivity level of the EH circuit
% saturation   -> RF saturation level of the EH circuit
% efficiency   -> EH conversion efficiency of the EH circuit (scalar between 0 and 1)

%% Output parameters:
% harvested_energy    -> harvested energy

%% Main code
%A linear EH transfer function but including sensitivity and saturation phenomena is used here [REF]
harvested_energy = efficiency*(RF_energy.*(RF_energy>=sensitivity & RF_energy<saturation)+saturation*(RF_energy>=saturation));

%Other, more evolved, EH transfer functions can be tested by modifying line 15

%[REF]    - O. L. A. L髉ez, et al., "Statistical Analysis of Multiple Antenna
%           Strategies for Wireless Energy Transfer," in IEEE Transactions on 
%           Communications, vol. 67, no. 10, pp. 7245-7262, Oct. 2019.
end
```

> OneL少考虑了Energy=saturation的特殊情况

## CSI-Free

### AA-IS

```MATLAB
function energy = AA_IS(kappa, M, x, y, sensitivity, saturation, efficiency)
    h = RicianFadingChannel(kappa, M, x, y, 'none');
    RF_energy = channel_path_loss(x, 0, y, 0)/M*norm(conj(h), 2)^2;
    energy = EH_Transfer_Function(RF_energy, sensitivity, saturation, efficiency);
end
```

如参考文献[^2]中建模**eqn:10**，假设所有发射机的能量：
$$
E=g(\frac{\beta}{M}||\textbf{h}^*||^2)
$$
其中，$$\beta$$是考虑路径损耗和总发射功率后，在接收端可用的功率，$$M$$是总的天线个数，$$h_i$$是第$$i$$个天线到EH的信道。

### SA

```matlab
function energy = AA_SA(kappa, M, x, y, sensitivity, saturation, efficiency)
    h = RicianFadingChannel(kappa, M, x, y, 'none');
    energy = 0;
    for ii=1:1:M
        energy = energy+EH_Transfer_Function(channel_path_loss(x, 0, y, 0)*abs(h(ii))^2, sensitivity, saturation, efficiency);
    end
    energy = 1/M*energy;
end
```



如参考文献[^2]中建模**eqn:12**或者参考文献[^3]中的**eqn:15**，假设所有发射机的能量：
$$
E = \frac{1}{M}\sum\limits_{i=1}^Mg(\beta|h^*_i|^2)
$$

值得注意的是，因为每根天线的持续时间为原始的$$1/M$$，所以其求和和平均在Energy Transfer Function $$g(\cdot)$$之外。



### AA-SS

```matlab
function energy = AA_SS_maxE(kappa, M, x, y, sensitivity, saturation, efficiency)
    h = RicianFadingChannel(kappa, M, x, y, 'mean');
    RF_energy = channel_path_loss(x, 0, y, 0)/M*abs(sum(h))^2;
    energy = EH_Transfer_Function(RF_energy, sensitivity, saturation, efficiency);
end



function energy = AA_SS_minVar(kappa, M, x, y, sensitivity, saturation, efficiency)
    h = RicianFadingChannel(kappa, M, x, y, 'variance');
    RF_energy = channel_path_loss(x, 0, y, 0)/M*abs(sum(h))^2;
    energy = EH_Transfer_Function(RF_energy, sensitivity, saturation, efficiency);
end
```

根据参考文献[^2]**eqn:8**或者参考文献[^3]的**eqn:14**：
$$
E = g(\frac{\beta}{M}|\sum\limits_{i=1}^Mh_i|^2)=g(\frac{\beta}{M}|\textbf{1}^T\textbf{h}^*|^2)
$$

### APS-EMW

```matlab
function energy = APS_EMW(kappa, M, x, y, sensitivity, saturation, efficiency)
    h = RicianFadingChannel(kappa, M, x, y, 'none');   
    h = h.*exp(1i*randn(M,1)*2*pi).*randn(1,1); % 幅度和相位都要乘一个随机数，且幅度随机数以用户为单位，相位随机数以天线为单位
    RF_energy = channel_path_loss(x, 0, y, 0)/M*abs(sum(h)).^2;
    energy = EH_Transfer_Function(RF_energy, sensitivity, saturation, efficiency);
end
```

根据参考文献[^4]**eqn:14**，有：
$$
y(t)=\sqrt{\frac{2P}{M}}\Re\{\varLambda^{-\frac{1}{2}}h(t)e^{jw_0t}\}
$$
其中的时变信道$$h(t)$$有：
$$
h(t)=\sum\limits_{m=1}^Mh_me^{j\psi_m(t)}
$$
其中的$$\psi_m(t)$$是一个时变的相位，控制信道的时变。

>快衰信道体现在幅度和相位的变化，所以在信道幅度上乘一个randn(N,1)，因为假设对N个用户中任意一个用户而言信道是准静态的；对于相位则是每根天线有一个随机相位randn(M,1)

### Plot Space

```matlab
clc;clear;close all;
M = 4;
kappa = 10;
kappa = 10.^(kappa./10); 
R = 15;
sensitivity = 10.^((-22-30)/10); %-22dBm
saturation = 10.^((-8-30)/10);   %-8dBm
efficiency = 0.35;               %35%


mtkl_epoch = 100;


delta = 0.2;
x = -R:delta:R;
y = -R:delta:R;

E_AA_SS_maxE_all = zeros(length(x),length(y));
E_AA_SS_minVar_all = zeros(length(x),length(y));
E_AA_IS_all = zeros(length(x),length(y));
E_AA_SA_all = zeros(length(x),length(y));
E_APS_EMW_all = zeros(length(x),length(y));

for m =1:1:mtkl_epoch 
    E_AA_SS_maxE = zeros(length(x),length(y));
    E_AA_SS_minVar = zeros(length(x),length(y));
    E_AA_IS = zeros(length(x),length(y));
    E_AA_SA = zeros(length(x),length(y));
    E_APS_EMW = zeros(length(x),length(y));
    
    for idx_x = 1:1:length(x)
        for idx_y = 1:1:length(y)
            E_AA_SS_maxE(idx_x,idx_y) = AA_SS_maxE(kappa, M, x(idx_x), y(idx_y), sensitivity, saturation, efficiency);
            E_AA_SS_minVar(idx_x,idx_y) = AA_SS_minVar(kappa, M, x(idx_x), y(idx_y), sensitivity, saturation, efficiency);
            E_AA_IS(idx_x,idx_y) = AA_IS(kappa, M, x(idx_x), y(idx_y), sensitivity, saturation, efficiency);
            E_AA_SA(idx_x,idx_y) = AA_SA(kappa, M, x(idx_x), y(idx_y), sensitivity, saturation, efficiency);
            E_APS_EMW(idx_x,idx_y) = APS_EMW(kappa, M, x(idx_x), y(idx_y), sensitivity, saturation, efficiency);
            
        end
    end
    E_AA_SS_maxE_all = E_AA_SS_maxE_all+E_AA_SS_maxE;
    E_AA_SS_minVar_all = E_AA_SS_minVar_all+E_AA_SS_minVar;
    E_AA_IS_all = E_AA_IS_all+E_AA_IS;
    E_AA_SA_all = E_AA_SA_all+E_AA_SA;
    E_APS_EMW_all = E_APS_EMW_all+E_APS_EMW;
    
    clc;
    fprintf('monte carlo running %d ...', m);

end
harvest_energy_AA_maxE = 10*log10(E_AA_SS_maxE_all/mtkl_epoch)+30;
harvest_energy_AA_minVar = 10*log10(E_AA_SS_minVar_all/mtkl_epoch)+30;
harvest_energy_IS = 10*log10(E_AA_IS_all/mtkl_epoch)+30;
harvest_energy_SA = 10*log10(E_AA_SA_all/mtkl_epoch)+30;
harvest_energy_APS_EMW = 10*log10(E_APS_EMW_all/mtkl_epoch)+30;

figure(1)
imagesc(x, y, harvest_energy_AA_maxE.')
colormap(flipud(hot))
xlabel('Distance X /m')
ylabel('Distance Y /m')
zlabel('Energy /dBW')
title('AA-SS_{maxE}  Strategy')

figure(2)
imagesc(x, y, harvest_energy_AA_minVar.')
colormap(flipud(hot))
xlabel('Distance X /m')
ylabel('Distance Y /m')
zlabel('Energy /dBW')
title('AA-SS_{minVar}  Strategy')

figure(3)
imagesc(x, y, harvest_energy_IS.')
colormap(flipud(hot))
xlabel('Distance X /m')
ylabel('Distance Y /m')
zlabel('Energy /dBW')
title('AA-IS  Strategy')

figure(4)
imagesc(x, y, harvest_energy_SA.')
colormap(flipud(hot))
xlabel('Distance X /m')
ylabel('Distance Y /m')
zlabel('Energy /dBW')
title('AA-SA  Strategy')

figure(5)
imagesc(x, y, harvest_energy_APS_EMW.')
colormap(flipud(hot))
xlabel('Distance X /m')
ylabel('Distance Y /m')
zlabel('Energy /dBW')
title('APS_EMW  Strategy')

```

### Result

![image-20220424145451687](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220424145451687.png)



- AA-IS和AA-SA还是不太一样，这个主要原因是因为EH-Transfer-Function是非线性造成的。

## CSI-Based

### Optimizer

```matlab
function W = CSI_EB_optimizer(h, beta)
    [M, N] = size(h);
    cvx_startup
    cvx_begin sdp quiet
        variable W(M,M) hermitian semidefinite
        variable t
        minimize(-t)   
        subject to
            for i=1:N           
                beta(i)*real(trace(W*(h(:,i)*h(:,i)'))) >= t;
            end
            trace(W)==1;
    cvx_end
end
```

完全按照参考文献[^5]进行设计

### Compute Energy

```matlab
function E = compute_energy(W, h, beta)
    [M , N] = size(h); 
    [U, S] = eig(W);
    S(S<10e-5)=0;
    r = rank(S);
    for j=1:r    
        w(:, j)=U(:, M-r+j).';
        w(:, j) = w(:, j)/norm(w(:, j));
    end
    E = zeros(1, N);
    for i=1:1:N
       for j=1:1:r
           E(i) = E(i)+beta(i)*abs(S(M-r+j, M-r+j)*h(:, i)'*w(:,j)*w(:,j)'*h(:,i));
       end
    end
end
```

注意这里用特征值代表对应$$\textbf{w}$$持续的时间，能量为：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220424175207762.png" alt="image-20220424175207762" style="zoom: 67%;" />

### Plot Space

```matlab
clc;clear;close all;
M = 32;
N = 16;
R = 10;
Kappa_dB = 10:5:30;         %LOS factor (in dB) of the Rician fading
Kappa = 10.^(Kappa_dB./10);

% 假设用户均匀分布在半径为R的圆周上。
phi = (0:1/N:1-1/N)*2*pi;
Phi = -(0:1:M-1)'.*pi*sin(phi);
x = R*cos(phi);
y = R*sin(phi);

mtkl_epoch = 100;
E_full_performance = zeros(1, length(Kappa));
E_Statistical_performance = zeros(1, length(Kappa));


for k = 1:length(Kappa) 
    kappa = Kappa(k);
    E_full_min = 0;
    E_Statistical_min = 0;
    for m=1:1:mtkl_epoch
        clc;
        fprintf('\nkappa = %d, epoch: %d/%d\n', kappa, m, mtkl_epoch);
        % channel
        h_los = exp(1i.*Phi);
        h_nlos = 1/sqrt(2)*(randn(M,N)+1i*randn(M,N)); 

        h_bar = sqrt(kappa/(1+kappa)).*h_los.*exp(1i*pi/4);
        h_hat = sqrt(1/(1+kappa)).*h_nlos;
        h = h_hat+h_bar;
        % compute the path loss
        beta = zeros(1,N);
        for i =1:1:N
            beta(i) = channel_path_loss(x(i),0,y(i),0);
        end

        % W=ww' with full CSI
        W_full = CSI_EB_optimizer(h_hat+h_bar, beta);
        % W=ww' with statistical CSI
        W_Statistical= CSI_EB_optimizer(h_bar, beta);

        % compute energy by W1
        E_full = compute_energy(W_full, h, beta);
        E_full_min = E_full_min + min(E_full);
        % compute energy by W2
        E_Statistical = compute_energy(W_Statistical, h, beta);
        E_Statistical_min = E_Statistical_min + min(E_Statistical);
    end
    E_full_performance(k) = E_full_min/mtkl_epoch;
    E_Statistical_performance(k) = E_Statistical_min/mtkl_epoch;
end
fCSI = 10*log10(E_Statistical_performance)+30;
aCSI = 10*log10(E_full_performance)+30;

%% Figure generation
figure(1)
set(gcf, 'Units', 'centimeters'); 
axesFontSize = 16;
legendFontSize = 16;
afFigurePosition = [2 7 19 12]; 
set(gcf, 'Position', afFigurePosition,'PaperSize',[18 8],'PaperPositionMode','auto'); 

plot(Kappa_dB, fCSI,'-ok','MarkerSize',6,'LineWidth',2.5)
hold on
plot(Kappa_dB, aCSI,'-sk','MarkerSize',6,'LineWidth',2.5)
hold on

xlabel('$\kappa$ (dB)','Interpreter', 'latex','fontsize',axesFontSize)
ylabel('average worst-case RF energy (dBm)','Interpreter', 'latex','fontsize',axesFontSize)
hl=legend('full CSI EB','LOS-based CSI');
set(hl,'FontSize',legendFontSize,'interpreter','latex')

set(gca,'FontSize',12)
box on
grid on
```

与Onel在论文中的设置不一样，由于Onel在论文中的设置是，在$$R$$为半径的圆内EH Receiver 随机分布，取其中最差的结果作为性能指标。这样随机性太大了



我的想法是以$$R$$为半径，均匀分布在圆周上，并取其中最差的结果作为衡量指标，这样结果比较稳定。结果见下节。

### Result

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/result2.jpg" alt="result2" style="zoom:50%;" />

## Reference

[^1]: https://github.com/onel2428/WEToverview
[^2]: O. L. A. López, S. Montejo-Sánchez, R. D. Souza, C. B. Papadias and H. Alves, "On CSI-Free Multiantenna Schemes for Massive RF Wireless Energy Transfer," in IEEE Internet of Things Journal, vol. 8, no. 1, pp. 278-296, 1 Jan.1, 2021, doi: 10.1109/JIOT.2020.3003114.
[^3]: O. L. A. López, H. Alves, R. D. Souza and S. Montejo-Sánchez, "Statistical Analysis of Multiple Antenna Strategies for Wireless Energy Transfer," in IEEE Transactions on Communications, vol. 67, no. 10, pp. 7245-7262, Oct. 2019, doi: 10.1109/TCOMM.2019.2928542.
[^4]: B. Clerckx and J. Kim, "On the Beneficial Roles of Fading and Transmit Diversity in Wireless Power Transfer With Nonlinear Energy Harvesting," in IEEE Transactions on Wireless Communications, vol. 17, no. 11, pp. 7731-7743, Nov. 2018, doi: 10.1109/TWC.2018.2870377.
[^5]: O. L. A. López, F. A. Monteiro, H. Alves, R. Zhang and M. Latva-Aho, "A Low-Complexity Beamforming Design for Multiuser Wireless Energy Transfer," in IEEE Wireless Communications Letters, vol. 10, no. 1, pp. 58-62, Jan. 2021, doi: 10.1109/LWC.2020.3020576.
[^6]: A. Thudugalage, S. Atapattu and J. Evans, "Beamformer design for wireless energy transfer with fairness," 2016 IEEE International Conference on Communications (ICC), 2016, pp. 1-6, doi: 10.1109/ICC.2016.7511170.
