---
title: Ubuntu+Anaconda+Pycharm从零开始完全配置
excerpt: 在Ubuntu上配置Anaconda和Pycharm
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20211203212547096.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - python
  - envs
categories:
  - [envs]
comment: valine
math: true
hide: false
date: 2021-12-04 14:39:11
---

# Ubuntu+Anaconda+Pycharm
## 安装VMware

[分享我的版本VMware15.5](https://pan.baidu.com/s/1Kkmc94VEe7eNREiRvFHYkQ)

提取码：3cxe

一路傻瓜式安装

## 下载Ubuntu

去阿里的镜像源下载更快，[点击这里](http://mirrors.aliyun.com/ubuntu-releases/)，我使用的是18.04.5

下载的时候注意选择64位或者32位（在18.04.5中都是64位的）。并且牢记，这对后面安装java jdk有影响。

![image-20210911141018838](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/7ad7fd0e3ef8d2f6d687bcfd8df788d1.png)

## 安装Ubuntu

打开VMware，选择主页-->创建新的虚拟机

![image-20210911141238134](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/0b82637d87adf497934bb258f7d7f5b4.png)

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1631340809(1).jpg" alt="1631340809(1)" style="zoom:50%;" width="60%" />

选择自定义，下一步

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20210911141449372.png" alt="image-20210911141449372" style="zoom: 50%;" width="60%"  />

默认设置，下一步

<img src="https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1631340961(1).jpg" alt="1631340961(1)" style="zoom:10%;" width="60%" />

选择稍后安装操作系统

![请添加图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/a0e14eb9a1f248a084b999dc510f88e9.jpg)

选择好客户机操作系统和版本

![请添加图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/04bd7cc833554833be86dc74cecf44e5.jpg)

选择名字和位置

![image-20210911141939579](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/05003a641be50ccdc7b57c0018d6ed8d.png)

处理器配置，这个需要根据个人的业务需求和电脑配置分配

![image-20210911142028889](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/a193d60e4440b59adbd97316c9c9df40.png)

虚拟机内存，分配大小也需要根据业务需求和电脑配置决定，太小了虚拟机会比较卡

![image-20210911142109837](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/d9590b8b0ea60d2c10685bc4f56959f1.png)

网络类型，默认

![image-20210911142134408](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/ee7859717696af99d153d4bd091d212c.png)

IO默认

![image-20210911142153119](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1e4e1225d0a6a518438abc52edaf52eb.png)

磁盘默认

![image-20210911142213674](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/dbd935507bf7bb03ca2145105b2fa06c.png)![请添加图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/fdf81c9f3b4c4e5aa63e37f5c069385c.jpg)

创建新虚拟磁盘

磁盘大小看个人需求

![image-20210911142405386](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/3e035a41326e42a867ced8d63acdb9d3.png)

磁盘文件的存储地址，默认即可

![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/72341f4e6e3a4d2fa07aee8d3371cf62.png)


选择自定义硬件，在新CD/DVD中选择使用ISO映像文件，选择之前下载的Ubuntu操作系统，然后点右下角关闭，点击完成。

![请添加图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/41762965302b4f21945f9227aaa65584.jpg)


## 安装系统

**安装系统时容易出现安装界面显示不完全，导致continue按钮无法选中，可以按住alt键拖动窗口即可。**

![image-20210911142826563](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/060accad7e28f04cd82ef62f7dffa127.png)

选择虚拟机，点击开启此虚拟机

![](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/7b1ddc722f134c2dab8411f8ad395ad5.png)


建议直接装英文版，中文字符使用不方便。点击Install Ubuntu

![image-20210911143054598](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/d6ec3004af3b4496d6181e4c6e224d5a.png)

选择键盘，就选英文键盘或者中文键盘都可以。

![image-20210911143209246](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/8bf9155f4fc323d6d2522d8919c2b9bd.png)

默认安装一些软件

![image-20210911143349971](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/8aeb4c04bedbab3ff66aa2859f4fe64d.png)

选择默认的安装方式，会将磁盘文件中的数据给清楚（磁盘文件指的是安装Ubuntu的那个50G磁盘文件）

![](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/78c41df3879144a298aab3be46163583.png)


continue开始安装，选择城市

![image-20210911143642255](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/4299c74e0a568ad2330f3b39e1de792f.png)

设置账号密码

![image-20210911143701815](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/9efd1b042ff6eefc19e7a6605bdb09a0.png)

安装完成后要求重启，完成安装。

## Ubuntu 全屏，VMware tools安装

安装完之后是非全屏的，需要安装VMware tools才能全屏显示

![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/105ec533b9e24e5c9abeb54fd4962ab3.png)


查看VMware tools的位置

![image-20210911145415327](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/48756f63548d3435d9f3444cf6481d95.png)

用Terminal（ctrl+alt+t打开）新建一个文件夹以供VMware tools 解压，建在哪都可以

```
cd Desktop
mkdir tools
```

然后右键VMware tools 压缩包，解压到新建的文件夹中

![image-20210911145859028](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/0f51ede49666ebe160f76dffdb621352.png)

如果显示Not Enough free Space...就先将压缩文件移到tools文件夹中再直接解压。

![image-20210911150013994](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/bd15a253c2837d5bbb8e66d46c4d3c2c.png)

然后进入解压后的文件夹，在此页面打开Terminal，进入超级用户

```
sudo su
```

然后输入密码，登录超级用户

然后运行安装程序：

```
./vmware-install.pl
```

输入yes开始安装，一路回车

![image-20210911150651319](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/cb67c6c1b897ccf02b066d5ac4dba2a7.png)

看到Enjoy--the Vmware team就安装完成了，全屏的时候就已经可以自动调整大小了。

## 安装java jdk

jdk包括了jre和jvm，分别是Java运行环境和Java虚拟机安装pycharm需要用得到，装pycharm和Anaconda之前先安装这个。

先在Oracle官网下载对应的jdk，个人觉得jdk8已经够用了，新的无非是多一些新特性，暂时用不上。

[下载地址点这里]([外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-P3hK6zd6-1631348653338)(C:\Users\joffrey\AppData\Roaming\Typora\typora-user-images\image-20210911151030631.png)][外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-w2Jxy34Q-1631348653339)(C:\Users\joffrey\AppData\Roaming\Typora\typora-user-images\image-20210911151030631.png)])

