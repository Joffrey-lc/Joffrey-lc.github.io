---
title: VVVVocabulary词汇
excerpt: 整理了一下专业词汇，特别是写文章的时候的框架
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img220/202208291846466.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - utils
categories:
  - Study field
comment: valine
math: true
hide: false
date: 2022-08-29 18:44:31
---

## 专业名词

- incident signal  入射信号
- inductance, capacitance, and resistance 电感、电容和电阻
- Base Stations 基站
- Wireless Routers 无线路由器
- Relays： 中继器
- Information Gateways： 信息网关
- Power Beacons: 能量塔
- identity matrix: 单位阵
- Benchmark Strategies/Benchmarking Schemes: 基准方案
- aforementioned: =mentioned above

- part->component 

- overhead：开销

- illustrate： 介绍/展示

- architecture： 架构



## 常见的框架

顺序：Assumption, Lemma, Theorm, Proof, Remark

- Assumption：假设，后面的Theorem{% label  success @一般会用到这个Assumption %}。

```latex
\newtheorem{assumption}{Assumption}[section]
\begin{assumption}
***
\end{assumption}
```

- Lemma：引理，{% label  success @一般是前人已经证明的结论 %}。

```latex
\newtheorem{lemma}{Lemma}[section]
\begin{lemma} \label{lemma1}

\end{lemma}
```

- Theorem：定理，{% label  success @是自己论文推导出的理论，也是论文主要的贡献说明 %}。

```latex
\newtheorem{thm}{\bf Theorem}[section]
\begin{thm}\label{thm1}

\end{thm} 
```

- Proof：证明，{% label success @证明之前的Theorem %}。

```latex
\begin{proof}
***
\end{proof}
```

- Remark：备注，{% label success @对Theorem进行说明补充 %}，例如解释自己的Theorem和别人的不同或者拓展Theorem到更广泛的模型；亦或者说明Theorem的有点，Motivation等。

---

- Observation: (Bruno—Survey(both two))一般是由公式、图像可以明显得到的结论，感觉可能用在Survey比较合适，目前没有看到其他地方使用

