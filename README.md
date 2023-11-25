# 对抗攻击实战

复现基础对抗攻击算法。

## USAGE

命令行调用。

```python
python run_attack.py <options>
```

可选参数有：`-a`、`-d`、`-m`，分别用以指定攻击算法、数据集、模型。

目前支持的攻击算法有FGSM、PGD，数据集为cifar-10，模型有预训练的resnet-20和resnet-110。默认参数是FGSM、cifar-10、resnet-20。

```python
python run_attack.py -a PGD -d cifar10 -m resnet110
```

代码正常执行后，在output文件夹中会产生名如：FGSM-cifar10-resnet20 的文件夹，内部共10000张图片（可能会存在由于总数不能整除batch size的问题，导致实际生成的图像不足10000张），命名规则为 index-原图标签-攻击后标签

其余超参数请在`config.json`中指定，算法所需的超参数部分，或许会存在冗余的情况，若当前所选算法不需要某参数，可直接忽略。

例如，在使用FGSM时，仅需要指定norm为$L_{\infty}$和$\varepsilon$的值，即`norm_p`项参数修改为"inf"、`epsilon`项修改为所需值，而剩下的`miu`项为MI-FGSM算法中所需的衰减因子，在调用FGSM中不会读取该值，请直接忽略。

## FGSM/FGM

> Paper link (Goodfellow et al. 2014): https://arxiv.org/pdf/1412.6572.pdf

FGSM: $L_{\infty}$ norm bound ${||x^{*}-x||}_{\infty}{\leqslant}{\varepsilon}$

$$x_{adv}=x+{\varepsilon}{\cdot}sgn({\triangledown}_xL(x,y;{\theta}))$$

FGM: $L_2$ norm bound ${||x^{*}-x||}_{2}{\leqslant}{\varepsilon}$

$$x_{adv}=x+{\varepsilon}{\cdot}\frac{{\triangledown}_xL(x,y;{\theta})}{{||{\triangledown}_xL(x,y;{\theta})||}_2}$$

## PGD

或BIM、I-FGSM，按照作者所述，本质上方法相同，在CleverHans库中的实现里，区别仅在于是否随机初始化，本项目仅学习之用，因此在这个地方不做细究，简单认为二者为同一算法。

> This class implements either the Basic Iterative Method (Kurakin et al. 2016) when rand_init is set to False. or the Madry et al. (2017) method if rand_init is set to True.
> Paper link (Kurakin et al. 2016): https://arxiv.org/pdf/1607.02533.pdf
> Paper link (Madry et al. 2017): https://arxiv.org/pdf/1706.06083.pdf

$$x_0^{'}=x$$

$$x_{t+1}^{'}={Clip}_x^{\varepsilon}(x_t^{'}+{\alpha}{\cdot}sgn({\triangledown}_xL(x,y;{\theta})))$$

其中迭代次数为$T=\min({\varepsilon}+4,1.25{\times}{\varepsilon})$，${\alpha}={\varepsilon}/T$，${Clip}_x^{\varepsilon}$指对抗样本应位于benign image的${\varepsilon}-ball$内部。

## MI-FGSM

> Paper link (Dong et al. 2018): https://arxiv.org/pdf/1710.06081.pdf

$$x_0^{'}=x$$

$$g_{t+1}={\mu}{\cdot}g_t+\frac{{\triangledown}_xL(x,y;{\theta}))}{{||{\triangledown}_xL(x,y;{\theta}))||}_1}$$

$L_{\infty}$ norm bound ${||x^{*}-x||}_{\infty}{\leqslant}{\varepsilon}$：

$$x_{t+1}^{'}={Clip}_x^{\varepsilon}(x_t^{'}+{\alpha}{\cdot}sgn(g_{t+1})$$

$L_2$ norm bound ${||x^{*}-x||}_{2}{\leqslant}{\varepsilon}$：

$$x_{t+1}^{'}={Clip}_x^{\varepsilon}(x_t^{'}+{\alpha}{\cdot}\frac{g_{t+1}}{{||g_{t+1}||}_2})$$

其中，${\mu}$为衰减因子，论文中选取值为1.0，若为0则MI-FGSM等价于PGD方法。
