---
title: 通信基础-Digital and Analog Modulation with Polar Code and Frequency hopping
excerpt: 2FSK\4QAM\4PSK\2ASK and AM\DSB\SSB\FM
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202305041514196.jpeg
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Modulation
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2023-05-04 14:06:53
---

[All Code can be found in Github](https://github.com/Joffrey-lc/Digital-and-Analog-Modulations)

Digital Modulations and Analog Modulations including 2FSK\4QAM\4PSK\2ASK and AM\DSB\SSB\FM. 

There are Polar code and frequency hopping in Digital Modulation.



Especially, due to the imperfect character of digital filter, the simulation of 2FSK does not match the theoretical values. The difference will vanish with the decreased number of frequencies selected in frequency hopping. 

## Digital Modulations 

### QPSK



<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202305041514196.jpeg" alt="decd46a10e4237aff3048222793848a" style="zoom:33%;" />

### 2ASK

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202305041514179.jpeg" alt="d53b5853c39d163163f835c4059b947" style="zoom: 33%;" />

### 2FSK

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202305041514186.jpeg" alt="da402ee4c27ddd3f2e27e562eb6b8b1" style="zoom:33%;" />

==(No longer envelope detection)==

```matlab
 for p=1:1:length(st1)/sps
    for is = sps*(p-1):sps*(p)-1
        st1_sum(p) = st1_sum(p)+st1(is+1);
        st2_sum(p) = st2_sum(p)+st2(is+1);
    end
end
rx_data = (st1_sum-st2_sum);
```

### 4QAM

![a940b5d5779316e9e05e8e7b8dbe19e](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202305041514171.jpeg)

## Analog Modulations

### AM

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202305041514168.jpeg" alt="889aaf78e35af52c2a35489fa447c5a" style="zoom:50%;" />

Refer to《通信原理》-第七版（樊昌信）Page 87

It should satisfy $$|m_t|_{max}\leq A_0$$ and then we can use envelope detection

### DSB

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202305041514101.jpeg" alt="9eb6e312bb328814357b3fbf99de153" style="zoom: 50%;" />

### SSB

Refer to 

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202305041514647.png" alt="image-20230327152726140" style="zoom: 25%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202305041514637.png" alt="image-20230327152714021" style="zoom:33%;" />

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202305041514718.jpeg" alt="a1a6e44169f9c3a43d61b8664bb7db7" style="zoom:33%;" />

### FM

![b3b580ca7fc4769612aee4ed9decdee](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202305041514778.jpeg)

## Notes

Sampling a stream of data with a small sampling rate will fold the signal, which means:
$$
f_\text{target}=\left\{f_{\text{original}}/f_s\times2-\text{floor}(f_{\text{original}}/f_s\times2)\right\}\times f_s.
$$
.But in 2FSK, we found that:

- If  $$f_{\text{original}}/f_s$$ is even, it holds,
- If $$f_{\text{original}}/f_s$$ is odd, it should be $$f_{t}=0.5\times f_s-f_{\text{target}}$$

---

We use digital filter in matlab and there will be a time delay. It can be calculated as:

```matlab
function out = firFilter(N, Wn, data)
    fir_lp =fir1(N, Wn, 'low'); %截止频率为Wn*(fs/2) 使用汉明窗设计一个N阶低通带线性相位的FIR滤波器。
    out = conv(fir_lp,data);
    delay_t = round((length(fir_lp)-1)/2);  %低通滤波器的延迟时长
    out = out(delay_t+1:end-delay_t);
end
```

---

Conversion between EbN0 and SNR:

```matlab
EbN0 = 0:1:20; % Eb是每个bit的能量,N0是噪声的功率谱密度;EbN0=Eb/N0;
snr = EbN0 - 10*log10(sps*1/2)+10*log10(log2(M)); % SNR和EbN0转换
```

![image-20230504151349128](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202305041514958.png)

