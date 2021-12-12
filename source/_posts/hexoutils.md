---
title: hexo 工具箱
excerpt: hexo工具箱集合，持续更新
index_img: https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211204140733338.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - utils
  - hexo
categories:
  - utils
  - hexo
date: 2021-12-03 21:27:54 
comment: 'valine'
---

# hexo本地文件同步到github

1. github新建分支，必须新建分支，血泪教训

2. 将新分支设置为默认分支

3. 将新分支clone到本地新文件夹A中

4. 删除除了.git之外的所有文件。.git文件夹是隐藏文件夹

5. 将本地文件除了.deploy_git和.git两个文件之外的所有文件全部复制，并粘贴到A

6. 修改.gitignore文件中忽略的文件夹。因为我用的主题决定了我需要保留node_modules，所以将其中的/node_modules删除

7. 
```
   git add .
   git commit -m "add branch"
   git push
   
```

之后每次更新完博客，记得重复<code>步骤7</code>

# 在新电脑上clone博客文件

安装git，安装nodejs，配置ssh key，安装hexo

1. clone github 上的仓库

2. 
```
   cd xxx.github.io
   npm install
   npm install hexo-deployer-git --save
```

3. 
```
   hexo g
   hexo d
```

每次打开博客文件夹，都需要同步一下。

```
git pull
```

# 创建新文档

```
hexo new [layout] <title>
```

例如 hexo new mypage utils

意思是创建一个以mypage为模板的博客文件，名字叫做utils.md

注意 <code>mypage</code>是我自己定义的，自带的只有<code>post</code>,<code>draft</code>,<code>page</code>三种，默认是<code>post</code>

# 创建草稿不发布

1. 创建草稿mydraft.md

   ```
   hexo new draft mydraft
   ```

2. 预览草稿

   ```
   hexo server --draft
   ```

3. 发布草稿mydraft.md

   ```
   hexo publish draft mydraft
   ```

