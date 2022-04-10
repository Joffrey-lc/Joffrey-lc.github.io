---
title: Typora And Hexo工具箱
excerpt: Typora和Hexo工具集合，持续更新
index_img: >-
 https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211204140733338.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Typora
  - Hexo
  - utils
categories:
  - utils
  - Typora
comment: valine
math: true
hide: false
date: 2022-04-09 22:38:43
---

## Typora 工具箱

### 公式编号

- 手动：

```markdown
$$y=a+b\label{eqn:1}\tag{1}$$
This is eqn $$\ref{eqn:1}$$
```


$$
\begin{align*}
y=a+b\label{eqn:1}\tag{1}
\end{align*}
$$

This is eqn $$\ref{eqn:1}$$

- 自动：

打开偏好设置中的自动编号，就不用写 \tag{1} 了。

### 引用段落

```markdown
[引用第一段](###公式编号)
```



[引用第1.1段](###公式编号)

## Hexo Fluid 工具箱

### 段落标签

```markdown
{% note success %}
文字 或者 markdown 均可
{% endnote %}
```

{% note success %}
文字 或者 markdown 均可
{% endnote %}

### 段内标签

```markdown
{% label primary @text %}
```

{% label primary @在这里填写的文字部分（text部分）不能以(at)开头 %}
