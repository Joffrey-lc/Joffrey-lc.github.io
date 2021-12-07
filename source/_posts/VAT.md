---
title: Virtual Adversarial Training文章解读+算法流程+核心代码详解
excerpt: 阅读解析VAT
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20211203212547096.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Deep Learning
categories:
  - Paper Reading
  - Semi-Supervised Learning
comment: valine
math: true
hide: false
date: 2021-12-04 14:53:33
---

# Virtual Adversarial Training
*本博客仅做算法流程疏导，具体细节请参见原文*
## 原文
[查看原文请点这里](http://arxiv.org/abs/1704.03976)
## Github代码
[Github代码请点这里](https://github.com/9310gaurav/virtual-adversarial-training)
## 解读
### 对比Adversarial Training和VAT
VAT(Virtual Adversarial Training)和adversarial training类似。对原始训练样本添加一个比较小的扰动，会大概率使分类器分类出现错误，而我们一般希望分类器将原始样本和添加一个较小扰动的样本（加噪版本）分为同一类别，所以将扰动版本的数据也作为训练样本添加进训练，这样就增加了分类器的泛化能力。

传统的adversarial training 的扰动方向一般通过损失函数确定，即取损失函数上升的方向添加一个扰动。无标记样本没有标签，就无法算损失函数，故传统方法不适用，所以一般的adversarial training仅在监督学习中使用较多，而virtual adversarial training的创新在于能在无标记样本上实现扰动的计算，因为没用使用标签进行运算，而是用模型预测的结果替代标签，类似于persudo label，这就是virtual的含义
#### Adversarial Training
adversarial training的数学表达如下，其中样本及标记$(x,y)$，当前epoch模型的参数$\theta$:
**损失函数**：$J(\theta)=\frac{1}{N}\sum^{N}_{i=1}L(x,\theta)$
其中，**单项损失**计算表达式为：$L(x,\theta)=D(y,p(y|x+r,\theta))$
**扰动方向**：$r=argmax_{|r|<\xi}D(y,p(y|x+r,\theta))$

简单叙述为：找到一个扰动$r$，且$r$的大小受限，即$|r|<\xi$，使其损失函数$L(x,\theta)=D(y,p(y|x+r,\theta))$取最大值，即在此$r$下上升最多。
#### VAT
同样形式的，virtual adversarial training 的数学表达式如下，其中其中样本及标记$(x,y)$，当前epoch模型的参数$\theta$，前一个epoch的模型参数为$\hat{\theta}$：
**损失函数**同上形式：$J(\theta)=\frac{1}{N}\sum^N_{i=1}L(x,\theta)$
**单项损失**表达式==不同==(LDS称为局部平滑度)：$L(x,\theta)=D(p(y|x,\hat\theta),p(y|x+r,\theta))=LDS(x,\theta)$
**扰动方向**：$r=argmax_{|r|<\xi}D(p(y|x,\theta),p(y|x+r,\theta))$

简单叙述为：找到一个扰动$r$，且$r$的大小受限，即$|r|<\xi$，使其损失函数$LDS(x,\theta)$取的最大值，即在此$r$下上升最多。


## 代码详解
代码核心就一个**VAT_Loss**的计算。整个框架的**Loss=Classfier_Loss + VAT_Loss**。其中**Classfier_Loss**损失函数为一般的监督网络的损失函数。**VAT_Loss**计算如下：
```python
def vat_loss(model, ul_x, ul_y, xi=1e-6, eps=2.5, num_iters=1):
    # find r_adv
    d = torch.Tensor(ul_x.size()).normal_()
    for i in range(num_iters):
        d = xi *_l2_normalize(d)
        d = Variable(d.cuda(), requires_grad=True)
        y_hat = model(ul_x + d)
        delta_kl = kl_div_with_logit(ul_y.detach(), y_hat)
        delta_kl.backward()
        d = d.clone().cpu()
        model.zero_grad()
    d = _l2_normalize(d)
    d = Variable(d.cuda())
    r_adv = eps * d
    # compute lds
    y_hat = model(ul_x + r_adv.detach())
    delta_kl = kl_div_with_logit(ul_y.detach(), y_hat)
    return delta_kl
```
其中对**r_adv**的计算采用的是一种快速计算方法。具体理论请[查阅原文](http://arxiv.org/abs/1704.03976)
```python
v_loss = vat_loss(model, inputs_All, logits_All, eps=args.epsilon)
loss = v_loss+ce_loss
optimizer.zero_grad()
loss.backward()
optimizer.step()
```
完整损失函数**Loss=Classfier_Loss + VAT_Loss**反向梯度传播更新网络即可。
