---
title: 知识储备-傅里叶级数
excerpt: Fourier Series
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20211203212547096.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Fourier Series
categories:
  - basic knowledge
comment: valine
math: true
hide: false
date: 2022-09-26 19:19:02
---

## 傅里叶级数

法国数学家[傅里叶](https://baike.baidu.com/item/傅里叶/841724?fromModule=lemma_inlink)认为，任何周期函数都可以用[正弦函数](https://baike.baidu.com/item/正弦函数/9601948?fromModule=lemma_inlink)和[余弦函数](https://baike.baidu.com/item/余弦函数/9602078?fromModule=lemma_inlink)构成的无穷级数来表示（选择正弦函数与余弦函数作为[基函数](https://baike.baidu.com/item/基函数/1801232?fromModule=lemma_inlink)是因为它们是正交的），后世称傅里叶级数为一种特殊的三角级数，根据[欧拉公式](https://baike.baidu.com/item/欧拉公式/92066?fromModule=lemma_inlink)，三角函数又能化成指数形式，也称[傅立叶级数](https://baike.baidu.com/item/傅立叶级数/7649046?fromModule=lemma_inlink)为一种指数级数[^1]。



给定一个周期为$$T$$的周期函数，那么它可以表示为无穷级数：
$$
x(t)=\sum_{k=-\infty}^{+\infty} a_k \cdot e^{j k\left(\frac{2 \pi}{T}\right) t}
$$
其中$$a_k$$可以由下式计算：
$$
a_k=\frac{1}{T} \int_T x(t) \cdot e^{-j k\left(\frac{2 \pi}{T}\right) t} d t
$$

[^1]:https://baike.baidu.com/item/%E5%82%85%E9%87%8C%E5%8F%B6%E7%BA%A7%E6%95%B0/5210337?fr=aladdin

