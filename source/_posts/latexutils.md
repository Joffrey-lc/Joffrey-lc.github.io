---
title: latex工具箱
excerpt: latex工具箱，持续更新
index_img: https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211204141222334.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - utils
categories:
  - utils
  - latex
comment: valine
math: true
hide: false
date: 2021-12-04 15:04:21
---

# 行间公式
```latex
\begin{equation}
\begin{aligned}
    \mathcal{L}_{dif} =& H(f_{\theta_1}(x),f_{\theta_2}(g_1(x)))\\+&H(f_{\theta_2}(x),f_{\theta_1}(g_2(x)))\label{eqn:5}
\end{aligned}
\end{equation}
```
# 插入图片（矢量图推荐.eps）
python直接保存的svg可以，但visio画的有时候不行，先转pdf再用inkscape转为.eps文件导入。
插入eps矢量图先导入两个包
```latex
 \usepackage{graphicx} %use graph format
 \usepackage{epstopdf}
```
然后正常的插图图像
```latex
\begin{figure}[htbp}
\centering
\includegraphics[width=0.5\textwidth]{pic/CLDNN.eps}%宽度为页面的50%
\caption{CLDNN Network} %标注
\label{fig:cldnn}
\end{figure}
```
# IEEE Conference 作者信息模板
```latex
\author{
\IEEEauthorblockN{1\textsuperscript{st} Name1}
\IEEEauthorblockA{\textit{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx} \\
Chengdu, China \\
xxxxx@qq.com}

\and
\IEEEauthorblockN{2\textsuperscript{nd} Name2}
\IEEEauthorblockA{\textit{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx} \\
Chengdu, China  \\
xxxxx@qq.con}
\and

\IEEEauthorblockN{3\textsuperscript{st} Name3}
\centerline~  % 让第三个作者居中
\IEEEauthorblockA{\textit{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx} \\
Chengdu, China  \\
xxxxx@qq.com}
}
```
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/2d320c1a614a4c919702e9c8c95790a2.png)
# 表格
```latex
\renewcommand{\arraystretch}{1.3}%调行距
%\setlength\tabcolsep{3pt}%调列距
\begin{table}[htbp]
\caption{Comparison of method performance}
\begin{center}
\begin{tabular}{|c|c|c|}
\hline
\textbf{Method}&\textbf{Acc:10+500} &\textbf{Acc:50+500}\\\hline
FixMatch&74.18\% &83.53\%\\\hline
SSACGAN-FM&50.77\%&71.00\%\\\hline
Enhanced DCT&\textbf{80.82}\%&\textbf{87.27}\%\\\hline
\end{tabular}
\label{tab:1}
\end{center}
\end{table}
```
# 强制符号在下方
```latex
\sum\limits_{x=0}^1

\mathop{\mathbb{E}}\limits_{X}
```
$\sum\limits_{x=0}^1$

