---
title: Weighted Sum Rate Maximization-SCA
excerpt: Le-Nam Tran et.al.--Fast Converging Algorithm for Weighted Sum Rate Maximization in Multicell MISO Downlink
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/simulationofSCA.jpg
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - SCA
  - Optimization
categories:
  - Optimization
comment: valine
math: true
hide: false
date: 2022-07-14 16:03:13
---



**Fast Converging Algorithm for Weighted Sum Rate Maximization in Multicell MISO Downlink**.  *Le-Nam Tran* et.al.  **IEEE Signal Processing Letters, December 2012**  ([pdf](https://ieeexplore.ieee.org/document/6327333))  (Citations **112**)

## Quick Overview

- Weighted sum rate maximization
- Successive Convex Approximation

## Main Idea

compare these two equation:

the **original** object is formed as follows:

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220713161428895.png" alt="image-20220713161428895" style="zoom: 67%;" />

and **finally**, we get: 

 ignore (11b) and (11c) in (11):

(11f)  is equivalent to (6d)

![image-20220713161513169](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220713161513169.png)



(11d) is equivalent to (6b) based on the following equations:

![image-20220714151240972](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220714151240972.png)

and:

![image-20220714151314162](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220714151314162.png)

其实到这里，已经可以做了。用$$G(\cdot)$$代替eqn7(a)中的$$f(\cdot)=\sqrt{x_k}\beta_k$$，就是Algorithm 1 7(b) not approximation.(upper bound) 

但是作者还将(7b)再次展开得到（11e）（upper bound）

得到**最终**的Algorithm 1 7(b) approximation. 

## Details

首先由香农公式得到并利用log的特点：

![image-20220714153124002](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220714153124002.png)

因为是maximization 问题，所以有upper bound，然后变量替换转换为上述形式。

进一步因为本来就需要$$t_k$$都越大越好，所以(5b)是{% label primary @active %}的。然后在进行一个变量替换。同样的(6d)也是active 的。

![image-20220714153242474](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220714153242474.png)

然后把（6b）用（7a）和（7b）替换，值得注意的是，{% label primary @都是将小的部分放大 %}



然后精髓在于：

利用算数和不等式，找到了一个$$f(\cdot)$$的 convex upper bound $$G(\cdot)$$，然后用$$G(\cdot)$$替换$$f(\cdot)$$。约束(7a)就是一个SOC约束。

![image-20220714155130326](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220714155130326.png)



同样的找$$t_k^{1/{\alpha_k}}$$的upper bound（first order Taylor expansion）来对（7b）近似：

![image-20220714155653666](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220714155653666.png)



## Simulation Result

### my Algorithm 1 (7(b) approximation)

```matlab
clc;clear;close all;

NumCells = 2;

Pb_dB = [12, 12];
Pb = 10.^(Pb_dB/10);

NumUes = 4; %2 cells times 2
NumAntennas = 8; % Num of each BS
sigma_2 = 1;

BS2Ue = [1, 1, 2, 2 ]; % it means the first BS serve the 1th and 2th User while the second BS serve the 3th and 4th User
load('channel.mat')
h = zeros(NumCells, NumAntennas, NumUes);
h(1, :, :) = channel(:, :, 1);
h(2, :, :) = channel(:, :, 2);

% h = sqrt(1/2)*(randn(NumCells, NumAntennas, NumUes)+1j*randn(NumCells, NumAntennas, NumUes));
% weights = ones(NumUes, 1); % real
weights = [0.14;0.21;0.28;0.36]; % weights in Fig. 2
% parameters initial  都取临界值
wK_init = sqrt(1/2)*(randn(NumAntennas, NumUes)+1j*randn(NumAntennas, NumUes));
% meet the constrain of BS power.
for iCell = 1:NumCells
    wK_init(:,BS2Ue==iCell) = sqrt(Pb(iCell))/norm(wK_init(:,BS2Ue==iCell))*wK_init(:,BS2Ue==iCell); % scalling to meet the power constraint
end

% tK_init = abs(randn(NumUes, 1)); % real
betaK_init = zeros(NumUes, 1); % complex
xK_init = zeros(NumUes, 1); % real
for iU =1:NumUes
   interfere = 0;
   otherUes = find(1:NumUes~=iU);
   interfere = interfere + sigma_2;
   for i = 1:length(otherUes)
       interfere = interfere+abs(h(BS2Ue(otherUes(i)), :, iU)*wK_init(:, otherUes(i)))^2;
   end  
   betaK_init(iU) = sqrt(interfere);
   
   xK_init(iU) = (h(BS2Ue(iU), :, iU)*wK_init(:, iU)/betaK_init(iU))^2;
end
phiK_init = sqrt(xK_init)./betaK_init; % complex
tK_init = (xK_init+1).^(weights);
tol = 1e-2;

max_itern = 20;
sumrate = zeros(max_itern, 1);
for iter =1:1:max_itern
    cvx_begin   quiet
    variables tK(NumUes, 1) xK(NumUes, 1) betaK(NumUes, 1)
    variable wK(NumAntennas, NumUes) complex 
    maximize(geo_mean(tK))
    subject to
    for iU = 1:1:NumUes
        b = h(BS2Ue(iU), :, iU)*wK(:, iU)-1/(2*phiK_init(iU, :))*xK(iU, :);
        norm([1/2*(b-1) sqrt(phiK_init(iU)/2)*betaK(iU)]) <= real(1/2*(b+1)) %因为要更新wK，所以wK是在约束中的
%         imag(h(BS2Ue(iU), :, iU)*wK(:, iU)) == 0; %(6c)
        real(tK_init(iU)^(1/weights(iU))+1/weights(iU)*tK_init(iU)^(1/weights(iU)-1)*(tK(iU)-tK_init(iU))) <= xK(iU)+1
        
        other_Ues = find(1:1:NumUes ~=iU);
        interfere = [];
        interfere = [interfere sigma_2];
        for i = 1:length(other_Ues)
            interfere = [interfere h(BS2Ue(other_Ues(i)), :, iU)*wK(:, other_Ues(i))];
        end
        norm(interfere) <= betaK(iU, 1);
    end
    
%     tK >= 1;
    
    for iC=1:NumCells
        norm(vec(wK(:,BS2Ue==iC))) <= sqrt(Pb(iC));
    end

    cvx_end;
    
    % update parameters
    phiK_init = sqrt(xK)./betaK;
    tK_init = tK;
    
    beamformer = wK; %保存当前最优的beamformer，绘制achievable rate
    
    SINR = zeros(NumUes,1);
    for iU =1:1:NumUes
        User_power = abs(h(BS2Ue(iU), :, iU)*beamformer(:, iU))^2;
        
        other_Ues = find(1:1:NumUes ~=iU);
        interfere = [];
        interfere = [interfere sigma_2];
        for i = 1:length(other_Ues)
            interfere = [interfere h(BS2Ue(other_Ues(i)), :, iU)*wK(:, other_Ues(i))];
        end
        
        SINR(iU) = User_power/norm(interfere)^2;
    end
    
    for iU =1:1:NumUes
        sumrate(iter) = sumrate(iter)+weights(iU)*log2(1+SINR(iU));
    end
    if iter>=2 && (sumrate(iter)-sum(iter-1))<tol
        sumrate(iter:end) = [];
        break   
    end
    
end
figure()
plot(sumrate)

```

### my Algorithm 1 (7(b) not approximation)

```matlab
clc;clear;close all;

NumCells = 2;

Pb_dB = [12, 12];
Pb = 10.^(Pb_dB/10);

NumUes = 4; %2 cells times 2
NumAntennas = 8; % Num of each BS
sigma_2 = 1;

BS2Ue = [1, 1, 2, 2 ]; % it means the first BS serve the 1th and 2th User while the second BS serve the 3th and 4th User
load('channel.mat')
h = zeros(NumCells, NumAntennas, NumUes);
h(1, :, :) = channel(:, :, 1);
h(2, :, :) = channel(:, :, 2);

% h = sqrt(1/2)*(randn(NumCells, NumAntennas, NumUes)+1j*randn(NumCells, NumAntennas, NumUes));
% weights = ones(NumUes, 1); % real
weights = [0.14;0.21;0.28;0.36]; % weights in Fig. 2
% parameters initial  都取临界值
wK_init = sqrt(1/2)*(randn(NumAntennas, NumUes)+1j*randn(NumAntennas, NumUes));
% meet the constrain of BS power.
for iCell = 1:NumCells
    wK_init(:,BS2Ue==iCell) = sqrt(Pb(iCell))/norm(wK_init(:,BS2Ue==iCell))*wK_init(:,BS2Ue==iCell); % scalling to meet the power constraint
end

% tK_init = abs(randn(NumUes, 1)); % real
betaK_init = zeros(NumUes, 1); % complex
xK_init = zeros(NumUes, 1); % real
for iU =1:NumUes
   interfere = 0;
   otherUes = find(1:NumUes~=iU);
   interfere = interfere + sigma_2;
   for i = 1:length(otherUes)
       interfere = interfere+abs(h(BS2Ue(otherUes(i)), :, iU)*wK_init(:, otherUes(i)))^2;
   end  
   betaK_init(iU) = sqrt(interfere);
   
   xK_init(iU) = (h(BS2Ue(iU), :, iU)*wK_init(:, iU)/betaK_init(iU))^2;
end
phiK_init = sqrt(xK_init)./betaK_init; % complex
tK_init = (xK_init+1).^(weights);
tol = 1e-2;

max_itern = 20;
sumrate = zeros(max_itern, 1);
for iter =1:1:max_itern
    cvx_begin   quiet
    variable tK(NumUes, 1) 
    variable xK(NumUes, 1)
    variable betaK(NumUes, 1)
    variable wK(NumAntennas, NumUes) complex 
    maximize(geo_mean(tK))
    subject to
    for iU = 1:1:NumUes
        
        b = h(BS2Ue(iU), :, iU)*wK(:, iU)-1/(2*phiK_init(iU, :))*xK(iU, :);
        norm([1/2*(b-1) sqrt(phiK_init(iU)/2)*betaK(iU)]) <= real(1/2*(b+1)) %因为要更新wK，所以wK是在约束中的
        xK(iU)+1 >= tK(iU)^(1/weights(iU));
        imag(h(BS2Ue(iU), :, iU)*wK(:, iU)) == 0; %(6c)
        
        other_Ues = find(1:1:NumUes ~=iU);
        interfere = [];
        interfere = [interfere sigma_2];
        for i = 1:length(other_Ues)
            interfere = [interfere h(BS2Ue(other_Ues(i)), :, iU)*wK(:, other_Ues(i))];
        end
        norm(interfere) <= betaK(iU, 1);
    end
    
    tK >= 1;
    
    for iC=1:NumCells
        norm(vec(wK(:,BS2Ue==iC))) <= sqrt(Pb(iC));
    end

    cvx_end;
    
    % update parameters
    phiK_init = sqrt(xK)./betaK;
    tK_init = tK;
    
    beamformer = wK; %保存当前最优的beamformer，绘制achievable rate
    
    SINR = zeros(NumUes,1);
    for iU =1:1:NumUes
        User_power = abs(h(BS2Ue(iU), :, iU)*beamformer(:, iU))^2;
        
        other_Ues = find(1:1:NumUes ~=iU);
        interfere = [];
        interfere = [interfere sigma_2];
        for i = 1:length(other_Ues)
            interfere = [interfere h(BS2Ue(other_Ues(i)), :, iU)*wK(:, other_Ues(i))];
        end
        
        SINR(iU) = User_power/norm(interfere)^2;
    end
    
    for iU =1:1:NumUes
        sumrate(iter) = sumrate(iter)+weights(iU)*log2(1+SINR(iU));
    end
%     if iter>=2 && (sumrate(iter)-sum(iter-1))<tol
%         sumrate(iter:end) = [];
%         break   
%     end
    
end
figure()
plot(sumrate)

```

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/simulationofSCA.jpg" alt="simulationofSCA" style="zoom:33%;" />

### Github 

```matlab
%{
 Simulation code for for Algorithm 1 presented in the following scientific paper:
 "Fast Converging Algorithm for Weighted Sum Rate Maximization in Multicell 
 MISO Downlink by Le-Nam Tran, Muhammad Fainan Hanif,Antti Tolli, Markku Juntti,
 IEEE Signal Processing Letters 19.12 (2012): 872-875
%}
clear variables
clc
clear
close all;

% Number of RX antennas
M=1;

% Number of antennas for each BS
nTx=8;

% total users
nUsers=4;

% No. of cells
nCells=2;

% for nUsers=4, usercellindex = [1 1 2 2], the first two elements give the users served
% by BS 1 and the other two elements give indeces of users served by BS 2
usercellindex=[1 1 2 2];

noise_power = 1; % noise power
powerpercell = 12; % maximum tx power per cell in dB (i.e., normalized with noise power)

powerpercell = 10.^(powerpercell./10)*ones(nCells,1); 

nIterations = 40;% maximum # of iterations

weights = [1; 1; 1; 1]; % for sum rate maximization

% generate channels
channel = sqrt(1/2)*(randn(M, nTx, nUsers, nCells)+ ...
                    1i*randn(M, nTx, nUsers, nCells));

%% Generate a feasible initial point
% Procedure: first generate  beamformers that stisfy the power constraints 
% and calculate \phi 
winit = rand(nTx,nUsers) + 1i*rand(nTx,nUsers); % randn can also be used here
for iCell = 1:nCells
    winit(:,usercellindex==iCell) = sqrt(powerpercell(iCell))/norm(winit(:,usercellindex==iCell))*winit(:,usercellindex==iCell); % scalling to meet the power constraint
end
mybetaInit = zeros(nUsers,1);
xInit = zeros(nUsers,1);
for iUser=1:nUsers
    % find the index of the other users
    otherusers = find(1:nUsers ~= iUser);
    mybetaInit(iUser) = norm([noise_power;diag(((reshape(channel(:,:,iUser,usercellindex(otherusers)),nTx,[])).')*(winit(:,otherusers)))]); % set (6d) to equality
    xInit(iUser) = (abs(channel(:,:,iUser,usercellindex(iUser))*winit(:,iUser))/mybetaInit(iUser))^2;  
end
phi = sqrt(xInit)./mybetaInit;
tNext = (1+xInit).^weights;

%% To generate Fig. 2, uncomment the following four lines
% load('channel.mat')
% tNext=ones(nUsers,1);        
% phi = 1./[0.14285714 2857143;0.214285714285714;0.285714285714286;0.357142857142857];
weights = [0.14;0.21;0.28;0.36]; % weights in Fig. 2

% scale the weights so that all are larger than 1 
% scalecoeff = 1.1/min(weights);
% weights = scalecoeff*weights;
scalecoeff = 1;

% error tolerance. Algorithm terminates if the increase between two iterations < tol
tol = 1e-2;   
% memory allocation
sumrate = zeros(nIterations,1); % the sequence of sum rate
weightedsumrate = zeros(nIterations,1); % the sequence of weighted sum rate
seqobj = zeros(nIterations,1); % the sequence of the objective of subproblems
%% main loop
for iIteration=1:nIterations
    cvx_begin   quiet
    variables   t(nUsers) mybeta(nUsers) x(nUsers) ;
    variable    w(nTx,nUsers) complex;
    maximize(geo_mean(t)) % CVX automatically implements (11b) and (11c)
    subject to
    for iUser=1:nUsers
        b = (channel(:,:,iUser,usercellindex(iUser))*w(:,iUser)) - 1/(phi(iUser)*2)*(x(iUser));
        imag(channel(:,:,iUser,usercellindex(iUser))*w(:,iUser)) == 0; %(6c)
        
        % constraint (11d) in the paper
        norm([0.5*(b-1);sqrt(phi(iUser)/2)*(mybeta(iUser))]) <= 0.5*real(b+1) ;
        
        % constraint (11e)
        x(iUser) >= tNext(iUser)^(1/weights(iUser))-1 + 1/weights(iUser)*(tNext(iUser)^(1/weights(iUser)-1))*(t(iUser)-tNext(iUser));
        
        % find the index of the other users
        otherusers = find(1:nUsers ~= iUser);
        
        interference = [noise_power;diag(((reshape(channel(:,:,iUser,usercellindex(otherusers)),nTx,[])).')*(w(:,otherusers)))];
        
        % constraint (11f)
        norm(interference) <= mybeta(iUser);
    end
    
    % implicit constraints in t (refer to (6b))
    t >= 1;
    
    % constraint (11g)
    for iCell=1:nCells
        norm(vec(w(:,usercellindex==iCell))) <= sqrt(powerpercell(iCell));
    end
    cvx_end;
    
    if(contains(cvx_status,'Solved'))
        
        % Step 3 of Algorithm 1 in the paper
        phi = x.^(0.5)./mybeta;
        tNext = t;
        
        %compute objective sequence returned by the solver after each iteration
        seqobj(iIteration) = sum(log2(t));
        
        % save the current values of beamformers
        beamformer = w;
        
        % compute the WSR and SR for each iteration
        for iUser=1:nUsers
            otherusers = find(1:nUsers ~= iUser);
            interference = [noise_power;diag(((reshape(channel(:,:,iUser,...
                usercellindex(otherusers)),nTx,[])).')*((beamformer(:,otherusers))))];
            
            % compute SINR for each user
            SINR=abs(channel(:,:,iUser,usercellindex(iUser))*beamformer(:,iUser))^2/((norm(interference))^2);
            
            % WSR and SR calculation
            weightedsumrate(iIteration) = weightedsumrate(iIteration) + weights(iUser)*log2(1+SINR);
            sumrate(iIteration)  = sumrate(iIteration)+log2(1+SINR);
        end
        % check stopping criterion
        if (iIteration>1)&&(abs(weightedsumrate(iIteration)-weightedsumrate(iIteration-1)) < tol)
            seqobj(min(iIteration+1,nIterations):end)=[];
            sumrate(min(iIteration+1,nIterations):end)=[];
            weightedsumrate(min(iIteration+1,nIterations):end)=[];
            break; %  converge, break
        end
    else % numerical issue
        disp('There may be a numerical issue in the solver. Early termination');
        break; 
    end
end
% rescale the objectives
seqobj = seqobj/scalecoeff; 
weightedsumrate = weightedsumrate/scalecoeff;
sumrate = sumrate/scalecoeff;

plot(1:length(weightedsumrate),weightedsumrate,'-rs','MarkerEdgeColor','r',...
                'MarkerFaceColor','r');
hold on
plot(1:length(seqobj),seqobj,'-bd','MarkerEdgeColor','b',...
                'MarkerFaceColor','b');
grid on            
xlim([1-0.1 length(seqobj)]);

xlabel('Iteration index');
ylabel('Weighted sum rate (b/s/Hz)');
h=legend( 'Weighted sum rate','The objective sequence of convex approximate subproblems','Location','SouthEast');
set(h,'Color', 'w','box','on','EdgeColor','w');
saveas(gcf, './ConvergencePlot.png')
```



## Note

- 变量比较多，首先得确定哪些是需要迭代的。这篇文章中需要迭代$$\phi_k$$和$$t_k$$，但是$$\phi_k$$和$$t_k$$需要$$\beta_k$$和$$x_k$$。所以首先得先给出一个$$\phi_{k-init}$$和$$t_{k-init}$$来进行迭代。

- 有些东西还不能直接求，得转换为一个SOC（二阶锥优化问题）约束去做。
- ![image-20220714152754044](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220714152754044.png)
- 放缩的时候都是大于符号右端放大。

