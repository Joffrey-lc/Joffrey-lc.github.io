---
title: hexomusic
excerpt: 没有添加摘要
index_img: >-
 https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211204141222334.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - hexo
  - utils
  - music
  - diy
categories:
  - utils
  - hexo 
comment: valine
math: true
hide: false
date: 2021-12-12 14:13:07
---



aplayer是一个非常漂亮好用的HTML5音乐播放器，和dplayer师出同门。我用的主题是fluid，记录一下添加音乐插件的过程。

我的[HEXO博客](https://lcjoffrey.top)

![整体效果](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211212140343669.png)

# 安装aplayer

npm和github两种方式二选一，拿到dist文件夹就可以了。

## npm安装

在hexo博客的文件夹根目录打开git bash，并输入:

```
npm install --save hexo-tag-aplayer
```

可以看到在node_module文件夹中多出来一个aplayer文件夹即可

![dist路径](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211212133506777.png)

为了方便，将这个dist文件夹复制一份到主题目录下的source文件夹中。

## Github下载源码

[去github clone源码](https://github.com/DIYgod/APlayer)，并复制dist文件夹到主题下的source。

![github下载dist](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211212133806994.png)



# 配置js组件

这一步可以根据[教程](https://blog.yleao.com/2018/0902/hexo%E4%B8%8A%E7%9A%84aplayer%E5%BA%94%E7%94%A8.html)选择自己喜欢的模式。新建一个music.js（名字随便起），放到主题的source文件夹里（我放在source/js/diy/music.js）例如：

![我的music.js路径](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211212135433717.png)

- 和我选择一样的跟随模式

```javascript
const ap = new APlayer({
    container: document.getElementById('aplayer'),
    fixed: true,
	autoplay: true, //自动播放
    audio: [
	{
        name: '',
        artist: '',
        url: '',
        cover: '',
    }, 
	]
});
```

- 选择普通模式

```javascript
const ap = new APlayer({
    container: document.getElementById('aplayer'),
    audio: [{
        name: '',
        artist: '',
        url: '',
        cover: '',
    }]
});
```

等等

# 搞音乐外链

- 在一些网站上搜索，例如：https://www.ytmp3.cn/

好用是好用，但是没有cover，逼格不够；包含的音乐也有点少。

- 自己动手薅

1. 比如说找[deca joins的浴室](https://music.163.com/#/song?id=483378334)，在页面按F12进入开发者模式，选择Network。

   ![Network](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211212134814313.png)

2. 点击播放，找media类型的Request URL就是音乐的URL。![media](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211212135032005.png)

   ![URL](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211212134955263.png)

3. 同样的找到想要的cover图片的URL，然后一起填到之前的music.js中。

例如我的：

```javascript
const ap = new APlayer({
    container: document.getElementById('aplayer'),
    fixed: true,
	autoplay: true, //自动播放
    audio: [
	{
        name: "浴室",
        artist: 'deca joins',
        url: 'https://m704.music.126.net/20211212133437/6298f876daf4b3a20b984659f71f8968/jdyyaac/000c/560b/5153/7f43625368aa52c4fbb0f968fa2007d2.m4a?authSecret=0000017dad0be60506550aa4681408a0',
        cover: 'https://p1.music.126.net/byjfkEIOWI_RmxSKEWTPyw==/18910500486297525.jpg?param=200y200',	
    },
	]
});
```

# 布置到想要的页面中

因为我用的是fluid主题，作者在_config.yml文件中预留了修改html的接口，所以我就直接添加在

![_config.yml中添加](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211212135816276.png)

```HTML
<link rel="stylesheet" href="/dist/APlayer.min.css">
<div id="aplayer"></div>
<script type="text/javascript" src="/dist/APlayer.min.js"></script>
<script type="text/javascript" src="/js/diy/music.js"></script>
```

值得注意的是，这里的<code>id="aplayer"</code>要和上面music.js中的<code>container: document.getElementById('aplayer')</code>填的Id相同。

然后就保存发布即可！

最终效果：

![整体效果](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211212140311292.png)

# TODO

如何获取歌词lrc，有哪位老哥知道可以和我分享一下。感谢！
