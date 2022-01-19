# 更新log

## 2022.1.19

对代码结构进行了修改，在攻击算法方面用类取代了简单的函数，为后续代码的可扩展性打基础。

在baseAlgorithm.py文件中定义基类，其内提供FGSM的算法，新建fgsm.py和pgd.py文件，内部为基类的派生类，允许用户自定义输入$\varepsilon$值。

算法统一通过`attack = algorithm(model, loss_fn, std)`和`attack.perturb(data, target)`来调用攻击算法。

## 2022.1.18

初步搭好项目框架，并在超参数固定情况下实现FGSM和PGD算法，部分代码学习参考自pytorch tutorial和台大李宏毅2021年春季课程HW10。

> https://pytorch.org/tutorials/beginner/fgsm_tutorial.html
> 
> https://github.com/ga642381/ML2021-Spring

支持使用cifar-10测试集数据共10000张作为待攻击数据，支持使用pytorchcv中提供的预训练resnet-20和resnet-110。

$batch\ size=64$，loss function: `nn.CrossEntropyLoss()`。

FGSM：指定$\varepsilon=8$。在resnet-20网络中有3401张攻击失败（对抗样本分类标签与原始标签相同）。

PGD：指定迭代次数为$n=10$次，$\varepsilon=8$，单次步长$\alpha=0.8$。在resnet-20网络中有13张攻击失败（对抗样本分类标签与原始标签相同）。