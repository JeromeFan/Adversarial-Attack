import torch
from baseAlgorithm import BaseAlgorithm


class MIFGSM(BaseAlgorithm):

    def __init__(self, model, loss_fn, std):
        super(MIFGSM, self).__init__(model, loss_fn, std)
        epsilon = int(input('请输入MI-FGSM算法所需的epsilon：'))
        self.epsilon = epsilon / 255 / self.std
        self.num_iter = min(epsilon + 4, int(1.25 * epsilon))
        self.alpha = self.epsilon / self.num_iter
        self.g = 0
        self.miu = float(input('请输入MI-FGSM算法所需的decay factor：'))

    def perturb(self, data, target):
        x_adv = data.detach().clone()
        for i in range(self.num_iter):
            x_adv = self.fgsm(x_adv, target, self.alpha)
            x_adv = torch.min(torch.max(x_adv, data - self.epsilon), data + self.epsilon)
        return x_adv

    def fgsm(self, data, target, epsilon):

        x_adv = data.detach().clone()
        x_adv.requires_grad = True
        loss = self.loss_fn(self.model(x_adv), target)
        loss.backward()
        self.g = self.miu * self.g + x_adv.grad.detach() / torch.norm(x_adv.grad.detach(), p=1)
        x_adv = x_adv + epsilon * self.g.sign()
        return x_adv
