---
title: 优化基础-高斯随机化
excerpt: Gaussian Randomization
index_img: >-
  https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img/image-20211203212547096.png
banner_img: 'https://mymarkdown-pic.oss-cn-chengdu.aliyuncs.com/img441/1638523690670.jpg'
tags:
  - Optimization
categories:
  - Optimization
comment: valine
math: true
hide: false
date: 2022-07-16 19:51:05
---

## 高斯随机化

原理见之前的博客[^1]和CSDN[^2]

## Code

两种高斯随机化的方案和元素迭代的方法作为对比， 思想就是每次固定向量的其他元素而单独优化一个元素。 最后的性能显示， **两种高斯随机化的方案性能差不多**， 而**元素迭代算法**的性能是最好的。

见CSDN[^2]

```matlab
Nt = 16;
M = 4;
L = 100; % number of Gaussian randomizations
G = sqrt(2) / 2 * (randn(M, Nt) + 1j * randn(M, Nt));
hr = sqrt(2) / 2 * (randn(M, 1) + 1j * randn(M, 1));
hd = sqrt(2) / 2 * (randn(Nt, 1) + 1j * randn(Nt, 1));
phi = diag(hr') * G;

R = [phi * phi' phi * hd; hd' * phi' 0];

cvx_begin sdp quiet
variable V(M+1, M+1) hermitian
maximize(real(trace(R*V)));
subject to
diag(V) == 1;
V >= 0;
cvx_end

%% method 1
max_F = 0;
max_v = 0;
[U, Sigma] = eig(V);
for l = 1 : L
    r = sqrt(2) / 2 * (randn(M+1, 1) + 1j * randn(M+1, 1));
    v = U * Sigma^(0.5) * r;
    if v' * R * v > max_F
        max_v = v;
        max_F = v' * R * v;
    end
end

v = exp(1j * angle(max_v / max_v(end)));
v = v(1 : M);
v' * phi * phi' * v

%% method 2
max_F = 0;
max_v = 0;
[U, Sigma] = eig(V);
for l = 1 : L
    r = sqrt(2) / 2 * (randn(M+1, 1) + 1j * randn(M+1, 1));
    v = U * Sigma^(0.5) * r;
    v = exp(1j * angle(v / v(end)));
    v = v(1 : M);
    if v' * phi * phi' * v > max_F
        max_v = v;
        max_F = v' * phi * phi' * v;
    end
end
max_v' * phi * phi' * max_v

%% method 3  element iteration
T = phi * phi';
v = sqrt(2) / 2 * (randn(M, 1) + 1j * randn(M, 1));
for n = 1 : 10
    for i = 1 : M
        tmp = 0;
        for j = 1 : M
            if i~= j
                tmp = tmp + T(i,j) * v(j);
            end
        end
        v(i) = exp(1j * angle(tmp));
    end
end
v' * phi * phi' * v

```



## Reference

[^1]:https://lcjoffrey.top/2022/04/20/TransmitBF4Phy-layer-Multicasting/
[^2]:https://blog.csdn.net/weixin_39274659/article/details/121619619?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522165795497016780357263986%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=165795497016780357263986&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_ecpm_v1~rank_v31_ecpm-1-121619619-null-null.185^v2^control&utm_term=%E9%AB%98%E6%96%AF%E9%9A%8F%E6%9C%BA%E5%8C%96&spm=1018.2226.3001.4450