注意下载jdk，jdk里面带有jre，不要下错了。另外要注意是64位还是32位，下错了会出现以下错误：
![image-20210910154704281](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/6adfa37ec30141a85239af03bd35cf7d.png)

还是用jdk8

![image-20210911151144787](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/73d98e58baaddd482d8e692f1892fe58.png)

先新建一个文件夹，存储解压后的文件

```
cd Desktop
mkdir jdk
```

然后解压文件到Desktop/jdk文件夹

```
sudo tar zxvf ~/Downloads/jdk-8u301-linux-x64.tar.gz -C ~/Desktop/jdk
```

![image-20210911151920137](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/3b780ae7f968f8a5cc8660fe7f2e0ccd.png)

添加环境变量：

```
sudo gedit ~/.bashrc
```

并在打开的文件中输入，第一行路径需要根据个人的解压路径填写

```
export JAVA_HOME=/home/lc/Desktop/jdk/jdk1.8.0_301
export JRE_HOME=${JAVA_HOME}/jre 
export CLASSPATH=:${JAVA_HOME}/lib:${JRE_HOME}/lib 
export PATH=${JAVA_HOME}/bin:$PATH
```

然后使环境变量生效:

```
source ~/.bashrc
```

最后查看是否完成

```
java -version
```

![image-20210911152700050](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/a000c5813faf481be8027494ffee14bc.png)

有版本信息就说明完成了。

## 安装pycharm

