---
title: pytorch的自定义数据集/DataLoader和Dataset重写
excerpt: pytorch必备知识
index_img: https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211204151011972.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - python
  - utils
categories:
  - utils
  - python
comment: valine
math: true
hide: false
date: 2021-12-04 15:08:48
---

# 背景介绍
&emsp;&emsp;做Modulation Recognition的时候需要加载自定义的数据集，这就涉及到DataLoader和Dataset类中的方法重写了。
# DataLoader介绍

&emsp;&emsp;源码中的介绍是：
~~~  java
*Data loader. Combines a dataset and a sampler, and provides an iterable over the given dataset.*
~~~
&emsp;&emsp;也就是说，我们可以通过输入一个数据集，及常用参数如：batch_size、shuffle,就可以得到一个打包好的迭代器。这个迭代器包含了batch_size的序号及根据batch_size分割好的数据块。
# Dataset 介绍
&emsp;&emsp;源码中的介绍是：
~~~  java
An abstract class representing a :class:`Dataset`.
~~~
&emsp;&emsp;很短，但是很经典。这是一个抽象类。所谓抽象类就是类的抽象化，而类本身就是不存在的，所以抽象类无法实例化。它存在的意义就是被继承。而且继承抽象类的类必须要重写抽象类的方法。
&emsp;&emsp;简单的说，我们构造一个MyDataset数据类，需要继承Dataset，并重写Dataset中的方法。

&emsp;&emsp;去掉源码中的注释，Dataset抽象类的定义就五行代码，两个方法：
~~~  java
class Dataset(object):
    def __getitem__(self, index):
        raise NotImplementedError

    def __add__(self, other):
        return ConcatDataset([self, other])
        
    # No `def __len__(self)` default?
    # See NOTE [ Lack of Default `__len__` in Python Abstract Base Classes ]
    # in pytorch/torch/utils/data/sampler.py
~~~
&emsp;&emsp;根据我们的需要，我们会重写  __getitem__方法，以及__len__方法。

# 工作原理
&emsp;&emsp;首先，我们要定义自己的数据集类，例如叫做MyDataset，则代码片段应该为：
~~~ java
class MyDataSet(Dataset):
    def __init__(self, data, label):
        self.data = data
        self.label = label
        self.length = data.shape[0]
        
    def __getitem__(self, mask):
        label = self.label[mask]
        data = self.data[mask]
        return label, data

    def __len__(self):
        return self.length
~~~


## 继承
&emsp;&emsp;很简单
~~~ java 
class MyDataSet(Dataset):
~~~
&emsp;&emsp;表示我们MyDataSet类继承了抽象类Dataset。该MyDataSet类中的有三个方法。
## __init__方法
&emsp;&emsp;__init__方法是python中的构造方法(java中是叫构造方法，不知道python是不是这么叫，如果不是请大家指正)，构造方法会在实例化对象时调用。其传入参数就是我们的==数据集==(data)和==标签集==(label)。
~~~ java
 def __init__(self, data, label):
        self.data = data
        self.label = label
        self.length = data.shape[0]
~~~

## __getitem__方法
&emsp;&emsp;__getitem__方法是获取返回数据的方法，传入参数是一个index，也被叫做mask，就是我们对数据集的选择索引。在自己使用时，比如想从data = [100, 99, 98, ..., 0]的集合中选出下标为[0, 2, 4]的集合，则index/mask 就取[0, 2, 4],返回data[index]即可。
&emsp;&emsp;其实在调用DataLoader时就会自己生成index，所以我们只需要写好方法即可。
~~~java
 def __getitem__(self, mask):
        return self.label[mask], self.data[mask]
~~~
## __len__方法
&emsp;&emsp;偷了个懒没有去看源码。听说不给返回length的话pytorch会一脸xx。
~~~java
 def __len__(self):
        return self.length
~~~
# 使用
&emsp;&emsp;完成了MyDataSet，就可以通过DataLoader使用了。例如此处我已经有了一个X_train,其中的数据的每一个batch都代表了一个信号。Y_train当中都是X_train对应的标签。
&emsp;&emsp;于是我的代码就是：
~~~java
train_set = MyDataSet(data=X_train, label=Y_train)
num_epoch = 100     # number of epochs to train on
batch_size = 1024  # training batch size
train_data = DataLoader(train_set, batch_size=batch_size, shuffle=True)
for epoch in range(num_epoch ):
    model.train()
    for batchsz, (label, data) in enumerate(train_data):
        # i表示第几个batch， data表示该batch对应的数据，包含data和对应的labels
        print("第 {} 个Batch size of label {} and size of data{}".format(batchsz, label.shape, data.shape))
~~~
&emsp;&emsp;DataLoader会根据设置的batch_size来产生index/mask，然后调用Datase的__getitem__方法取出数据。
&emsp;&emsp;输出结果如下：
![在这里插入图片描述](https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/20200919225212630.png)
&emsp;&emsp;接下来就可以愉快的写模型了！！！

# 总结
&emsp;&emsp;其实看起来很简单的一个Dataset抽象类重写和DataLoader使用，包含了面向对象编程的三大特点：==封装==、==继承==、==多态==。
- 封装体现在Dataset抽象类的封装及我们的MyDataSet类的封装上。
- 继承体现在我们MyDataSet继承Dataset抽象类上。
- ~~多态体现在DataLoader对数据集的操作上~~（这点纯属个人理解，感觉有点像java中的向上转型，但python好像没有这一概念）。
