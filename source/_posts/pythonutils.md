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

## 字典数据读取/分割数据集

数据分割，可以根据输入的proportion维度自定义分割组数

```python
def mysplit_n(dataset: Dict[str, np.ndarray], proportion: Tuple[int, ...]) -> List[Any]:
    out_list = []
    for n in range(len(proportion)):
        exec('dataset_'+str(n)+' = {}')
        exec('index_'+str(n)+' = np.arange(sum(proportion[:n]), sum(proportion[:n+1]))')
        exec('out_list.append(dataset_' + str(n)+')')
    for name in dataset:
        for n in range(len(proportion)):
            exec('dataset_' + str(n) + '[name] = dataset[name][index_'+str(n)+']')
    return out_list
```

先读取数据：

```python
dataset = shuffle(dict(np.load(f'./datasets/'+'RML2016_'+str(args.SNR)+'dB_normalize_power.npz', allow_pickle=True)))
```

再对数据进行划分

```python
dataset = dict(zip(['training', 'unlabeled', 'valid', 'test'], mysplit_n(dataset,
                                                                         (args.num_labeled,
                                                                          args.num_unlabeled,
                                                                          args.num_valid,
                                                                          args.num_test
                                                                          ))))
```

取出分割的数据

```python
def make(dataset: Dict[str, np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
    xs, ys = [], []
    nclass = len(dataset.keys())
    for k, name in enumerate(dataset):
        xs.append(dataset[name])
        label = np.zeros((len(dataset[name]), nclass))
        label[:, k] = 1.0
        ys.append(label)
    xs = np.vstack(xs)
    ys = np.vstack(ys)
    index = np.arange(len(xs))
    np.random.shuffle(index)
    xs = xs[index]
    ys = ys[index]
    return xs, ys

labeled_dataset, labeled_label = make(dataset['training'])
unlabeled_dataset, unlabeled_label = make(dataset['unlabeled'])
valid_dataset, valid_label = make(dataset['valid'])
test_dataset, test_label = make(dataset['test'])
```

## 指定返回值类型

```python
from typing import List, Tuple


def test(a: int, b: str) -> Tuple[int, str]:
    print(a, b)
    return 1000, '11'
```

## 自动给文章建好文件夹并创建.md

```python
import os
import glob
import shutil
import time


def mymkdirs(path_dir):
    if os.path.exists(path_dir) is False:
        os.makedirs(path_dir)
        print(path_dir+'已创建')


def mypaperspace(path_paper):
    shutil.move(src=path_paper + '.pdf', dst=os.path.join(path_paper, 'paper.pdf'))
    with open(path_paper + '\\notes.md', 'a') as f:
        f.write('Date: ' + time.strftime('%Y.%m.%d  %H:%M', time.localtime(time.time())))
        f.write('\n')
        f.write('Author: Joffrey LC')
        f.write('\n')
        f.write('\n------------------------------------------------')


cwd_path = 'H:\学习\阅读\面向智能反射面数能系统的波形设计\\test'
mymkdirs(os.path.join(cwd_path, '文章备份'))
for filename in glob.glob(cwd_path+'/*.pdf'):
    shutil.copy(src=os.path.join(cwd_path, filename), dst=os.path.join(cwd_path, '文章备份'))
    path_dir = filename.split('.pdf')[0].split('\\')[-1]
    mymkdirs(os.path.join(cwd_path, path_dir))
    mypaperspace(os.path.join(cwd_path, path_dir))

# To do:
# shutil.move 移动文件名较长的文件时会发生错误，有时间的话尝试自己写一个移动文件的代码


```

## python调制识别数据集读取

### RML2016a