[官网下载](https://www.jetbrains.com/pycharm/download/#section=linux)

解压下载的文件夹到目录，我这里是解压到Pycharm文件夹下：

```
mkdir ~/Pycharm
sudo tar zxvf ~/Downloads/pycharm-professional-2021.2.1.tar.gz -C ~/Pycharm
```

进入文件夹/home/lc/Pycharm/pycharm-2021.2.1/bin 运行pycharm.sh

```
cd /home/lc/Pycharm/pycharm-2021.2.1/bin
sh pycharm.sh
```

![image-20210911153916643](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/f9b266960a55dbd98b88d5f04fa38b36.png)

选择continue

![image-20210911153947829](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/e8564be8122306f39d1220160b33fce9.png)

初次安装，不导入设置。剩下的就是激活了。网上有很多激活教程，或者免费试用30天，或者学生认证都可以。

### 配置快捷按钮

在/usr/share/applications 创建一个名为pycharm.desktop的文件

```
cd /usr/share/applications
sudo gedit pycharm.desktop
```

在打开的文件中粘贴

```
[Desktop Entry]
Version=1.0
Type=Application
Name=Pycharm
Icon=/home/lc/Pycharm/pycharm-2021.2.1/bin/pycharm.png
Exec=sh /home/lc/Pycharm/pycharm-2021.2.1/bin/pycharm.sh
MimeType=application/x-py;
Name[en_US]=pycharm
```

主要注意 Icon是图标，Exec 执行的命令，其中的路径要改。

保存后就可以在所有的程序中看到pycharm了

![image-20210911154907027](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/44c46c71f28466a08a05445515f58ddd.png)

## Anaconda 安装

[官网下载](https://www.anaconda.com/products/individual#Downloads)

下载好了执行shell脚本

```
bash Anaconda3-2021.05-Linux-x86_64.sh
```

![image-20210911155401162](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1d05a7e0fd993b8f48185336b560f047.png)

然后一直回车，直到左下角没有--More--

![image-20210911155458129](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/7b4686cc3e10a564a2e4afaf2ae19ca1.png)

输入yes，回车

![image-20210911155529304](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/4622d61c5398e2a0a117908584bdc118.png)

![image-20210911155646959](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/24f17f4634fe18a9406ea0ac6c2d18e6.png)

添加环境变量，路径根据自己的修改

```
echo 'export PATH="/home/lc/anaconda3/bin/:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

完成后有两个步骤，第一换源，第二做启动图标，第三创建新环境和激活

### 换源

```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --append channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/fastai/
conda config --append channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
conda config --append channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
conda config --set show_channel_urls yes

```

### 启动图标

类似于pycharm

创建一个文件：

```
cd /usr/share/applications/
sudo gedit anaconda.desktop
```

然后在打开的文件中粘贴如下，注意修改Icon和Exec路径：

```
[Desktop Entry]
Version=1.0
Name=Anaconda
Type=Application
GenericName=Anaconda
Comment=Scientific Python Development Environment - Python3
Exec=/home/lc/anaconda3/bin/anaconda-navigator
Categories=Development;Science;IDE;Qt;Education;
Icon=/home/lc/anaconda3/lib/python3.8/site-packages/anaconda_navigator/static/images/anaconda-icon-256x256.png
Terminal=false
StartupNotify=true
MimeType=text/x-python;
```

![image-20210911161538078](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/df1750433d50f7a00c23b0547be0fbf6.png)

### 创建新环境并激活

```
conda create --name xxx python=3.8
```

创建一个名字叫做xxx 的python版本为3.8的环境。我创造的环境名叫mytorch

![image-20210911161839275](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/ac71dda9b9df98464922c6def590ac46.png)

通过如下命令来激活环境

```
conda activate mytorch
```

![image-20210911161908586](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/394851edbfa2fef606abc4b98908cb28.png)

## Anaconda和Pycharm联合使用

参考之前的windows系统中的做法。即将pycharm中的编译器选择位anaconda环境的python编译器
