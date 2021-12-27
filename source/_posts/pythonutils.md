---
title: python工具箱
excerpt: python工具箱，持续更新
index_img: https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/image-20211204140733338.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - python
  - utils
categories:
  - utils
  -	python
comment: valine
math: true
hide: false
date: 2021-12-04 14:04:37
---

# 记录常用的一些工具代码
## 遍历某文件夹下的所有文件路径（递归）
可以用来对某个数据集进行批量处理。这里只返回所有文件的路径， 并存储到一个list.txt文件中。
```python
def get_file_path(path, txt: list):
    dir_path = os.listdir(path)
    for dp in dir_path:
        if os.path.isdir(os.path.join(path, dp)):
            get_file_path(os.path.join(path, dp), txt)
        else:
            txt.append(os.path.join(path, dp))
```

## np.savez保存后的读取
```python
val_set_all = dict(np.load('savemodel/fine_tune_test_set.npz', allow_pickle=True))
for name in val_set_all.keys():
    val_set_all[name] = val_set_all[name][()]
```

## JS散度
```python
def loss_js(p_output, q_output, get_softmax=True):
    KLDivLoss = nn.KLDivLoss(reduction='batchmean')
    if get_softmax:
        p_output = F.softmax(p_output, dim=1)
        q_output = F.softmax(q_output, dim=1)
    mean_output = (p_output + q_output)/2
    return (KLDivLoss(p_output.log(), mean_output) + KLDivLoss(q_output.log(), mean_output))/2
```
## pytorch 设置随机种子
```python
def seed_torch(seed=1029):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed) # 为了禁止hash随机化，使得实验可复现
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  # if you are using multi-GPU.
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
```
## Pytorch梯度裁剪
```python
loss.backward()
nn.utils.clip_grad_norm_(net1.parameters(), max_norm=20, norm_type=2)
nn.utils.clip_grad_norm_(net2.parameters(), max_norm=20, norm_type=2)
optimizer.step()
```
## matplotlib写中文
```python
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 
```
## 多个list按其中一个排序，其余的跟着变
```python
u_idx = [4, 2, 3, 1, 0]
label = [0, 3, 4, 1, 2]
print([list(x) for x in zip(*sorted(zip(u_idx, label), key=lambda x: x[0]))][1])
```

## 绘制混淆矩阵

```python
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np


def plot_confusion_matrix(cm, labels, title='Confusion Matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    xlocations = np.array(range(len(labels)))
    plt.xticks(xlocations, labels, rotation=90)
    plt.yticks(xlocations, labels)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def showmatrix(y_true, y_pred, labels, titlename):
    tick_marks = np.array(range(len(labels))) + 0.5
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    cm = confusion_matrix(y_true, y_pred)
    np.set_printoptions(precision=2)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    # 混淆矩阵
    print(cm_normalized)
    dd = np.zeros(len(cm_normalized))
    for i in range(len(dd)):
        dd[i] = cm_normalized[i, i]
    print(dd)
    max_c = cm_normalized.max()
    min_c = cm_normalized.min()
    print(sum(dd)/len(dd))
    np.save('result/matrixdata.npy', dd)
    plt.figure(figsize=(12, 8), dpi=120)
    ind_array = np.arange(len(labels))
    x, y = np.meshgrid(ind_array, ind_array)
    for x_val, y_val in zip(x.flatten(), y.flatten()):
        c = cm_normalized[y_val][x_val]
        if c > 0.01:
            if c > 0.5*(max_c+min_c):
                plt.text(x_val, y_val, "%0.2f" % (c,), color='white', fontsize=10, va='center', ha='center')
            else:
                plt.text(x_val, y_val, "%0.2f" % (c,), color='black', fontsize=10, va='center', ha='center')
    plt.gca().set_xticks(tick_marks, minor=True)
    plt.gca().set_yticks(tick_marks, minor=True)
    plt.gca().xaxis.set_ticks_position('none')
    plt.gca().yaxis.set_ticks_position('none')
    plt.grid(True, which='minor', linestyle='-')
    plt.gcf().subplots_adjust(bottom=0.15)
    plot_confusion_matrix(cm=cm_normalized, title=titlename, labels=labels)
    plt.savefig('result/confusionmatrix.svg', format='svg')
    plt.show()

```

然后在需要绘制的地方

```python
    showmatrix(val_label.cpu(), y_pred.cpu(), ['1', '2'], 'Confusion matrix')
```

