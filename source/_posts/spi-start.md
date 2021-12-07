---
title: 树莓派启动——安装+无显示器使用+自启动VNC
excerpt: Raspberry Pi 启动！
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
date: 2021-12-04 15:16:47
---

时隔一年多，拿起树莓派却忘记如何使用了。本想用作自己搭建git服务器，后续再完成了。在此记录一下使用流程。

## 硬件准备
1. 树莓派(3b+)
2. TF卡和读卡器（16-256GB，但不要太大，SD卡格式化要很久。我是32GB）
3. 网线
4. 电源线


## 软件准备
（[至树莓派实验室下载](https://shumeipai.nxez.com/download#tools)）:
1. SD卡格式化工具 SD Formatter
2. 镜像烧录工具 Win32DiskImager
3. SSH工具 PUTTY
4. [树莓派os官网下载](https://www.raspberrypi.org/downloads/raspberry-pi-os/) 
5. VNCviewer


## 写入系统

1. 使用SD Formatter格式化TF卡![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/2020080916412384.png)
（格式化会有点久）
2.解压官网下载的操作系统，得到.img 文件。打开Win32DiskImager，在①中选择解压得到的.img文件；在②中选择自己的TF卡；点击③。系统烧录完成！！
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200809164521285.png)
## 启动树莓派

1. 首先电脑打开TF卡，创建一个名为ssh的空白文件（没有后缀）
2. TF卡插入树莓派，并通电。此时树莓派已启动。但由于没有多余的显示器，不能看到图形界面。
3. 用网线链接电脑和树莓派。
4. 在wlan属性中设置internet共享
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200809165043538.png)
5. 然后查询树莓派ip地址：
    通过cmd输入 arp -a，查看 b8-开头的ip就是树莓派ip。![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200809165641164.png)
6. 打开putty。输入ip地址打开。默认账号为:pi，默认密码为：raspberry。完成！
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200809165959464.png)
7. 为了看到图形界面，启动树莓派的vncserver，即在命令行中输入：
```
vncserver
```
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200809170309463.png)

8. 打开VNCviewer，输入ip地址和账号密码，即可看到图形界面了！

## 换源
1. 在terminal中输入：
```
sudo nano /etc/apt/sources.list
```
2. 注释掉源文件中的内容，更换为阿里源：
```
deb http://mirrors.aliyun.com/raspbian/raspbian/ stretch main contrib non-free rpi
deb-src http://mirrors.aliyun.com/raspbian/raspbian/ stretch main contrib non-free rpi
```
3. 打开并编辑/etc/apt/sources.list.d/raspi.list文件
```
sudo nano /etc/apt/sources.list.d/raspi.list
```
4. 注释掉源文件内容，更换为：
```
deb http://mirrors.ustc.edu.cn/archive.raspberrypi.org/debian/ stretch main ui
deb-src http://mirrors.ustc.edu.cn/archive.raspberrypi.org/debian/ stretch main ui
```
5. 更新软件源列表
```
sudo apt-get update
```
## VNC自启动
为了下次使用方便，首先将树莓派脸上wifi。通过图形界面右上角打开WiFi，并连接：
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200809170824182.png)
然后记一下树莓派所分得的ip地址，并拔掉网线。拔掉网线后会断开vnc。因为现在的ip地址变了。
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200809171006256.png)
如果没有看ip地址就断开了
* 可以使用arp -a查询b8开头的ip地址
* 可以通过路由器管理设备查询（192.168.0.1 or 192.168.1.1）

现在只要启动树莓派 并启动vncserver，就可以通过vncviewer查看图形界面了。

现在的问题是如何开机自启vncserver？
1. 打开terminal，输入以下打开设置
```
sudo raspi-config
```
2. 选择Interfacing Options->VNC->选择yes  等待完成
3. 打开初始化文件
```
sudo vim /etc/init.d/vncserver
```
并粘贴以下内容,粘贴后 按 ctrl+X 保存并退出:
```
#!/bin/sh
### BEGIN INIT INFO
# Provides: vncserver
# Required-Start: $local_fs
# Required-Stop: $local_fs
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Start/stop vncserver
### END INIT INFO
# More details see:
# http://www.penguintutor.com/linux/vnc
### Customize this entry
# Set the USER variable to the name of the user to start vncserver under
export USER='pi'
### End customization required
eval cd ~$USER
case "$1" in
start)
# 启动命令行。此处自定义分辨率、控制台号码或其它参数。
su $USER -c '/usr/bin/vncserver -depth 16 -geometry 1920x1200 :1'
echo "Starting VNC server for $USER "
;;
stop)
# 终止命令行。此处控制台号码与启动一致。
su $USER -c '/usr/bin/vncserver -kill :1'
echo "vncserver stopped"
;;
*)
echo "Usage: /etc/init.d/vncserver {start|stop}"
exit 1
;;
esac
exit 0

```
4. 修改权限
```
sudo chmod 755 /etc/init.d/vncserver
```
5. 添加开机启动项
```
sudo update-rc.d vncserver defaults
```
6. 重启树莓派
```
sudo reboot
```


至此全部完成
