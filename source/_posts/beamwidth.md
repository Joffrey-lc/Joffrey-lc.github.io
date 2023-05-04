---
title: 知识储备-波束宽度
excerpt: 波束宽度和扫描角度的关系
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202303281328609.gif
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - beam width
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2023-03-28 13:12:55
---

## 天线方向图

天线方向图：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202303281321924.png" alt="image-20230328132116860" style="zoom:33%;" />



由两部分组成，第一部分是{% label primary @Element Factor %}，称为{% label primary @阵元因子 %}，第二部分是{% label primary @Array Factor%}，称为{% label primary @阵（列）因子%}。

>Element Factor：阵列的每个独立阵元（或许是贴片）都存在增益。定向天线？全向天线？
>
>Array Factor：通过阵列波束成型会产生增益影响。波束赋形

总的天线方向图是二者的乘积。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202303281325821.gif" alt="图片来源link1" style="zoom:33%;" />

Ref:https://blog.csdn.net/qq_23176133/article/details/120056777



在我的理解中，如果是全向天线，可以认为Element Factor 在各个方向上都是相同的定值；对于定向天线，就不一样了。

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202303281326726.png" alt="image-20230328132636687" style="zoom:33%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202303281326397.png" alt="image-20230328132652356" style="zoom:33%;" />

Ref:https://blog.csdn.net/qq_23176133/article/details/120056777



当$$d=0.5\lambda$$时，有Array Factor方向图：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202303281328609.gif" alt="在这里插入图片描述" style="zoom:33%;" />

Ref:https://blog.csdn.net/qq_23176133/article/details/120056777

当$$d=0.8\lambda$$时，有Array Factor方向图：

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202303281328489.gif" alt="在这里插入图片描述" style="zoom:33%;" />

Ref:https://blog.csdn.net/qq_23176133/article/details/120056777



参考雷达通信电子战的[公众号文章](https://mp.weixin.qq.com/s/IoBHFRdP2PhJnElv0OzZEw)，以及问题：https://ask.csdn.net/questions/1049835，有代码：

```matlab
% 更多专业内容请关注：
% 雷达通信电子战
clc;clear all;close all;
N=32;
a=0.5; % a=d/lambda
theta=-pi:0.01:pi;
for thetaB=0:1:60
    thetaB1=thetaB/180*pi;
    sum=0;
    for i=0:N-1
        y1=exp(1i*2*pi*i*a*(sin(theta)-sin(thetaB1)));   
        sum=sum+y1;
    end    
    sum=abs(cos(theta).^0.5.*sum);
    sum=sum/N;
    clf;
%     polarplot(theta,sum2,'-r');
    polarplotdb(theta,sum,'-r');
    pause(0.0005);    
end
 
 
for thetaB=60:-1:0    
    thetaB1=thetaB/180*pi;    
    sum=0;
    for i=0:N-1
        y1=exp(1i*2*pi*i*a*(sin(theta)-sin(thetaB1)));   
        sum=sum+y1;
    end    
    sum=abs(cos(theta).^0.5.*sum);
    sum=sum/N;
 
    clf;
%     polarplot(theta,sum2,'-r');
    polarplotdb(theta,sum,'-r');
    pause(0.0005);    
end

```

当为全向天线，将line 14 {% label primary @cos(theta).^0.5%}置1,即可。

## 波束宽度

$$
A F[\theta]=\frac{\sin \left(\frac{N \pi d}{\lambda}\left[\sin (\theta)-\sin \left(\theta_0\right)\right]\right)}{N \sin \left(\frac{\pi d}{\lambda}\left[\sin (\theta)-\sin \left(\theta_0\right)\right]\right)}
$$

其中$$\theta_0$$为波束指向方向（中线的指向方向），$$AF[\theta]$$为在$$\theta$$方向上的波束增益。注意，这里只考虑了Array Factor,没有考虑Element Factor，因为Element Factor只决定了在该方向上的增益大小，但是不决定波束宽度（算3dB可能要考虑？）。







---

上述内容还有个Niub的参考文献：

Delos, Peter, Bob Broughton, and Jon Kraft. "Phased array antenna patterns-part 1: Linear array beam characteristics and array factor." *Analog Dialogue* 54.2 (2020): 1-8.

其中文版：

https://www.analog.com/media/cn/analog-dialogue/volume-54/number-2/phased-array-antenna-patterns-part-1-linear-array-beam-characteristics-and-array-factor_cn.pdf

---
