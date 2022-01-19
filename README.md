# 对抗攻击实战

本项目力图将主流攻击方法基于pytorch框架进行复现，通过本项目的实现从而对对抗攻击方法有一个更为清晰的了解。

Inspired by The CleverHans library, https://github.com/cleverhans-lab/cleverhans

> Clever Hans was a horse that appeared to have learned to answer arithmetic questions, but had in fact only learned to read social cues that enabled him to give the correct answer. In controlled settings where he could not see people's faces or receive other feedback, he was unable to answer the same questions. The story of Clever Hans is a metaphor for machine learning systems that may achieve very high accuracy on a test set drawn from the same distribution as the training data, but that do not actually understand the underlying task and perform poorly on other inputs.

Clever Hans是一只看起来很聪明的马。刚出现的时候人们认为这匹马会做算术，但实际上它只是会阅读人的表情，当它点马蹄的次数接近正确答案时，人们的表情会更兴奋，它就知道该这个时候停止了。

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

代码正常执行后，在output文件夹中会产生名如：FGSM-cifar10-resnet20 的文件夹，内部共10000张图片，命名规则为 index-原图标签-攻击后标签

## FGSM

> Paper link (Goodfellow et al. 2014): https://arxiv.org/pdf/1412.6572.pdf

$$x_{adv}=x+{\varepsilon}{\cdot}sgn({\triangledown}_xL(x,y;{\theta}))$$

## PGD

或BIM、I-FGSM，按照作者所述，本质上方法相同，在CleverHans库中的实现里，区别仅在于是否随机初始化，本项目仅学习之用，因此在这个地方不做细究，简单认为二者为同一算法。

> This class implements either the Basic Iterative Method (Kurakin et al. 2016) when rand_init is set to False. or the Madry et al. (2017) method if rand_init is set to True.
> Paper link (Kurakin et al. 2016): https://arxiv.org/pdf/1607.02533.pdf
> Paper link (Madry et al. 2017): https://arxiv.org/pdf/1706.06083.pdf

$$x_0^{'}=x$$

$$x_{t+1}^{'}={Clip}_x^{\varepsilon}(x_t^{'}+{\alpha}{\cdot}sgn({\triangledown}_xL(x,y;{\theta})))$$

其中迭代次数为$T=\min({\varepsilon}+4,1.25{\times}{\varepsilon})$，${\alpha}={\varepsilon}/T$，${Clip}_x^{\varepsilon}$指对抗样本应位于benign image的${\varepsilon}-ball$内部。
