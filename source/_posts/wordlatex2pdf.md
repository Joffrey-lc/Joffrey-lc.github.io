---
title: word/latex插入矢量图
excerpt: 制作矢量图插入word和latex
index_img: https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211204141222334.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - utils
  - office
categories:
  - utils
  - latex
comment: valine
math: true
hide: false
date: 2021-12-04 14:11:16
---

## 制作论文插图
有人喜欢用visio，有人喜欢用drawio，我就不一样了，我喜欢的drawio+viso。这也没办法。drawio画图舒服，但是导出的矢量图插入word有bug，[详情见这里](https://desk.draw.io/support/solutions/articles/16000042487)，但是我试了没有用，所以只能用drawio画好后，用visio打开，调整一下可能变化的格式，然后导出矢量图插入word。
##  visio调整格式
假如说现在已经在drawio画好了图，如下：
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/91f772eb97cb4b36a0deeb1110858011.png)
保存为.svg文件
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/70a7bd2998054a5c98e28b7e9df889a1.png)
然后用visio打开，如下：
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/0dfc294f0dd94f90812cf019edfae868.png)
发现有个主要问题，就是用latex打的公式在visio中不能识别。我在visio和word套件中都是用的AxMath插件，类似于Mathtype。现在重新打公式。插入对象AxMath:
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/9e8e93b5ac3d4d139d06b9be8f5c3646.png)
完成后结果如下：
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/de2bed6d89574ad781c8c8d9c1b79980.png)
删掉周围的空白部分
①在空白处右键选择显示ShapeSheet
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1e23f934a7ef417cb613b6f758775ad6.png)
②将参数改为如下所示：
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/9a8699c59eb04682b43eac6763a1f086.png)
③选择设计->大小->适应绘图
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/dcc9bd31b5374770bfeac8e08787f0b5.png)
得到了一个没有白边的图：
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/9734dcf8d4cd447bb6f106171784b375.png)

然后就是保存为矢量图，我习惯用.emf文件，不容易出问题。
## 在word中插入
就如同插入图片，直接插入就可以
## 转pdf
转为pdf容易出现问题，~~最好装上Adobe套件~~：建议直接用系统自带的pdf打印机打印pdf，这样基本上不会出问题。
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/70b98db116e54f8c956fccbb28f21a3a.png)
选择另存为Adobe PDF即可。

## 注意
如果选择的.svg，转为pdf后会出现公式模糊；不使用Adobe套件，矢量图的字体会放得极大，完全失真


## 补充
有时候用python画好的图，只需要保存为.svg格式：
```python
plt.savefig('Acc with SNR.svg', format='svg')
```
直接插入word是不行的，线条会乱掉。解决办法是下一个[inkscape](https://inkscape.org/)然后直接打开python导出的.svg矢量图。选中图像主体，按<code>**ctrl**+**shift**+**R**</code>,去除白边之后再另存为.emf文件即可。

#LaTex插入矢量图
## 制作矢量图
visio画好图之后，另存为pdf。
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/c38ea1b813da42d8be1dd2b2bddc6077.png)
## 使用inkscape编辑
inkscape导入的pdf图有两个问题，第一是有黑色的边框；第二是有白边。我找到一种简单粗暴的解决方法：
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/dbdb92b8f7c54a54a8afbe9fdb9d5752.png)

1. 先用inkscape打开pdf图![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/b9baa2037d8247418842a55a8ab2bed9.png)
2. 选中要保存的主体并直接复制，![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/b399e488cbcd43b5a6272ce53e445701.png)
3. 然后新建一个inkscape文档，直接粘贴，并在选中粘贴内容的情况下按<code>**ctrl**+**shift**+**R**</code>,去除白边之后再另存为.eps文件即可.
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/4847c3863aee42a99d839d376001ea2c.png)

# 注意
在word中推荐使用emf，在latex中推荐使用eps