$\mathop{\mathbb{E}}\limits_{X}$
# 大括号公式
```latex
\lambda (t)=\left\{ \begin{array}{l}
	\lambda _{max}exp(-5(\frac{t-T}{80})^2),\quad t\le T\\
	\lambda _{max},\quad t>T\\
\end{array} \right. 
```
$$
\lambda (t)=\left\{ \begin{array}{l}
	\lambda _{max}exp(-5(\frac{t-T}{80})^2),\quad t\le T\\
	\lambda _{max},\quad t>T\\
\end{array} \right. 
$$
# 标题深度和目录深度

默认只到subsubsection。想要显示更深，在导言区加入：

```latex
\setcounter{tocdepth}{3} # toc即table of content，表示目录显示的深度
\setcounter{secnumdepth}{4} #secnum即section number，表示章节编号的深度
```

# 希腊字母加粗

一般加粗使用<code>\textbf{}</code>，希腊字母使用：

```latex
\boldsymbol{\phi}
for example:
\boldsymbol{\phi}||\phi
```

$$\boldsymbol{\phi}||\phi$$

# Latex横向纸张

```latex
\documentclass[review, 11pt]{article}%调用elsevier模板
\usepackage[backend=bibtex]{biblatex}
\usepackage[UTF8]{ctex}
\usepackage{pdflscape}
\usepackage{geometry}
\geometry{layoutwidth=297mm,layoutheight=210 mm, left=2.7cm,right=2.7cm,top=1.8cm,bottom=1.5cm, includehead,includefoot}
\paperwidth=\pdfpageheight
\paperheight=\pdfpagewidth
\pdfpageheight=\paperheight
\pdfpagewidth=\paperwidth

\begin{document} %开始正文书写
%\begin{landscape}
\begin{table}[h]
\centering
\caption{Soil physico-chemical characteristics of Horqin Desert with various GE time in two soil depths}
\label{Table.1}
\begin{tabular}{c c c c c c c c}
\hline
Time since GE & Soil Depth & Soil Moisture Content & pH & Conductivity & SOC & TN & TP\\
(years) && ($\%$)&&(us/cm)&(g/Kg)&(g/Kg)&(mg/Kg)\\
0&0-15 cm& 3.16$\pm$0.09 d&7.19$\pm$0.15 a& 16.19$\pm$4.72 b& 1.71$\pm$1.38 c&0.15$\pm$0.11 c& 0.07$\pm$0.003 b\\
\hline
\end{tabular}
\end{table}
%\end{landscape}
\end{document}
```

# vs code open json

[json配置](https://blog.csdn.net/qq_24502469/article/details/114269806)

# 公式编号

用latex写论文的时候，每次公式换行都会有编号，可以通过在换行符\\\前加\nonumber



# Research Style

在进行调研的时候，可以通过如下参数配置调研表格。

```latex
\documentclass[review, 11pt]{article}%调用elsevier模板
\usepackage[UTF8]{ctex}
\usepackage{pdflscape}
\usepackage{diagbox}
\usepackage{geometry}
\usepackage{cite}
\usepackage{hyperref}
\usepackage{ulem}
\usepackage{float}
\usepackage{amsthm,amsmath,amssymb}
\usepackage{mathrsfs}
\usepackage{amsfonts}
\usepackage{gensymb}
\usepackage[resetlabels]{multibib}
\usepackage{subfigure}

\usepackage{caption}
\usepackage{graphicx}


% \newcites{Info}{ }
% \newcites{Idea}{ }
% \newcites{WETIRS}{ }
% \newcites{COOPIRS}{ }
% \newcites{ACTIRS}{ }

\geometry{layoutwidth=297mm,layoutheight=210 mm, left=1cm,right=1cm,top=1cm,bottom=1cm, includehead,includefoot}
\paperwidth=\pdfpageheight
\paperheight=\pdfpagewidth
\pdfpageheight=\paperheight
\pdfpagewidth=\paperwidth

\begin{document} 
\section*{CSI-free}
% for table I
\begin{table}[H]
    \caption{Channel State Information free for \textbf{Energy} Harvesting System}
    \label{Table.1}
    \begin{center}
        \begin{tabular}{|p{2cm}|p{3cm}|p{1.5cm}|p{4.5cm}|p{2.5cm}|p{1cm}|p{3cm}|p{6cm}|}
        \hline
        \textbf{Literature} & \textbf{System Model} & \textbf{Channel} & \textbf{CSI-free Method} &\textbf{Signal Type}& \textbf{With IRS} &\textbf{Further work} &\textbf{P.S.}\\
        \hline
        \href{https://ieeexplore.ieee.org/document/8470248}{Bruno et.al.}\cite[]{}& Multi-antennas BS, Single antenna user&LOS& Transimit Diversity (form a quick fading channel and Transmit Diversity can also benefit for EH) &Energy Only& No & Energy Waveform, Energy Modulation& Fading and Transmit Diversity are both benefit for Energy Harvesting\\
        \hline
        \end{tabular}
    \end{center}
\end{table}

\bibliographystyle{IEEEtran}
\bibliography{mybib}
\end{document}

```

值得注意的是，需要在调研中出现多个reference的方法在：line21-line25。新建一个citation，例如：

```latex
\newcites{Info}{ }
```

然后再后面需要显示reference的地方，使用：

```latex
% citation
\citeInfo{}
% show reference 
\bibliographystyleInfo{IEEEtran}
\bibliographyInfo{mybib}
```

最后，在编译的时候选择latexmk进行编译。Done。
