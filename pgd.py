import torch
from baseAlgorithm import BaseAlgorithm


class PGD(BaseAlgorithm):

    def __init__(self, model, loss_fn, std):
        super(PGD, self).__init__(model, loss_fn, std)
        print('欢迎使用PGD/BIM/I-FGSM算法模块！')
        epsilon = int(input('请输入PGD算法所需的epsilon：'))
        self.epsilon = epsilon / 255 / self.std
        self.num_iter = min(epsilon + 4, int(1.25 * epsilon))
        self.alpha = self.epsilon / self.num_iter

    def perturb(self, data, target):
        x_adv = data.detach().clone()
        for i in range(self.num_iter):
            x_adv = self.fgsm(x_adv, target, self.alpha, 'inf')
            x_adv = torch.min(torch.max(x_adv, data - self.epsilon), data + self.epsilon)
        return x_adv
