---
title: anaconda+pycharm+pytorch1.7+tensorflow1.14.0+tensorflow2.2.0多种环境共存
excerpt: Anaconda+Pycharm YYDS
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20211203212547096.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Deep Learning
  - python
categories:
  - envs
comment: valine
math: true
hide: false
date: 2021-12-04 15:01:56
---

# 前期准备
Anaconda+pycharm+pytorch 的安装见我[前期博文(点这里)](https://blog.csdn.net/qq_41380292/article/details/107693355)
# 说明
Anaconda起到一个包管理的作用，可以将不同环境的python、库等分隔开来，互不影响。所以我们可以搭建不同的框架和环境且互相独立。（为了保证我和师兄的代码互相能看懂，只能舍弃pytorch了。pytorch yyds！）
# 查看匹配
首先明确一件事情，tensorflow、cudnn、cudatoolkit（cuda）是我们每个tensorflow环境需要安装的。这三个库之间是有一个匹配关系。这个匹配关系不对会导致安装后报错。建议大家先明确一下匹配关系，需要下载哪个版本的（百度或者官网查）。
下面给出我安装的两个版本的对应关系：
| tensorflow版本 | cudnn | cudatoolkit |
| -------------- | ----- | ----------- |
| 1.14.0         | 7.6.4 | 10.0        |
| 2.2.0          | 7.6.5 | 10.1        |
# 新建Anaconda环境
打开Anaconda或Anaconda prompt，然后按照前面博文中[“创建新环境”](https://blog.csdn.net/qq_41380292/article/details/107693355)小节操作即可。
在此我创建了一个名为tensorflow1_14_0的新环境。python版本选择3.6
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20201205225552692.png)
#  安装CUDA
首先打开Anaconda prompt，激活刚刚创建的环境：
```python
activate tensorflow1_14_0
```
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20201205230032718.png)
可以看到环境从之前的mytorch（我修改了默认，正常默认环境是base）变为了新创建的tensorflow1_14_0
然后在Anaconda prompt中通过命令下载==对应版本的cuda==：
```python
conda install cudatoolkit=10.0
```
这里建议大家参考[我的博文](https://blog.csdn.net/qq_41380292/article/details/107693355)换源，如果不换源会很慢。
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/2020120523150050.png)
# 安装cudnn
同样在Anaconda prompt中键入(注意版本号)：
```python
conda install cudnn=7.6.4
```
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/2020120523190131.png)
# 安装tensorflow
tensorflow分为CPU版本和GPU版本。GPU版本自带了CPU版本。
如果想安装CPU版本，使用命令:
```python
pip install -i https://pypi.doubanio.com/simple/ tensorflow==1.14.0
```
这里借助了豆瓣源，实测要快一些。
如果安装GPU版本，如下：
```python
pip install -i https://pypi.doubanio.com/simple/ tensorflow_gpu==1.14.0
```
然后在Anaconda中进入python编译：
```python
python
```
调用tensorflow包
```python
import tensorflow
```
会出现一堆错误：
FutureWarning: Passing (type, 1) or '1type' as a synonym of type is deprecated; in a future version of numpy, it will be understood as (type, (1,)) / '(1,)type'.
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20201205232816515.png)
不要怕，问题很简单，numpy版本过高。这是我用Anaconda经常会遇到的问题。每次都是numpy整个最新版，不知道是为什么。
我们需要做的就是给numpy降级。如下我给了两个版本的参考（我是这么装的没问题），大家有兴趣可以试试其他版本。

| tensorflow版本                                               | numpy版本 |
| ------------------------------------------------------------ | --------- |
| 1.14.0                                                       | 1.16.0    |
| 2.2.0                                                        | 1.17.0    |
| 为了降级，输入命令（我这里是tensorflow1.14.0，对应的numpy1.16.0）： |           |
```python
conda install numpy==1.16.0
```
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20201205233318517.png)
然后可以检查一下是否安装完成了，即在python编译器中输入:
```python
import tensorflow as tf 
tf.__version__
```
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20201205234611462.png)
看到确实是1.14.0
==完成了吗？？==
试一下pycharm，同之前的博文，在pycharm中的编译器选择Existing environment->anaconda安装目录下的env->tensorflow1_14_0（环境名）->python.exe
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20201205234951589.png)
 等待库全部加载完，新建一个python文件，键入以下代码测试：
 ```python
 import tensorflow as tf
import os
# 降低警告优先级，去掉一堆加速警告。可以不写
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

gpu_device_name = tf.test.gpu_device_name()
print(gpu_device_name)

print(tf.test.is_gpu_available())  # 返回True或者False
 ```
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20201205235651478.png)
可以看到安装成功！！！：）
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20201206000927183.png)
我现在四个环境共存了。

# 写在最后
1. tensorflow2.2.0安装过程完全一样，只是把cudnn、tensorflow、cudatoolkit的版本号改掉就可。
2. 可能会遇到DLL 未找到。。。之类的错误，可能是没装Microsoft vistal C++ 。但我的解决方案是在环境变量中把新建的环境下的路径添加到环境变量中，如：
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20201206000036986.png)
有兴趣可以试试。

（tensorflow1.x真的不友好TAT还是keras和pytorch好使）
