---
title: Linux服务器使用
excerpt: 实验室Linux python服务器
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20211203212547096.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Linux
categories:
  - utils
  - linux
comment: valine
math: true
hide: false
date: 2024-08-06 12:52:16
---

## 使用python脚本

### 直接使用

``` shell
python xxx.py
```



### 后台运行

```cmd
nohup python xxx.py &
```

然后在代码文件夹会生成一个nohup.out文件，记录cmd的输出

通过

```cmd
tail -f nohup.out 
```

查看

> 注意，nohup默认的python是系统默认base的python

解决办法是

```
conda activate myenv
nohup conda run -n myenv python main.py &
```

> 这种办法似乎会占用nohup.out文件，从而使输出在tail -f nohup.out 时不可以实时查看

另外一种是

```shell
nohup ~/.conda/envs/mypytoch/bin/python main.py &
```



### 查询

如果是当前shell的后台，可以直接

```shell
jobs
```

或者

```shell
jobs -l
```

查询，并且可以通过

```shell
fg jobsNum
```

调到前台

---

如果不是当前shell的后台，可以通过

```
ps -aux | grep xxx
```

进行查询，其中xxx可以是python or xxx.py


## linux 基础

### kill

```cmd
kill -9 PID
```

-9：强制执行

