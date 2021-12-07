---
title: 树莓派+Git——GitPi启动（树莓派搭建git服务器）并解决git bash中文英文乱码的问题
excerpt: Git Pi 已启动！
index_img: https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211204151836098.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - RaspberryPi
categories:
  - gadget
  - Raspberry Pi
comment: valine
math: true
hide: false
date: 2021-12-04 15:23:25
---

# 准备
1. 装好系统的树莓派
2. win10+git

# 树莓派安装git
在树莓派的命令行中输入以下安装Git：
```
sudo apt-get install wget git-core
```
（如果没安装的话）安装ssh：
```
sudo apt-get install ssh
```
设置自启动ssh：
```
sudo /etc/init.d/ssh start
sudo update-rc.d ssh defaults
```
# 添加用户和组
会在树莓派/home下创建一个git文件夹，用作储存。
```
adduser --system --shell /bin/bash --gecos 'git version control by pi' --group --home /home/git git
```
如果想要更换目录，请更改”/home/git”
然后更改git用户的密码，以后每次上传都需要使用：
```
passwd git
```
~~当然，如果想要删除git用户，使用~~
```
userdel git
```
这个时候，可以通过文件管理器查看树莓派/home中多了一个git空文件夹。
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200810110631578.png)
# 创建新的仓库并初始化
正式开始，我们需要先在树莓派上创建一个新的仓库。这就是管理我们代码的地方。
首先，先进入/home/git 路径：
```
cd /home/git
```
切换至创建的git用户:
```
su git
```
会提醒输入password，输入之前修改的密码后，成功切换用户。
创建一个新的仓库：
```
mkdir test.git
```
创建后需要进入仓库（否则初始化的是git文件夹）：
```
cd test.git
```
初始化仓库：
```
git --bare init
```
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200810111257618.png)
树莓派上的操作全部完成，可以打开test.git看到里面多了一堆东西
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200810111347786.png)
# 在win10上上传文件至远程仓库
对于我们的PC而言，树莓派的仓库就相当于一个远程仓库。（树莓派和PC必须要连接同一网络）
在想要保存文件的路径下（此处我放在桌面）鼠标右击，点击git bash here，打开git bash
先将我们创建的远程仓库clone下来：
```
git clone git@192.168.0.106:/home/git/test.git
```
（此处我的树莓派ip地址是192.168.0.106；我们要clone的仓库是之前创建的位于/home/git下的test.git）
输入密码后会提醒clone了一个空仓库
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200810111947936.png)
看桌面也发现多了一个test文件夹，就是我们的仓库。
然后打开桌面上的文件夹，增加修改。为了演示方便，我增加了一个名为“中文测试.txt”的文件。
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/202008101121278.png)
然后和正常上传文件的方法一样，git bash 进入test文件夹。
然后添加所有文件
```
git add .
```
提交修改进暂存区：
```
git commit -m "上传了一个中文名的文件"
```
提交至远程仓库：
```
git push origin master
```
没有意外的话就提交成功了！
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200810112438991.png)
我们再测试一下提交的成果。先退出test文件夹，删除test文件夹，并再次clone
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/2020081011261574.png)
再在桌面打开test文件夹，发现确实是我们修改后的文件！
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200810112701796.png)
再在git bash 中查询记录：
```
git log 
```
(我的自定义了log->lg，所以我的是git lg)
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200810112837354.png)
完美！！

# 总结
1. 先在树莓派创建用户和仓库。并初始化。后续使用只需要创建仓库即可，不需要重复创建用户（会告诉你用户已存在）。
2. 在电脑上clone创建的远程仓库，并修改后，正常提交即可。

# 可能遇到的问题
1. 在git bash中可能出现英文乱码的情况。
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200810113458404.png)
测试了一下上传github没有问题，说明是树莓派的文字编码有问题，于是我把树莓派的文字显示改回了英文，修复了该问题。
在树莓派命令行中：
```
sudo nano/etc/default/locale 
```
将原来的配置内容修改为：
```
LANG=zh_CN.UTF-8
LANGUAGE=en_US:en
```
（ctrl+X保存并退出）再
```
locale-gen -en_US:en
```
重启树莓派即可生效。

2. git bash 在提交文件时，如果文件中有中文，可能出现乱码。
测试了GitHub也有这样的现象，说明是win10的问题。正常而言[参考知乎](https://zhuanlan.zhihu.com/p/91741156)即可解决。如果和我一样还是无法解决的，问题可能在于win10默认的中文编码方式是GKB，而更国际化的是utf-8，修改win10中文编码为utf-8即可。![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200810114350471.png)
①打开语言中的 管理语言设置
②点击 更改系统区域设置
③勾选beta版
④确定 并重启电脑 完成！
