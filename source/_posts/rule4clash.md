---
title: 设置CLASH规则
excerpt: 更新配置文件不覆盖
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20211203212547096.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - clash
categories:
    - utils
    - 科学上网
comment: valine
math: true
hide: false
date: 2022-01-19 17:26:26
---

# 设置CLASH规则

因为最近发现在clash中设置规则，一旦更新配置文件，就会将之前的规则覆盖掉。所以研究了一下怎么在解析器中直接添加规则，这样以后更新配置文件也不会覆盖掉规则了。

找到clash->settings->profiles->parsers->edit

![98e560c90353e3ce71da9cb8f75a6eb](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/98e560c90353e3ce71da9cb8f75a6eb.png)

然后在以下界面中编辑自己的规则

![image-20220119170045041](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220119170045041.png)

其中url是自己的订阅地址，也能在配置文件中找到。具体路径如下（就是URL）：

![image-20220119170213721](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220119170213721.png)

在prepend-rules中设置自己的规则：

```
parsers: # array
  - url: https://xxxxxxxxxxxxx
    yaml:
      prepend-rules:
        - DOMAIN-SUFFIX,ieeexplore.ieee.org,DIRECT
```

我这里设置ieee的网站都使用直连，方便使用校园网下载文献。

其他的规则类型还有：

![image-20220119172231945](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220119172231945.png)

- DOMAIN-SUFFIX：域名后缀匹配
- DOMAIN：域名匹配
- ......

连接的策略有：

![image-20220119172307480](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20220119172307480.png)

- Direct：直连，不使用代理
- Reject：拒绝访问
- ......