```python
import os
import pickle

dataset = pickle.load(open("dataset/RML2016.10a_dict.pkl", "rb"), encoding='bytes')
save_path = 'dataset/split_dB_rml2016a'
if not os.path.exists(save_path):
    os.mkdir(save_path)
print('processing')

all_type: set = set()
all_snr: set = set()
for name in dataset.keys():
    type_name, snr = name[0], name[1]
    all_type.add(type_name)
    all_snr.add(snr)
print('调制形式为：', all_type)
list_snr = list(all_snr)
list_snr.sort()
print('信噪比为：', list_snr)

total = len(all_type)
for name in dataset.keys():
    type_name, snr = name[0], name[1]
    if int(snr) < 0:
        snr = 'b'+str(-snr)
    try:
        exec('dataset_'+str(snr)+'dB')
    except NameError:
        exec('dataset_'+str(snr)+'dB = {}')
    data = dataset[name]
    exec('dataset_'+str(snr)+'dB[type_name] = dataset[name]')
    if eval('len(dataset_'+str(snr)+'dB) == total'):
        with open(save_path+'/RML_2016_'+str(snr)+'dB.pkl', 'wb') as f:
            pickle.dump(eval('dataset_'+str(snr)+'dB'), f, pickle.HIGHEST_PROTOCOL)
```

### RML2016c

```python
import os
import pickle

dataset = pickle.load(open("dataset/2016.04C.multisnr.pkl", "rb"), encoding='bytes')
save_path = 'dataset/split_dB_rml2016c'
if not os.path.exists(save_path):
    os.mkdir(save_path)
print('processing')

all_type: set = set()
all_snr: set = set()
for name in dataset.keys():
    type_name, snr = name[0], name[1]
    all_type.add(type_name)
    all_snr.add(snr)
print('调制形式为：', all_type)
list_snr = list(all_snr)
list_snr.sort()
print('信噪比为：', list_snr)

total = len(all_type)
for name in dataset.keys():
    type_name, snr = name[0], name[1]
    if int(snr) < 0:
        snr = 'b'+str(-snr)
    try:
        exec('dataset_'+str(snr)+'dB')
    except NameError:
        exec('dataset_'+str(snr)+'dB = {}')
    data = dataset[name]
    exec('dataset_'+str(snr)+'dB[type_name] = dataset[name]')
    if eval('len(dataset_'+str(snr)+'dB) == total'):
        with open(save_path+'/RML_2016_'+str(snr)+'dB.pkl', 'wb') as f:
            pickle.dump(eval('dataset_'+str(snr)+'dB'), f, pickle.HIGHEST_PROTOCOL)
```

### RML2018

```python
import h5py
import pickle as pkl
import os
# file['X']是数据， file['Y']是one-hot 一类一类的  file['Z']是snr 一类的-20-30dB在一起

classes = ['OOK', '4ASK', '8ASK', 'BPSK', 'QPSK',
'8PSK', '16PSK', '32PSK', '16APSK', '32APSK', '64APSK',
'128APSK', '16QAM', '32QAM', '64QAM', '128QAM',
'256QAM', 'AM-SSB-WC', 'AM-SSB-SC', 'AM-DSB-WC',
'AM-DSB-SC', 'FM', 'GMSK', 'OQPSK']

save_path = 'dataset/split_dB_rml2018'
if not os.path.exists(save_path):
    os.mkdir(save_path)

need_snr = [20]

file = h5py.File('H:/DATASETS/RML/GOLD_XYZ_OSC.0001_1024.hdf5', 'r+')
for name in file.keys():
    print(name, file[name].shape)
num_per_class = int(file['Y'].shape[0]/file['Y'].shape[1])
print('每类所有dB信号总数:', num_per_class)
num_per_snr = 4096

data_list = file['X']
print(len(data_list))
# name_idx = [i for i in range(len(classes)) if classes[i] in ['BPSK', 'QPSK', '8PSK', '16QAM', '32QAM', '64QAM']]
name_idx = [i for i in range(len(classes)) if classes[i] in classes]

print(name_idx)

snr_list = file['Z'][:num_per_class]
# print(snr_list, len(snr_list))
idx_snr = []
for i in range(len(need_snr)):
    idx_part = [j for j in range(num_per_class) if snr_list[j] == need_snr[i]]
    idx_snr.append(idx_part)

for snr_iidx in range(len(need_snr)):
    exec('dict_out_'+str(need_snr[snr_iidx])+'dB = {}')
    for idx in range(len(name_idx)):
        start = name_idx[idx]*num_per_class
        end = (name_idx[idx]+1)*num_per_class
        out_one_class_all_snr = data_list[start:end]
        exec('dict_out_'+str(need_snr[snr_iidx])+'dB[classes[name_idx[idx]]] = out_one_class_all_snr[idx_snr[snr_iidx]]')
    with open(save_path+'\RML_2018_' + str(need_snr[snr_iidx])+'dB.pkl', 'wb') as f:
        pkl.dump(eval('dict_out_' + str(need_snr[snr_iidx]) + 'dB'), f, pkl.HIGHEST_PROTOCOL)
```

