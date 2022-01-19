import torch


class BaseAlgorithm:
    def __init__(self, model, loss_fn, std):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        std = std.to(device)
        self.model = model
        self.loss_fn = loss_fn
        self.std = std

    def fgsm(self, data, target, epsilon):

        x_adv = data.detach().clone()
        x_adv.requires_grad = True
        loss = self.loss_fn(self.model(x_adv), target)
        loss.backward()
        x_adv = x_adv + epsilon * x_adv.grad.detach().sign()
        return x_adv
