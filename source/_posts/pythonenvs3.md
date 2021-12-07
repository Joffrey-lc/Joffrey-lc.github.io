---
title: 安装Anaconda+pytorch+pycharm配置，并创建新的环境
excerpt: Anaconda+Pycharm YYDS*2
index_img: https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20211203212547096.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Deep Learning
  - python
categories:
  - envs
comment: valine
math: true
hide: false
date: 2021-12-04 15:14:31
---

# 提前准备

检查一下系统是否已经安装了python，建议删除，不然容易遇到一些奇怪的问题。
如果需要卸载已有的python，先查询自己python版本，再下次相同版本，点击运行时选择uninstall即可。
如果想完全卸载anaconda，参考[如何彻底的卸载anaconda（包括配置文件）](https://blog.csdn.net/kuweicai/article/details/90145242)

# 下载并安装Anaconda
## 下载Anaconda
   直接[官网下载](https://www.anaconda.com/products/individual).
## 安装Anaconda
  傻瓜式安装一路next。值得注意的是：
![选择是否添加路径](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200730171324257.png)
此处的路径不添加也可，后面在环境变量手动加。
![了解更多](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/202007301712511.png)
此处两个勾都去掉。

安装完成后，如果添加了环境变量anaconda安装就完成了，没有添加的话：

1.win + S 输入 环境变量，打开系统环境变量中的path变量
2.根据自己anaconda安装路径添加：
![根据自己路径添加环境变量](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200730174738575.png)

Anaconda安装完成！可以使用 win+R 打开cmd ，输入python检查是否安装完成。
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/2020073018183797.png)
## 换国内镜像源
然后换清华的源（不然下载库会很慢）

1.win + R  输入:
```
%HOMEPATH%
```
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200730172715491.png)
2.进入路径，打开.condarc
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200730172743361.png)
3.修改为如下即可：
```
channels:
  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/peterjc123/

show_channel_urls: true
ssl_verify: true
```
没有.condarc文件的话，先在cmd中输入

```
conda config --add channels http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
conda config --add channels http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
conda config --set show_channel_urls yes
```
也可以生成.condarc文件并换源
## 创建新环境
方法一： 
	可以通过打开Anaconda Navigator -->Enviroments-->Create 来创建新环境
![创建新环境方法1](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200730180857607.png)
方法二（个人推荐）：
使用 Anaconda Prompt （win + s 搜索），输入：

```
conda create -n xxxxx python=?? anaconda
```
其中xxxxx是自己想创建的环境名 ；??是python版本号，如下图
![](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200730181423527.png)
可以看到一堆要安装的包。如果不想安装这么多，可以创建一个只有最基本包的环境，和上面命令大致一样，只是不要最后的 anaconda ：
```
conda create -n xxxxx python=??
```
因为换了源，所以这一步应该比较快。完成后可以在Anaconda Prompt中检查：
```
activate xxxxx
```
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200730182210831.png)
可以看到前缀由（base）变成了（xxxxx），base是anaconda自带的，xxxxx是刚刚创建的。我创建的名字是pytorch。

# 安装Pytorch
依然[官网下载](https://pytorch.org/)
然后根据自己的需要选择pytorch版本
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200730182712563.png)
然后复制官网生成的  Run this Command：
```
conda install pytorch torchvision cudatoolkit=10.2 pytorch
```
注意，这行代码去掉了 -c，是因为去掉后才会从清华的源上下载。
打开 Anaconda Prompt ，并激活需要安装pytorch的环境。我安装在刚刚生成的pytorch环境中。
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200730183025287.png)
安装pytorch完成。

这里可能还会遇到两个问题：
问题一：
如果pytorch安装在自己创建的环境中，例如我安装在了名为pytorch的环境中，需要重新设置环境变量：![重新设置环境变量](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200730183300706.png)
问题二：
python pycharm 和anaconda的库版本可能不合。
我的pytorch环境中python是3.7.8，而numpy是1.19.0。建议降低numpy的版本。在Anaconda Prompt中切换到需要更改的环境，输入：
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200730183727188.png)
等待完成即可。
到此完成了pytorch安装

# pycharm配置
安装就懒得写了。
在创建项目时，选择Existing interpreter：
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200730184208253.png)
点击Existing interpreter旁边的三个点展开选择。
再按顺序选择即可
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200730184457273.png)
此处的路径是安装anaconda的路径。如果选择的是base环境，python.exe的位置就在安装路径下；如果选择自己创建的环境，python.exe在。...(安装路径)\envs\xxxxx（自己创建的环境名）


完成！！！