重新更新了一下，速度更快

```python
import h5py
import numpy as np
import pickle
classes = ['OOK', '4ASK', '8ASK', 'BPSK', 'QPSK',
'8PSK', '16PSK', '32PSK', '16APSK', '32APSK', '64APSK',
'128APSK', '16QAM', '32QAM', '64QAM', '128QAM',
'256QAM', 'AM-SSB-WC', 'AM-SSB-SC', 'AM-DSB-WC',
'AM-DSB-SC', 'FM', 'GMSK', 'OQPSK']

file = h5py.File('H:/DATASETS/RML/GOLD_XYZ_OSC.0001_1024.hdf5', 'r+')
# for name in file.keys():
#     print(name, file[name].shape)
# num_per_class = int(file['Y'].shape[0]/file['Y'].shape[1])
# print('每类所有dB信号总数:', num_per_class)
# num_per_snr = 4096

# file['X']是数据， file['Y']是one-hot 一类一类的  file['Z']是snr 一类的-20-30dB在一起

data_all = file['X']
label_all = np.array(file['Y']).argmax(axis=1)
snr_all = file['Z']


need_snr = 20


need_idx = [idx for idx in range(int(len(label_all)/24)) if snr_all[idx] == need_snr]

need_idx_all = []
for i in range(24):
    need_idx_all.append([a+int(i*len(label_all)/24) for a in need_idx])

# for i in range(24):
#     exec('snr_'+str(i)+' = snr_all[need_idx_all[i]]')

data_out = {}
for i in range(24):
    data_out[classes[i]] = data_all[need_idx_all[i], :, :]

with open('datasets/dict_out_' + str(need_snr) + 'dB.pkl', 'wb') as f:
    pickle.dump(data_out, f, pickle.HIGHEST_PROTOCOL)
print('11')
```



### load data

```python
import numpy as np
import pickle as pkl


print('\nloading 2016c ... ')
# 读取2016c
with open('dataset/split_dB_rml2016c/RML_2016_0dB.pkl', 'rb') as f:
    data_2016c = pkl.load(f)
for k in data_2016c.keys():
    print(k, data_2016c[k].shape)

print('\nloading 2016a ... ')
# 读取2016a
with open('dataset/split_dB_rml2016a/RML_2016_0dB.pkl', 'rb') as f:
    data_2016a = pkl.load(f)
for k in data_2016a.keys():
    print(k, data_2016a[k].shape)


print('\nloading 2018 ... ')
# 读取2016a
with open('dataset/split_dB_rml2018/RML_2018_20dB.pkl', 'rb') as f:
    data_2018 = pkl.load(f)
for k in data_2018.keys():
    print(k, data_2018[k].shape)


print('\nloading WIDEFT-A2197_1 ... ')
data_WIDEFT = np.load('dataset/A2197_1/1.npy')
print(data_WIDEFT.real.shape, data_WIDEFT.imag.shape)
```

