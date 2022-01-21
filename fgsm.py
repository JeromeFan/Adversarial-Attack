import torch
from baseAlgorithm import BaseAlgorithm


class FGSM(BaseAlgorithm):

    def __init__(self, model, loss_fn, std):
        super(FGSM, self).__init__(model, loss_fn, std)
        print('欢迎使用FGSM/FGM算法模块！')
        print('FGSM generates adversarial example to meet the L_infinity norm bound.')
        print('FGM is a generalization of FGSM to meet the L_2 norm bound.')
        print('详细区别请查阅README文档中的算法详述模块。')
        self.normType = input('请输入欲选择的p范数("inf"为FGSM，"2"为FGM)：')
        self.epsilon = int(input('请输入FGSM算法所需的epsilon：')) / 255 / self.std

    def perturb(self, data, target):

        return self.fgsm(data, target, self.epsilon, self.normType)


