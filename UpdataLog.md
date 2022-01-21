# 更新log

## 2022.1.21

part 1：

加入了正则norm的选项，FGSM为$L_{\infty}$，FGM为$L_2$，PGD中迭代的为$L_{\infty}$的FGSM，MI-FGSM中有$L_{\infty}$和$L_2$两版。

part 2：

修改代码中范数的计算部分，`torch.norm`计算出的是一个值，因此上一版代码中，在MI-FGSM算法中的动量计算上，相当于在整个batch中去求了1范数，即将$64{\times}3{\times}32{\times}32$中求了所有值的绝对值之和，修改后在$shape[0]$即batch维度循环，从而计算出的norm值shape为$64{\times}1$。

todo: 由于加入了范数部分，导致输出时候的文件夹的命名存在重复命名导致出错无法保存图片的问题，下次修复。

todo: 随着参数的增加，通过命令行读取参数的方式有点麻烦，后续更新中考虑使用 config.json 型的json文件来读取参数。

## 2022.1.19

part 1：

添加MI-FGSM算法的实现，由于动量的引入，在代码中data loader部分设置`drop_last=True`，若以64为batch size，输入10000张图片时，最后一个batch大小为16，但$g_t$的shape为64维张量，因此在相加时发生错误。

问题遗留：MI-FGSM效果远逊色于PGD，可能是……代码写错了？但是将衰减因子设置为0时MI-FGSM的攻击失败数量和PGD都是13张（衰减因子为0时MI-FGSM退化为PGD），似乎这样子的话，应该证明了代码是对的？

todo：下一版代码将范数因素考虑进去，进一步完整代码。

part 2:

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