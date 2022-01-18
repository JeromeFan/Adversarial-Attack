# 对抗攻击实战

本项目力图将主流攻击方法基于pytorch框架进行复现，通过本项目的实现从而对对抗攻击方法有一个更为清晰的了解。

## 更新log

### 2022.1.18

初步搭好项目框架，并在超参数固定情况下实现FGSM和I-FGSM算法，部分代码学习参考自pytorch tutorial和台大李宏毅2021年春季课程HW10。

> https://pytorch.org/tutorials/beginner/fgsm_tutorial.html
> https://github.com/ga642381/ML2021-Spring

支持使用cifar-10测试集数据共10000张作为待攻击数据，支持使用pytorchcv中提供的预训练resnet-20和resnet-110。

$batch\ size=64$，loss function: `nn.CrossEntropyLoss()`。
FGSM：指定$\varepsilon=8$。

I-FGSM：指定迭代次数为$n=20$次，$\varepsilon=8$，单次步长$\alpha=0.8$。

## USAGE

```python
> python run_attack.py <options>
```

可选参数有：`-a`、`-d`、`-m`，分别用以指定攻击算法、数据集、模型。

目前支持的攻击算法有FGSM、I-FGSM，数据集为cifar-10，模型有预训练的resnet-20和resnet-110。默认参数是FGSM、cifar-10、resnet-20。

```python
> python run_attack.py -a IFGSM -d cifar10 -m resnet110
```

## FGSM

实现$x_{adv}=x+{\varepsilon}{\cdot}sgn({\triangledown}_xL(x,y;{\theta}))$。

## I-FGSM

$x_0^{'}=x$

$x_{n+1}^{'}={Clip}_x^{\varepsilon}(x_n^{'}+{\alpha}{\cdot}sgn({\triangledown}_xL(x,y;{\theta})))$

其中迭代次数为$n$，${Clip}_x^{\varepsilon}$指对抗样本应位于benign image的${\varepsilon}-ball$内部。